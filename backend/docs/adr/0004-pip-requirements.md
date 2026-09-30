# ADR-0004 — pip com requirements.txt e requirements-test.txt

- **Status:** Aceito
- **Data:** 2026-09-30

## Contexto
O backend precisa de um jeito único de declarar e instalar dependências, igual na máquina do desenvolvedor, no Docker e no CI, e separar o que vai para produção do que só serve para testar e validar o código.

## Decisão
- **pip** (o instalador do próprio Python) com dois arquivos na raiz do projeto:

  | Arquivo | Conteúdo | Onde é instalado |
  |---------|----------|------------------|
  | `requirements.txt` | Dependências de **runtime** | Imagem de produção, dev, CI |
  | `requirements-test.txt` | `-r requirements.txt` + testes (pytest, pytest-asyncio, pytest-mock, freezegun, coverage, httpx2) e qualidade (ruff, mypy, import-linter, pre-commit) | Dev, CI — **nunca** na imagem de produção |

- **Toda versão fixada com `==`**, inclusive dependências transitivas que precisam de controle (ex.: `starlette`, `urllib3` por segurança). Atualização = MR `build(deps): …` com os testes verdes.
- Ambiente local em `.venv` (`python3.13 -m venv .venv`); no Docker, venv só no estágio de runtime.
- `pyproject.toml` guarda **apenas a configuração das ferramentas** (ruff, mypy, pytest, coverage, import-linter), sem dependências.
- O pacote não é instalado: o código em `api/` entra no caminho de import por `PYTHONPATH` na raiz do projeto (Docker, Makefile) e `pythonpath` do pytest.

Lista de libs, uso de cada uma e processo de atualização: [13 — Dependências](../13-dependencias.md).

## Alternativas consideradas
- **Poetry / pip-tools (lockfile de toda a árvore):** exigem uma ferramenta extra na máquina, no Docker e no CI. `requirements*.txt` com pip é o padrão que a equipe e os pipelines usam.

## Consequências
- Nenhuma ferramenta além do Python/pip para instalar o projeto.
- Dependências transitivas não fixadas podem mudar entre builds; as sensíveis ficam fixadas explicitamente no `requirements.txt`.
- Docker e CI instalam com `pip install -r requirements*.txt` (cache do pip no build e no CI).
