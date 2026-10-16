---
type: Smart Contract
title: FullTrustedUW
description: Underwriter that just decodes what it receives; access validations are done on the RiskModule methods.
tags:
- smart-contracts
- risk-modules
timestamp: '2026-10-16T00:00:00+00:00'
---

# FullTrustedUW

This is an implementation of the [IUnderwriter](overview.md) interface that just decodes what it receives with `abi.decode` and returns it, without any pricing computation or signature validation.

The access validations are expected to be done on the [RiskModule](../riskmodule.md) methods: only callers authorized to call `newPolicy`, `replacePolicy` or `cancelPolicy` can use this underwriter.

> **Source:** [FullTrustedUW.sol](https://github.com/ensuro/ensuro/blob/main/contracts/underwriters/FullTrustedUW.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/underwriters/FullTrustedUW](https://ensuro.readthedocs.io/en/latest/underwriters/FullTrustedUW/)

## External Methods

### priceNewPolicy

```solidity
function priceNewPolicy(address rm, bytes calldata inputData) external pure returns (uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, uint96 internalId, Policy.Params memory params)
```

Decodes `inputData` as `(uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, uint96 internalId, Policy.Params params)`.

### pricePolicyReplacement

```solidity
function pricePolicyReplacement(address rm, bytes calldata inputData) external pure returns (Policy.PolicyData memory oldPolicy, uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, uint96 internalId, Policy.Params memory params)
```

Decodes `inputData` as `(Policy.PolicyData oldPolicy, uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, uint96 internalId, Policy.Params params)`.

### pricePolicyCancellation

```solidity
function pricePolicyCancellation(address rm, bytes calldata inputData) external view returns (Policy.PolicyData memory policyToCancel, uint256 purePremiumRefund, uint256 jrCocRefund, uint256 srCocRefund)
```

Decodes `inputData` as `(Policy.PolicyData policyToCancel, uint256 purePremiumRefund, uint256 jrCocRefund, uint256 srCocRefund)`. A refund of `type(uint256).max` is interpreted as the full non-accrued cost of capital.
