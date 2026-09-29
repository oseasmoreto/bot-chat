## Backend — Contratos de API (REST, WebSocket, OpenAPI)

## Convenções gerais

| Item | Convenção |
|------|-----------|
| Prefixo REST | `/api/v{major}/{scope}/...` — ex.: `/api/v1/public/health` |
| Escopos | `public` (cliente final) e `admin` (operação) |
| Versionamento | Major no path. Mudança incompatível = `v2` convivendo com `v1` até migração |
| Formato | JSON UTF-8 |
| Nomes de campos | **camelCase** no JSON (ADR-0008); snake_case no Python é convertido por `BaseSchema` |
| Datas | ISO 8601 em UTC — `2026-09-29T14:30:00Z` |
| Enums | strings minúsculas — `"ok"`, `"degraded"`, `"down"` |
| Recursos (futuro) | substantivos no plural, kebab-case — `/api/v1/admin/partner-services` |
| IDs de operação (OpenAPI) | camelCase — `getPublicHealth`, `getAdminHealth` (viram nomes no client) |
| Correlação | Header `X-Request-ID` aceito e devolvido |

## REST

### Endpoints da CPBS-275

| Método | Path | Escopo | operationId | Respostas |
|--------|------|--------|-------------|-----------|
| `GET` | `/api/v1/public/health` | public | `getPublicHealth` | `200` HealthResponse · `503` HealthResponse |
| `GET` | `/api/v1/admin/health` | admin | `getAdminHealth` | `200` HealthResponse · `503` HealthResponse |
| `GET` | `/api/docs` | — | — | Swagger UI |
| `GET` | `/api/redoc` | — | — | ReDoc |
| `GET` | `/api/openapi.json` | — | — | Especificação OpenAPI 3.1 |

Regras do status HTTP do health:

| `status` do relatório | HTTP | Motivo |
|-----------------------|------|--------|
| `ok` | 200 | Tudo saudável |
| `degraded` | 200 | Funciona com alguma dependência não crítica ruim — não deve derrubar o container |
| `down` | 503 | Load balancer / Docker healthcheck devem tirar a instância de rotação |

### Schema `HealthResponse`

```json
{
  "status": "ok",
  "scope": "public",
  "version": "0.1.0",
  "uptimeSeconds": 1234.56,
  "checkedAt": "2026-09-29T14:30:00Z",
  "components": []
}
```

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `status` | `"ok" \| "degraded" \| "down"` | sim | Pior status entre os componentes; `ok` se não houver componentes |
| `scope` | `"public" \| "admin"` | sim | Escopo que respondeu — prova que o roteamento chegou ao lugar certo |
| `version` | `string` | sim | Versão da aplicação (`APP_VERSION`) |
| `uptimeSeconds` | `number` | sim | Segundos desde o start do processo |
| `checkedAt` | `string` (date-time) | sim | Momento da verificação (UTC) |
| `components` | `ComponentHealth[]` | sim | Dependências verificadas. Vazio nesta fase (não há banco) |

`ComponentHealth`:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `name` | `string` | sim | Ex.: `database`, `partner:acme` |
| `status` | `"ok" \| "degraded" \| "down"` | sim | Status do componente |
| `detail` | `string \| null` | não | Mensagem curta, sem dados sensíveis |

### Formato padrão de erro

Todo erro (4xx/5xx), exceto o 503 do health, segue:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Dados de entrada inválidos",
    "details": [{ "field": "name", "message": "Campo obrigatório" }],
    "requestId": "7f1c…"
  }
}
```

| Campo | Descrição |
|-------|-----------|
| `code` | Identificador estável, snake_case, para o front tomar decisão (`not_found`, `validation_error`, `internal_error`…) |
| `message` | Mensagem legível (pt-BR) |
| `details` | Opcional — lista de detalhes (ex.: erros por campo) |
| `requestId` | Mesmo valor do header `X-Request-ID` |

## Protocolo WebSocket

### Endpoints

| Path | Escopo |
|------|--------|
| `/ws/public` | public |
| `/ws/admin` | admin |

URL no navegador: `ws(s)://<mesmo host>/ws/<scope>` (montada por `buildWsUrl`).

### Envelope

Toda mensagem, nos dois sentidos, é um objeto JSON:

```json
{ "type": "dominio.acao", "id": "uuid-opcional", "payload": {} }
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `type` | `string` | `<contexto>.<ação>` em minúsculas com ponto. Ex.: `health.ping` |
| `id` | `string \| null` | Correlação: a resposta repete o `id` da requisição |
| `payload` | `object` | Dados da mensagem (camelCase) |

### Mensagens da CPBS-275

| Direção | `type` | `payload` | Resposta |
|---------|--------|-----------|----------|
| cliente → servidor | `health.ping` | `{}` | `health.pong` |
| servidor → cliente | `health.pong` | `HealthResponse` | — |
| servidor → cliente | `error` | `{ "code": string, "message": string }` | — |

Códigos de erro WS:

| `code` | Quando |
|--------|--------|
| `invalid_message` | Texto não é JSON ou não respeita o envelope |
| `unknown_message_type` | Não há handler registrado para `type` |

### Exemplo de sessão

```text
→ {"type":"health.ping","id":"a1","payload":{}}
← {"type":"health.pong","id":"a1","payload":{"status":"ok","scope":"admin","version":"0.1.0","uptimeSeconds":42.1,"checkedAt":"2026-09-29T14:30:00Z","components":[]}}
→ {"type":"chat.send","id":"a2","payload":{}}
← {"type":"error","id":"a2","payload":{"code":"unknown_message_type","message":"Tipo de mensagem não suportado: chat.send"}}
→ não é json
← {"type":"error","id":null,"payload":{"code":"invalid_message","message":"Envelope inválido"}}
```

### Ciclo de vida da conexão

```mermaid
stateDiagram-v2
    [*] --> connecting
    connecting --> open: 101 Switching Protocols
    connecting --> closed: falha
    open --> open: ping a cada 15s / pong
    open --> closed: servidor/rede caiu
    closed --> connecting: reconexão (backoff 1s, 2s, 4s… máx 30s)
    closed --> [*]: componente desmontado
```

## OpenAPI e Swagger

- Gerado automaticamente pelo FastAPI a partir dos schemas Pydantic e das anotações de tipo.
- Disponível em `/api/docs` (Swagger UI), `/api/redoc` e `/api/openapi.json`.
- Tags: `public`, `admin` (escopo) e `health` (context) — o Swagger agrupa por elas.
- Controlado por `APP_DOCS_ENABLED` (padrão `true`; em produção pode ser desligado ou protegido quando existir auth).
- Uma cópia é versionada em `packages/api-client/openapi.json` e **o CI falha se ela divergir do backend** (teste de contrato em `backend/tests/contract/`).
- Cada rota deve declarar `summary`, `operation_id` e as respostas não-2xx relevantes (`responses=`).
