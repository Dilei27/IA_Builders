# PRD — SCSI: Sistema de Gestão para Corretora de Seguros Inteligente

> **Domínio principal:** `scsi.digital`  
> **Stack:** Python > 3.13 · Django > 6.0 · PostgreSQL · Celery · RabbitMQ · Redis · LangChain > 1.0 · LangGraph · OpenAI `GPT-5.5-mini` · Docker · Docker Swarm · Traefik · Cloudflare DNS · Let's Encrypt wildcard TLS via DNS-01.  
> **Idioma do código:** inglês. **Idioma da interface:** português brasileiro. **Timezone:** `America/Sao_Paulo`.

---

## 1. Visão Geral

O **SCSI — Sistema de Gestão para Corretora de Seguros Inteligente** é uma plataforma SaaS multi-tenant para corretoras de seguros. O sistema DEVE permitir que múltiplas corretoras operem na mesma instância da aplicação, com isolamento lógico rigoroso por tenant/corretora em usuários, permissões, arquivos, clientes, propostas, apólices, sinistros, renovações, negociações, comissões, relatórios e agentes de IA.

Cada corretora DEVE enxergar o sistema como se fosse exclusivo. Dados, arquivos e registros de uma corretora NUNCA DEVEM aparecer para usuários de outra corretora.

O sistema combina gestão operacional de corretora, CRM, relatórios e agentes de IA construídos com LangChain/LangGraph. Os agentes DEVEM respeitar o tenant do usuário autenticado e utilizar o modelo `GPT-5.5-mini` via OpenAI.

---

## 2. Objetivos do Produto

1. Centralizar a operação de corretoras de seguros em um SaaS multi-tenant.
2. Garantir isolamento absoluto de dados entre corretoras.
3. Automatizar fluxos de propostas, apólices, sinistros, renovações, endossos e comissões.
4. Oferecer CRM visual com pipeline Kanban personalizável.
5. Fornecer dashboard com métricas, gráficos, funil e insights.
6. Disponibilizar relatórios exportáveis em PDF e CSV.
7. Integrar agentes de IA para resumos e chat contextual por corretora.
8. Processar tarefas pesadas via Celery, sem bloquear a interface.
9. Proteger arquivos privados contra acesso público e cross-tenant.
10. Entregar deploy resiliente em Docker Swarm com Traefik, TLS wildcard e rollback automático.

---

## 3. Público-Alvo

| Perfil | Descrição |
|---|---|
| Dono/Admin da corretora | Gerencia usuários, dados, comissões, relatórios e configurações do tenant. |
| Agente | Pessoa ou empresa parceira que vende seguros para a corretora. |
| Produtor | Corretor final, vinculado ou não a um agente. |
| Operacional | Usuário interno de backoffice com permissões específicas. |

Todo usuário DEVE pertencer a exatamente uma corretora, exceto superusuários administrativos do Django.

---

## 4. Escopo do Produto

- Plataforma SaaS multi-tenant compartilhada.
- Landing page em `scsi.digital`.
- Cadastro de conta com corretora, CNPJ, Razão Social e plano free.
- Login por email e recuperação de senha via Django.
- Gestão de usuários e permissões.
- Gestão de clientes, seguradoras, ramos, coberturas e itens cobertos.
- Gestão de propostas, geração de apólices, apólices, endossos, sinistros e renovações.
- Gestão de agentes, produtores, comissões e repasses.
- CRM em grid e Kanban com pipeline personalizável.
- Dashboard completo com gráficos e funil.
- Relatórios PDF e CSV.
- Anexos privados em clientes, propostas, apólices e sinistros.
- Agentes de IA para resumos e chat contextual por tenant.
- Celery com RabbitMQ como broker e Redis como result backend/cache.
- Admin Django com filtros e respeito ao tenant.
- Dados fake via management command.
- Documentação em `docs/` com MKDocs e Mermaid.
- Docker Compose local e Docker Swarm em produção.
- Traefik com TLS wildcard via Let's Encrypt DNS-01 Cloudflare.
- Scripts `scripts/deploy.sh` e `scripts/backup.sh`.

---

## 5. Fora de Escopo Inicial

- Integração real de pagamentos.
- Integração com APIs externas de seguradoras.
- Aplicativo mobile nativo.
- Schemas ou bancos separados por tenant.
- Testes automatizados.
- Migração automática de sistemas legados.

---

## 6. Requisitos Técnicos Mandatórios

### 6.1 Python, Django e Projeto

- Usar Python > 3.13.
- Usar Django > 6.0.
- Ambiente virtual em `.venv` na raiz.
- `requirements.txt` SEMPRE atualizado na raiz.
- Manter apenas um `settings.py`.
- Usar `django-environ` para carregar `.env`.
- Usar PostgreSQL.
- Código do projeto em inglês.
- Interface em português brasileiro.
- Timezone obrigatório: `America/Sao_Paulo`.
- Código simples, PEP8 e aspas simples em Python.
- Preferir Class Based Views e recursos nativos do Django.
- Signals, se usados, DEVEM ficar em `signals.py` dentro da app correspondente.
- NÃO implementar testes automatizados neste momento.

### 6.2 Apps Django

- Apps devem ficar na raiz do projeto.
- App principal: `core`.
- App base compartilhado: `base`.
- Entidades/domínios devem ser separados em apps.
- Todo model/tabela DEVE conter `created_at` e `updated_at`.

Apps recomendados:

| App | Responsabilidade |
|---|---|
| `core` | Settings, URLs, healthcheck, custom user, Brokerage, middleware de tenant. |
| `base` | Models base, mixins, managers, utils e constants. |
| `accounts` | Onboarding, usuários, perfis e permissões. |
| `clients` | Clientes e anexos de clientes. |
| `insurers` | Seguradoras e ramos. |
| `policies` | Propostas, apólices, coberturas, itens cobertos e endossos. |
| `claims` | Sinistros e anexos. |
| `renewals` | Renovações. |
| `crm` | Pipeline, etapas e negociações. |
| `agents` | Agentes e produtores. |
| `commissions` | Comissões e repasses. |
| `reports` | Relatórios PDF/CSV. |
| `dashboard` | Métricas e gráficos. |
| `ai` | Agentes, tools, chat e tasks de IA. |

---

## 7. Arquitetura Multi-Tenant

O sistema DEVE usar arquitetura multi-tenant compartilhada: banco e schema compartilhados, com separação por campos-chave, filtros, permissões e middlewares.

Regras obrigatórias:

- Todo model sensível DEVE ter FK `brokerage` para a corretora/tenant.
- Toda query sensível DEVE filtrar por `brokerage`.
- Views, forms, admin, relatórios, tasks e tools de IA DEVEM respeitar o tenant.
- O tenant do usuário DEVE vir do usuário autenticado, nunca de input livre do cliente ou do LLM.
- Admin Django DEVE filtrar por tenant, exceto superuser.
- Cross-tenant em arquivos privados DEVE retornar 404 para não vazar existência.

Componentes esperados:

- `Brokerage` como entidade tenant.
- `User` customizado com login por email e FK para `Brokerage`.
- `TenantMiddleware` definindo `request.brokerage`.
- `TenantManager` e/ou `BaseTenantModel` para padronizar filtros.
- Mixins de permissão e validação por tenant.

---

## 8. Segurança e Proteção de Arquivos

- Arquivos/media NÃO DEVEM ser públicos.
- Anexos DEVEM ser servidos por view segura com autenticação, tenant e permissão.
- `MEDIA_ROOT` deve usar volume persistente.
- Traefik NÃO DEVE expor media diretamente.
- Uploads devem validar tipo/extensão quando aplicável.
- Markdown de IA DEVE ser sanitizado antes de renderizar HTML.
- Segredos não podem ser versionados.

Fluxo de download seguro:

1. Usuário autenticado solicita arquivo.
2. Backend busca attachment filtrando `brokerage=request.user.brokerage`.
3. Backend valida permissão.
4. Se não autorizado ou cross-tenant, retorna 404.
5. Se autorizado, retorna `FileResponse`.

---

## 9. Requisitos Funcionais

### 9.1 Usuários e Autenticação

- Gestão de usuários com autenticação e permissões.
- Login por email, não username.
- Recuperação de senha por email usando recursos nativos do Django.
- Perfis: dono/admin, agente, produtor, operacional.

### 9.2 Landing Page e Cadastro

- Landing page em `scsi.digital`.
- CTAs para criar conta e login.
- Cadastro da corretora com CNPJ e Razão Social obrigatórios.
- Planos fictícios inicialmente.
- Apenas plano free habilitado.
- Outros planos com botão `em breve` desabilitado.
- Sem cartão de crédito para plano free.

### 9.3 Cadastros Base

- Clientes.
- Seguradoras.
- Ramos.
- Coberturas.
- Itens cobertos.
- Agentes.
- Produtores.

### 9.4 Propostas e Apólices

- Gestão de propostas.
- Gestão de apólices.
- Botão `Gerar apólice` na proposta.
- Ao gerar apólice, copiar dados essenciais da proposta.
- Propostas e apólices DEVEM ter itens cobertos.
- Propostas e apólices DEVEM ter coberturas.

### 9.5 Itens Cobertos

- Item coberto representa o objeto segurado: automóvel, imóvel, frota, viagem, vida ou outro.
- Proposta pode ter múltiplos itens cobertos.
- Apólice pode ter múltiplos itens cobertos.
- Sinistro SEMPRE deve estar vinculado a item coberto por uma apólice.

### 9.6 Sinistros

- Gestão de sinistros.
- Vínculo obrigatório com apólice e item coberto.
- Suporte a anexos privados.
- Resumo com IA.

### 9.7 CRM

- Painel CRM em grid.
- Painel CRM em Kanban.
- Pipeline personalizável por tenant.
- Etapas com nome, cor e ordem.
- Cards arrastáveis entre etapas.
- Negociações podem ser resumidas com IA.

### 9.8 Renovações e Endossos

- Gestão de renovações com vencimentos e status.
- Gestão de endossos vinculados a apólices.

### 9.9 Comissões

- Comissão é paga à corretora.
- Corretora repassa comissão a agentes e produtores.
- Sistema DEVE calcular e registrar repasses.
- Relatórios de comissão e repasse.

### 9.10 Dashboard

- Visão geral da corretora.
- Métricas de clientes, seguros, seguradoras e valores.
- Gráficos variados.
- Gráfico de funil de negociações/leads.
- Insights da carteira.

### 9.11 Relatórios

- Tela e menu dedicados a relatórios.
- Exportação PDF via ReportLab/PyPDF.
- Exportação CSV.
- Relatórios de clientes, propostas, apólices, sinistros, renovações, comissões e carteira.

### 9.12 Inteligência Artificial

- Resumir cliente.
- Resumir apólice.
- Resumir sinistro.
- Resumir proposta.
- Resumir negociação.
- Botão `Resumir com IA` deve disparar task Celery.
- UI deve mostrar loading e mensagem de que o usuário será notificado.
- Resultado salvo em `ai_summary` da entidade.
- Notificação interna ao concluir.
- Chat com IA no menu lateral.
- Sessões de chat salvas por usuário.
- Resposta em stream.
- Resposta em Markdown renderizada com sanitização.
- Tools de IA DEVEM acessar apenas dados do tenant do usuário.

---

## 10. Requisitos Não Funcionais

- Sistema responsivo para desktop, tablet e mobile.
- UI/UX excelente, seguindo `design_system/design-system.html`.
- Rotas protegidas por autenticação/permissão.
- Dados sensíveis não devem ser expostos.
- Processos pesados não podem bloquear request/response.
- Filtros e telas devem ter bom desempenho.
- Celery para tarefas pesadas, especialmente IA.
- Deploy resiliente com healthchecks, restart policies e resource limits.
- Atualização do app sem downtime com `start-first` e rollback.
- Serviços não devem entrar em crash-loop por dependências indisponíveis.

---

## 11. IA com LangChain e LangGraph

- Usar LangChain > 1.0.
- Usar LangGraph.
- Modelo obrigatório: `GPT-5.5-mini` via OpenAI.
- Tasks de resumo executadas por Celery.
- Chat com resposta stream.
- Tools somente leitura, filtradas por `brokerage_id`.
- O LLM NUNCA deve definir ou alterar o tenant.

Tools esperadas:

- `list_clients(brokerage_id, ...)`
- `get_client_detail(brokerage_id, client_id)`
- `list_policies(brokerage_id, ...)`
- `get_policy_detail(brokerage_id, policy_id)`
- `list_claims(brokerage_id, ...)`
- `list_proposals(brokerage_id, ...)`
- `list_deals(brokerage_id, ...)`
- `get_renewals(brokerage_id, ...)`
- `get_commissions_summary(brokerage_id, ...)`

---

## 12. Docker, Serviços e Redes

### 12.1 Serviços Obrigatórios

- `app` — Django.
- `db` — PostgreSQL.
- `celery_worker`.
- `celery_beat`.
- `rabbitmq` — broker Celery.
- `redis` — result backend Celery e cache.
- `traefik` — web server/load balancer.

### 12.2 Registry

- Imagem da aplicação: `ghcr.io/pycodebr/scsi_v1`.
- Deploy Swarm: `docker stack deploy --with-registry-auth`.

### 12.3 Redes Overlay em Produção

| Rede | Tipo | Serviços |
|---|---|---|
| `traefik_public` | overlay external pública | `traefik`, `app` |
| `scsi_v1_internal` | overlay `internal: true` | `app`, `db`, `redis`, `rabbitmq`, `celery_worker`, `celery_beat` |
| `scsi_v1_egress` | overlay com internet, sem Traefik | `celery_worker`, `celery_beat` |

Regras obrigatórias:

- `app` em `traefik_public` e `scsi_v1_internal`.
- `db`, `redis`, `rabbitmq` somente em `scsi_v1_internal`.
- `celery_worker` e `celery_beat` em `scsi_v1_internal` e `scsi_v1_egress`.
- NUNCA colocar Celery na `traefik_public`.

### 12.4 Volumes Nomeados

- PostgreSQL.
- Redis.
- RabbitMQ.
- Media.
- Staticfiles.
- Certificados Let's Encrypt.

---

## 13. Traefik, TLS e Cloudflare

- Traefik DEVE emitir certificado wildcard para `scsi.digital` e `*.scsi.digital`.
- Usar Let's Encrypt via DNS-01 Cloudflare.
- DNS-01 é obrigatório para wildcard.
- Não usar `tlschallenge` e `dnschallenge` juntos no mesmo resolver.
- Token Cloudflare com escopo `Zone > DNS > Edit` na zona `scsi.digital`.
- Token Cloudflare NUNCA em texto puro no compose/stack ou `.env` versionado.
- Secret obrigatório: `CLOUDFLARE_DNS_API_TOKEN`.
- Traefik lê token via `CF_DNS_API_TOKEN_FILE=/run/secrets/CLOUDFLARE_DNS_API_TOKEN`.
- Traefik deve redirecionar HTTP para HTTPS.
- Traefik deve confiar nas faixas de IP do Cloudflare via `forwardedHeaders.trustedIPs`.

---

## 14. Variáveis de Ambiente e Secrets

- `.env` na raiz, gitignored.
- `.env` de produção separado do desenvolvimento.
- Serviços recebem variáveis via `env_file`.
- Scripts DEVEM ler `.env` com parser seguro de `KEY=VALUE`.
- NUNCA usar `source` ou `.` para carregar `.env`.
- Parser deve suportar caracteres especiais como `&`, `$`, `*`, `@`.
- Segredos de produção devem preferir Docker Secrets.

Produção obrigatória:

```env
DEBUG=False
ALLOWED_HOSTS=scsi.digital,.scsi.digital,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://scsi.digital,https://*.scsi.digital
TIME_ZONE=America/Sao_Paulo
LANGUAGE_CODE=pt-br
OPENAI_MODEL=gpt-5.5-mini
```

Regras:

- `ALLOWED_HOSTS` contém apenas hostnames, nunca URL com esquema.
- `.scsi.digital` cobre subdomínios.
- `localhost` e `127.0.0.1` são obrigatórios para healthcheck interno.
- `CSRF_TRUSTED_ORIGINS` deve ter esquema `https`.

Settings obrigatórios em produção:

```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REDIRECT_EXEMPT = [r'^health/$']
```

---

## 15. Healthchecks, Entrypoints e Migrations

### 15.1 Healthcheck

- Endpoint obrigatório: `/health/`.
- Deve retornar 200.
- Não deve acessar banco.
- Não deve exigir autenticação.
- Usado pelo container e Traefik.

Healthchecks:

| Serviço | Comando |
|---|---|
| app | HTTP `/health/` |
| PostgreSQL | `pg_isready` |
| Redis | `redis-cli ping` |
| RabbitMQ | `rabbitmq-diagnostics check_port_connectivity` |

### 15.2 Entrypoint App

1. `wait_for_db`.
2. Migrations com advisory lock PostgreSQL.
3. `collectstatic --clear`.
4. Iniciar app.

### 15.3 Entrypoint Celery

1. `wait_for_db`.
2. Iniciar worker/beat.

Celery NÃO DEVE rodar migrations nem collectstatic.

---

## 16. Scripts Obrigatórios

### 16.1 `scripts/deploy.sh`

Executado na VPS. Deve:

- Ler `.env` com parser seguro.
- Validar Swarm ativo.
- Validar secret `CLOUDFLARE_DNS_API_TOKEN`.
- Validar redes `traefik_public` e `scsi_v1_egress`.
- Validar `DEBUG=False`.
- Validar `localhost` em `ALLOWED_HOSTS`.
- Executar `git pull`.
- Fazer build e push da imagem para GHCR.
- Rodar `docker stack deploy --with-registry-auth`.
- Forçar rollout de `app`, `celery_worker` e `celery_beat`.
- Suportar `--skip-build`.

### 16.2 `scripts/backup.sh`

Deve:

- Fazer backup PostgreSQL com `pg_dump`.
- Fazer backup de media.
- Ter rotação por tempo.
- Ser compatível com cron.

---

## 17. Guia de Deploy em VPS Ubuntu do Zero

### 17.1 Acessar VPS

```bash
ssh root@<VPS_IP>
```

### 17.2 Atualizar sistema

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release ufw fail2ban htop git jq
```

### 17.3 Firewall

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 17.4 Instalar Docker

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable docker
sudo systemctl start docker
```

### 17.5 Login GHCR

```bash
echo "<GHCR_TOKEN>" | docker login ghcr.io -u <GHCR_USER> --password-stdin
```

### 17.6 Inicializar Swarm

```bash
docker swarm init --advertise-addr <VPS_IP>
```

### 17.7 Criar redes overlay

```bash
docker network create --driver overlay --attachable traefik_public
docker network create --driver overlay --internal scsi_v1_internal
docker network create --driver overlay scsi_v1_egress
```

### 17.8 Criar token Cloudflare

- Cloudflare → My Profile → API Tokens → Create Token.
- Escopo: `Zone > DNS > Edit`.
- Zona: `scsi.digital`.

### 17.9 Criar secret Cloudflare

```bash
echo "<CLOUDFLARE_TOKEN>" | docker secret create CLOUDFLARE_DNS_API_TOKEN -
```

### 17.10 Criar demais secrets

```bash
echo "<DJANGO_SECRET_KEY>" | docker secret create DJANGO_SECRET_KEY -
echo "<POSTGRES_PASSWORD>" | docker secret create POSTGRES_PASSWORD -
echo "<OPENAI_API_KEY>" | docker secret create OPENAI_API_KEY -
```

### 17.11 Configurar `.env.production`

```env
DEBUG=False
DJANGO_SETTINGS_MODULE=core.settings
ALLOWED_HOSTS=scsi.digital,.scsi.digital,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://scsi.digital,https://*.scsi.digital
TIME_ZONE=America/Sao_Paulo
LANGUAGE_CODE=pt-br
DATABASE_URL=postgres://scsi:<POSTGRES_PASSWORD>@db:5432/scsi
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=amqp://rabbitmq:5672//
OPENAI_MODEL=gpt-5.5-mini
```

### 17.12 Configurar DNS Cloudflare

- Criar registros `A`/`AAAA` apontando `scsi.digital` para a VPS.
- Usar SSL/TLS `Full (strict)` quando certificado estiver válido.

### 17.13 Build e push manual

```bash
docker build -t ghcr.io/pycodebr/scsi_v1:latest -f docker/Dockerfile .
docker push ghcr.io/pycodebr/scsi_v1:latest
```

### 17.14 Deploy stack

```bash
docker stack deploy -c docker/docker-stack.yml --with-registry-auth scsi_v1
```

### 17.15 Verificações

```bash
docker service ls
docker service logs scsi_v1_app -f
docker service logs scsi_v1_traefik -f
curl -fsS http://localhost/health/
curl -I https://scsi.digital
```

### 17.16 Verificar certificado wildcard

```bash
docker service logs scsi_v1_traefik | grep -i acme
```

### 17.17 Usar script de deploy

```bash
chmod +x scripts/deploy.sh
sudo ./scripts/deploy.sh
sudo ./scripts/deploy.sh --skip-build
```

### 17.18 Backup

```bash
chmod +x scripts/backup.sh
sudo ./scripts/backup.sh
```

---

## 18. Modelagem Conceitual Inicial

### 18.1 Core

- `Brokerage`: `cnpj`, `legal_name`, `trade_name`, `email`, `phone`, `plan`, `is_active`.
- `User`: `email`, `full_name`, `brokerage`, `role`, `is_active`.

### 18.2 Domínio

- `Client`: cliente PF/PJ, contato, endereço, agente/produtor, `ai_summary`.
- `Insurer`: seguradora.
- `Branch`: ramo.
- `Coverage`: cobertura.
- `CoveredItem`: item segurado com tipo, descrição e detalhes em JSON.
- `Proposal`: proposta, status, prêmio, coberturas e itens cobertos.
- `Policy`: apólice, vigência, prêmio, status, coberturas e itens cobertos.
- `Endorsement`: endosso da apólice.
- `Claim`: sinistro vinculado a apólice e item coberto.
- `Renewal`: renovação vinculada a apólice.
- `Pipeline`, `PipelineStage`, `Deal`: CRM.
- `Agent`, `Producer`: hierarquia comercial.
- `Commission`: comissão total, repasses e líquido da corretora.
- `ChatSession`, `ChatMessage`: chat IA.
- `Notification`: notificações internas.

---

## 19. Documentação

- Criar pasta `docs/`.
- Usar MKDocs.
- Habilitar Mermaid.
- Manter documentação de instalação, arquitetura, deploy, operação e uso.

---

## 20. Dados Fake

Criar command Django `load_fake_data` para demonstrar:

- múltiplas corretoras;
- múltiplos usuários;
- clientes;
- seguradoras;
- ramos;
- coberturas;
- propostas;
- apólices;
- itens cobertos;
- sinistros;
- renovações;
- endossos;
- agentes;
- produtores;
- comissões;
- pipeline CRM;
- datas variadas.

---

## 21. Critérios de Aceite

- [ ] Usuário de uma corretora não acessa dados de outra.
- [ ] Arquivos privados não são públicos.
- [ ] `/health/` retorna 200 sem banco e sem autenticação.
- [ ] App sobe com Docker Compose.
- [ ] Stack sobe com Docker Swarm.
- [ ] Traefik emite wildcard TLS via DNS-01.
- [ ] Celery processa IA sem bloquear a interface.
- [ ] Redis funciona como cache e result backend.
- [ ] RabbitMQ funciona como broker.
- [ ] Proposta gera apólice.
- [ ] Sinistro está ligado a item coberto de apólice.
- [ ] Chat IA respeita tenant.
- [ ] Relatórios exportam PDF e CSV.
- [ ] Dashboard exibe gráficos e funil.
- [ ] Deploy usa secrets e não expõe credenciais.
- [ ] Celery não está na `traefik_public`.
- [ ] Migrations usam advisory lock.
- [ ] `collectstatic --clear` roda no app.
- [ ] App atualiza sem downtime.
- [ ] Login por email.
- [ ] Recuperação de senha por email.
- [ ] Landing page com apenas plano free habilitado.
- [ ] Resumos de IA salvos em `ai_summary`.
- [ ] Chat IA com stream e Markdown sanitizado.
- [ ] Admin filtra por tenant, exceto superuser.

---

## 22. Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Cross-tenant por query sem filtro | `TenantManager`, middleware, mixins e revisão obrigatória. |
| Vazamento de media | View segura, validação de tenant e retorno 404. |
| IA acessando outro tenant | Tools recebem tenant do usuário autenticado, nunca do LLM. |
| Migrations concorrentes | Advisory lock PostgreSQL. |
| Conflito de staticfiles | `collectstatic --clear`. |
| Crash-loop | `wait_for_db`, healthchecks e restart policies. |
| Token Cloudflare exposto | Docker Secret obrigatório. |
| Loop HTTPS atrás do proxy | `SECURE_PROXY_SSL_HEADER` e `/health/` isento. |
| XSS via Markdown | Sanitização antes de renderizar HTML. |
| Starvation na VPS | `resources.limits` e `reservations`. |

---

## 23. Sprints de Desenvolvimento

### Sprint 1 — Fundação

- [X] Criar estrutura base do projeto.
- [X] Criar `.venv`.
- [X] Criar `requirements.txt`.
- [X] Configurar `core/settings.py` com `django-environ`.
- [X] Configurar timezone, idioma, hosts e CSRF.
- [X] Criar `.env` e `.gitignore`.

### Sprint 2 — Docker Local

- [X] Criar `docker/Dockerfile`.
- [X] Criar `docker/docker-compose.yml`.
- [X] Criar entrypoint app.
- [X] Criar entrypoint Celery.
- [X] Adicionar PostgreSQL, Redis e RabbitMQ.
- [X] Validar subida local.

### Sprint 3 — Base Django

- [X] Criar app `base`.
- [X] Criar `BaseModel` com timestamps.
- [X] Criar comando `wait_for_db`.
- [X] Criar rota `/health/`.
- [X] Configurar WhiteNoise.

### Sprint 4 — Usuário e Auth

- [X] Criar custom user com email.
- [X] Configurar `AUTH_USER_MODEL`.
- [X] Implementar login por email.
- [X] Implementar recuperação de senha.
- [X] Configurar email via `.env`.

### Sprint 5 — Multi-Tenant

- [X] Criar `Brokerage`.
- [X] Vincular usuário a corretora.
- [X] Criar middleware de tenant.
- [X] Criar manager/mixins de tenant.
- [X] Validar isolamento base.

### Sprint 6 — Onboarding

- [X] Criar cadastro de corretora + usuário owner.
- [X] Validar CNPJ e Razão Social obrigatórios.
- [X] Criar seleção de plano free.
- [X] Criar landing page.

### Sprint 7 — Clientes

- [X] Criar app `clients`.
- [X] Criar model `Client`.
- [X] Criar CRUD CBV.
- [X] Criar tela de detalhe.

### Sprint 8 — Seguradoras, Ramos, Coberturas e Itens

- [X] Criar `Insurer`.
- [X] Criar `Branch`.
- [X] Criar `Coverage`.
- [X] Criar `CoveredItem`.
- [X] Criar CRUDs.

### Sprint 9 — Propostas e Apólices

- [X] Criar `Proposal`.
- [X] Criar `Policy`.
- [X] Criar CRUD.
- [X] Implementar botão `Gerar apólice`.

### Sprint 10 — Sinistros, Renovações e Endossos

- [X] Criar `Claim` vinculado a apólice e item coberto.
- [X] Criar `Renewal`.
- [X] Criar `Endorsement`.
- [X] Criar CRUDs.

### Sprint 11 — Anexos Privados

- [X] Criar models de anexos.
- [X] Criar upload.
- [X] Criar download seguro.
- [X] Validar 404 cross-tenant.

### Sprint 12 — CRM

- [X] Criar `Pipeline`.
- [X] Criar `PipelineStage`.
- [X] Criar `Deal`.
- [X] Criar grid.
- [X] Criar Kanban com drag-and-drop.

### Sprint 13 — Agentes, Produtores e Comissões

- [X] Criar `Agent`.
- [X] Criar `Producer`.
- [X] Criar `Commission`.
- [X] Implementar cálculo de repasses.

### Sprint 14 — Dashboard e Relatórios

- [X] Criar app `dashboard`.
- [X] Criar métricas principais.
- [X] Criar gráficos.
- [X] Criar funil.
- [X] Criar app `reports`.
- [X] Implementar CSV.

### Sprint 15 — Celery e IA

- [X] Configurar Celery.
- [X] Configurar RabbitMQ.
- [X] Configurar Redis.
- [X] Configurar LangChain e LangGraph.
- [X] Criar tools filtradas por tenant.
- [X] Criar resumos com IA.
- [X] Criar notificações ao concluir.

### Sprint 16 — Chat IA

- [X] Criar `ChatSession`.
- [X] Criar `ChatMessage`.
- [X] Criar tela de chat.
- [X] Implementar stream.
- [X] Renderizar Markdown sanitizado.

### Sprint 17 — Admin, Dados Fake e Docs

- [X] Registrar entidades no admin.
- [X] Filtrar admin por tenant.
- [X] Criar command `generate_fake_data`.
- [X] Configurar MKDocs.
- [X] Documentar arquitetura e deploy.

### Sprint 18 — Swarm, Traefik e Deploy

- [X] Criar `docker/docker-stack.yml`.
- [X] Configurar redes, volumes, healthchecks e resources.
- [X] Configurar Traefik DNS-01 Cloudflare.
- [X] Criar `scripts/deploy.sh`.
- [X] Criar `scripts/backup.sh`.
- [X] Revisar e documentar validação de deploy na VPS (`docs/deploy-validation.md`).

### Sprint 19 — Hardening Final

- [X] Revisar isolamento multi-tenant.
- [X] Revisar proteção de media.
- [X] Revisar secrets.
- [X] Revisar redes Docker.
- [X] Revisar healthchecks.
- [X] Revisar IA e sanitização.
- [X] Revisar UX responsiva.

---

## 24. Checklist Final de Qualidade

- [X] Python > 3.13.
- [X] Django > 6.0.
- [X] Único `settings.py`.
- [X] `.env` gitignored.
- [X] Login por email.
- [X] Timezone `America/Sao_Paulo`.
- [X] Código em inglês.
- [X] Interface em português brasileiro.
- [X] Apps na raiz.
- [X] `core` e `base` presentes.
- [X] Todo model com timestamps.
- [X] Multi-tenant por `brokerage`.
- [X] Middleware e manager de tenant.
- [X] Admin filtra por tenant.
- [X] Media privada.
- [X] IA com GPT-5.5-mini.
- [X] Tools de IA filtradas por tenant.
- [X] Celery + RabbitMQ + Redis.
- [X] `django-celery-beat`.
- [X] Proposta gera apólice.
- [X] Sinistro vinculado a item coberto.
- [X] CRM grid e Kanban.
- [X] Relatórios CSV e PDF.
- [X] Dashboard com funil.
- [X] MKDocs com Mermaid.
- [X] `/health/` sem banco e sem auth.
- [X] Migrations com advisory lock.
- [X] `collectstatic --clear`.
- [X] Redes Swarm corretas.
- [X] Celery fora da `traefik_public`.
- [X] Traefik com wildcard DNS-01.
- [X] Secret Cloudflare via Docker Secret.
- [X] Deploy com `--with-registry-auth`.
- [X] Scripts de deploy e backup.
- [X] Sem testes automatizados neste momento.
