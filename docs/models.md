# Modelos

## Convencoes

- Todo modelo sensivel estende `BaseTenantModel` (possui FK `brokerage`)
- Todo modelo possui `created_at` e `updated_at`
- Managers usam `TenantManager` com `for_brokerage()` e `for_request()`

## Diagrama de Entidades

```mermaid
erDiagram
    Brokerage ||--o{ User : "tem"
    Brokerage ||--o{ Client : "tem"
    Brokerage ||--o{ Insurer : "tem"
    Brokerage ||--o{ Branch : "tem"
    Brokerage ||--o{ Coverage : "tem"
    Brokerage ||--o{ Proposal : "tem"
    Brokerage ||--o{ Policy : "tem"
    Brokerage ||--o{ Claim : "tem"
    Brokerage ||--o{ Renewal : "tem"
    Brokerage ||--o{ Endorsement : "tem"
    Brokerage ||--o{ Pipeline : "tem"
    Brokerage ||--o{ PipelineStage : "tem"
    Brokerage ||--o{ Deal : "tem"
    Brokerage ||--o{ Agent : "tem"
    Brokerage ||--o{ Producer : "tem"
    Brokerage ||--o{ Commission : "tem"
    Brokerage ||--o{ Attachment : "tem"
    Brokerage ||--o{ Notification : "tem"
    Brokerage ||--o{ ChatSession : "tem"

    Client ||--o{ Proposal : "tem"
    Client ||--o{ Policy : "tem"
    Client ||--o{ CoveredItem : "tem"
    Client ||--o{ Deal : "tem"

    Policy ||--o{ Claim : "tem"
    Policy ||--o{ Renewal : "tem"
    Policy ||--o{ Endorsement : "tem"
    Policy ||--o{ Commission : "tem"

    Branch ||--o{ Coverage : "tem"
    Branch ||--o{ Proposal : "tem"
    Branch ||--o{ Policy : "tem"

    Pipeline ||--o{ PipelineStage : "tem"
    Pipeline ||--o{ Deal : "tem"
    PipelineStage ||--o{ Deal : "tem"

    Agent ||--o{ Producer : "tem"

    CoveredItem ||--o{ Claim : "tem"
```

## Apps e Responsabilidades

| App | Modelos | Responsabilidade |
|---|---|---|
| `core` | Brokerage, User | Settings, auth, tenant middleware |
| `base` | - | Models base, mixins, managers |
| `accounts` | - | Onboarding, cadastro, landing |
| `clients` | Client | Clientes PF/PJ |
| `insurers` | Insurer, Branch, Coverage | Seguradoras, ramos, coberturas |
| `policies` | Proposal, Policy, CoveredItem, Endorsement | Propostas, apolices, endossos |
| `claims` | Claim | Sinistros |
| `renewals` | Renewal | Renovacoes |
| `crm` | Pipeline, PipelineStage, Deal | CRM, pipeline, kanban |
| `agents` | Agent, Producer | Agentes e produtores |
| `commissions` | Commission | Comissoes e repasses |
| `attachments` | Attachment | Anexos (GenericForeignKey) |
| `dashboard` | - | Dashboard com metricas |
| `reports` | - | Exportacao CSV |
| `ai` | Notification, ChatSession, ChatMessage | IA, resumos, chat, notificacoes |
