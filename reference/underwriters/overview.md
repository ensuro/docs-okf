---
type: Smart Contract
title: IUnderwriter
description: Interface for contracts that validate policy inputs and convert them into the fields required to create a policy.
tags:
- smart-contracts
- risk-modules
timestamp: '2026-10-16T00:00:00+00:00'
---

# IUnderwriter

The pricing responsibility of a [RiskModule](../riskmodule.md) — including pricing and validating new policies, replacements and cancellations — is delegated to an _Underwriter_ contract plugged into it. `IUnderwriter` defines the interface of these contracts.

An underwriter receives the raw `inputData` sent by the caller, decodes it, validates it (possibly checking a signature) and returns the fields required to build the policy. The concrete RiskModule then submits the result to the [PolicyPool](../policypool.md).

> **Source:** [IUnderwriter.sol](https://github.com/ensuro/ensuro/blob/main/contracts/interfaces/IUnderwriter.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/interfaces/IUnderwriter](https://ensuro.readthedocs.io/en/latest/interfaces/IUnderwriter/)

## External Methods

### priceNewPolicy

```solidity
function priceNewPolicy(address rm, bytes calldata inputData) external view returns (uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, uint96 internalId, Policy.Params memory params)
```

Prices a new policy request for RiskModule `rm`.

| Name      | Type  | Description                                         |
| --------- | ----- | --------------------------------------------------- |
| rm        | address | The RiskModule address requesting pricing.        |
| inputData | bytes | Opaque payload consumed by the implementation.      |

### pricePolicyReplacement

```solidity
function pricePolicyReplacement(address rm, bytes calldata inputData) external view returns (Policy.PolicyData memory oldPolicy, uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, uint96 internalId, Policy.Params memory params)
```

Prices a policy replacement request for RiskModule `rm`. Returns the policy being replaced together with the fields of the replacement policy.

### pricePolicyCancellation

```solidity
function pricePolicyCancellation(address rm, bytes calldata inputData) external view returns (Policy.PolicyData memory policyToCancel, uint256 purePremiumRefund, uint256 jrCocRefund, uint256 srCocRefund)
```

Prices a policy cancellation request for RiskModule `rm`. Returns the policy to cancel and the amounts to refund from the pure premium and the junior/senior cost of capital.
