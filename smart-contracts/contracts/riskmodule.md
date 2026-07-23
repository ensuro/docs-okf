---
type: Smart Contract
title: RiskModule
description: Abstract contract that manages the insurance products of the protocol, responsible for pricing and resolution of policies.
tags:
- smart-contracts
- core
- risk-modules
timestamp: '2026-07-20T21:03:37+00:00'
---

# RiskModule

> **Note:** This page is a placeholder. In the new version of the protocol there is a single risk
> module implementation, and this documentation will be rewritten accordingly. The content below
> summarizes the legacy abstract `RiskModule` contract that the former implementations
> (Trustful, SignedQuote, SignedBucket, FlightDelay and Price risk modules) extended.

Risk Module is an abstract contract that needs to be implemented with specific policies for the main responsibilities of the contract: pricing and resolution.

The contract also stores several parameters that are used for the creation and validation of the policies.

## **Roles**

The specific roles and functions of the contract are as follows:

| Role | Global* | Description | Methods Accessible |
| --- | --- | --- | --- |
| LEVEL1_ROLE | ✓ | High impact changes like upgrades or other critical operations. | [setParam](#setting-parameters): Set parameters. |
| LEVEL2_ROLE | ✓ | Mid-impact changes like changing some parameters. | [setParam](#setting-parameters): Set parameters. |
| LEVEL3_ROLE | ✓ | Low-impact changes like changing some parameters up to given percentage (tweaks). | [setParam](#setting-parameters): Set parameters. |
| RM_PROVIDER | ✗ | Manages the risk module. | setWallet: Sets the risk module wallet. |

( \* ) Global means that the role can be delegated to a user at the protocol level (for all components) or only for a specific component. Non-global roles can only be granted for a specific component.

## Parameters

These parameters are managed and adjusted by the protocol governance. Some come from business decisions and others are quantitative analysis decisions.

| Field              | Type             | Description                                                                                                                                                                    |
| ------------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| moc                | uint256 (wad)    | Margin of Conservatism. A factor used to scale the expected losses calculated as `payout * lossProb`                                                                           |
| jrCollRatio        | uint256 (wad)    | The collateralization ratio up to the junior eToken (see [Solvency Breakdown](../policy.md#solvency-breakdown))                                                             |
| collRatio          | uint256 (wad)    | The overall collateralization ratio (see [Solvency Breakdown](../policy.md#solvency-breakdown))                                                                             |
| ensuroPpFee        | uint256 (wad)    | Percentage applied to the pure premium used to compute the [Ensuro Commision](../policy.md#ensuro-commission).                                                              |
| ensuroCocFee       | uint256 (wad)    | Percentage applied to the cost of capital used to compute the [Ensuro Commision](../policy.md#ensuro-commission).                                                           |
| jrRoc              | uint256 (wad)    | Annualized return expected by Junior eToken liquidity providers for the capital exposed to these risks. See [more details](../policy.md#junior-and-senior-cost-of-capital). |
| srRoc              | uint256 (wad)    | Annualized return expected by Senior eToken liquidity providers for the capital exposed to these risks. See [more details](../policy.md#junior-and-senior-cost-of-capital). |
| maxPayoutPerPolicy | uint256 (amount) | The maximum payout that's allowed as payout for each individual policy of this risk module.                                                                                    |
| exposureLimit      | uint256 (amount) | The limit on the cumulative exposure of all the active policies of this module.                                                                                                |
| maxDuration        | uint256(hours)   | The maximum duration of the policies (in hours).                                                                                                                               |

### Packed parameters

To save gas, the parameters are stored in a packed struct that fits in 256bits (a _word_ in the EVM). This is not visible externally, but put's limits on the precision of the parameters. The _wad_ ones, have 4 decimals as precision, so 1.12345 will be truncated to 1.1234. _maxPayoutPerPolicy_ has a precision of two decimals, and _exposureLimit_ 0 decimals.

## Internal methods

### \_newPolicy

```solidity
function _newPolicy(uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, address payer, address onBehalfOf, uint96 internalId) internal returns (struct Policy.PolicyData)
```

Called from child contracts to create policies (after they validated the pricing)

| Name       | Type    | Description                                                                       |
| ---------- | ------- | --------------------------------------------------------------------------------- |
| payout     | uint256 | The exposure (maximum payout) of the policy                                       |
| premium    | uint256 | The premium that will be paid by the policyHolder                                 |
| lossProb   | uint256 | The probability of having to pay the maximum payout (wad)                         |
| expiration | uint40  | The expiration of the policy (timestamp)                                          |
| payer      | address | The account that pays for the premium                                             |
| onBehalfOf | address | The policy holder                                                                 |
| internalId | uint96  | An id that's unique within this module and it will be used to identify the policy |

## External Methods

### releaseExposure

```solidity
function releaseExposure(uint256 payout) external
```

Called when a policy expires or is resolved to update the exposure.

Requirements:

* Must be called by `policyPool()`

| Name   | Type    | Description                                 |
| ------ | ------- | ------------------------------------------- |
| payout | uint256 | The exposure (maximum payout) of the policy |

### Setting parameters

Usually, **LEVEL1\_ROLE, LEVEL2\_ROLE** or **LEVEL3\_ROLE** is requested for performing operations that change numerical parameters of the components. Both global and component role are accepted. If the user has **LEVEL3\_ROLE** the changes might be restricted to small tweaks.
