# 01 — Arquitetura

Os diagramas seguem a ideia do modelo **C4** (Contexto → Containers → Componentes), escritos em Mermaid.

## 1. Diagrama de contexto

Quem usa o sistema e com o que ele conversa (hoje e no futuro).

```mermaid
flowchart TB
    cliente["👤 Cliente final<br/>(consumidor do parceiro)"]
    operador["👤 Operador / Admin<br/>(time interno e parceiros)"]

    sistema["🟦 Bot Varejo<br/>Plataforma de atendimento via chat"]

    parceiros["⬜ APIs de parceiros de varejo<br/>(futuro)"]
    canais["⬜ Canais de mensagem<br/>(futuro: WhatsApp etc.)"]

    cliente -->|"Conversa, contrata e consulta serviços<br/>(navegador — escopo public)"| sistema
    operador -->|"Configura fluxos, integrações, acompanha<br/>(navegador — escopo admin)"| sistema
    sistema -.->|"Integrações HTTP (futuro)"| parceiros
    sistema -.->|"Webhooks (futuro)"| canais
```

> Linhas tracejadas = fora do escopo da CPBS-275.

## 2. Diagrama de containers

O que roda, onde, e como se comunica. Tudo dentro de **uma única imagem Docker**.

```mermaid
flowchart TB
    browser["🌐 Navegador"]

    subgraph container["Container: bot-varejo (imagem única)"]
        direction TB
        sup["supervisord<br/>(PID 1 — gerencia processos)"]
        nginx["Nginx<br/>porta 8080 (exposta)"]
        subgraph static["Arquivos estáticos (/var/www/html)"]
            web["web/ — build Next.js<br/>servido em /"]
            admin["admin/ — build Next.js<br/>servido em /admin"]
        end
        api["FastAPI + Uvicorn<br/>127.0.0.1:8000 (interno)"]

        sup --> nginx
        sup --> api
        nginx -->|"arquivos"| static
        nginx -->|"proxy HTTP /api/*"| api
        nginx -->|"proxy WebSocket /ws/*"| api
    end

    browser -->|"HTTP/WS :8080"| nginx
```

### Responsabilidades

| Container / processo | Responsabilidade | Não é responsável por |
|----------------------|------------------|------------------------|
| **Nginx** | Porta de entrada única; roteia por prefixo de path; serve os builds estáticos (um HTML por rota + 404 de cada app); faz *upgrade* de WebSocket; headers de segurança e cache | Regras de negócio |
| **FastAPI/Uvicorn** | APIs REST (`/api/*`), WebSocket (`/ws/*`), OpenAPI/Swagger | Servir HTML/JS/CSS |
| **web** (build) | Interface do cliente final (escopo public) | Chamar serviços externos direto — tudo passa pela API |
| **admin** (build) | Interface administrativa (escopo admin) | Idem |
| **supervisord** | Subir e reiniciar Nginx e Uvicorn; logs em stdout/stderr | — |

## 3. Roteamento (visão lógica)

Todo o tráfego entra pelo Nginx e é decidido pelo **prefixo do path**. Detalhes em [03 — Nginx](./03-nginx-roteamento.md).

```mermaid
flowchart LR
    req["Requisição :8080"] --> d{"Prefixo do path?"}
    d -->|"/api/"| api["FastAPI (REST)<br/>/api/v1/public/*<br/>/api/v1/admin/*<br/>/api/docs, /api/openapi.json"]
    d -->|"/ws/"| ws["FastAPI (WebSocket)<br/>/ws/public<br/>/ws/admin"]
    d -->|"/admin"| adm["Build admin<br/>HTML por rota, senão /admin/404.html"]
    d -->|"qualquer outro"| web["Build web<br/>HTML por rota, senão /404.html"]
```

## 4. Fluxos de requisição

### 4.1 Carregamento da SPA

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant N as Nginx
    participant FS as /var/www/html

    U->>N: GET /admin/health/
    N->>FS: try_files $uri $uri/ → /admin/health/index.html
    FS-->>N: index.html (pré-renderizado no build)
    N-->>U: 200 text/html
    U->>N: GET /admin/_next/static/chunks/*.js
    N->>FS: arquivo com hash
    FS-->>N: JS
    N-->>U: 200 (Cache-Control: immutable, 1 ano)
    Note over U: React hidrata a página e<br/>a partir daqui a navegação é client-side
```

### 4.2 Health check via HTTP (escopo public)

```mermaid
sequenceDiagram
    autonumber
    participant W as web (SPA)
    participant N as Nginx
    participant R as Router /api/v1/public
    participant UC as GetHealthUseCase
    participant C as ClockPort / HealthCheckPort[]

    W->>N: GET /api/v1/public/health
    N->>R: proxy_pass http://127.0.0.1:8000
    R->>UC: execute(scope=PUBLIC)
    UC->>C: now(), check() de cada dependência
    C-->>UC: horário + status das dependências
    UC-->>R: HealthReport (entidade de domínio)
    R-->>N: 200 HealthResponse (JSON camelCase)
    N-->>W: 200
```

### 4.3 Health check via WebSocket (escopo admin)

```mermaid
sequenceDiagram
    autonumber
    participant A as admin (SPA)
    participant N as Nginx
    participant WS as WS endpoint /ws/admin
    participant D as MessageDispatcher
    participant UC as GetHealthUseCase

    A->>N: GET /ws/admin (Upgrade: websocket)
    N->>WS: proxy com Upgrade/Connection
    WS-->>A: 101 Switching Protocols
    A->>WS: {"type":"health.ping","id":"c1f…"}
    WS->>D: dispatch(message, scope=ADMIN)
    D->>UC: execute(scope=ADMIN)
    UC-->>D: HealthReport
    D-->>WS: {"type":"health.pong","id":"c1f…","payload":{…}}
    WS-->>A: health.pong
    Note over A,WS: Conexão permanece aberta,<br/>cliente envia ping periódico (heartbeat)
```

## 5. Arquitetura interna do backend (componentes)

Detalhada em [backend/](./backend/README.md). Visão resumida:

```mermaid
flowchart TB
    subgraph presentation["presentation (FastAPI)"]
        rpub["Router public<br/>/api/v1/public"]
        radm["Router admin<br/>/api/v1/admin"]
        wsx["WebSocket endpoints<br/>/ws/public, /ws/admin"]
    end
    subgraph application["application"]
        uc["Casos de uso<br/>(GetHealthUseCase)"]
    end
    subgraph domain["domain (Python puro)"]
        ent["Entidades / Value Objects<br/>(HealthReport, HealthStatus, Scope)"]
        ports["Ports (Protocols)<br/>(ClockPort, HealthCheckPort)"]
    end
    subgraph infrastructure["infrastructure"]
        adp["Adapters<br/>(SystemClock, futuros: DbHealthCheck…)"]
    end

    rpub --> uc
    radm --> uc
    wsx --> uc
    uc --> ent
    uc --> ports
    adp -.->|"implementa"| ports
```

**Regra de dependência:** setas apontam sempre para dentro (`presentation → application → domain`). `infrastructure` implementa as *ports* do domínio e é injetada na composição (`main.py`/dependências).

## 6. Arquitetura interna dos frontends

Detalhada em [frontend-comum/](./frontend-comum/README.md) (regras dos dois fronts); particularidades de cada app em [web/](./web/README.md) e [admin/](./admin/README.md).

```mermaid
flowchart TB
    subgraph app["app/ (rotas Next.js — finas)"]
        page["health/page.tsx"]
    end
    subgraph features["features/ (isoladas entre si)"]
        fh["health/<br/>components · hooks · api · types"]
        fx["outra-feature/ (futuro)"]
    end
    subgraph shared["shared/ (do app)"]
        prov["providers, layout"]
    end
    subgraph packages["packages/ (workspace)"]
        ui["@bot-varejo/ui"]
        apic["@bot-varejo/api-client<br/>(tipos gerados do OpenAPI)"]
        wsc["@bot-varejo/ws-client"]
    end

    page --> fh
    page --> prov
    fh --> ui
    fh --> apic
    fh --> wsc
    fx --> ui
    fh -. "❌ proibido" .-> fx
```

## 7. Pipeline de build da imagem

```mermaid
flowchart LR
    subgraph s1["Stage 1: frontend-builder (node)"]
        i1["pnpm install --frozen-lockfile"] --> b1["pnpm --filter web build<br/>pnpm --filter admin build"]
    end
    subgraph s2["Stage 2: backend-builder (python + uv)"]
        i2["uv sync --frozen --no-dev"]
    end
    subgraph s3["Stage 3: runtime (python-slim + nginx + supervisord)"]
        r["/app (venv + src)<br/>/var/www/html (web)<br/>/var/www/html/admin (admin)<br/>nginx.conf, supervisord.conf"]
    end
    b1 -->|"web/out, admin/out"| r
    i2 -->|".venv + src"| r
```

## 8. Evolução prevista (não implementar agora)

Para que a fundação já nasça preparada, os *bounded contexts* futuros ficam registrados:

```mermaid
flowchart LR
    health["health ✅<br/>(CPBS-275)"]
    conv["conversation<br/>sessões e mensagens de chat"]
    flows["flows<br/>construção/execução de fluxos"]
    integ["integrations<br/>conectores de parceiros"]
    partners["partners<br/>cadastro de parceiros e serviços"]
    iam["identity<br/>autenticação/autorização admin"]

    conv --> flows
    flows --> integ
    integ --> partners
    iam -.-> flows
    iam -.-> partners
```

Cada um será um pacote em `backend/src/bot_varejo/contexts/<nome>/` com as mesmas quatro camadas, e uma pasta em `features/` nos fronts que o consomem.
