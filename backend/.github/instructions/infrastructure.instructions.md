---
applyTo: "api/contexts/**/infrastructure/**"
description: "Camada infrastructure: adapters que implementam as ports (DynamoDB, HTTP de parceiros, relógio)"
---

# Camada `infrastructure` (adapters)

Referência: `api/contexts/health/infrastructure/system_clock.py` e o modelo de repositório em [docs/12 — Persistência](../../docs/12-persistencia-dynamodb.md).

- Cada arquivo implementa **uma** port do domínio, sem herdar dela (Protocol é estrutural). Nome da classe = tecnologia + conceito: `DynamoDbPartnerRepository`, `HttpAcmeCatalogClient`, `SystemClock`.
- Pode importar: `domain`, `api.core`, libs externas. **Nunca** `presentation`.
- Conversão entre item/JSON externo e entidade do domínio em funções `…_to_item` / `…_from_item` (ou `…_from_response`) num `codecs.py` do context — o domínio nunca vê `dict` cru.

## DynamoDB

- Uma tabela por context: `DynamoDbResource.table("<context>")`; nunca acesse tabela de outro context.
- Chaves `PK`/`SK` (`PARTNER#<id>`, `METADATA`), `GSI1PK`/`GSI1SK`, atributos em camelCase, `entityType`, `version`, `schemaVersion`, `createdAt`/`updatedAt`.
- Escrita com `ConditionExpression` (locking otimista por `version`); `ConditionalCheckFailedException` vira `ConflictError`.
- Nada de `Scan` em fluxo de requisição; `Query` com paginação por cursor opaco.
- Documente a tabela de padrões de acesso do context antes de implementar (docs/12, seção 3).
- Teste de integração contra o DynamoDB Local em `tests/integration/contexts/<ctx>/`.

## HTTP de parceiros

- `httpx.AsyncClient` com `timeout` explícito; um cliente por integração, criado no container e reutilizado.
- Retry só em falhas transitórias (timeout, 5xx, 429) com `tenacity` (backoff exponencial, número máximo de tentativas).
- Erros externos viram exceções do domínio ou `ComponentHealth` degradado — nunca vazam `httpx.HTTPError` para o caso de uso.
- Credenciais e URLs vêm do `Settings` (`api/config.py`), nunca hardcoded.
- Teste com `httpx.MockTransport` (sem rede real).
