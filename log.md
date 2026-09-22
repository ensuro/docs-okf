---
noindex: true
---

# Directory Update Log

## 2026-09-22

* **Network migration**: Updated the documentation to reflect that Ensuro v3 now lives on Ethereum Mainnet and that the former Polygon (v2) deployment is deprecated and inactive. Removed the deprecated Polygon v2 deployment addresses and audit tables, updated the Offchain API base URLs (now `offchain-v3.ensuro.co` and `offchain-sepolia-v3.ensuro.co`), and replaced Polygon/MATIC references with chain-neutral or Ethereum Mainnet language across the liquidity-provider, risk-partner, offchain-API and legal documentation. Governance timelock/multisig addresses remain unchanged pending the Ethereum Mainnet addresses.
* **Audits**: Replaced the placeholder audits page with the current audit information from the `ensuro/ensuro` and `ensuro/vaults` repositories. The v3 core protocol was audited by Quantstamp (2025-11-24 through 2025-12-03), and the yield vaults were audited by Quantstamp (2025-02-24 through 2025-03-03) and AuditAgent (2026-09-19).
* **Architecture, roles & governance**: Refreshed the Architecture page with the updated diagram and the v3 component descriptions from the `ensuro/ensuro` README. Rewrote the Roles and Governance pages to describe the AccessManager-based permissions from the deploy-scripts manifest: `ADMIN_ROLE`/`ADMIN_OPERATIVE_ROLE` role admins, the `LEVEL1_ROLE`/`LEVEL2_ROLE`/`GUARDIAN_ROLE` protocol roles with their delays, the operative roles, and the Safe multisigs (ADMINS_V3 3/4, LOW_RISK_V3 2/N, TREASURY_V3, TREASURY_PETTY_CASH, RECOVERY_MULTISIG).

## 2026-08-27

* **Reorganization**: Merged `protocol/` into `smart-contracts/`, which is now the top-level `ensuro-v3/` section. It groups the protocol concepts (Architecture, Roles, Governance, Policy Lifecycle, Policies, Liquidity pools, Premiums Accounts, Reserves, Asset Management) together with the Protocol FAQ and Risk Management pages, and now also hosts `deployments/` and `audits.md`. The contract reference pages moved from `smart-contracts/contracts/` to a new top-level `reference/` section, and the "APIs" sidebar entry was renamed to "Offchain APIs".

## 2026-07-23

* **Creation**: Migrated the full documentation from GitBook ([ensuro/docs](https://github.com/ensuro/docs) @ `5cc0120`) into this OKF v0.1 bundle. The GitBook site is deprecated and archived.
* **Deprecation**: The five legacy risk module implementation pages (TrustfulRiskModule, SignedQuoteRiskModule, SignedBucketRiskModule, FlightDelayRiskModule and PriceRiskModule) were not migrated, since the new version of the protocol has a single risk module. [RiskModule](reference/riskmodule.md) is now a placeholder pending the new protocol version documentation; links that pointed to those pages resolve there (anchors were dropped).
* **TODO**: `assets/openapi/pricing-api.yaml` is the newest pricing API spec copy archived from GitBook, but it lacks the documented `POST /example/cancel-policy` operation. Replace it with an export of the canonical `ensuro-quote-api` spec when available.
