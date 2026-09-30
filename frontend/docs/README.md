# Documentação — Frontend

> Projeto `frontend/` do Bot Varejo
> Backend: `docs/README.md` no repositório do **backend** · Branch/commit/MR: [CONTRIBUTING.md](../CONTRIBUTING.md) · Templates de MR: [`.gitlab/merge_request_templates/`](../.gitlab/merge_request_templates)

Um único app **Next.js** (servidor padrão, usado como SPA) servido em `app.<dominio>`, com duas áreas: **web** em `/` (cliente final, escopo `public`) e **admin** em `/admin` (operação, escopo `admin`). Consome a API em outro domínio (`api.<dominio>`).

## Índice

| # | Documento | Conteúdo |
|---|-----------|----------|
| 00 | [Visão geral](./00-visao-geral.md) | Contexto, áreas, stack, princípios |
| 01 | [Arquitetura](./01-arquitetura.md) | Contexto do sistema, containers, rotas, fluxos |
| 02 | [Estrutura de pastas](./02-estrutura.md) | Árvore do projeto, onde colocar código novo |
| 03 | [Next.js como SPA](./03-nextjs-spa.md) | Regras do modo SPA, `next.config.ts`, layout raiz, `/healthz` |
| 04 | [Organização por áreas e features](./04-organizacao-areas-features.md) | Camadas, regras de isolamento, lint de fronteiras, checklist |
| 05 | [Área web](./05-area-web.md) | Telas, features e cuidados da área pública |
| 06 | [Área admin](./06-area-admin.md) | Telas, features e cuidados da área administrativa |
| 07 | [Integração com a API](./07-integracao-api.md) | Config em runtime, cliente HTTP tipado, WebSocket, CORS, `pnpm openapi` |
| 08 | [Feature `health`](./08-feature-health.md) | Código de referência da tela de status |
| 09 | [Estilo e TypeScript](./09-estilo-e-typescript.md) | Tailwind v4, tema, `tsconfig` |
| 10 | [Docker e deploy](./10-docker-deploy.md) | Dockerfile, compose, variáveis |
| 11 | [Testes](./11-testes.md) | TDD, matriz obrigatória, infraestrutura, exemplos, E2E |
| 12 | [Padrões de código](./12-padroes-codigo.md) | Nomenclatura camelCase, tipagem, boas práticas, lint |
| 13 | [CI e comandos](./13-ci.md) | Pipeline por ambiente (developer, staging, master), E2E, deploy, scripts, Makefile |
| — | [Tarefas](./tasks/README.md) | Objetivo, critérios de aceitação e escopo de cada tarefa |
| — | [ADRs](./adr/README.md) | Decisões de arquitetura do frontend |
| — | [Glossário](./glossario.md) | Termos de negócio e técnicos |

## Telas

| Área | Rota | Descrição |
|------|------|-----------|
| web | `/` | Início (placeholder) |
| web | `/health` | Status da API — escopo `public` (HTTP + WebSocket) |
| admin | `/admin` | Início do admin (placeholder) |
| admin | `/admin/health` | Status da API — escopo `admin` (HTTP + WebSocket) |
| — | `/healthz` | Liveness do servidor Next (container) |

## Como manter esta documentação

1. Nova tela → tabela de telas da área ([05](./05-area-web.md) / [06](./06-area-admin.md)) e a tabela acima.
2. Nova feature → tabela de features da área; se for comum às duas, citar nas duas.
3. Contrato da API mudou → `pnpm openapi` e revisar [07](./07-integracao-api.md).
4. Nova decisão → novo ADR (não edite ADR aceito; marque-o como *Substituído*).
5. Diagramas em **Mermaid**, versionados e revisados em MR como código.
