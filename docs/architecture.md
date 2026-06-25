# Arquitetura

## Diagrama de Componentes

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
    APP --> PG
    APP --> REDIS
    APP --> RABBITMQ
    CELERY_W --> PG
    CELERY_W --> RABBITMQ
    CELERY_W --> REDIS
    CELERY_W --> OPENAI
    CELERY_B --> RABBITMQ
    APP --> MEDIA
    APP --> STATIC
    TRAEFIK --> DNS
```

## Arquitetura Multi-Tenant

```mermaid
graph LR
    subgraph "Banco Compartilhado"
        DB[(PostgreSQL)]
    end

    subgraph "Corretora A"
        CA[Cliente A1]
        CA2[Cliente A2]
        PA[Proposta A]
    end

    subgraph "Corretora B"
        CB[Cliente B1]
        PB[Proposta B]
    end

    CA --> DB
    CA2 --> DB
    PA --> DB
    CB --> DB
    PB --> DB
```

O sistema usa arquitetura multi-tenant compartilhada: banco e schema compartilhados, com separacao por campos-chave (`brokerage`), filtros, managers e middlewares.

### Componentes de Tenant

- `Brokerage` - Entidade tenant
- `User.brokerage` - FK para corretora
- `TenantMiddleware` - Define `request.brokerage`
- `TenantManager` / `TenantQuerySet` - Filtros padrao
- `BaseTenantModel` - Model abstrato com FK brokerage
- `TenantAdminMixin` - Filtro no admin Django

## Fluxo de Download Seguro

```mermaid
sequenceDiagram
    Usuario->>+App: GET /attachments/1/download/
    App->>+DB: SELECT * WHERE pk=1 AND brokerage=user.brokerage
    alt Encontrado
        DB-->>App: Attachment
        App-->>-Usuario: FileResponse (arquivo)
    else Nao encontrado
        DB-->>App: Vazio
        App-->>-Usuario: 404 Not Found
    end
```
