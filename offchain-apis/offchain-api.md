---
type: API Reference
title: Offchain API
description: REST API to query information about policies and other components of the protocol.
tags:
- api
- reference
timestamp: '2024-05-22T16:18:34+00:00'
resource: https://offchain-v2.ensuro.co/api/
spec: assets/openapi/offchain-api.yaml
---

# Offchain API

You can navigate our offchain API at these URLs:

* Polygon Mainnet: [https://offchain-v2.ensuro.co/api/](https://offchain-v2.ensuro.co/api/)
* Sepolia Testnet: [https://offchain-sepolia.ensuro.co/api/](https://offchain-sepolia.ensuro.co/api/)

The full machine-readable specification is bundled with this bundle at
[assets/openapi/offchain-api.yaml](../assets/openapi/offchain-api.yaml) (OpenAPI/Swagger 2.0).

# Endpoints

## etokenblockshots

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/etokenblockshots/` | `etokenblockshots_list` |
| GET | `/etokenblockshots/by_day/` | `etokenblockshots_by_day` |
| GET | `/etokenblockshots/by_week/` | `etokenblockshots_by_week` |
| GET | `/etokenblockshots/{id}/` | `etokenblockshots_read` |


## etokens

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/etokens/` | `etokens_list` |
| GET | `/etokens/apy_range/` | `etokens_apy_range` |
| GET | `/etokens/{address}/` | `etokens_read` |
| GET | `/etokens/{address}/apr/` | `etokens_apr` |
| GET | `/etokens/{address}/apr_history/` | `etokens_apr_history` |
| GET | `/etokens/{address}/block_shots/` | `etokens_block_shots` |
| GET | `/etokens/{address}/composition_history/` | `etokens_composition_history` |
| GET | `/etokens/{address}/liquidity_history/` | `etokens_liquidity_history` |
| GET | `/etokens/{address}/lockup/` | `etokens_lockup` |
| GET | `/etokens/{address}/lps_breakdown/` | `etokens_lps_breakdown` |
| GET | `/etokens/{address}/net_deposits/` | `etokens_net_deposits` |
| GET | `/etokens/{address}/net_deposits_history/` | `etokens_net_deposits_history` |
| GET | `/etokens/{address}/pa_scr_breakdown/` | `etokens_pa_scr_breakdown` |
| GET | `/etokens/{address}/scr_breakdown/` | `etokens_scr_breakdown` |
| GET | `/etokens/{address}/scr_history/` | `etokens_scr_history` |
| GET | `/etokens/{address}/ur_history/` | `etokens_ur_history` |


## events

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/events/` | `events_list` |
| POST | `/events/alchemy_webhook/` | `events_alchemy_webhook` |
| GET | `/events/{id}/` | `events_read` |


## lpevents

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/lpevents/` | `lpevents_list` |
| GET | `/lpevents/{event}/` | `lpevents_read` |


## lps

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/lps/` | `lps_list` |
| GET | `/lps/{address}/` | `lps_read` |


## policies

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/policies/` | `policies_list` |
| GET | `/policies/nft/{ensuro_id}/` | `policies_nft` |
| GET | `/policies/{id}/` | `policies_read` |


## pools

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/pools/` | `pools_list` |
| GET | `/pools/{address}/` | `pools_read` |


## premiumsaccounts

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/premiumsaccounts/` | `premiumsaccounts_list` |
| GET | `/premiumsaccounts/{address}/` | `premiumsaccounts_read` |
| GET | `/premiumsaccounts/{address}/active_policies/` | `premiumsaccounts_active_policies` |
| GET | `/premiumsaccounts/{address}/active_policies_history/` | `premiumsaccounts_active_policies_history` |
| GET | `/premiumsaccounts/{address}/active_premiums/` | `premiumsaccounts_active_premiums` |
| GET | `/premiumsaccounts/{address}/active_premiums_history/` | `premiumsaccounts_active_premiums_history` |
| GET | `/premiumsaccounts/{address}/cashflow/` | `premiumsaccounts_cashflow` |
| GET | `/premiumsaccounts/{address}/composition_history/` | `premiumsaccounts_composition_history` |
| GET | `/premiumsaccounts/{address}/gwp/` | `premiumsaccounts_gwp` |
| GET | `/premiumsaccounts/{address}/gwp_history/` | `premiumsaccounts_gwp_history` |
| GET | `/premiumsaccounts/{address}/matured_surplus/` | `premiumsaccounts_matured_surplus` |
| GET | `/premiumsaccounts/{address}/matured_surplus_history/` | `premiumsaccounts_matured_surplus_history` |
| GET | `/premiumsaccounts/{address}/rm_breakdown/` | `premiumsaccounts_rm_breakdown` |
| GET | `/premiumsaccounts/{address}/scr/` | `premiumsaccounts_scr` |
| GET | `/premiumsaccounts/{address}/scr_history/` | `premiumsaccounts_scr_history` |
| GET | `/premiumsaccounts/{address}/surplus/` | `premiumsaccounts_surplus` |
| GET | `/premiumsaccounts/{address}/surplus_history/` | `premiumsaccounts_surplus_history` |
| GET | `/premiumsaccounts/{address}/wonpremiumsinout/` | `premiumsaccounts_wonpremiumsinout` |


## quotes

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/quotes/` | `quotes_list` |
| POST | `/quotes/webhook/` | `quotes_webhook` |
| GET | `/quotes/{id}/` | `quotes_read` |


## riskmodules

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/riskmodules/` | `riskmodules_list` |
| GET | `/riskmodules/total_premiums/` | `riskmodules_total_premiums` |
| GET | `/riskmodules/{address}/` | `riskmodules_read` |
| GET | `/riskmodules/{address}/active_policies/` | `riskmodules_active_policies` |
| GET | `/riskmodules/{address}/active_premiums/` | `riskmodules_active_premiums` |
| GET | `/riskmodules/{address}/cashflow/` | `riskmodules_cashflow` |
| GET | `/riskmodules/{address}/gwp/` | `riskmodules_gwp` |
| GET | `/riskmodules/{address}/gwp_history/` | `riskmodules_gwp_history` |
| GET | `/riskmodules/{address}/matured_surplus/` | `riskmodules_matured_surplus` |
| GET | `/riskmodules/{address}/matured_surplus_history/` | `riskmodules_matured_surplus_history` |
| GET | `/riskmodules/{address}/scr/` | `riskmodules_scr` |
| GET | `/riskmodules/{address}/scr_history/` | `riskmodules_scr_history` |
| GET | `/riskmodules/{address}/surplus/` | `riskmodules_surplus` |
| GET | `/riskmodules/{address}/surplus_history/` | `riskmodules_surplus_history` |
| GET | `/riskmodules/{address}/wonpremiumsinout/` | `riskmodules_wonpremiumsinout` |


## wallet

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/wallet/` | `wallet_list` |
| POST | `/wallet/` | `wallet_create` |
| POST | `/wallet/access_token/` | `wallet_access_token` |
| POST | `/wallet/webhook/` | `wallet_webhook` |
| GET | `/wallet/{address}/` | `wallet_read` |
| PUT | `/wallet/{address}/` | `wallet_update` |
| PATCH | `/wallet/{address}/` | `wallet_partial_update` |
| DELETE | `/wallet/{address}/` | `wallet_delete` |
| POST | `/wallet/{address}/refresh/` | `wallet_refresh` |

# Citations

[1] [Offchain API OpenAPI specification](../assets/openapi/offchain-api.yaml)
