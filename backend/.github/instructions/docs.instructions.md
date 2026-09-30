---
applyTo: "docs/**,README.md,CONTRIBUTING.md"
description: "Regras de escrita da documentação do backend: estado atual, estrutura, ADRs, tarefas, diagramas, código embutido e links"
---

# Documentação do backend

## Princípios

- **pt-BR**, frases curtas, voz ativa. Nomes de código, arquivos e comandos em `código`.
- **Só o estado atual do sistema.** Sem histórico, sem "antes/agora", sem propostas descartadas, sem citar a ferramenta ou solução anterior (nem como alternativa). O histórico fica no git.
- **Docs permanentes** (`docs/`, ADRs, README, CONTRIBUTING) descrevem o que o sistema **é**; **nunca** citam tarefas/tickets. O que é de uma entrega vai para `docs/tasks/`.
- O backend é um **projeto independente**: não mencione outros repositórios além do "repositório do **frontend**" (sem link relativo para ele).
- Fora do escopo: CI/CD, pipelines, deploy automatizado, hooks de commit, templates de mensagem de commit e tutoriais de configuração do GitLab.
- Prefira **tabelas** a listas longas; um assunto por seção; links em vez de repetir conteúdo de outro doc.

## Onde cada coisa vai

| Conteúdo | Lugar |
|----------|-------|
| Como rodar, configurar e resolver problemas | `README.md` |
| Branches, commits, MRs, versionamento | `CONTRIBUTING.md` |
| Arquitetura, padrões, contratos, guias técnicos | `docs/NN-nome.md` (numeração sequencial, kebab-case) + linha no índice `docs/README.md` |
| Decisão de arquitetura | `docs/adr/NNNN-nome.md` + linha em `docs/adr/README.md` |
| Objetivo, análise, critérios e escopo de uma entrega | `docs/tasks/CPBS-<n>-<slug>.md` + linha em `docs/tasks/README.md` |
| Termo de negócio ou técnico novo | `docs/glossario.md` |
| Contrato com o frontend (endpoints, schemas, mensagens WS, erros) | `docs/06-contratos-api.md` + `openapi.json` |
| Variável de ambiente | `.env.example` + `docs/08-docker.md` (§4) + tabela do README |
| Lib nova | `docs/13-dependencias.md` |

Doc novo: título `# NN — Título`, entra no índice `docs/README.md` e, se mudar a árvore, em `docs/02-estrutura.md`.

## ADRs

- Formato: título `# ADR-NNNN — Título`, `- **Status:** Aceito`, `- **Data:** AAAA-MM-DD`, seções **Contexto**, **Decisão**, **Alternativas consideradas**, **Consequências**.
- Uma ADR por decisão; numeração sequencial.
- Decisão alterada → **reescreva a ADR** com a decisão vigente (sem status "Substituído", sem ADR de transição).
- Alternativas: só opções avaliadas e não adotadas — nunca a solução que o projeto usava antes.

## Código embutido

- Trecho que representa um arquivo real é **cópia exata** do arquivo: título `## \`caminho/arquivo.py\`` seguido do bloco, ou bloco cuja primeira linha é `# caminho/arquivo.py`. O teste `tests/contract/test_docs.py` falha se divergir.
- Caminhos relativos a `api/` (ex.: `core/scope.py`) ou à raiz do projeto (ex.: `Dockerfile`, `tests/fakes.py`).
- Trecho ilustrativo (arquivo que ainda não existe, recorte) não usa esse formato de título, ou é marcado como exemplo no texto.
- Blocos com a linguagem: ` ```python `, ` ```bash `, ` ```yaml `, ` ```text `…

## Comandos

- Comandos rodam na raiz do projeto; mostre o atalho `make` e o comando por extenso.
- Quando o comando muda por sistema, cubra **Linux/macOS/WSL**, **Git Bash** e **PowerShell** (ex.: ativar o venv — [11](../../docs/11-comandos.md#1-ambiente-virtual-venv)).
- Commits de exemplo: `feat: [CPBS-123] adiciona health check por escopo`.
- Nomes de serviço/container sempre os reais (`bot-varejo-api`, `bot-varejo-dynamodb`), nunca genéricos.

## Diagramas Mermaid

- Diagramas em Mermaid, dentro de ` ```mermaid `; um diagrama por ideia.
- Rótulos com espaço, acento ou símbolo entre aspas: `a["API FastAPI"]`; quebra de linha com `<br/>`; `&lt;`/`&gt;` para `<`/`>`.
- `sequenceDiagram`: não use `;` em notas ou mensagens.
- `gitGraph`: não faça `merge` de uma branch nela mesma; crie um `commit` antes do back-merge.
- IDs de nó sem espaço e sem palavras reservadas (`end`, `graph`).

## Links

- Sempre relativos (`./08-docker.md#4-variáveis-de-ambiente`); âncora = título em minúsculas, sem pontuação, espaços viram `-`.
- O teste `tests/contract/test_docs.py` valida arquivos e âncoras de todos os `.md` do projeto.
