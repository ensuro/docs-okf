---
type: Concept
title: Governance
description: Ensuro's governance relies on Safe multisigs and the AccessManager's timelocks to provide transparency and security for the protocol.
tags:
- smart-contracts
- governance
timestamp: '2026-09-22T00:00:00+00:00'
---

# Governance

Ensuro's governance relies on [Safe](https://safe.global/) multisigs and the execution delays enforced by the [AccessManager](../reference/accessmanager.md) to provide transparency and security for the protocol.

No major changes to the protocol will ever be made without first going through an internal vetting process that requires sign-off from several senior staff members and a public announcement with an appropriate warning period.

## Multisigs

| Name | Address | Description |
| --- | --- | --- |
| ADMINS_V3 | [0xB809C75914c62DA604B1f6F1C4300bAc91797Aa1](https://etherscan.io/address/0xB809C75914c62DA604B1f6F1C4300bAc91797Aa1) | Main admin multisig. A 3/4 Safe controlled by Ensuro. Holds `ADMIN_ROLE`, `LEVEL1_ROLE` and `LEVEL2_ROLE`. |
| LOW_RISK_V3 | [0x5848A5a692373CAd6FAAbB7b96EF43Ec1a386867](https://etherscan.io/address/0x5848A5a692373CAd6FAAbB7b96EF43Ec1a386867) | Emergency multisig with the same signers as ADMINS_V3 but a threshold of 2. Holds `GUARDIAN_ROLE` and other non-critical roles. |
| TREASURY_V3 | [0x03Dabf3315C794807A27516d7440F41B427eD40f](https://etherscan.io/address/0x03Dabf3315C794807A27516d7440F41B427eD40f) | Main treasury multisig (3/4 Safe controlled by Ensuro). Receives Ensuro fees and executes other treasury related operations. |
| TREASURY_PETTY_CASH | [0x3385a4dcfEc931DCFD185616b1323ABf7120674B](https://etherscan.io/address/0x3385a4dcfEc931DCFD185616b1323ABf7120674B) | Petty cash multisig requiring 2/6 signatures. Used for day-to-day operative roles. |
| RECOVERY_MULTISIG | [0xA6CA4bFF8F0197D8d675B585d8aD12165Cebb5cB](https://etherscan.io/address/0xA6CA4bFF8F0197D8d675B585d8aD12165Cebb5cB) | Recovery multisig. 4/8 multisig with Safe account recovery rights (delays of +21 days). |

## Operative accounts

Besides the multisigs, several accounts are used by Ensuro's team and automated processes to hold the [operative roles](roles.md#operative-roles):

| Name | Address | Description |
| --- | --- | --- |
| MIMIC_SMART_ACCOUNT | [0x85E8647d9228196A3D6d89e8c9Bbe096276500E4](https://etherscan.io/address/0x85E8647d9228196A3D6d89e8c9Bbe096276500E4) | Smart account operated with [Mimic Protocol](https://mimic.fi/) to execute automations and scheduled operations. |
| DEPLOYER_V3 | [0x0EF551eA2291ebC83EF6ba1B9d7c3f5847fa9b0a](https://etherscan.io/address/0x0EF551eA2291ebC83EF6ba1B9d7c3f5847fa9b0a) | Deployer account used for contract deployments, initial configuration and minor operative tasks. |
| RELAYER_BRIDGE | [0xB8aCc68DAEDb5C131870D71f83d2FF7BFc89bFb7](https://etherscan.io/address/0xB8aCc68DAEDb5C131870D71f83d2FF7BFc89bFb7) | Relayer account used for relaying risk partners operations and other operative tasks. |
| OFFCHAIN_EOA | [0xF38785DFF30B39aB5fF4afd58a6E4DCD87D34553](https://etherscan.io/address/0xF38785DFF30B39aB5fF4afd58a6E4DCD87D34553) | Offchain account used by Ensuro's back-end to expire policies (uses `multicall`). |
| CFL_GATEWAY_ACCOUNT_EP | [0x7529ABff0F8665A4E7FcD532d0f528090435D10E](https://etherscan.io/address/0x7529ABff0F8665A4E7FcD532d0f528090435D10E) | Account-abstraction gateway that forwards operations to the cash-flow lender. Gas-optimized smart account that follows entrypoint interface. |

## Timelocks and delays

The AccessManager enforces an execution delay on the roles it grants. A change must first be scheduled, and it can only be executed once the corresponding delay has elapsed.

| Role | Delay |
| --- | --- |
| ADMIN_ROLE | 4 days |
| LEVEL1_ROLE | 4 days |
| LEVEL2_ROLE | 18 hours |

## Transaction signing

All members of the multisigs must use secure hardware wallets and isolated environments for signing transactions. This is audited internally as part of our compliance program with the Bermuda Monetary Authority.

Transactions are signed using [Safe Wallet Multisigs](https://safe.global/), as described above.

All critical transactions, such as upgrades or major parameter changes, must be signed by at least 3 different senior staff members.
