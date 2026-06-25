#!/usr/bin/env bash
# =============================================================================
#  deploy.sh — Deploy da stack SCSI no Docker Swarm
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# --- Configurações ---
REGISTRY="${REGISTRY:-registry.scsi.digital}"
TAG="${TAG:-latest}"
STACK_NAME="${STACK_NAME:-scsi}"
ENV_FILE="${ENV_FILE:-.env}"

# --- Cores para output ---
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[1;33m'
nc='\033[0m'

info()  { echo -e "${green}[INFO]${nc}  $*"; }
warn()  { echo -e "${yellow}[WARN]${nc}  $*"; }
error() { echo -e "${red}[ERROR]${nc} $*"; }

# --- Validações ---
command -v docker >/dev/null 2>&1 || { error 'Docker nao encontrado.'; exit 1; }

if ! docker node ls >/dev/null 2>&1; then
    error 'Este node nao e manager do Swarm. Execute em um manager.'
    exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
    error "Arquivo .env nao encontrado: $ENV_FILE"
    exit 1
fi

# --- Build e push da imagem ---
info "Construindo imagem: ${REGISTRY}/scsi-app:${TAG}"
docker build \
    -f docker/Dockerfile \
    -t "${REGISTRY}/scsi-app:${TAG}" \
    .

info "Enviando imagem para o registry..."
docker push "${REGISTRY}/scsi-app:${TAG}"

# --- Secrets (cria se nao existirem) ---
create_secret_if_not_exists() {
    local name="$1"
    local value="$2"

    if ! docker secret inspect "$name" >/dev/null 2>&1; then
        echo "$value" | docker secret create "$name" -
        info "Secret criado: $name"
    else
        warn "Secret ja existe: $name (skip)"
    fi
}

# Carrega variaveis do .env
set -a
source "$ENV_FILE"
set +a

create_secret_if_not_exists 'postgres_password' "${POSTGRES_PASSWORD:-}"
create_secret_if_not_exists 'rabbitmq_password' "${RABBITMQ_DEFAULT_PASS:-}"
create_secret_if_not_exists 'secret_key' "${SECRET_KEY:-}"
create_secret_if_not_exists 'openai_api_key' "${OPENAI_API_KEY:-}"
create_secret_if_not_exists 'cf_api_token' "${CF_API_TOKEN:-}"

# --- Rede publica do Traefik ---
if ! docker network inspect traefik-public >/dev/null 2>&1; then
    docker network create --driver overlay traefik-public
    info 'Rede traefik-public criada.'
fi

# --- Deploy da stack ---
info "Fazendo deploy da stack ${STACK_NAME}..."
docker stack deploy \
    --with-registry-auth \
    -c docker/docker-stack.yml \
    "${STACK_NAME}"

info "Aguardando servicos iniciarem..."
sleep 10
docker stack services "${STACK_NAME}"

info "Deploy concluido!"
info "Acesse: https://scsi.digital"
info "Traefik dashboard: https://traefik.scsi.digital"
