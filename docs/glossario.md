# Glossário

## Negócio

| Termo | Significado |
|-------|-------------|
| **Parceiro** | Empresa de varejo que oferece serviços atendidos pela plataforma |
| **Serviço** | O que o parceiro oferece e o cliente contrata/consulta via chat |
| **Cliente final** | Consumidor que conversa com o bot (escopo *public*) |
| **Operador** | Pessoa do time interno ou do parceiro que usa o *admin* |
| **Fluxo** | Roteiro de conversa configurável (etapas, perguntas, decisões) — futuro |
| **Integração** | Conexão com a API de um parceiro para executar/consultar serviços — futuro |
| **Atendimento** | Uma conversa entre cliente final e bot/operador — futuro |

## Técnico

| Termo | Significado |
|-------|-------------|
| **Escopo (scope)** | Separação de acesso: `public` (cliente final) ou `admin` (operação). Define prefixos de rota e, no futuro, regras de auth |
| **Bounded context** | Fronteira de um subdomínio no DDD; aqui, uma pasta em `backend/src/bot_varejo/contexts/` |
| **Shared kernel** | Código mínimo compartilhado entre contexts (`core/`) |
| **Entidade / Value object** | Objetos de domínio; value objects são imutáveis e comparados por valor |
| **Caso de uso** | Classe da camada `application` que orquestra uma ação do sistema (`GetHealthUseCase`) |
| **Port** | Interface (`Protocol`) que o domínio/aplicação precisa (`ClockPort`) |
| **Adapter** | Implementação concreta de uma port (`SystemClock`) |
| **Composition root** | Único lugar onde as dependências concretas são montadas (`container.py`) |
| **Feature** | Pasta autocontida no front (`src/features/<nome>`) com componentes, hooks, api e testes |
| **Static export** | Modo do Next.js que gera HTML/JS/CSS estáticos, sem servidor Node |
| **basePath** | Prefixo de URL do app Next (`/admin`) |
| **Envelope WS** | Formato padrão de mensagem WebSocket: `type`, `id`, `payload` |
| **Health check** | Endpoint que informa se a aplicação está saudável (`ok`, `degraded`, `down`) |
| **ADR** | Architecture Decision Record — registro de decisão em `docs/adr/` |
| **TDD** | Test-Driven Development — teste antes do código (red → green → refactor) |
| **MSW** | Mock Service Worker — intercepta HTTP nos testes do front |
| **HMR** | Hot Module Replacement — recarga do front em dev sem refresh completo |
