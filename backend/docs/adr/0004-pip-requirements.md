# ADR-0004 — pip com requirements.txt e requirements-test.txt

- **Status:** Aceito
- **Data:** 2026-09-30

## Contexto
O backend precisa de um jeito único de declarar e instalar dependências, igual na máquina do desenvolvedor e no Docker, e separar o que vai para produção do que só serve para testar e validar o código.

## Decisão
- **pip** (o instalador do próprio Python) com dois arquivos na raiz do projeto:

  | Arquivo | Conteúdo | Onde é instalado |
  |---------|----------|------------------|
  | `requirements.txt` | Dependências de **runtime** | Imagem de produção e desenvolvimento |
  | `requirements-test.txt` | `-r requirements.txt` + testes (pytest, pytest-asyncio, pytest-mock, freezegun, coverage, httpx2) e qualidade (ruff, mypy, import-linter, pre-commit) | Desenvolvimento — **nunca** na imagem de produção |

- **Toda versão fixada com `==`**, inclusive dependências transitivas que precisam de controle (ex.: `starlette`, `urllib3` por segurança). Atualização = MR `build(deps): …` com os testes verdes.
- Ambiente local em `.venv` (`python -m venv .venv`, ativado antes de usar `pip`); no Docker, venv só no estágio de runtime.
- `pyproject.toml` guarda **apenas a configuração das ferramentas** (ruff, mypy, pytest, coverage, import-linter), sem dependências.
- O pacote não é instalado: o código em `api/` entra no caminho de import rodando os comandos na raiz do projeto (e por `PYTHONPATH` no Docker).

Lista de libs, uso de cada uma e processo de atualização: [13 — Dependências](../13-dependencias.md).

## Alternativas consideradas
- **Poetry / pip-tools (lockfile de toda a árvore):** exigem uma ferramenta extra na máquina e no Docker. `requirements*.txt` com pip é o padrão que a equipe já usa.

## Consequências
- Nenhuma ferramenta além do Python/pip para instalar o projeto.
- Dependências transitivas não fixadas podem mudar entre builds; as sensíveis ficam fixadas explicitamente no `requirements.txt`.
- O Docker instala com `pip install -r requirements*.txt` (cache do pip no build).
