# 01 — Arquitetura (frontend)

Diagramas no estilo **C4** (Contexto → Containers → Componentes), em Mermaid.

## 1. Contexto do sistema

```mermaid
flowchart TB
    cliente["👤 Cliente final"]
    operador["👤 Operador / Admin"]

    subgraph sistema["Bot Varejo"]
        front["🟦 Frontend (este projeto)<br/>Next.js — app.&lt;dominio&gt;<br/>web em / · admin em /admin"]
        api["🟩 Backend<br/>FastAPI — api.&lt;dominio&gt;"]
    end

    cliente -->|"navegador → /"| front
    operador -->|"navegador → /admin"| front
    front -.->|"o código JS roda no navegador e chama a API<br/>HTTPS /api/v1/* · WSS /api/v1/ws/*"| api
```

## 2. Containers

```mermaid
flowchart LR
    browser["🌐 Navegador"]
    subgraph fc["Container: bot-varejo-frontend (node:24-slim)"]
        next["Next.js server<br/>node server.js :3000"]
    end
    subgraph bc["Container: bot-varejo-backend"]
        api["FastAPI :8000"]
    end
    browser -->|"1 · HTML, JS, CSS<br/>https://app.&lt;dominio&gt;"| next
    browser -->|"2 · dados REST e WS<br/>https://api.&lt;dominio&gt;"| api
```

| Elemento | Responsabilidade | Não é responsável por |
|----------|------------------|------------------------|
| **Next.js server** | Entregar HTML/JS/CSS das duas áreas, injetar a **configuração de runtime** (URL da API), headers de segurança, `/healthz`; no futuro, *middleware* de autenticação do `/admin` | Buscar dados de negócio (SPA: quem busca é o navegador) |
| **Código no navegador** | Toda a interação e busca de dados (TanStack Query + WebSocket) direto na API | — |
| **Backend** | REST, WebSocket, CORS | Servir o front |

TLS e domínio (`app.<dominio>`) ficam na plataforma de deploy. **Um processo por container.**

## 3. Rotas do app

```mermaid
flowchart LR
    req["app.&lt;dominio&gt;"] --> d{"path"}
    d -->|"/ · /health · …"| web["Área web<br/>src/app/(web)"]
    d -->|"/admin · /admin/health · …"| adm["Área admin<br/>src/app/admin"]
    d -->|"/healthz"| hz["Route handler<br/>liveness do servidor"]
    d -->|"/_next/static/*"| st["Assets com hash<br/>(cache longo)"]
```

## 4. Fluxos

### 4.1 Carregamento de uma tela

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant N as Next.js server
    participant B as Navegador (React)
    participant A as API

    U->>N: GET /admin/health
    N->>N: layout raiz lê API_URL / WS_URL do ambiente
    N-->>U: HTML (shell) + config de runtime
    U->>N: GET /_next/static/chunks/*.js
    N-->>U: JS (somente os chunks da área admin)
    Note over B: React hidrata e a navegação passa a ser client-side (SPA)
    B->>A: GET https://api…/api/v1/admin/health (CORS)
    A-->>B: 200 HealthResponse
    B->>A: WSS /api/v1/ws/admin + health.ping
    A-->>B: health.pong
```

### 4.2 Navegação entre telas (SPA)

```mermaid
sequenceDiagram
    autonumber
    participant B as Navegador
    participant N as Next.js server
    participant A as API
    B->>B: clique em <Link href="/admin/flows">
    B->>N: busca o payload da rota (RSC) e chunks ainda não carregados
    N-->>B: payload + JS
    B->>A: dados da tela via TanStack Query
    Note over B: sem recarregar a página
```

## 5. Componentes internos

Detalhes em [04 — Organização por áreas e features](./04-organizacao-areas-features.md).

```mermaid
flowchart TB
    subgraph app["src/app — ROTAS (finas)"]
        rw["(web)/health/page.tsx"]
        ra["admin/health/page.tsx"]
    end
    subgraph areas["src/areas — exclusivo de cada área"]
        aw["web/ (shell, features só do web)"]
        aa["admin/ (shell, features só do admin)"]
    end
    subgraph features["src/features — usadas pelas duas áreas"]
        fh["health/"]
    end
    subgraph shared["src/shared — infraestrutura técnica"]
        s["ui · api · ws · config · providers"]
    end
    rw --> aw
    rw --> fh
    ra --> aa
    ra --> fh
    aw --> shared
    aa --> shared
    fh --> shared
    aw -. "❌" .-> aa
    aa -. "❌" .-> aw
```

## 6. Evolução prevista (não implementar agora)

| Área | Features futuras |
|------|------------------|
| web | `chat` (conversa com o bot em tempo real) |
| admin | `flows` (construtor de fluxos), `integrations`, `partners`, `attendances` |
| ambas | `auth` (login/sessão — admin primeiro, com *middleware* no `/admin`) |
