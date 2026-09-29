# Glossário (frontend)

## Negócio

| Termo | Significado |
|-------|-------------|
| **Parceiro** | Empresa de varejo que oferece serviços atendidos pela plataforma |
| **Serviço** | O que o parceiro oferece e o cliente contrata/consulta via chat |
| **Cliente final** | Consumidor que usa a área **web** |
| **Operador** | Pessoa do time interno ou do parceiro que usa a área **admin** |
| **Fluxo** | Roteiro de conversa configurável — futuro |
| **Integração** | Conexão com a API de um parceiro — futuro |

## Técnico

| Termo | Significado |
|-------|-------------|
| **Área** | Parte do app com público próprio: `web` (em `/`) ou `admin` (em `/admin`) |
| **Escopo (scope)** | Lado da API usado pela área: `public` (web) ou `admin` (admin) |
| **Feature** | Pasta autocontida com componentes, hooks, api e testes de uma funcionalidade |
| **Route group** | Pasta `(nome)` do App Router que organiza rotas sem aparecer na URL — ex.: `(web)` |
| **Shell** | Layout visual de uma área (`WebShell`, `AdminShell`) |
| **SPA** | Single Page Application: navegação e dados no navegador, sem recarregar a página |
| **Standalone** | Saída do `next build` com um `server.js` e só as dependências necessárias |
| **Config de runtime** | `API_URL`/`WS_URL` lidas do container a cada requisição e entregues ao navegador pelo `ConfigProvider` |
| **Server Component / Client Component** | Componente renderizado só no servidor / componente com `'use client'` que roda no navegador |
| **CORS** | Autorização que a API dá para o navegador chamá-la a partir de outro domínio |
| **MSW** | Mock Service Worker — intercepta HTTP nos testes |
| **HMR** | Hot Module Replacement — recarga do código em dev sem refresh completo |
| **ADR** | Architecture Decision Record — registro de decisão em `docs/adr/` |
| **TDD** | Test-Driven Development — teste antes do código |
