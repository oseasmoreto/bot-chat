# Bot Varejo — Backend

API REST + WebSocket do Bot Varejo: **Python 3.13 · FastAPI · async · WebSockets · DynamoDB**. Atende os escopos `public` (cliente final) e `admin` (operação), consumidos pelo **frontend** (repositório próprio) em outro domínio.

> 📚 Documentação completa: [`docs/`](./docs/README.md) · Branch/commit/MR: [CONTRIBUTING.md](./CONTRIBUTING.md) · Templates de MR: [`.gitlab/`](./.gitlab/merge_request_templates)
>
> **Status:** fundação implementada — health check (`public`/`admin`) via HTTP e WebSocket, CORS, validação de `Origin`, erros padronizados, log JSON e `X-Request-ID`. O acesso ao DynamoDB (`core/dynamodb`) chega com o primeiro context que persistir dados.

## O sistema

O Bot Varejo tem dois projetos, implantados de forma independente:

| Projeto | Domínio | Papel |
|---------|---------|-------|
| **Backend** (este) | `api.<dominio>` | APIs REST (`/api/v1/public`, `/api/v1/admin`) e WebSocket (`/api/v1/ws/public`, `/api/v1/ws/admin`) |
| Frontend | `app.<dominio>` | App Next.js: web em `/` (escopo `public`) e admin em `/admin` (escopo `admin`) |

```mermaid
flowchart LR
    u["👤 Cliente final"] --> f
    o["👤 Operador"] --> f
    f["Frontend<br/>app.&lt;dominio&gt;"] -. "navegador chama a API<br/>HTTPS + WSS (CORS)" .-> a["Backend (este)<br/>api.&lt;dominio&gt;"]
```

- **Um processo por container** (Uvicorn); TLS e domínio ficam na plataforma de deploy.
- A única ligação com o frontend é o **contrato** HTTP/WebSocket: [docs/06-contratos-api.md](./docs/06-contratos-api.md) + `openapi.json`.
- O frontend tem repositório, documentação e deploy próprios.

## Pré-requisitos

| Ferramenta | Versão | Obrigatória para |
|------------|--------|------------------|
| Docker Engine + Docker Compose v2 | Compose ≥ 2.24 | Rodar a API e o banco (caminho recomendado) |
| Python + venv | 3.13 (`python3.13 -m venv` — no Debian/Ubuntu: `sudo apt install python3.13-venv`) | Rodar sem Docker, testes e lint |
| make | qualquer | *(opcional)* atalhos do `Makefile` — todo comando também está escrito por extenso abaixo |
| websocat, AWS CLI | — | *(opcionais)* testar WebSocket e inspecionar o DynamoDB Local |

> **Linux/WSL:** seu usuário precisa estar no grupo `docker` — `sudo usermod -aG docker $USER` e abra um novo terminal. Sem isso aparece `permission denied … docker.sock`.

## Configuração

1. **Clonar e entrar no repositório**

   ```bash
   git clone <url-do-repositorio-backend> bot-varejo-backend
   cd bot-varejo-backend
   ```

2. **Criar o `.env`** a partir do exemplo (os valores padrão já funcionam localmente):

   ```bash
   cp .env.example .env
   ```

   O `.env` é lido pelo Docker Compose (portas e variáveis `APP_*`) e pela aplicação. O endereço do banco (`APP_DYNAMODB_ENDPOINT_URL`) já é definido pelo compose; só precisa ir no `.env` quando a API roda **fora** do Docker. Todas as variáveis estão em [Variáveis de ambiente](#variáveis-de-ambiente).

3. **Preparar o ambiente para contribuir** *(uma vez por clone)*:

   ```bash
   git config commit.template .gitmessage   # template de mensagem de commit
   python3.13 -m venv .venv                  # ambiente virtual do projeto
   .venv/bin/pip install -r requirements-test.txt   # runtime + testes e qualidade (inclui pre-commit)
   source .venv/bin/activate                 # ativa o venv neste terminal
   pre-commit install                        # hooks: commitlint, nome da branch, ruff, mypy
   ```

## Rodando

O compose sobe dois serviços:

| Serviço | Container (runtime / dev) | Porta no host | O que é |
|---------|---------------------------|---------------|---------|
| `bot-varejo-api` | `bot-varejo-api` / `bot-varejo-api-dev` | `8000` (`API_PORT`) | API FastAPI |
| `bot-varejo-dynamodb` | `bot-varejo-dynamodb` / `bot-varejo-dynamodb-dev` | `8001` (`DYNAMODB_PORT`) | DynamoDB Local (dados no volume `bot-varejo-dynamodb-data` / `…-dev-data`) |

### Desenvolvimento (recomendado no dia a dia)

Código de `api/` montado no container: **cada alteração recarrega a API sozinha** (~2 s), sem subir de novo. Só mudar `requirements.txt`, `requirements-test.txt` ou `Dockerfile` pede `--build`.

```bash
docker compose -f docker-compose.dev.yml up --build
```

### Imagem de produção

Mesma imagem que vai para os ambientes (sem reload, usuário não-root, healthcheck):

```bash
docker compose up --build -d
```

### Sem Docker para a API

Útil para depurar na IDE. O banco continua no Docker:

```bash
docker compose -f docker-compose.dev.yml up -d bot-varejo-dynamodb
APP_DYNAMODB_ENDPOINT_URL=http://localhost:8001 \
  PYTHONPATH=. .venv/bin/uvicorn api.app_run:create_app --factory --reload --port 8000
```

### Tabelas do banco

Cada bounded context com persistência tem sua tabela ([docs/12](./docs/12-persistencia-dynamodb.md)). O script que cria as tabelas no DynamoDB Local (`python -m api.scripts.create_tables`, idempotente) chega junto com o primeiro context que persistir dados.

### Comandos úteis

Acrescente `-f docker-compose.dev.yml` quando estiver usando o compose de desenvolvimento.

| Ação | Comando |
|------|---------|
| Ver status | `docker compose ps` |
| Acompanhar logs da API | `docker compose logs -f bot-varejo-api` |
| Parar tudo | `docker compose down` |
| Parar e **apagar os dados** do banco local | `docker compose down -v` |
| Recriar após mudar `requirements*.txt`/`Dockerfile` (código em `api/` não precisa) | `docker compose up --build` |
| Shell dentro da API | `docker compose exec bot-varejo-api sh` |
| Listar tabelas do banco local | `aws dynamodb list-tables --endpoint-url http://localhost:8001` |

### URLs

| URL | O quê |
|-----|-------|
| http://localhost:8000/api/v1/public/health | Health (public) |
| http://localhost:8000/api/v1/admin/health | Health (admin) |
| ws://localhost:8000/api/v1/ws/public · /api/v1/ws/admin | WebSocket |
| http://localhost:8000/api/docs | Swagger |
| http://localhost:8000/api/redoc | ReDoc |
| http://localhost:8000/api/openapi.json | OpenAPI |
| http://localhost:8001 | DynamoDB Local |

### Verificação rápida

```bash
curl -s http://localhost:8000/api/v1/public/health
# {"status":"ok","scope":"public","version":"0.0.0-local","uptimeSeconds":3.2,"checkedAt":"…","components":[]}

# WebSocket (websocat) — o header Origin precisa estar em APP_CORS_ORIGINS
echo '{"type":"health.ping","id":"1","payload":{}}' \
  | websocat -H "Origin: http://localhost:3000" ws://localhost:8000/api/v1/ws/public
# {"type":"health.pong","id":"1","payload":{"status":"ok","scope":"public",…}}
```

### Junto com o frontend

1. Suba este projeto (API em `:8000`, banco em `:8001`).
2. No repositório do **frontend**, suba o compose dele (`bot-varejo-web` em `:3000`).
3. Acesse `http://localhost:3000/health` e `http://localhost:3000/admin/health`.

O CORS já libera `http://localhost:3000` por padrão; se o front rodar em outra porta, ajuste `APP_CORS_ORIGINS` no `.env`.

## Estrutura e dependências

```text
api/                     # código da aplicação
├── app_run.py           # create_app()
├── config.py            # Settings (variáveis APP_*)
├── container.py         # montagem de adapters e casos de uso
├── core/                # cors, swagger, logs, errors, request_id, websocket…
├── routes/              # public.py, admin.py, websocket.py
├── contexts/<context>/  # DDD: domain, application, infrastructure, presentation
└── scripts/             # python -m api.scripts.<nome>
tests/                   # unit, integration, contract
config/                  # deploy/infra da plataforma (não alterar a estrutura)
certificates/            # certificados de CA adicionais (.crt)
requirements.txt         # dependências de runtime (versões fixadas)
requirements-test.txt    # -r requirements.txt + testes e qualidade
```

- O que vai em cada pasta e onde colocar algo novo: [docs/02 — Estrutura](./docs/02-estrutura.md#o-que-vai-em-cada-pasta).
- Cada lib, para que serve e como adicionar/atualizar: [docs/13 — Dependências](./docs/13-dependencias.md).
- GitHub Copilot (VS Code): regras em `.github/`, prompts `/novo-context`, `/novo-modulo`, `/novo-endpoint`, `/nova-mensagem-ws`, `/revisar-arquitetura` e o agente `backend-ddd` — ver [docs/14 — IA](./docs/14-ia-copilot.md). Lib nova = linha com versão fixada no arquivo certo + `docker compose … up --build`.

## Testes e qualidade

Com o venv ativado, na raiz do projeto (`export PYTHONPATH=.`):

```bash
coverage run -m pytest && coverage report   # testes + cobertura (≥ 90%) + contrato OpenAPI
ruff check .                                # lint
ruff format .                               # formatação
mypy api tests                              # tipos (--strict)
lint-imports                                # fronteiras das camadas DDD
python -m api.scripts.export_openapi openapi.json   # atualiza o contrato
```

Com `make`: `make check` roda tudo o que o CI valida (`make help` lista os atalhos).

Os testes de integração dos repositórios usam o DynamoDB Local: deixe `bot-varejo-dynamodb` no ar e rode com `APP_DYNAMODB_ENDPOINT_URL=http://localhost:8001`.

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `APP_ENV` | `local` | Ambiente |
| `APP_VERSION` | `0.0.0-local` | Versão exibida no health/OpenAPI |
| `APP_LOG_LEVEL` | `INFO` | Nível de log |
| `APP_DOCS_ENABLED` | `true` | Habilita Swagger/OpenAPI |
| `APP_CORS_ORIGINS` | `["http://localhost:3000"]` | Origens do frontend (JSON) — CORS e WebSocket |
| `FORWARDED_ALLOW_IPS` | `127.0.0.1` | Proxies confiáveis (`X-Forwarded-*`) |
| `API_PORT` | `8000` | Porta publicada no host |
| `APP_AWS_REGION` | `sa-east-1` | Região do DynamoDB |
| `APP_DYNAMODB_ENDPOINT_URL` | `http://bot-varejo-dynamodb:8000` (compose) | DynamoDB Local; vazio na AWS |
| `DYNAMODB_PORT` | `8001` | Porta do DynamoDB Local no host |
| `APP_DYNAMODB_TABLE_PREFIX` | `bot-varejo-local` | Prefixo das tabelas |

## Solução de problemas

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| `permission denied … docker.sock` | Usuário fora do grupo `docker` | `sudo usermod -aG docker $USER` e abrir um novo terminal |
| `port is already allocated` (8000 ou 8001) | Porta em uso por outro processo | Parar o outro compose ou mudar `API_PORT`/`DYNAMODB_PORT` no `.env` |
| DynamoDB Local não sobe ou não grava | Volume corrompido ou de outra versão | `docker compose down -v` e subir de novo (apaga os dados locais) |
| Front mostra erro de CORS no console | Origem do front fora de `APP_CORS_ORIGINS` | Ajustar `.env`: `APP_CORS_ORIGINS='["http://localhost:3000"]'` |
| WebSocket fecha na hora (código 1008) | `Origin` ausente ou não permitido | Enviar `Origin` permitido (navegador envia sozinho) |
| Teste de contrato falhando | `openapi.json` desatualizado | `python -m api.scripts.export_openapi openapi.json` (venv ativado, `PYTHONPATH=.`) e commitar |
| Lib nova não aparece no dev (`ModuleNotFoundError`) | Deps instaladas no build da imagem | Subir com `--build`; fora do Docker, `.venv/bin/pip install -r requirements-test.txt` |
| `ModuleNotFoundError: No module named 'api'` fora do Docker | Raiz do projeto fora do caminho de import | Rodar da raiz do projeto com `PYTHONPATH=.` (o `make` já define) |

## Contribuindo

Leia o [CONTRIBUTING.md](./CONTRIBUTING.md). Resumo:

```text
branch:    feat/CPBS-123-descricao-curta                        ← sai da developer
commit:    feat(backend): adiciona health check por escopo      ← escopos: backend | ci deps repo
           (linha em branco)
           Refs: CPBS-123
MR:        → developer · merge commit (sem squash) · template de .gitlab/ · ≥ 1 aprovação · pipeline verde
publicar:  developer → staging → master   (MRs de promoção, template Release)
tag:       backend-vX.Y.Z na master → deploy em production (aprovação manual)
```

- Template de commit: [`.gitmessage`](./.gitmessage) (ativado com `git config commit.template .gitmessage` — ver [Configuração](#configuração)).
- Templates de MR: [`.gitlab/merge_request_templates/`](./.gitlab/merge_request_templates) — Default, Bugfix, Docs, Hotfix, Release.
- Branches permanentes e protegidas: `developer` (development), `staging` (homologação), `master` (production) — fluxo e promoção em [CONTRIBUTING §1](./CONTRIBUTING.md#1-branches-e-fluxo-de-publicação).
- Mudanças que envolvem o frontend: ver [CONTRIBUTING §3.5](./CONTRIBUTING.md#35-mudanças-que-envolvem-o-frontend).
