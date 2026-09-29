# Glossário (backend)

## Negócio

| Termo | Significado |
|-------|-------------|
| **Parceiro** | Empresa de varejo que oferece serviços atendidos pela plataforma |
| **Serviço** | O que o parceiro oferece e o cliente contrata/consulta via chat |
| **Cliente final** | Consumidor que conversa com o bot (escopo *public*) |
| **Operador** | Pessoa do time interno ou do parceiro que usa a área admin (escopo *admin*) |
| **Fluxo** | Roteiro de conversa configurável — futuro |
| **Integração** | Conexão com a API de um parceiro — futuro |
| **Atendimento** | Uma conversa entre cliente final e bot/operador — futuro |

## Técnico

| Termo | Significado |
|-------|-------------|
| **Escopo (scope)** | `public` ou `admin`. Define prefixos de rota (`/api/v1/{scope}`, `/api/v1/ws/{scope}`) e, no futuro, regras de auth |
| **Bounded context** | Fronteira de um subdomínio no DDD; uma pasta em `src/bot_varejo/contexts/` |
| **Shared kernel** | Código mínimo compartilhado entre contexts (`core/`) |
| **Entidade / Value object** | Objetos de domínio; value objects são imutáveis e comparados por valor |
| **Caso de uso** | Classe da camada `application` que orquestra uma ação (`GetHealthUseCase`) |
| **Port** | Interface (`Protocol`) de que o domínio/aplicação precisa (`ClockPort`) |
| **Adapter** | Implementação concreta de uma port (`SystemClock`) |
| **Composition root** | Único lugar onde as dependências concretas são montadas (`container.py`) |
| **CORS** | Mecanismo do navegador que exige autorização da API para chamadas de outra origem |
| **Origin** | Header enviado pelo navegador com o domínio da página; validado no handshake WS |
| **Envelope WS** | Formato padrão de mensagem WebSocket: `type`, `id`, `payload` |
| **Health check** | Endpoint que informa a saúde da API (`ok`, `degraded`, `down`) |
| **Contrato** | Endpoints, schemas e mensagens que o frontend consome (`openapi.json` + doc 06) |
| **ADR** | Architecture Decision Record — registro de decisão em `docs/adr/` |
| **TDD** | Test-Driven Development — teste antes do código (red → green → refactor) |
