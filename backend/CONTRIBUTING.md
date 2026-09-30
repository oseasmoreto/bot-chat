# Contribuindo — Backend

> Projeto: **Backend** — API REST + WebSocket (Python 3.13 · FastAPI).

Plataforma: **GitLab** (repositório e merge requests) · Tickets: **Jira** (`CPBS-xxx`).

Resumo: **branch de trabalho** `tipo/CPBS-123-descricao` criada da `developer` → **commits** Conventional Commits com `Refs: CPBS-123` → **MR para `developer`** (merge commit) → **promoção** `developer → staging → master` (MRs de release, merge commit) → **tag** `backend-vX.Y.Z` na `master` → produção.

```mermaid
flowchart LR
    t["Ticket CPBS-123"] --> b["branch de trabalho<br/>feat/CPBS-123-…<br/>(sai da developer)"]
    b -->|"MR · merge commit"| dev["developer<br/>ambiente dev"]
    dev -->|"MR de promoção<br/>merge commit"| stg["staging<br/>homologação"]
    stg -->|"MR de promoção<br/>merge commit"| mst["master<br/>produção"]
    mst --> tag["tag backend-vX.Y.Z<br/>versão de produção"]
```

## 1. Branches e fluxo de publicação

### 1.1 Branches permanentes (protegidas)

O repositório tem **três branches permanentes**, cada uma ligada a um ambiente. **Todas são travadas**: ninguém faz push direto, force push é proibido e elas não podem ser apagadas. Só recebem código por **merge request** aprovado.

| Branch | Ambiente | Recebe | Quem pode fazer merge |
|--------|----------|--------|------------------------|
| `developer` | **development** (`api-dev.<dominio>`) | MRs das branches de trabalho · back-merge da `staging` | Developers + Maintainers |
| `staging` | **staging / homologação** (`api-staging.<dominio>`) | **Somente** promoção da `developer` · back-merge da `master` | Maintainers |
| `master` | **production** (`api.<dominio>`) | **Somente** promoção da `staging` · `hotfix/*` | Maintainers |

- **Branch padrão do repositório: `developer`** — é o destino padrão dos MRs e a base de todas as branches de trabalho.
- `master` é sempre o que está (ou vai para) produção; `staging` é o candidato a release; `developer` é a integração contínua do time.
- Domínios de cada ambiente: a definir (os nomes acima são a convenção proposta).

### 1.2 Fluxo de publicação: `developer → staging → master`

```mermaid
%%{init: {'gitGraph': {'mainBranchName': 'master'}}}%%
gitGraph
    commit id: "release anterior" tag: "backend-v0.1.0"
    branch staging
    branch developer
    branch feat/CPBS-123-health
    commit id: "feat(backend): health"
    checkout developer
    merge feat/CPBS-123-health id: "merge MR 1"
    branch fix/CPBS-301-ajuste
    commit id: "fix(backend): cors"
    checkout developer
    merge fix/CPBS-301-ajuste id: "merge MR 2"
    checkout staging
    merge developer id: "promoção p/ staging"
    checkout master
    merge staging id: "promoção p/ master" tag: "backend-v0.2.0"
```

| Etapa | O que acontece | Ambiente atualizado |
|-------|----------------|---------------------|
| 1. Desenvolvimento | Branch de trabalho criada da `developer`; MR para `developer` (merge commit — todos os commits da branch entram na `developer`) | **development** |
| 2. Promoção para homologação | MR **`developer → staging`** (template *Release*, merge commit) | **staging** |
| 3. Homologação | QA/validação em staging. Problema encontrado? Correção vai **na `developer`** e sobe numa nova promoção — nunca direto na `staging` | — |
| 4. Promoção para produção | MR **`staging → master`** (template *Release*, merge commit) | — |
| 5. Release | Tag **`backend-vX.Y.Z`** criada na `master`, marcando a versão que vai para produção | **production** |

### 1.3 Matriz origem → destino

Qualquer combinação fora desta tabela é **proibida**: as branches protegidas limitam quem faz merge em cada destino (§5.4) e quem revisa confere origem e destino (§3.4).

| Origem | Destino | Tipo de MR | Método | Template |
|--------|---------|------------|--------|----------|
| `feat/*` `fix/*` `docs/*` `test/*` `refactor/*` `perf/*` `build/*` `chore/*` | `developer` | Trabalho | merge commit | Default / Bugfix / Docs |
| `developer` | `staging` | Promoção | merge commit | Release |
| `staging` | `master` | Promoção | merge commit | Release |
| `hotfix/*` | `master` | Hotfix | merge commit | Hotfix |
| `master` | `staging` | Back-merge (pós-hotfix) | merge commit | Release |
| `staging` | `developer` | Back-merge (pós-hotfix) | merge commit | Release |

**Não usamos squash** em nenhum MR: todos são integrados com **merge commit**. Assim cada commit da branch de trabalho — com seu `Refs: CPBS-xxx` — é preservado, e as três branches compartilham **exatamente os mesmos commits**: o que está em produção é, commit a commit, o que foi validado em staging.

### 1.4 Nome das branches de trabalho

```text
<tipo>/<TICKET>-<descricao-curta>
```

| Parte | Regra | Exemplo |
|-------|-------|---------|
| `tipo` | Um dos tipos da tabela abaixo | `feat` |
| `TICKET` | Chave do Jira, **obrigatória**, em maiúsculas | `CPBS-123` |
| `descricao-curta` | 2 a 5 palavras, kebab-case, minúsculas, sem acentos | `health-check` |
| Tamanho total | Máximo 60 caracteres | — |

Regex validada no hook local `pre-push` (as permanentes `developer`, `staging` e `master` são aceitas à parte):

```text
^(feat|fix|hotfix|docs|test|refactor|perf|build|chore)/CPBS-[0-9]+-[a-z0-9]+(-[a-z0-9]+)*$
```

| Tipo | Quando usar | Sai de | Volta para |
|------|-------------|--------|------------|
| `feat` | Nova funcionalidade | `developer` | `developer` |
| `fix` | Correção de bug (fluxo normal, inclusive bug achado em staging) | `developer` | `developer` |
| `hotfix` | Correção **urgente** de algo em **produção** | `master` | `master` (+ back-merge) |
| `docs` | Somente documentação / ADR | `developer` | `developer` |
| `test` | Somente testes | `developer` | `developer` |
| `refactor` | Refatoração sem mudar comportamento | `developer` | `developer` |
| `perf` | Melhoria de performance | `developer` | `developer` |
| `build` | Docker, dependências, build | `developer` | `developer` |
| `chore` | Manutenção geral | `developer` | `developer` |

✅ `feat/CPBS-123-health-check` · ✅ `hotfix/CPBS-290-ws-timeout`
❌ `feature/fundacao` (tipo inválido, sem ticket) · ❌ `feat/cpbs-123-Saúde` (ticket minúsculo, maiúscula, acento) · ❌ `fulano/teste` (sem padrão)

### 1.5 Regras de vida da branch de trabalho

1. **Sempre** criar a partir da `developer` atualizada: `git switch developer && git pull && git switch -c feat/CPBS-123-descricao` (hotfix: a partir da `master`).
2. **Uma branch = um ticket.** Ticket grande? Quebre em sub-tickets e MRs menores.
3. **Vida curta:** ideal até 3 dias. Branch parada fica desatualizada e gera conflito.
4. **Atualizar com rebase** na branch de origem: `git fetch && git rebase origin/developer` (hotfix: `origin/master`). Depois: `git push --force-with-lease` (nunca `--force` puro; nunca em branch permanente).
5. **Apagar após o merge** (opção "Delete source branch" marcada por padrão no GitLab). Branches permanentes nunca são apagadas — o GitLab não remove branches protegidas.

### 1.6 Promoção (release)

Feita por um **Maintainer** (responsável pelo release).

**`developer → staging`**

1. Conferir que a validação completa da `developer` está verde (§3.1) e que o ambiente **development** está saudável.
2. Abrir MR `developer → staging` com o template **Release**, título `chore(release): promove developer para staging`.
3. Listar os MRs/tickets incluídos: `git log --oneline --no-merges origin/staging..origin/developer`.
4. Confirmar dependências entre projetos (§3.5) e variáveis de ambiente novas já configuradas em **staging**.
5. Merge **sem apagar a branch de origem**; o ambiente **staging** passa a rodar esta versão.
6. Validação/QA em staging. Bug encontrado → `fix/*` a partir da `developer` → nova promoção.

**`staging → master`**

1. Validação em staging concluída e registrada no MR.
2. Abrir MR `staging → master` com o template **Release**, título `chore(release): promove staging para master (backend-vX.Y.Z)`.
3. Calcular a versão (§4) e conferir variáveis de ambiente de **production**.
4. Merge → criar a tag **`backend-vX.Y.Z`** no commit de merge da `master`: é a versão que vai para **production**.
5. Validação em **production** (health, telas/fluxos críticos) e comunicação do release.

Enquanto uma versão está em homologação, a `developer` continua recebendo MRs normalmente; eles entram na **próxima** promoção.

### 1.7 Hotfix

```mermaid
%%{init: {'gitGraph': {'mainBranchName': 'master'}}}%%
gitGraph
    commit id: "em produção" tag: "backend-v0.2.0"
    branch staging
    commit id: "candidato em homologação"
    branch developer
    commit id: "features em andamento"
    checkout master
    branch hotfix/CPBS-290-correcao
    commit id: "fix(backend): timeout ws"
    checkout master
    merge hotfix/CPBS-290-correcao id: "merge hotfix" tag: "backend-v0.2.1"
    checkout staging
    merge master id: "back-merge master→staging"
    checkout developer
    merge staging id: "back-merge staging→developer"
```

1. Ticket de prioridade alta; branch `hotfix/CPBS-xxx-descricao` **a partir da `master`**.
2. Correção **mínima** + teste de regressão; MR `hotfix/* → master` com o template **Hotfix**.
3. Merge → tag de patch `backend-vX.Y.Z+1`, a versão que vai para **production**.
4. **Back-merge obrigatório** no mesmo dia: MR `master → staging` e depois `staging → developer` (template **Release**, merge commit, título `chore(release): back-merge master para staging` / `… staging para developer`). Sem isso a correção some na próxima promoção.

## 2. Commits — Conventional Commits

### 2.1 Formato

```text
<tipo>(<escopo>): <descrição>
                                        ← linha em branco
[corpo opcional: POR QUE a mudança foi feita]
                                        ← linha em branco
Refs: CPBS-123
[BREAKING CHANGE: descrição, se houver]
```

| Parte | Regra |
|-------|-------|
| `tipo` | Obrigatório — tabela §2.2 |
| `escopo` | Esperado (aviso se ausente) — tabela §2.3 |
| `descrição` | Obrigatória; **pt-BR**, verbo no presente (completa a frase "este commit…": *adiciona*, *corrige*, *remove*); começa com **minúscula**; **sem ponto final** |
| Cabeçalho | Máximo **72 caracteres** |
| Corpo | Opcional; explica o **porquê** e o contexto, não o "o quê" (o diff já mostra); linhas até 100 caracteres |
| `Refs: CPBS-123` | **Obrigatório** em todo commit de trabalho — liga o commit ao ticket |
| `BREAKING CHANGE:` | Obrigatório quando quebra contrato ou comportamento esperado por quem consome. Também marcar `!` no cabeçalho |

Template de mensagem: [`.gitmessage`](./.gitmessage) — ativado por `make setup` (venv + dependências + `pre-commit install` + `git config commit.template .gitmessage`).

Os commits de merge gerados pelo GitLab em todos os MRs (`Merge branch 'feat/…' into 'developer'`) são aceitos automaticamente pelo commitlint.

### 2.2 Tipos

| Tipo | Uso | Gera versão |
|------|-----|-------------|
| `feat` | Nova funcionalidade para o usuário/consumidor | minor |
| `fix` | Correção de bug | patch |
| `perf` | Melhoria de performance | patch |
| `refactor` | Mudança de código sem alterar comportamento | — |
| `test` | Adiciona/ajusta testes, sem mudar produção | — |
| `docs` | Somente documentação | — |
| `style` | Formatação pura (sem mudança de lógica) | — |
| `build` | Dockerfile, dependências, build | — |
| `chore` | Manutenção; `chore(release)` nos títulos de promoção/back-merge | — |
| `revert` | Reverte um commit anterior | — |

Qualquer tipo com `!` ou rodapé `BREAKING CHANGE:` gera versão **major** (em `0.x`, **minor**).

### 2.3 Escopos

| Escopo | Quando usar |
|--------|-------------|
| `backend` | Qualquer mudança de código, testes, docs, Docker ou config do backend |
| `deps` | Atualização de dependências (`requirements.txt` / `requirements-test.txt`) |
| `repo` | Arquivos de repositório: `README.md`, `CONTRIBUTING.md`, `.gitmessage`, templates, hooks |
| `release` | **Somente** título de MR de promoção e de back-merge (§1.6 e §1.7) |

### 2.4 Exemplos

✅ Bons:

```text
feat(backend): adiciona health check por escopo

Expõe GET /api/v1/{public,admin}/health usando o mesmo caso de uso,
para que o frontend valide a comunicação ponta a ponta.

Refs: CPBS-123
```

```text
fix(backend): fecha websocket com código 1008 para origem não permitida

Refs: CPBS-301
```

```text
feat(backend)!: renomeia campo uptime para uptimeSeconds no health

BREAKING CHANGE: consumidores do health devem ler `uptimeSeconds`.
Refs: CPBS-340
```

```text
test(backend): cobre rejeição de origem no handshake websocket

Refs: CPBS-123
```

✅ Título de MR de promoção (não precisa de `Refs`):

```text
chore(release): promove developer para staging
chore(release): promove staging para master (backend-v0.2.0)
```

❌ Ruins:

| Mensagem | Problema |
|----------|----------|
| `ajustes` | Sem tipo, sem escopo, sem ticket, não diz nada |
| `feat: Adicionado health.` | Maiúscula, particípio, ponto final, sem escopo e sem `Refs` |
| `feat(frontend): ...` neste repositório | Escopo de outro projeto — mudanças do front vão no repositório do frontend |
| `feat(release): ...` em MR de trabalho | `release` é exclusivo de promoção/back-merge |
| `wip`, `ajuste`, `fix review` | Sem squash, todo commit vai para o histórico: reescreva commits temporários antes de abrir o MR (`git rebase -i origin/developer`) |

### 2.5 Boas práticas

- **Um commit = uma mudança lógica.** Facilita revisão e `git revert`.
- **Sem squash, o histórico é o que você commitar:** todos os commits da branch vão para `developer`, `staging` e `master`. Antes de abrir o MR, revise-os (`git log origin/developer..HEAD`) e reescreva mensagens fora do padrão ou commits temporários com `git rebase -i origin/developer`.
- **Durante a revisão:** ajustes pedidos entram como **novos commits** no padrão (ex.: `fix(backend): trata origem ausente no handshake`), sem reescrever o que já foi revisado.
- **TDD no histórico:** é bem-vindo o par `test(...)` → `feat(...)`, mostrando o teste antes da implementação.
- **Nada quebrado:** cada commit deveria passar em lint e testes.
- **Sem arquivos gerados** fora os previstos (`openapi.json`) e **sem segredos** — nunca.

## 3. Merge Requests

### 3.1 Regras

| Regra | MR de trabalho (→ `developer`) | MR de promoção / back-merge | MR de hotfix (→ `master`) |
|-------|-------------------------------|-----------------------------|---------------------------|
| **Título** | Cabeçalho de commit: `feat(backend): adiciona health check por escopo` | `chore(release): promove <origem> para <destino>` | Cabeçalho de commit: `fix(...)` |
| Template | Default / Bugfix / Docs | **Release** | **Hotfix** |
| Apagar branch de origem | Sim | **Não** (branch permanente) | Sim |
| Aprovações | ≥ 1 (não o autor) | ≥ 1 **Maintainer**; para `master`: **2** | **2**, incluindo 1 Maintainer |
| Quem faz o merge | Autor, após aprovação | Maintainer responsável pelo release | Maintainer |

Regras comuns a todos:

| Regra | Valor |
|-------|-------|
| Método de merge | **Merge commit** em todos os MRs — squash **desabilitado** no projeto |
| Commits | Todos no padrão da §2 (validados pelo commitlint no hook `commit-msg`); nada de `wip` |
| Em andamento | Prefixo `Draft:` no título — não pode ser mergeado |
| Preenchimento | **Todas** as seções do template; o que não se aplica recebe "N/A" com motivo |
| Tamanho (trabalho) | Ideal **até ~400 linhas** alteradas (sem contar arquivos gerados). Maior que isso: quebrar |
| Escopo do MR | Só mudanças **deste projeto** |
| Validação | Lint, tipos e testes rodados localmente e verdes antes de abrir o MR (checklist do template) |
| Threads | Todas resolvidas antes do merge |

### 3.2 Templates

Em [`.gitlab/merge_request_templates/`](./.gitlab/merge_request_templates) — aparecem no seletor **"Description → Choose a template"** ao criar o MR; o `Default.md` é aplicado automaticamente.

| Template | Arquivo | Usar para |
|----------|---------|-----------|
| **Default** (feature/geral) | [`Default.md`](./.gitlab/merge_request_templates/Default.md) | `feat`, `refactor`, `perf`, `test`, `build`, `chore` → `developer` |
| **Bugfix** | [`Bugfix.md`](./.gitlab/merge_request_templates/Bugfix.md) | `fix` → `developer` |
| **Docs** | [`Docs.md`](./.gitlab/merge_request_templates/Docs.md) | `docs` → `developer` |
| **Hotfix** | [`Hotfix.md`](./.gitlab/merge_request_templates/Hotfix.md) | `hotfix/*` → `master` |
| **Release** | [`Release.md`](./.gitlab/merge_request_templates/Release.md) | Promoções (`developer → staging`, `staging → master`) e back-merges |

| Seção | O que o template do backend pede |
|-------|----------------------------------|
| Partes afetadas | Camadas DDD (domínio, aplicação, infraestrutura, apresentação), WebSocket, `core/`, Docker |
| Contrato | `openapi.json` atualizado, retrocompatibilidade, impacto no frontend |
| Configuração | Novas variáveis, mudanças em `APP_CORS_ORIGINS` |
| Evidências | Requests/respostas, logs |
| Checklist | ruff, mypy `--strict`, lint-imports, pytest ≥ 90%, camadas DDD |
| Validação de hotfix | Health dos escopos `public`/`admin` + WebSocket |
| Release | MRs/tickets incluídos, contrato compatível com o frontend do ambiente de destino, variáveis configuradas, rollback |

Todos terminam com *quick actions* (`/assign me`, `/label ~tipo ~backend`) aplicadas ao criar o MR.

### 3.3 Labels

Criar no projeto do GitLab (Manage → Labels):

| Label | Cor sugerida | Aplicada por |
|-------|--------------|--------------|
| `feature` | azul | template Default |
| `bug` | vermelho | template Bugfix |
| `hotfix` | vermelho escuro | template Hotfix |
| `documentation` | cinza | template Docs |
| `release` | dourado | template Release |
| `backend` | verde | todos os templates deste projeto |
| `contract-change` | roxo | autor, quando o MR muda/consome contrato novo da API |
| `breaking-change` | laranja | autor, quando houver `BREAKING CHANGE` |

### 3.4 Checklist de revisão (para quem revisa)

- [ ] O título e os commits seguem o padrão; o ticket faz sentido com a mudança.
- [ ] Origem e destino respeitam a matriz da §1.3.
- [ ] O código segue os [padrões do backend](./docs/10-padroes-codigo.md) (PEP 8 no Python, camelCase no JSON — ADR-0005).
- [ ] Camadas DDD respeitadas: domínio sem FastAPI/Pydantic; presentation não acessa infrastructure direto; contexts isolados.
- [ ] Toda rota HTTP e mensagem WebSocket nova/alterada tem teste de integração; casos de uso com teste unitário.
- [ ] Contrato mudou? `openapi.json` e [Contratos de API](./docs/06-contratos-api.md) atualizados; mudança **retrocompatível** (ou `/api/v2`); frontend avisado (ticket/MR).
- [ ] CORS / `Origin` do WebSocket continuam restritos a `APP_CORS_ORIGINS`.
- [ ] Persistência (DynamoDB): cada context só acessa a própria tabela; consultas por chave/índice (sem `Scan`); escritas com condição/`version`; padrões de acesso documentados ([12](./docs/12-persistencia-dynamodb.md)).
- [ ] Documentação (`docs/`) e ADR atualizados quando necessário.
- [ ] Sem segredos, logs de debug, código comentado ou TODO sem ticket.

Comentários de revisão: prefixar com **`bloqueante:`**, **`sugestão:`** ou **`dúvida:`** para deixar claro o que impede o merge.

### 3.5 Mudanças que envolvem o Frontend

Mudanças de contrato consumidas pelo **frontend** seguem esta ordem **em cada ambiente**, porque os dois projetos são implantados separadamente:

```mermaid
flowchart LR
    b["MR backend (este repo)<br/>retrocompatível + openapi.json"] --> bd["backend chega<br/>ao ambiente X"]
    bd --> f["frontend que usa o contrato<br/>pode chegar ao ambiente X"]
    f --> r["(se preciso) MR backend<br/>remove o que ficou obsoleto"]
```

- O backend é promovido (`developer → staging → master`) **antes ou junto** do frontend que depende dele — nunca depois.
- Toda mudança precisa ser compatível com o frontend que **já está** no ambiente de destino.
- Incompatibilidade inevitável → nova versão de rota (`/api/v2`) convivendo com a anterior; ver [evolução do contrato](./docs/06-contratos-api.md#evolução-do-contrato).
- Cada MR cita o outro na seção **"MRs relacionados"** do template.

## 4. Versionamento e tags

- **SemVer**, com tags anotadas **somente na `master`**, no formato **`backend-vMAJOR.MINOR.PATCH`** (ex.: `backend-v0.2.0`). O prefixo identifica o projeto nas tags.
- A versão é derivada dos commits desde a última tag (tabela §2.2): `feat` → minor, `fix`/`perf` → patch, breaking → major. Em `0.x`, breaking sobe o **minor**. Hotfix → patch.
- Criada pelo Maintainer responsável pelo release, **depois** do merge na `master`: tag anotada no commit de merge, enviada com `git push origin <tag>`.
- `developer` e `staging` **não recebem tags de versão**.
- Futuro (opcional): `CHANGELOG.md` gerado a partir dos Conventional Commits.

## 5. Como o padrão é garantido

Duas camadas — hooks locais (feedback rápido) e configuração do GitLab (bloqueio).

```mermaid
flowchart LR
    subgraph local["Na máquina (pre-commit)"]
        h1["commit-msg<br/>commitlint"]
        h2["pre-push<br/>check-branch-name.sh"]
        h3["pre-commit<br/>lint/format"]
    end
    subgraph gl["Configuração do GitLab"]
        g1["developer, staging, master<br/>protegidas"]
        g2["merge commit<br/>(squash desabilitado)"]
        g3["threads resolvidas e<br/>aprovações"]
    end
    local --> gl
```

Os arquivos abaixo ficam **na raiz do repositório**.

### 5.1 `commitlint.config.mjs`

O commitlint roda pelo `pre-commit` (que instala o Node e as dependências sozinho) no hook `commit-msg`.

```js
const TYPES = ['feat', 'fix', 'perf', 'refactor', 'test', 'docs', 'style', 'build', 'chore', 'revert'];
const SCOPES = ['backend', 'deps', 'repo', 'release'];


export default {
  extends: ['@commitlint/config-conventional'],
  parserPreset: { parserOpts: { issuePrefixes: ['CPBS-'] } },
  rules: {
    'type-enum': [2, 'always', TYPES],
    'scope-enum': [2, 'always', SCOPES],
    'scope-empty': [1, 'never'],
    'header-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100],
    'references-empty': [2, 'never'],
  },
};
```

### 5.2 `scripts/check-branch-name.sh`

```bash
#!/usr/bin/env bash
# Valida o nome da branch. Uso: check-branch-name.sh [nome]  (padrão: branch atual)
set -euo pipefail

branch="${1:-$(git rev-parse --abbrev-ref HEAD)}"
pattern='^(feat|fix|hotfix|docs|test|refactor|perf|build|chore)/CPBS-[0-9]+-[a-z0-9]+(-[a-z0-9]+)*$'
max_length=60

case "$branch" in
  developer|staging|master) exit 0 ;;   # branches permanentes
esac

if [[ "$branch" =~ $pattern ]] && (( ${#branch} <= max_length )); then
  exit 0
fi

echo "✖ Nome de branch inválido: '$branch'" >&2
echo "  Esperado: <tipo>/CPBS-<numero>-<descricao-em-kebab-case> (máx. $max_length caracteres)" >&2
echo "  Exemplo:  feat/CPBS-123-health-check" >&2
echo "  Ver: CONTRIBUTING.md §1.4" >&2
exit 1
```

### 5.3 `.pre-commit-config.yaml`

```yaml
default_install_hook_types: [pre-commit, commit-msg, pre-push]

repos:
  # Mensagem de commit
  - repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
    rev: v9.x.x   # fixar a versão na implementação
    hooks:
      - id: commitlint
        stages: [commit-msg]
        additional_dependencies: ['@commitlint/config-conventional']

  - repo: local
    hooks:
      # Nome da branch
      - id: branch-name
        name: nome da branch
        entry: scripts/check-branch-name.sh
        language: script
        pass_filenames: false
        always_run: true
        stages: [pre-push]

      # Qualidade do backend — usa o ruff/mypy do .venv: faça o commit com o venv ativado
      - id: ruff
        name: ruff (lint)
        entry: ruff check --fix
        language: system
        types: [python]
      - id: ruff-format
        name: ruff (format)
        entry: ruff format
        language: system
        types: [python]
      - id: mypy
        name: mypy --strict
        entry: mypy api tests
        language: system
        types: [python]
        pass_filenames: false
```

### 5.4 Configurações do projeto no GitLab

| Onde (GitLab) | Configuração |
|---------------|--------------|
| Settings → Repository → Branch defaults | **Default branch: `developer`** |
| Settings → Repository → Protected branches | `developer`: *Allowed to merge* = Developers + Maintainers · `staging`: Maintainers · `master`: Maintainers. Nas três: *Allowed to push and merge* = **No one**; *Allowed to force push* = **desligado** |
| Settings → Repository → Protected tags | `backend-v*`: só Maintainers criam |
| Settings → Merge requests → Merge method | **Merge commit** (todos os MRs; preserva cada commit e o mesmo histórico entre ambientes) |
| Settings → Merge requests → Squash commits when merging | **Do not allow** (squash desabilitado) |
| Settings → Merge requests → Merge commit message template | Padrão do GitLab (`Merge branch '%{source_branch}' into '%{target_branch}'` + título + referência do MR). Começa com `Merge`, então o commitlint o ignora |
| Settings → Merge requests → Merge checks | ✅ *All threads must be resolved* |
| Settings → Merge requests → Merge options | ✅ *Delete source branch by default* (branches protegidas nunca são apagadas) |
| Settings → Merge requests → Approvals | Regras da §3.1; autor não pode aprovar o próprio MR |
| Settings → Repository → Push rules *(se o plano tiver)* | Branch name regex = a do §1.4 (+ permanentes) |
| Settings → Integrations → Jira *(se usado)* | Ativar para que `CPBS-xxx` em branch, commit e MR crie o link no ticket |

> **Plano do GitLab:** aprovações **obrigatórias**, regras de aprovação por branch de destino/caminho e *Push rules* são recursos pagos (Premium/Ultimate). No plano Free, essas regras valem **por convenção** (checklist de revisão), com a garantia técnica nas branches protegidas, nas tags protegidas e nos hooks locais.

## 6. Cola rápida

```bash
# começar uma tarefa
git switch developer && git pull
git switch -c feat/CPBS-123-minha-feature

# commitar (abre o editor com o template .gitmessage)
git add -p
git commit

# atualizar com a developer
git fetch && git rebase origin/developer
git push --force-with-lease

# abrir o MR → developer: título "feat(backend): adiciona ..." + template Default

# hotfix
git switch master && git pull
git switch -c hotfix/CPBS-456-correcao
# MR → master com template Hotfix; depois back-merge master → staging → developer

# release (Maintainer): MR developer → staging e staging → master com template Release;
# após o merge na master, criar a tag anotada backend-vX.Y.Z e enviar com git push origin <tag>
```
