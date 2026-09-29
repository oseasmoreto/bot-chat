# 01 — Arquitetura (backend)

Diagramas no estilo **C4** (Contexto → Containers → Componentes), em Mermaid.

## 1. Contexto do sistema

```mermaid
flowchart TB
    cliente["👤 Cliente final"]
    operador["👤 Operador / Admin"]

    subgraph sistema["Bot Varejo"]
        front["🟦 Frontend<br/>Next.js — app.&lt;dominio&gt;<br/>(web em / · admin em /admin)"]
        api["🟩 Backend (este projeto)<br/>FastAPI — api.&lt;dominio&gt;"]
    end

    parceiros["⬜ APIs de parceiros<br/>(futuro)"]
    canais["⬜ Canais de mensagem<br/>(futuro)"]

    cliente -->|"navegador"| front
    operador -->|"navegador"| front
    front -->|"HTTPS REST /api/v1/*<br/>WSS /api/v1/ws/*"| api
    api -.->|"integrações (futuro)"| parceiros
    canais -.->|"webhooks (futuro)"| api
```

> O navegador chama a API **diretamente** (outro domínio): por isso CORS e validação de `Origin` são parte da arquitetura.

## 2. Containers

```mermaid
flowchart LR
    browser["🌐 Navegador<br/>(código do frontend)"]
    lb["Load balancer / ingress<br/>TLS · api.&lt;dominio&gt;<br/>(plataforma de deploy)"]
    subgraph c["Container: bot-varejo-backend (python:3.13-slim)"]
        uv["Uvicorn :8000<br/>FastAPI app"]
    end
    browser -->|"HTTPS / WSS"| lb -->|"HTTP / WS"| uv
```

| Elemento | Responsabilidade |
|----------|------------------|
| Load balancer / ingress | TLS, domínio, balanceamento. Fora do escopo desta task (plataforma) |
| Uvicorn + FastAPI | REST (`/api/v1/*`), WebSocket (`/api/v1/ws/*`), OpenAPI/Swagger, CORS, validação de `Origin` |

**Um processo por container.** Detalhes em [08 — Docker e deploy](./08-docker-deploy.md).

## 3. Rotas expostas

```mermaid
flowchart LR
    req["api.&lt;dominio&gt;"] --> d{"path"}
    d -->|"/api/v1/public/*"| pub["Router public"]
    d -->|"/api/v1/admin/*"| adm["Router admin"]
    d -->|"/api/v1/ws/public · /api/v1/ws/admin"| ws["WebSocket endpoints"]
    d -->|"/api/docs · /api/redoc · /api/openapi.json"| doc["Documentação da API"]
```

## 4. Fluxos de requisição

### 4.1 Health via HTTP (escopo public)

```mermaid
sequenceDiagram
    autonumber
    participant F as Frontend (navegador)
    participant M as CORSMiddleware
    participant R as Router /api/v1/public
    participant UC as GetHealthUseCase
    participant P as ClockPort / HealthCheckPort[]

    F->>M: GET /api/v1/public/health (Origin: app.dominio)
    M->>R: origem permitida
    R->>UC: execute(scope=PUBLIC)
    UC->>P: now(), check() de cada dependência
    P-->>UC: horário + status
    UC-->>R: HealthReport (domínio)
    R-->>M: 200 HealthResponse (camelCase)
    M-->>F: 200 + Access-Control-Allow-Origin
```

### 4.2 Health via WebSocket (escopo admin)

```mermaid
sequenceDiagram
    autonumber
    participant F as Frontend (navegador)
    participant WS as /api/v1/ws/admin
    participant D as MessageDispatcher
    participant UC as GetHealthUseCase

    F->>WS: GET /api/v1/ws/admin (Upgrade, Origin: app.dominio)
    alt Origin não permitido
        WS-->>F: close 1008
    else Origin permitido
        WS-->>F: 101 Switching Protocols
        F->>WS: {"type":"health.ping","id":"c1f"}
        WS->>D: dispatch(message, scope=ADMIN)
        D->>UC: execute(scope=ADMIN)
        UC-->>D: HealthReport
        D-->>WS: health.pong
        WS-->>F: {"type":"health.pong","id":"c1f","payload":{…}}
    end
```

## 5. Componentes internos (DDD)

Detalhes em [03 — Arquitetura DDD](./03-arquitetura-ddd.md).

```mermaid
flowchart TB
    subgraph presentation["presentation (FastAPI)"]
        rpub["Router public /api/v1/public"]
        radm["Router admin /api/v1/admin"]
        wsx["WebSocket /api/v1/ws/public, /api/v1/ws/admin"]
    end
    subgraph application["application"]
        uc["Casos de uso (GetHealthUseCase)"]
    end
    subgraph domain["domain (Python puro)"]
        ent["Entidades / Value Objects"]
        ports["Ports (Protocols)"]
    end
    subgraph infrastructure["infrastructure"]
        adp["Adapters (SystemClock…)"]
    end
    rpub --> uc
    radm --> uc
    wsx --> uc
    uc --> ent
    uc --> ports
    adp -.->|"implementa"| ports
```

## 6. Evolução prevista (não implementar agora)

```mermaid
flowchart LR
    health["health ✅<br/>(CPBS-275)"]
    conv["conversation<br/>sessões e mensagens de chat"]
    flows["flows<br/>construção/execução de fluxos"]
    integ["integrations<br/>conectores de parceiros"]
    partners["partners<br/>parceiros e serviços"]
    iam["identity<br/>autenticação/autorização"]
    conv --> flows
    flows --> integ
    integ --> partners
    iam -.-> flows
    iam -.-> partners
```

Cada um será um pacote em `src/bot_varejo/contexts/<nome>/` com as mesmas quatro camadas. Com mais de uma réplica e WebSocket com estado (chat), será necessário *pub/sub* (ex.: Redis) — decisão futura em ADR.
