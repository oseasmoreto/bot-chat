# Bot Varejo

Plataforma de atendimento, via chat, de serviços de parceiros de varejo.

Este repositório contém **dois projetos independentes**. Cada um tem seu próprio README, CONTRIBUTING, documentação, ADRs, templates de MR, Dockerfile, docker compose e Makefile.

| Projeto | Stack | Domínio | Imagem | Documentação |
|---------|-------|---------|--------|--------------|
| [**backend/**](./backend/README.md) | Python 3.13 · FastAPI · async · WebSockets · DynamoDB | `api.<dominio>` | `python:3.13-slim` | [backend/docs](./backend/docs/README.md) |
| [**frontend/**](./frontend/README.md) | Node 24 · Next.js (SPA) · React · TypeScript · Tailwind | `app.<dominio>` | `node:24-slim` | [frontend/docs](./frontend/docs/README.md) |

> ⚠️ **Status:** fase de documentação. Os comandos descrevem o funcionamento **alvo**.

## Visão geral

```mermaid
flowchart LR
    u["👤 Cliente final"] -->|"app.&lt;dominio&gt;/"| f
    o["👤 Operador"] -->|"app.&lt;dominio&gt;/admin"| f
    subgraph front["frontend/ — container Node 24"]
        f["Next.js<br/>web em / · admin em /admin"]
    end
    subgraph back["backend/ — container Python 3.13"]
        a["FastAPI + Uvicorn<br/>/api/v1/public · /api/v1/admin · /api/v1/ws/*"]
    end
    f -. "navegador chama a API direto<br/>HTTPS + WSS (CORS)" .-> a
```

- Cada projeto roda **um processo por container**; TLS e domínios ficam na plataforma de deploy.
- A única ligação entre os projetos é o **contrato HTTP/WebSocket** ([backend/docs/06-contratos-api.md](./backend/docs/06-contratos-api.md)).

## Rodando tudo localmente

```bash
# terminal 1 — API em http://localhost:8000
cd backend && docker compose up --build

# terminal 2 — front em http://localhost:3000
cd frontend && docker compose up --build
```

Acesse http://localhost:3000/health (web) e http://localhost:3000/admin/health (admin). Detalhes e alternativas sem Docker nos READMEs de cada projeto.

## Instalando o make no Windows

Os atalhos `make …` do backend (`make install`, `make dev`, `make check`) precisam do `make`:

1. Abra o **PowerShell** e rode `winget install ezwinports.make` (aceite os termos com `Y`).
2. **Feche todos os terminais** (inclusive o do VS Code) e abra o **Git Bash** de novo.
3. Confira: `make --version`.
4. No projeto: `cd backend && make help`.

Alternativas (Chocolatey, Scoop), o que fazer se aparecer `make: command not found` e instalação no Linux/macOS: [backend/README.md — Instalando o make](./backend/README.md#instalando-o-make).

## Estrutura do repositório

```text
bot-varejo/
├── README.md                 # este arquivo
├── CONTRIBUTING.md           # padrão de branches, commits, MRs e versionamento
├── backend/                  # projeto backend — README, CONTRIBUTING, .gitlab, docs, Dockerfile, compose, Makefile
└── frontend/                 # projeto frontend — README, CONTRIBUTING, .gitlab, docs, Dockerfile, compose
```

## Contribuindo

Leia o [CONTRIBUTING.md](./CONTRIBUTING.md). Cada projeto tem também o seu guia completo: [backend/CONTRIBUTING.md](./backend/CONTRIBUTING.md) · [frontend/CONTRIBUTING.md](./frontend/CONTRIBUTING.md). Resumo:

```text
branches:  developer (development) → staging (homologação) → master (production) — todas protegidas
branch:    feat/CPBS-123-descricao-curta  (sai da developer)
commit:    feat: [CPBS-123] adiciona health check por escopo   ← tipo: [ticket] descrição
MR:        → developer · merge commit (sem squash) · um projeto por MR · template do projeto · validação local verde
publicar:  MRs de promoção developer → staging → master (template Release)
tags:      backend-vX.Y.Z · frontend-vX.Y.Z (na master)
```

## Templates de merge request

Cada projeto tem os seus, em `<projeto>/.gitlab/merge_request_templates/` (Default, Bugfix, Docs, Hotfix, Release).

> ⚠️ O GitLab só oferece no seletor os templates que estão em `.gitlab/merge_request_templates/` **na raiz do repositório**. Neste repositório, copie o conteúdo do template do projeto para a descrição do MR.
