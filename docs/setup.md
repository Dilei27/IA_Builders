# Setup

## Requisitos

- Python > 3.13
- Docker e Docker Compose (para ambiente completo)
- PostgreSQL 16+ (ou SQLite para dev leve)

## Ambiente Local (Sem Docker)

```bash
# Clonar repositorio
git clone <repo-url> && cd scsi

# Criar ambiente virtual
python3.13 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variaveis de ambiente
cp .env.example .env
# Editar .env com suas configuracoes

# Rodar migracoes
python manage.py migrate

# Criar superusuario
python manage.py createsuperuser

# Gerar dados ficticios
python manage.py generate_fake_data

# Rodar servidor
python manage.py runserver
```

## Ambiente Docker

```bash
docker compose -f docker/docker-compose.yml up -d
```

Isso inicia: Django App, Celery Worker, Celery Beat, PostgreSQL, Redis, RabbitMQ.

## Variaveis de Ambiente

| Variavel | Descricao | Padrao |
|---|---|---|
| `DATABASE_URL` | URL do banco de dados | `postgres://scsi:scsi@db:5432/scsi` |
| `CELERY_BROKER_URL` | URL do broker Celery | `amqp://guest:guest@localhost:5672//` |
| `CELERY_RESULT_BACKEND` | Backend de resultados Celery | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | Chave da API OpenAI | (vazio - modo simulado) |
| `OPENAI_MODEL` | Modelo OpenAI | `gpt-4.1-nano` |
| `SECRET_KEY` | Chave secreta Django | (gerada automaticamente em dev) |
| `DEBUG` | Modo debug | `False` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost, 127.0.0.1` |
| `EMAIL_BACKEND` | Backend de email | `console` |
