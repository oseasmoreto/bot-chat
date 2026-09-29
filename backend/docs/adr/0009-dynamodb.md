# ADR-0009 — Amazon DynamoDB como banco de dados

- **Status:** Aceito
- **Data:** 2026-09-29

## Contexto
O backend vai persistir conversas, fluxos, parceiros, serviços e integrações. O acesso é dominado por consultas por chave e por listas ordenadas dentro de um agregado (ex.: mensagens de uma conversa), com volume variável e necessidade de baixa latência para o chat em tempo real.

## Decisão
- **Amazon DynamoDB** é o banco de dados do backend.
- **Uma tabela por bounded context** (ex.: `conversation`, `flows`, `partners`), com **single-table design dentro da tabela**: chaves genéricas `PK`/`SK`, índices `GSI1`… com `GSI1PK`/`GSI1SK`, atributo `entityType` em todo item. Um context **nunca** lê ou escreve na tabela de outro.
- Acesso **assíncrono** com **aioboto3**, isolado na camada `infrastructure` (adapters que implementam as ports `…Repository` do domínio). O domínio não conhece DynamoDB nem boto.
- Nome das tabelas: `<APP_DYNAMODB_TABLE_PREFIX>-<context>` (ex.: `bot-varejo-production-partners`).
- Capacidade **on-demand** (`PAY_PER_REQUEST`); **Point-in-Time Recovery** e **deletion protection** em staging e production.
- Concorrência por **locking otimista** (atributo `version` + `ConditionExpression`).
- **DynamoDB Local** (`amazon/dynamodb-local`) no desenvolvimento, nos testes de integração e no CI.
- Tabelas na AWS provisionadas por infraestrutura como código (ferramenta a definir); localmente, por `make db-init` a partir das mesmas definições.

Detalhes: [12 — Persistência (DynamoDB)](../12-persistencia-dynamodb.md).

## Alternativas consideradas
- **Single-table para todo o backend:** menos tabelas, mas acopla os bounded contexts no mesmo keyspace e nos mesmos índices.
- **Uma tabela por entidade:** modelo relacional em cima do DynamoDB — mais leituras e sem itens relacionados na mesma partição.
- **boto3 síncrono em threadpool:** SDK mais conhecido, mas bloqueia threads num backend async.
- **PynamoDB:** modelos declarativos, porém síncrono e acopla o formato de persistência a classes de ORM.
- **LocalStack:** emula vários serviços AWS; desnecessário enquanto só o DynamoDB for usado.

## Consequências
- Modelagem guiada por **padrões de acesso**: cada repositório documenta os acessos que atende antes de definir chaves e índices.
- Sem `Scan` em fluxos de requisição; consultas sempre por chave ou índice.
- Transações (`TransactWriteItems`) só dentro da tabela do próprio context.
- Números voltam como `Decimal` — a conversão fica nos codecs do adapter.
- Itens limitados a 400 KB: conteúdo grande vai para armazenamento de arquivos (futuro), com referência no item.
- O health check ganha o componente `database` quando a primeira tabela existir.
