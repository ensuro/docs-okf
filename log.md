---
noindex: true
---

# Directory Update Log

## 2026-07-23

* **Creation**: Migrated the full documentation from GitBook ([ensuro/docs](https://github.com/ensuro/docs) @ `5cc0120`) into this OKF v0.1 bundle. The GitBook site is deprecated and archived.
* **Deprecation**: The five legacy risk module implementation pages (TrustfulRiskModule, SignedQuoteRiskModule, SignedBucketRiskModule, FlightDelayRiskModule and PriceRiskModule) were not migrated, since the new version of the protocol has a single risk module. [RiskModule](smart-contracts/contracts/riskmodule.md) is now a placeholder pending the new protocol version documentation; links that pointed to those pages resolve there (anchors were dropped).
* **TODO**: `assets/openapi/pricing-api.yaml` is the newest pricing API spec copy archived from GitBook, but it lacks the documented `POST /example/cancel-policy` operation. Replace it with an export of the canonical `ensuro-quote-api` spec when available.
