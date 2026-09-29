# ADRs — Backend

Decisões de arquitetura do **backend**. Formato: Contexto, Decisão, Alternativas, Consequências. Uma decisão nova que altera outra cria um novo ADR e marca o anterior como *Substituído*.

| ADR | Título | Status |
|-----|--------|--------|
| [0001](./0001-imagem-python-uvicorn.md) | Imagem python:3.13-slim com Uvicorn | Aceito |
| [0002](./0002-dominio-proprio-cors.md) | Domínio próprio da API, CORS e validação de Origin | Aceito |
| [0003](./0003-ddd.md) | DDD com bounded contexts e camadas | Aceito |
| [0004](./0004-uv.md) | uv como gerenciador de dependências | Aceito |
| [0005](./0005-convencao-de-nomes.md) | Convenção de nomes: PEP 8 no Python, camelCase no contrato | Aceito |
| [0006](./0006-contrato-openapi.md) | Contrato via OpenAPI gerado, versionado e publicado | Aceito |
| [0007](./0007-protocolo-websocket.md) | Protocolo WebSocket com envelope type/id/payload | Aceito |
| [0008](./0008-branches-e-fluxo-de-publicacao.md) | Branches `developer`, `staging`, `master` e fluxo de publicação | Aceito |

ADRs do frontend: `docs/adr/README.md` no repositório do **frontend**.
