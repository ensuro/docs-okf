---
type: Smart Contract
title: RiskModule
description: Contract that manages the insurance products of the protocol, responsible for injecting policies and policy resolution.
tags:
- smart-contracts
- core
- risk-modules
timestamp: '2026-10-16T00:00:00+00:00'
---

# RiskModule

This contract allows risk partners and customers to interact with the protocol. It keeps the configuration of a single insurance product and is responsible for injecting policies and policy resolution.

The pricing responsibility — including validating and pricing new policies, replacements and cancellations — is delegated to an [Underwriter](underwriters/overview.md) contract plugged into the RiskModule. To create a new policy, the RiskModule is called with the raw input; it forwards it to the underwriter, builds the Policy object with the resulting fields, and submits it to the [PolicyPool](policypool.md).

> **Source:** [RiskModule.sol](https://github.com/ensuro/ensuro/blob/main/contracts/RiskModule.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/RiskModule](https://ensuro.readthedocs.io/en/latest/RiskModule/)

## Parameters

| Field       | Type         | Description                                                                                        |
| ----------- | ------------ | -------------------------------------------------------------------------------------------------- |
| underwriter | address (IUnderwriter) | Contract in charge of decoding, validating and pricing the policies. See [IUnderwriter](underwriters/overview.md). |
| wallet      | address      | The wallet that receives the partner commission of the policies created by this risk module.       |

## External Methods

### newPolicy

```solidity
function newPolicy(bytes calldata inputData, address onBehalfOf) public returns (Policy.PolicyData memory policy)
```

Creates a new policy. The premium is paid by `msg.sender` and the policy is owned by `onBehalfOf`.

| Name       | Type    | Description                                                                              |
| ---------- | ------- | ---------------------------------------------------------------------------------------- |
| inputData  | bytes   | Input data decoded and priced by the underwriter to build the policy.                    |
| onBehalfOf | address | The address that will be the owner of the created policy.                                |

### newPolicies

```solidity
function newPolicies(bytes[] calldata inputData, address onBehalfOf) external
```

Creates several policies in a single call. The premium is paid by `msg.sender` and all the policies are owned by `onBehalfOf`.

### replacePolicy

```solidity
function replacePolicy(bytes calldata inputData) external returns (Policy.PolicyData memory policy)
```

Replaces an existing policy with a new one, with the same owner. The underwriter decodes both the old policy and the parameters for the new policy.

### cancelPolicy

```solidity
function cancelPolicy(bytes calldata inputData) external
```

Cancels a policy, giving back all (or part) of the pure premium and the non-accrued cost of capital.

### resolvePolicy

```solidity
function resolvePolicy(Policy.PolicyData calldata policy, uint256 payout) external
```

Resolves a policy. If `payout > 0`, the amount is paid to the policyholder. The payout must be less than or equal to `policy.payout`.

| Name   | Type               | Description                                          |
| ------ | ------------------ | ---------------------------------------------------- |
| policy | Policy.PolicyData  | The policy previously created (from the `NewPolicy` event). |
| payout | uint256            | The payout to transfer to the policy holder.         |

### getMinimumPremium

```solidity
function getMinimumPremium(uint256 payout, uint256 lossProb, uint40 start, uint40 expiration, Policy.Params memory p) public pure returns (uint256)
```

Returns the minimum premium computed by the [Policy](../protocol/policy.md) library for the given policy parameters.
