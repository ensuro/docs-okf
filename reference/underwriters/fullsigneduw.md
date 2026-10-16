---
type: Smart Contract
title: FullSignedUW
description: Underwriter that decodes the input and requires it to be signed by an authorized account.
tags:
- smart-contracts
- risk-modules
timestamp: '2026-10-16T00:00:00+00:00'
---

# FullSignedUW

This is an implementation of the [IUnderwriter](overview.md) interface that decodes what it receives with `abi.decode` and checks that the input was signed by an authorized account.

The input is `payload || signature`, where the signature is a 65-byte ECDSA signature. The contract recovers the signer and verifies through the RiskModule's AccessManager that the signer has the corresponding permission (`FULL_PRICE_NEW_POLICY`, `FULL_PRICE_REPLACE_POLICY` or `FULL_PRICE_CANCEL_POLICY`). This allows risk partners to price policies off-chain and let anyone submit them on-chain.

> **Source:** [FullSignedUW.sol](https://github.com/ensuro/ensuro/blob/main/contracts/underwriters/FullSignedUW.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/underwriters/FullSignedUW](https://ensuro.readthedocs.io/en/latest/underwriters/FullSignedUW/)

## External Methods

### priceNewPolicy

```solidity
function priceNewPolicy(address rm, bytes calldata inputData) external view returns (uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, uint96 internalId, Policy.Params memory params)
```

Validates the appended signature against `rm` and decodes the payload.

### pricePolicyReplacement

```solidity
function pricePolicyReplacement(address rm, bytes calldata inputData) external view returns (Policy.PolicyData memory oldPolicy, uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, uint96 internalId, Policy.Params memory params)
```

Validates the appended signature against `rm` and decodes the payload (old policy and replacement fields).

### pricePolicyCancellation

```solidity
function pricePolicyCancellation(address rm, bytes calldata inputData) external view returns (Policy.PolicyData memory policyToCancel, uint256 purePremiumRefund, uint256 jrCocRefund, uint256 srCocRefund)
```

Validates the appended signature against `rm` and decodes the payload. A refund of `type(uint256).max` is interpreted as the full non-accrued cost of capital.
