# Validação de Deploy na VPS

## Pré-requisitos

- VPS com Ubuntu 22.04+ ou Debian 12+
- Docker Engine >= 25.x
- Docker Swarm inicializado (`docker swarm init`)
- Domínio `scsi.digital` apontando para o IP da VPS
- Token de API Cloudflare com permissão DNS:Edit
- Container registry (Docker Hub, GitHub Container Registry, ou registry próprio)

## Checklist de Validação

### 1. Infraestrutura da VPS

```bash
# Verificar Docker e Swarm
docker --version
docker node ls

# Verificar portas abertas
ss -tlnp | grep -E ':(80|443)'
```

### 2. Secrets

```bash
# Criar secrets manualmente (ou via deploy.sh)
echo "senha_segura_db" | docker secret create postgres_password -
echo "senha_segura_rabbit" | docker secret create rabbitmq_password -
echo "chave_secreta_django" | docker secret create secret_key -
echo "sk-openai-..." | docker secret create openai_api_key -
echo "cf_api_token_real" | docker secret create cf_api_token -

# Verificar
docker secret ls
```

### 3. Build e Push

```bash
# Build
docker build -f docker/Dockerfile -t registry.scsi.digital/scsi-app:latest .

# Push (requer login no registry)
docker push registry.scsi.digital/scsi-app:latest
```

### 4. Rede Traefik

```bash
docker network create --driver overlay traefik-public
docker network ls | grep traefik
```

### 5. Deploy da Stack

```bash
TAG=latest REGISTRY=registry.scsi.digital \
  POSTGRES_PASSWORD=senha_segura_db \
  RABBITMQ_PASSWORD=senha_segura_rabbit \
  ./scripts/deploy.sh
```

### 6. Verificar Serviços

```bash
# Todos os serviços devem estar running
docker stack services scsi

# Logs de cada serviço
docker service logs scsi_app --tail 20
docker service logs scsi_traefik --tail 20
docker service logs scsi_db --tail 20
```

### 7. Healthcheck da Aplicação

```bash
# Healthcheck interno
curl -f http://localhost:8000/health/
# Deve retornar: {"status":"ok","database":"connected"}

# Via Traefik (HTTPS)
curl -f https://scsi.digital/health/
```

### 8. TLS/SSL

```bash
# Verificar certificado
echo | openssl s_client -connect scsi.digital:443 -servername scsi.digital 2>/dev/null | openssl x509 -noout -dates

# Verificar HTTP->HTTPS redirect
curl -sI http://scsi.digital | head -1
# Deve retornar 301 ou 308
```

### 9. Backup

```bash
# Testar backup
BACKUP_DIR=/tmp/test-backup ./scripts/backup.sh
ls -lh /tmp/test-backup/
```

### 10. Rollback

```bash
# Em caso de falha, o deploy tem failure_action: rollback
# Verificar se houve rollback
docker service ps scsi_app

# Rollback manual se necessário
docker service update --rollback scsi_app
```

## Erros Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `no such host: registry.scsi.digital` | Registry não acessível | Usar Docker Hub: `REGISTRY=seuuser` |
| `certificate resolves to wrong IP` | DNS não propagado | Aguardar propagação ou testar com `--header "Host: scsi.digital" localhost` |
| `acme: error: 403` | Cloudflare token sem permissão | Verificar permissão DNS:Edit no token |
| `service replicas are all available with no leader` | Swarm sem leader | `docker swarm init` ou verificar nós |
| `secret not found` | Secret não criado | `docker secret create` antes do deploy |
