#!/usr/bin/env bash
# =============================================================================
#  backup.sh — Backup do banco de dados e arquivos do SCSI
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# --- Configurações ---
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
STACK_NAME="${STACK_NAME:-scsi}"
ENV_FILE="${ENV_FILE:-.env}"

# --- Cores ---
green='\033[0;32m'
yellow='\033[1;33m'
nc='\033[0m'

info()  { echo -e "${green}[INFO]${nc}  $*"; }
warn()  { echo -e "${yellow}[WARN]${nc}  $*"; }

# --- Cria diretório de backup ---
mkdir -p "${BACKUP_DIR}"

# --- Carrega .env ---
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

# --- 1. Backup do PostgreSQL ---
info "Realizando backup do PostgreSQL..."
DB_CONTAINER="$(docker ps --filter "name=${STACK_NAME}_db" --format '{{.Names}}' | head -1)"

if [ -n "$DB_CONTAINER" ]; then
    docker exec "$DB_CONTAINER" \
        pg_dump -U "${POSTGRES_USER:-scsi}" -d "${POSTGRES_DB:-scsi}" \
        --clean --if-exists --no-owner --no-privileges \
        > "${BACKUP_DIR}/scsi_db_${TIMESTAMP}.sql"

    gzip "${BACKUP_DIR}/scsi_db_${TIMESTAMP}.sql"
    info "Backup do banco: ${BACKUP_DIR}/scsi_db_${TIMESTAMP}.sql.gz"
else
    warn "Container do PostgreSQL nao encontrado no stack ${STACK_NAME}."
fi

# --- 2. Backup de arquivos (media) ---
info "Realizando backup dos arquivos de media..."
MEDIA_VOLUME="${STACK_NAME}_scsi_media"

if docker volume inspect "$MEDIA_VOLUME" >/dev/null 2>&1; then
    docker run --rm \
        -v "${MEDIA_VOLUME}:/source:ro" \
        -v "${BACKUP_DIR}:/backup" \
        alpine:3.19 \
        tar czf "/backup/scsi_media_${TIMESTAMP}.tar.gz" -C /source .

    info "Backup de media: ${BACKUP_DIR}/scsi_media_${TIMESTAMP}.tar.gz"
else
    warn "Volume de media nao encontrado: ${MEDIA_VOLUME}"
fi

# --- 3. Limpeza de backups antigos ---
info "Removendo backups com mais de ${RETENTION_DAYS} dias..."
find "${BACKUP_DIR}" -name 'scsi_*.gz' -type f -mtime "+${RETENTION_DAYS}" -delete

# --- 4. Resumo ---
info "Backup concluido em: ${BACKUP_DIR}"
ls -lh "${BACKUP_DIR}/scsi_"*"${TIMESTAMP}"*
