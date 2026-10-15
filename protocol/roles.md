---
type: Concept
title: Roles and permissions
description: The protocol manages permissions through an AccessManager contract, following the Access Managed Proxy pattern.
tags:
- smart-contracts
- roles
- governance
timestamp: '2026-09-22T00:00:00+00:00'
---

# Roles and permissions

The protocol uses the _Access Managed Proxy_ design pattern. Under this design pattern, the access control logic of permissioned methods is not defined in the code with modifiers (like `onlyOwner` or `onlyRole`). Instead, the contracts are deployed behind an [AccessManagedProxy](https://github.com/ensuro/access-managed-proxy) that delegates the access control configuration to an [AccessManager](https://docs.openzeppelin.com/contracts/5.x/api/access#AccessManager) contract.

A single [AccessManager](../reference/accessmanager.md) stores, for each target contract and function, the role required to call it, together with the accounts that hold each role and the execution delay that applies to them.

## Role admins

Role admins are the roles allowed to grant and revoke other roles.

| Role | Held by | Delay | Purpose |
| --- | --- | --- | --- |
| ADMIN_ROLE | ADMINS_V3 | 4 days | Administers the protocol's critical roles (`LEVEL1_ROLE`, `LEVEL2_ROLE`, and others). |
| ADMIN_OPERATIVE_ROLE | LOW_RISK_V3, ADMINS_V3 | — | Administers the operative roles, which require a faster setup. |

## Protocol roles

These roles control the protocol's configuration. They are granted to the governing multisigs with an execution delay.

| Role | Held by | Delay | Purpose | Examples of accessible methods |
| --- | --- | --- | --- | --- |
| LEVEL1_ROLE | ADMINS_V3 | 4 days | Critical and infrequent operations. | `upgradeToAndCall`, `setTreasury`, `addComponent`, `removeComponent`, `setYieldVault`, `setWhitelist`, `setCooler`, `setUnderwriter`, `setWallet`, `addStrategy`, `removeStrategy` |
| LEVEL2_ROLE | ADMINS_V3 | 18 hours | Parameter changes that don't alter the protocol's structure. | `setParam`, `setExposureLimit`, `setDeficitRatio`, `setLoanLimits`, `withdrawWonPremiums`, `setCooldownPeriod` |
| GUARDIAN_ROLE | LOW_RISK_V3 | — | Emergency operations to protect the protocol in case of attacks or hacks. | `pause`, `unpause`, `changeComponentStatus` |

The `GUARDIAN_ROLE` also acts as the guardian of both `LEVEL1_ROLE` and `LEVEL2_ROLE`: it can cancel scheduled operations before their delay expires, preventing them from being executed.

## Operative roles

These roles are used by Ensuro's team and automated processes to perform routine operations. They are administered by the `ADMIN_OPERATIVE_ROLE`.

| Role | Held by | Purpose |
| --- | --- | --- |
| YIELD_REBALANCER_ROLE | TREASURY_PETTY_CASH, ADMINS_V3, MIMIC_SMART_ACCOUNT | Moves funds between the liquid and invested states of the reserves (`depositIntoYieldVault`, `withdrawFromYieldVault`). |
| MSV_REBALANCER_ROLE | DEPLOYER_V3, TREASURY_PETTY_CASH, ADMINS_V3 | Rebalances the multi-strategy vault (`rebalance`). |
| WHITELISTER_ROLE | DEPLOYER_V3, RELAYER_BRIDGE, TREASURY_PETTY_CASH | Adds addresses to the LP whitelist (`whitelistAddress`). |
| RECORD_EARNINGS_ROLE | TREASURY_PETTY_CASH, MIMIC_SMART_ACCOUNT | Records the earnings of the reserves (`recordEarnings`). |
| REPAY_LOANS_ROLE | RELAYER_BRIDGE | Triggers loan repayment taken by the premiums accounts (`repayLoans`). |
| CFL_TREASURY_REPAY_ROLE | TREASURY_PETTY_CASH, TREASURY_V3 | Repays the cash-flow lender's debt (`repayDebt`). |
| CFL_TREASURY_ROLE | ADMINS_V3, TREASURY_V3 | Cashes out payouts from the cash-flow lender (`cashOutPayouts`). |
| PA_GRANTOR_ROLE | TREASURY_V3, TREASURY_PETTY_CASH | Sends grants to the premiums accounts (`receiveGrant`). Used for adjustments or other special cases. |
| OFFCHAIN_ROLE | OFFCHAIN_EOA, CFL_GATEWAY_ACCOUNT_EP | Batches calls to the PolicyPool (`multicall`). Used for expiring multiple policies at once. |

The accounts referenced here (`ADMINS_V3`, `LOW_RISK_V3`, `TREASURY_V3`, etc.) are described in the [Governance](governance.md) page.
