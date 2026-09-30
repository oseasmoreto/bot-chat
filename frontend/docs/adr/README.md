# ADRs — Frontend

Decisões de arquitetura do **frontend**. Formato: Contexto, Decisão, Alternativas, Consequências. Os ADRs descrevem **só a decisão vigente**: quando uma decisão muda, o ADR correspondente é reescrito com a decisão atual (o histórico fica no git).

| ADR | Título | Status |
|-----|--------|--------|
| [0001](./0001-nextjs-padrao-como-spa.md) | Next.js padrão (servidor Node) usado como SPA | Aceito |
| [0002](./0002-app-unico-areas-e-features.md) | Um único app com áreas (web/admin) e features | Aceito |
| [0003](./0003-imagem-node.md) | Imagem node:24-slim rodando o servidor Next | Aceito |
| [0004](./0004-config-em-runtime.md) | Configuração da API em runtime (não no build) | Aceito |
| [0005](./0005-pnpm.md) | pnpm como gerenciador de pacotes | Aceito |
| [0006](./0006-convencao-de-nomes.md) | Convenção de nomes: camelCase | Aceito |
| [0007](./0007-cliente-tipado-openapi.md) | Cliente HTTP tipado gerado do OpenAPI do backend | Aceito |
| [0008](./0008-branches-e-fluxo-de-publicacao.md) | Branches `developer`, `staging`, `master` e fluxo de publicação | Aceito |

ADRs do backend: `docs/adr/README.md` no repositório do **backend**.
