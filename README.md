# Ensuro OKF Documentation Bundle

This repository is the [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) documentation bundle for the [Ensuro](https://ensuro.co) protocol — a blockchain-based, regulated reinsurance protocol.

## Structure

```
├── index.md                  Bundle root (landing page)
├── README.md                 This file
├── AGENTS.md                 AI-agent instructions
├── log.md                    Change log
├── docmd.config.json         docmd static site configuration
├── package.json              Node dependencies
├── .github/workflows/deploy.yml  GitHub Pages deploy workflow
├── scripts/
│   └── check_okf.py          OKF conformance checker
├── assets/
│   ├── images/               Diagrams and logos
│   └── openapi/              OpenAPI specs
├── ensuro-v3/                Protocol v3: concepts, FAQ, risk management, deployments, audits
├── reference/                Smart contract reference
├── liquidity-providers/      LP documentation
├── risk-partners/            Risk partner documentation
├── offchain-apis/            REST API documentation
├── frontend/                 Frontend security and monitoring
└── legal/                    Legal and compliance documents
```

## Local Development

```sh
npm install
npm run dev       # Start dev server at http://localhost:3000
npm run build     # Build static site to ./site/
```

## Conformance

```sh
python3 scripts/check_okf.py
```

Validates OKF frontmatter, internal links, and asset references.

## Migration

This bundle was migrated from the GitBook site [ensuro/docs](https://github.com/ensuro/docs) (archived). See [`log.md`](log.md) for details and known gaps.
