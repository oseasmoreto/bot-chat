# 00 — Visão geral (frontend)

## Contexto

O **Bot Varejo** é a plataforma de atendimento, via chat, de serviços oferecidos por parceiros de varejo. O sistema tem dois projetos independentes, cada um com repositório, documentação e deploy próprios:

| Projeto | Domínio | Responsabilidade |
|---------|---------|------------------|
| **Frontend** (este) | `app.<dominio>` | App Next.js com as áreas **web** (`/`) e **admin** (`/admin`) |
| Backend | `api.<dominio>` | APIs REST e WebSocket dos escopos `public` e `admin` |

O frontend é **um único app Next.js** com duas áreas:

| Área | URL | Escopo da API | Público | Exemplo de uso futuro |
|------|-----|---------------|---------|------------------------|
| **web** | `/` | `public` | Cliente final do parceiro | Conversar com o bot, contratar/consultar serviços |
| **admin** | `/admin` | `admin` | Operadores, time interno, parceiros | Construir fluxos, configurar integrações, acompanhar atendimentos |

## Stack

| Item | Tecnologia |
|------|------------|
| Runtime | Node.js 24 LTS |
| Framework | Next.js (App Router), **servidor padrão** (`output: 'standalone'`), usado como **SPA** |
| UI | React + TypeScript (`strict`) + Tailwind CSS v4 |
| Dados | TanStack Query (estado de servidor) · `openapi-fetch` + `openapi-typescript` (cliente tipado) |
| Tempo real | WebSocket nativo do navegador (cliente próprio em `shared/ws`) |
| Dependências | pnpm |
| Qualidade | ESLint (flat config, `eslint-plugin-boundaries`), Prettier |
| Testes | Vitest, Testing Library, MSW, Playwright |
| Container | Imagem `node:24-slim` rodando `node server.js` |

## Princípios

| Princípio | Como se aplica no frontend |
|-----------|----------------------------|
| **Modularidade** | Áreas (web/admin) e features isoladas; mexer em uma não afeta as outras — garantido por lint |
| **Componentização** | UI reutilizável em `shared/ui`; features compõem componentes |
| **DRY** | Features comuns às duas áreas em `features/`; cliente HTTP/WS e tipos gerados em `shared/` |
| **KISS** | Um app, um processo, uma imagem; SPA simples com TanStack Query |
| **TDD** | Teste antes do código; nenhuma feature/rota/tela sem teste |
| **Tipagem forte** | TS `strict`, tipos da API gerados do OpenAPI do backend |

## Tarefas

Objetivo, critérios de aceitação e escopo de cada tarefa ficam em [tasks/](./tasks/README.md).
