# SCSI — Sistema de Gestão para Corretora de Seguros Inteligente

> Plataforma SaaS multi-tenant para corretoras de seguros com IA integrada.

**Stack:** Python > 3.13 · Django > 6.0 · PostgreSQL · Celery · RabbitMQ · Redis · LangChain > 1.0 · LangGraph · OpenAI GPT-5.5-mini · Docker · Docker Swarm · Traefik · Cloudflare DNS · Let's Encrypt wildcard TLS via DNS-01

**Domínio principal:** `scsi.digital`  
**Idioma do código:** inglês · **Interface:** português brasileiro · **Timezone:** `America/Sao_Paulo`

---

## Funcionalidades

| Módulo | Descrição |
|--------|-----------|
| **Multi-tenant** | Isolamento lógico por corretora (`Brokerage`) com middleware, managers e mixins |
| **Autenticação** | Login por email, recuperação de senha, onboarding com cadastro de corretora |
| **Clientes** | Cadastro PF/PJ com contato, endereço, documentos e resumo IA |
| **Seguradoras** | Cadastro de seguradoras, ramos e coberturas |
| **Propostas e Apólices** | Ciclo completo com itens cobertos, coberturas e botão "Gerar Apólice" |
| **Sinistros** | Vinculados a apólice e item coberto, com resumo IA |
| **Renovações e Endossos** | Gestão de renovações e endossos vinculados a apólices |
| **CRM** | Pipeline personalizável com Kanban e drag-and-drop |
| **Agentes e Produtores** | Cadastro com taxas de comissão |
| **Comissões e Repasses** | Registro de comissões recebidas/repassadas com cálculo de saldo |
| **Dashboard** | Métricas, gráficos por status e funil de negociações |
| **Relatórios** | Exportação CSV de todas as entidades |
| **Anexos Privados** | Upload e download seguro com isolamento cross-tenant (GenericForeignKey) |
| **IA** | Resumo de entidades via Celery + LangChain e Chat contextual por tenant |
| **Notificações** | Alertas de conclusão de tarefas com link direto |
| **Admin** | Django Admin customizado com `TenantAdminMixin` e `TenantFilter` |

---

## Arquitetura

```mermaid
graph TB
    subgraph "Cliente"
        WEB[Navegador]
    end
    subgraph "Docker Swarm"
        TRAEFIK[Traefik - Proxy Reverso]
        subgraph "App Services"
            APP[Django App]
            CELERY_W[Celery Worker]
            CELERY_B[Celery Beat]
        end
        subgraph "Data Layer"
            PG[(PostgreSQL)]
            REDIS[(Redis)]
            RABBITMQ[RabbitMQ]
        end
        subgraph "Storage"
            MEDIA[Media Files]
            STATIC[Static Files]
        end
    end
    subgraph "External"
        OPENAI[OpenAI API]
        DNS[Cloudflare DNS]
    end
    WEB --> TRAEFIK
    TRAEFIK --> APP
    APP --> PG & REDIS & RABBITMQ & MEDIA & STATIC
    CELERY_W --> PG & RABBITMQ & REDIS & OPENAI
    CELERY_B --> RABBITMQ
    TRAEFIK --> DNS
```

### Multi-Tenant

O sistema usa arquitetura multi-tenant **compartilhada**: mesmo banco e schema, separação por campo `brokerage`.

**Componentes de isolamento:**
- `Brokerage` — entidade tenant
- `User.brokerage` — FK para corretora
- `TenantMiddleware` — define `request.brokerage`
- `TenantManager` / `TenantQuerySet` — `for_brokerage()` e `for_request()`
- `BaseTenantModel` — model abstrato com FK `brokerage` + `TenantManager`
- `TenantQuerysetMixin` — filtra views por `request.brokerage`
- `TenantAdminMixin` — filta admin por tenant
- `TenantCreateMixin` — atribui `brokerage` automaticamente na criação

### Fluxo de Download Seguro

```mermaid
sequenceDiagram
    Usuario->>+App: GET /attachments/1/download/
    App->>+DB: SELECT * WHERE pk=1 AND brokerage=user.brokerage
    alt Encontrado
        DB-->>App: Attachment
        App-->>-Usuario: FileResponse
    else Nao encontrado
        DB-->>App: Vazio
        App-->>-Usuario: 404 Not Found
    end
```

---

## Modelos

```mermaid
erDiagram
    Brokerage ||--o{ User : ""
    Brokerage ||--o{ Client : ""
    Brokerage ||--o{ Insurer : ""
    Brokerage ||--o{ Branch : ""
    Brokerage ||--o{ Coverage : ""
    Brokerage ||--o{ Proposal : ""
    Brokerage ||--o{ Policy : ""
    Brokerage ||--o{ Claim : ""
    Brokerage ||--o{ Renewal : ""
    Brokerage ||--o{ Endorsement : ""
    Brokerage ||--o{ Pipeline : ""
    Brokerage ||--o{ PipelineStage : ""
    Brokerage ||--o{ Deal : ""
    Brokerage ||--o{ Agent : ""
    Brokerage ||--o{ Producer : ""
    Brokerage ||--o{ Commission : ""
    Brokerage ||--o{ Attachment : ""
    Brokerage ||--o{ Notification : ""
    Brokerage ||--o{ ChatSession : ""
    Client ||--o{ Proposal : ""
    Client ||--o{ Policy : ""
    Client ||--o{ CoveredItem : ""
    Client ||--o{ Deal : ""
    Policy ||--o{ Claim : ""
    Policy ||--o{ Renewal : ""
    Policy ||--o{ Endorsement : ""
    Policy ||--o{ Commission : ""
    Branch ||--o{ Coverage : ""
    Branch ||--o{ Proposal : ""
    Branch ||--o{ Policy : ""
    Pipeline ||--o{ PipelineStage : ""
    Pipeline ||--o{ Deal : ""
    PipelineStage ||--o{ Deal : ""
    Agent ||--o{ Producer : ""
    CoveredItem ||--o{ Claim : ""
```

### Apps e Responsabilidades

| App | Modelos | Responsabilidade |
|-----|---------|------------------|
| `core` | Brokerage, User | Settings, auth, tenant middleware |
| `base` | — | Models base, mixins, managers, admin mixins |
| `accounts` | — | Onboarding, cadastro, landing page |
| `clients` | Client | Clientes PF/PJ |
| `insurers` | Insurer, Branch, Coverage | Seguradoras, ramos, coberturas |
| `policies` | Proposal, Policy, CoveredItem, Endorsement | Propostas, apólices, itens cobertos, endossos |
| `claims` | Claim | Sinistros |
| `renewals` | Renewal | Renovações |
| `crm` | Pipeline, PipelineStage, Deal | CRM, pipeline, kanban |
| `agents` | Agent, Producer | Agentes e produtores |
| `commissions` | Commission | Comissões e repasses |
| `attachments` | Attachment | Anexos (GenericForeignKey) |
| `dashboard` | — | Dashboard com métricas e funil |
| `reports` | — | Exportação CSV |
| `ai` | Notification, ChatSession, ChatMessage | IA, resumos, chat, notificações |

---

## Setup

### Pré-requisitos

- Python >= 3.13
- Docker e Docker Compose (opcional, para ambiente completo)
- PostgreSQL 16+ (ou SQLite para dev leve)

### Ambiente Local (sem Docker)

```bash
# Clonar
git clone <repo-url> && cd scsi

# Criar ambiente virtual
python3.13 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Copiar .env e ajustar
cp .env.example .env

# Migrar e criar superusuário
python manage.py migrate
python manage.py createsuperuser

# (Opcional) Gerar dados fictícios
python manage.py generate_fake_data

# Iniciar servidor
python manage.py runserver
```

Acessar: http://localhost:8000

### Ambiente Docker (desenvolvimento)

```bash
docker compose -f docker/docker-compose.yml up -d
```

Inicia: Django App (porta 8000), Celery Worker, Celery Beat, PostgreSQL, Redis, RabbitMQ.

### Ambiente Docker Swarm (produção)

```bash
# Na VPS com Swarm inicializado
./scripts/deploy.sh
```

Detalhes em [docs/deploy-validation.md](docs/deploy-validation.md).

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URL` | URL do banco | `postgres://scsi:scsi@db:5432/scsi` |
| `CELERY_BROKER_URL` | Broker Celery | `amqp://guest:guest@localhost:5672//` |
| `CELERY_RESULT_BACKEND` | Result backend | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | Chave OpenAI | (vazio — modo simulado) |
| `OPENAI_MODEL` | Modelo OpenAI | `gpt-4.1-nano` |
| `SECRET_KEY` | Chave Django | gerada automaticamente |
| `DEBUG` | Modo debug | `False` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost, 127.0.0.1` |
| `EMAIL_BACKEND` | Backend de email | `console` |
| `CELERY_TASK_ALWAYS_EAGER` | Executa tasks síncronas | `False` |

---

## Rotas da Aplicação

| Rota | Descrição |
|------|-----------|
| `/` | Landing page |
| `/accounts/signup/` | Cadastro de corretora |
| `/accounts/login/` | Login |
| `/dashboard/` | Dashboard com métricas |
| `/clients/` | CRUD clientes |
| `/insurers/` | CRUD seguradoras |
| `/branches/` | CRUD ramos |
| `/coverages/` | CRUD coberturas |
| `/proposals/` | CRUD propostas + Gerar Apólice |
| `/policies/` | CRUD apólices |
| `/covered-items/` | CRUD itens cobertos |
| `/claims/` | CRUD sinistros |
| `/renewals/` | CRUD renovações |
| `/endorsements/` | CRUD endossos |
| `/pipelines/` | Pipeline CRM + Kanban |
| `/deals/` | CRUD negociações |
| `/agents/` | CRUD agentes |
| `/producers/` | CRUD produtores |
| `/commissions/` | CRUD comissões |
| `/repasses/` | Cálculo de repasses |
| `/attachments/` | Anexos + upload/download seguro |
| `/chat/` | Chat IA |
| `/notifications/` | Notificações |
| `/reports/` | Exportação CSV |
| `/health/` | Healthcheck (público) |
| `/admin/` | Django Admin |

---

## Comandos Úteis

```bash
# Dados fictícios
python manage.py generate_fake_data

# Healthcheck
curl http://localhost:8000/health/

# Rodar checks Django
python manage.py check

# Migrations
python manage.py makemigrations
python manage.py migrate

# Admin (após criar superuser)
open http://localhost:8000/admin/

# Docs (com MKDocs instalado)
mkdocs serve
```

---

## Deploy em Produção

**Arquivos de deploy:**
- `docker/docker-stack.yml` — Stack Swarm (Traefik, App 2 réplicas, Celery, PostgreSQL, Redis, RabbitMQ)
- `docker/traefik/traefik.yml` — Config Traefik (Let's Encrypt DNS-01 Cloudflare, TLS 1.2+, HSTS)
- `scripts/deploy.sh` — Build → Push → Secrets → Deploy
- `scripts/backup.sh` — Backup PostgreSQL + media com retenção de 30 dias

**Fluxo:**
1. `docker swarm init` na VPS
2. Configurar DNS (Cloudflare) apontando `scsi.digital` para o IP da VPS
3. Definir `CF_API_TOKEN` com permissão DNS:Edit
4. Executar `./scripts/deploy.sh`

Veja [docs/deploy-validation.md](docs/deploy-validation.md) para checklist completo de validação.

---

## Segurança

- **Media privada**: sem rota pública (`static()` não incluído nas URLs); download via `AttachmentDownloadView` com autenticação e tenant
- **Cross-tenant**: toda query usa `for_brokerage()` ou `for_request()`; acesso negado retorna 404 (não 403)
- **Secrets**: Docker secrets em produção; `.env` no `.gitignore`
- **Redes Swarm**: serviços internos (db, redis, rabbitmq) isolados em `scsi-internal`; apenas Traefik exposto
- **TLS**: Let's Encrypt via DNS-01 Cloudflare com mínimo TLS 1.2
- **Sanitização IA**: `html.escape()` antes de converter Markdown para HTML no chat
- **Healthcheck sem auth**: `/health/` público, sem necessidade de banco

---

## Documentação Técnica

A documentação completa está em [`docs/`](docs/) com MKDocs + Mermaid:

```bash
mkdocs serve
# Acessar: http://localhost:8001
```

- [Visão Geral](docs/index.md)
- [Arquitetura](docs/architecture.md)
- [Setup](docs/setup.md)
- [Modelos](docs/models.md)
- [Validação de Deploy](docs/deploy-validation.md)
- [PRD Completo](PRD_SCSI.md)

---

## Licença

Proprietário — Uso interno.
