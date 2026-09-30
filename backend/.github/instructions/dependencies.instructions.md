---
applyTo: "requirements.txt,requirements-test.txt,pyproject.toml"
description: "Dependências do backend (pip + requirements) e configuração das ferramentas"
---

# Dependências e `pyproject.toml`

Referência: [docs/13 — Dependências](../../docs/13-dependencias.md).

- `requirements.txt`: só o que a aplicação importa em runtime. `requirements-test.txt`: começa com `-r requirements.txt` e traz testes e ferramentas de qualidade. Nada de teste na imagem de produção.
- Toda versão com `==` (`pip index versions <lib>` para ver as disponíveis). Agrupe por seção com comentário (`# --- … ---`) e explique em uma linha o uso de libs não óbvias.
- Dependência transitiva só é fixada com motivo (segurança/compatibilidade) escrito no comentário.
- Antes de propor uma lib nova, verifique se a stdlib ou uma lib já presente resolve. Lib nova precisa de uso real no código.
- Ao adicionar/atualizar: conferir conflitos com `pip install --dry-run -r requirements-test.txt`, atualizar a tabela de `docs/13-dependencias.md` e lembrar que o container de dev precisa de `up --build`.
- `pyproject.toml` guarda **só** configuração de ferramentas (ruff, mypy, pytest, coverage, import-linter) — nunca dependências.
- Contratos do import-linter usam `api.contexts.*`: context novo já é coberto; não afrouxe contratos para "passar".
