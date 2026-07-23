---
type: Meta
title: Repository conventions
description: Conventions and maintenance notes for the Ensuro OKF documentation bundle.
tags:
- meta
timestamp: '2026-07-23T00:00:00Z'
---

# AGENTS.md

This repository is the public documentation of [Ensuro](https://ensuro.co), a blockchain-based
regulated reinsurance protocol. The documentation is maintained as an
[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) knowledge bundle:
a tree of markdown *concept* files with YAML frontmatter. It was migrated from the former GitBook
site ([ensuro/docs](https://github.com/ensuro/docs) @ `5cc0120`, archived) on 2026-07-23.

## Conventions

* The bundle root is the repository root. Reserved filenames per OKF: `index.md` (directory
  listings, no frontmatter except `okf_version` in the root one) and `log.md` (chronological
  change log, newest first, `YYYY-MM-DD` headings).
* Every other `.md` file is a concept and MUST have YAML frontmatter with a non-empty `type`.
  Known types: `Guide`, `Concept`, `Smart Contract`, `API Reference`, `FAQ`, `Reference`,
  `Legal Document`, `Meta`. Include `title`, `description`, `tags` and `timestamp` (ISO 8601)
  when adding or meaningfully editing a concept.
* Content is renderer-neutral markdown: no GitBook/MkDocs-specific syntax. Notes are written as
  `> **Note:** ...` blockquotes; multi-language code samples use `#### Shell` / `#### Python` /
  `#### NodeJS` subheadings; math uses `$$ ... $$` blocks.
* Internal links are relative markdown links to the target `.md` file. Binary assets live under
  `assets/images/`; OpenAPI specs under `assets/openapi/`.
* When adding/removing/renaming concepts, update the affected `index.md` files and add an entry
  to `log.md`.

## Verification

Run the conformance checker before committing:

```sh
python3 scripts/check_okf.py
```

It validates OKF conformance (frontmatter presence/`type`), internal link and anchor resolution,
and asset references.

## Known gaps

See `log.md` for the migration entry: the pricing API spec (`assets/openapi/pricing-api.yaml`) is
missing the `cancel-policy` operation, and `smart-contracts/contracts/riskmodule.md` is a
placeholder pending the new protocol version docs.
