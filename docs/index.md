# SCSI - Sistema de Gestao para Corretora de Seguros Inteligente

> Plataforma SaaS multi-tenant para corretoras de seguros com IA integrada.

**Stack:** Python > 3.13 · Django > 6.0 · PostgreSQL · Celery · RabbitMQ · Redis · LangChain > 1.0 · OpenAI GPT-5.5-mini · Docker · Docker Swarm · Traefik

## Documentacao

- [Arquitetura](architecture.md)
- [Setup](setup.md)
- [Modelos](models.md)

## Visao Geral

O SCSI e uma plataforma SaaS multi-tenant que permite que multiplas corretoras de seguros operem na mesma instancia da aplicacao, com isolamento logico rigoroso por tenant/corretora.

### Funcionalidades Principais

- **Multi-tenant:** Isolamento logico por corretora (brokerage)
- **Gestao de Clientes:** Cadastro PF/PJ com contato e endereco
- **Seguradoras e Ramos:** Catalogacao de seguradoras, ramos e coberturas
- **Propostas e Apolices:** Ciclo completo de proposal/apolice com itens cobertos
- **Sinistros:** Registro vinculado a apolice e item coberto
- **CRM:** Pipeline personalizavel com Kanban e drag-and-drop
- **Comissoes:** Registro de comissoes recebidas e repassadas
- **Dashboard:** Metricas, graficos e funil de negociacoes
- **Relatorios:** Exportacao CSV
- **IA:** Resumo de entidades e chat contextual por tenant
- **Anexos Privados:** Upload e download seguro com isolamento cross-tenant
