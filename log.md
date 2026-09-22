---
noindex: true
---

# Directory Update Log

## 2026-08-27

* **Reorganization**: Merged `protocol/` into `smart-contracts/`, which is now the top-level `ensuro-v3/` section. It groups the protocol concepts (Architecture, Roles, Governance, Policy Lifecycle, Policies, Liquidity pools, Premiums Accounts, Reserves, Asset Management) together with the Protocol FAQ and Risk Management pages, and now also hosts `deployments/` and `audits.md`. The contract reference pages moved from `smart-contracts/contracts/` to a new top-level `reference/` section, and the "APIs" sidebar entry was renamed to "Offchain APIs".

## 2026-07-23

* **Creation**: Migrated the full documentation from GitBook ([ensuro/docs](https://github.com/ensuro/docs) @ `5cc0120`) into this OKF v0.1 bundle. The GitBook site is deprecated and archived.
* **Deprecation**: The five legacy risk module implementation pages (TrustfulRiskModule, SignedQuoteRiskModule, SignedBucketRiskModule, FlightDelayRiskModule and PriceRiskModule) were not migrated, since the new version of the protocol has a single risk module. [RiskModule](reference/riskmodule.md) is now a placeholder pending the new protocol version documentation; links that pointed to those pages resolve there (anchors were dropped).
* **TODO**: `assets/openapi/pricing-api.yaml` is the newest pricing API spec copy archived from GitBook, but it lacks the documented `POST /example/cancel-policy` operation. Replace it with an export of the canonical `ensuro-quote-api` spec when available.
