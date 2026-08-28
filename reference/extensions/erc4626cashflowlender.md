---
type: Smart Contract
title: ERC4626CashFlowLender
description: Implements the ERC-4626 standard tracking how much liquidity was provided by each LP.
tags:
- smart-contracts
- extensions
timestamp: '2024-03-06T19:26:15+00:00'
---

# ERC4626CashFlowLender

Implements the ERC-4626 standard tracking how much liquidity was provided by each LP. The assets managed by the vault are a mix of liquid USDC + the `_debt` tracked by the CFL. The `_debt` can be negative, in that case, the CFL owes to the customer.

## **Roles**

The roles and functions of the contract are as follows:

| Role | Description | Methods Accessible |
| --- | --- | --- |
| CHANGE_RM_ROLE | Sets the risk module for the contract. | setRiskModule: Sets the risk module. |
| LP_ROLE | Manages withdrawing assets for LPs. | withdraws: Withdraws assets from the contract. |
| CUSTOMER_ROLE | Enables to cash out payouts. | [cashOutPayouts](erc4626cashflowlender.md#cashoutpayouts): Allows customers to cash out payouts. |
| BORROWER_ROLE | Borrows funds from the CFL. | [borrow](erc4626cashflowlender.md#borrow-1): Borrows funds. |
| POLICY_CREATOR_ROLE | Creates new policies. | [newPolicyWithRm](erc4626cashflowlender.md#newpolicywithrm): Creates a new policy with the specified risk module.<br>[newPoliciesInBatchWithRm](erc4626cashflowlender.md#newpoliciesinbatchwithrm): Creates multiple policies with the specified risk modules.<br>[newPolicy](erc4626cashflowlender.md#newpolicy): Creates a new policy.<br>[newPoliciesInBatch](erc4626cashflowlender.md#newpoliciesinbatch): Creates multiple policies. |
| RESOLVER_ROLE | Resolves policies. | [resolvePolicyFullPayout](erc4626cashflowlender.md#resolvepolicyfullpayout): Resolves a single policy with full payout<br>[resolvePoliciesInBatch](erc4626cashflowlender.md#resolvepoliciesinbatch): Resolves multiple policies |

This contract does not use Access Manager as an access control solution. It has its own [access control ](https://docs.openzeppelin.com/contracts/5.x/api/access)mechanism.

## Events

### DebtChanged

```solidity
event DebtChanged(int256 currentDebt)
```

Event emitted when the debt is changed. Could be positive or negative.

* When policy is created, the debt increases.
* When the customer borrows, the debt increases.
* When policy is resolved, the debt decreases.

| Name        | Type   | Description  |
| ----------- | ------ | ------------ |
| currentDebt | int256 | The new debt |

### RiskModuleChanged

```solidity
event RiskModuleChanged(contract SignedQuoteRiskModule newRiskModule)
```

Event emitted when the risk module changed.

| Name          | Type                                                            | Description         |
| ------------- | --------------------------------------------------------------- | ------------------- |
| newRiskModule | [SignedQuoteRiskModule](../riskmodule.md) | The new risk module |

### CashOutPayout

```solidity
event CashOutPayout(address destination, uint256 amount)
```

Event emitted when a customer cashes out a payout.

* When the customer cashes out, the debt increases.

| Name        | Type    | Description                                       |
| ----------- | ------- | ------------------------------------------------- |
| destination | address | The address where the payout will be transferred. |
| amount      | uint256 | The amount to pay                                 |

### Borrow

```solidity
event Borrow(address destination, uint256 amount)
```

Event emitted when a customer borrows funds.

| Name        | Type    | Description                                               |
| ----------- | ------- | --------------------------------------------------------- |
| destination | address | The address where the borrowed funds will be transferred. |
| amount      | uint256 | The amount of funds to be borrowed.                       |

## External Methods

### currentDebt

```solidity
function currentDebt() external view returns (int256)
```

Returns the current debt. If negative, the customer can cash out.

### cashOutPayouts

```solidity
function cashOutPayouts(uint256 amount, address destination) external
```

Requirements:

* Caller must have CUSTOMER\_ROLE
* The debt must be lower than the amount to pay.
* The contract's balance must be sufficient to pay the amount.

If the debt is negative, the customer can cash out. This function facilitates cashing out by customers, transferring the payout to the customer.

Emits:

* {CashOutPayout}

| Name        | Type    | Description                                       |
| ----------- | ------- | ------------------------------------------------- |
| amount      | uint256 | The amount to pay                                 |
| destination | address | The address where the payout will be transferred. |

### borrow

```solidity
function borrow(uint256 amount, address destination) external
```

Allows a customer to borrow funds.

This function facilitates borrowing by customers, increasing their debt and transferring the borrowed funds.

Requirements:

* Caller must have BORROWER\_ROLE.
* The contract's balance must be sufficient for the borrowing amount.

Emits:

* {Borrow}

| Name        | Type    | Description                                               |
| ----------- | ------- | --------------------------------------------------------- |
| amount      | uint256 | The amount of funds to be borrowed.                       |
| destination | address | The address where the borrowed funds will be transferred. |

### newPolicyWithRm

```solidity
function newPolicyWithRm(address riskModule_, uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, bytes32 policyData, uint256 bucketId, bytes32 quoteSignatureR, bytes32 quoteSignatureVS, uint40 quoteValidUntil) external returns (uint256 policyId)
```

Creates a new policy paid by this contract and increases the debt.

If it is a RiskModule without bucket, send type(uint256).max If it is a RiskModule with bucket, send the bucketId

Requirements:

* Caller must have POLICY\_CREATOR\_ROLE
* \_balance() >= than the amount of the premium

Emits:

* {PolicyPool.NewPolicy}
* {NewSignedPolicy}

| Name             | Type    | Description                                                                              |
| ---------------- | ------- | ---------------------------------------------------------------------------------------- |
| riskModule\_     | address | The address of the risk module that will be used to create the policy                    |
| payout           | uint256 | The exposure (maximum payout) of the policy                                              |
| premium          | uint256 | The premium that will be paid by the payer                                               |
| lossProb         | uint256 | The probability of having to pay the maximum payout (wad)                                |
| expiration       | uint40  | The expiration of the policy (timestamp)                                                 |
| policyData       | bytes32 | A hash of the private details of the policy. The last 96 bits will be used as internalId |
| bucketId         | uint256 | The bucketId. If the risk module doesn't use buckets, send type(uint256).max             |
| quoteSignatureR  | bytes32 | The signature of the quote. R component (EIP-2098 signature)                             |
| quoteSignatureVS | bytes32 | The signature of the quote. VS component (EIP-2098 signature)                            |
| quoteValidUntil  | uint40  | The expiration of the quote                                                              |

| Name | Type    | Description                          |
| ---- | ------- | ------------------------------------ |
| \[0] | uint256 | Returns the id of the created policy |

### newPoliciesInBatchWithRm

```solidity
function newPoliciesInBatchWithRm(address[] riskModules, uint256[] payout, uint256[] premium, uint256[] lossProb, uint40[] expiration, bytes32[] policyData, uint256[] bucketId, bytes32[] quoteSignatureR, bytes32[] quoteSignatureVS, uint40[] quoteValidUntil) external
```

Creates several policies paid by this contract and increases the debt.

If it is a RiskModule without bucket, send type(uint256).max If it is a RiskModule with bucket, send the bucketId

Requirements:

* Caller must have POLICY\_CREATOR\_ROLE
* \_balance() >= than the amount of the premium

Emits:

* {PolicyPool.NewPolicy}
* {NewSignedPolicy}

| Name             | Type       | Description                                                                               |
| ---------------- | ---------- | ----------------------------------------------------------------------------------------- |
| riskModules      | address\[] | The addresses of the risk module that will be used to create the policy                   |
| payout           | uint256\[] | The exposure (maximum payout) of each policy                                              |
| premium          | uint256\[] | The premium that will be paid by the payer                                                |
| lossProb         | uint256\[] | The probability of having to pay the maximum payout (wad)                                 |
| expiration       | uint40\[]  | The expiration of each policy (timestamp)                                                 |
| policyData       | bytes32\[] | A hash of the private details of each policy. The last 96 bits will be used as internalId |
| bucketId         | uint256\[] | The bucketId. If the risk module doesn't use buckets, send type(uint256).max              |
| quoteSignatureR  | bytes32\[] | The signature of each quote. R component (EIP-2098 signature)                             |
| quoteSignatureVS | bytes32\[] | The signature of each quote. VS component (EIP-2098 signature)                            |
| quoteValidUntil  | uint40\[]  | The expiration of each quote                                                              |

### newPolicy

```solidity
function newPolicy(uint256 payout, uint256 premium, uint256 lossProb, uint40 expiration, address, bytes32 policyData, bytes32 quoteSignatureR, bytes32 quoteSignatureVS, uint40 quoteValidUntil) external returns (uint256 policyId)
```

Creates a new policy paid by this contract and increases the debt. See [{SignedQuoteRiskModule.newPolicy}](../riskmodule.md)

Requirements:

* Caller must have POLICY\_CREATOR\_ROLE
* \_balance() >= than the amount of the premium

### newPoliciesInBatch

```solidity
function newPoliciesInBatch(uint256[] payout, uint256[] premium, uint256[] lossProb, uint40[] expiration, bytes32[] policyData, bytes32[] quoteSignatureR, bytes32[] quoteSignatureVS, uint40[] quoteValidUntil) external
```

Creates several policies paid by this contract and increases the debt. See [{SignedQuoteRiskModule.newPolicy}](../riskmodule.md)

Requirements:

* Caller must have POLICY\_CREATOR\_ROLE
* \_balance() >= than the amount of the premium

### resolvePolicy

```solidity
function resolvePolicy(struct Policy.PolicyData policy, uint256 payout) external
```

Resolves a policy with a payout. See [{SignedQuoteRiskModule.resolvePolicy}](../riskmodule.md)

Requirements:

* Caller must have RESOLVER\_ROLE

### resolvePolicyFullPayout

```solidity
function resolvePolicyFullPayout(struct Policy.PolicyData policy, bool customerWon) external
```

Resolves a policy with a payout that can be either 0 or the maximum payout of the policy. See [{SignedQuoteRiskModule.resolvePolicyFullPayout}](../riskmodule.md)

Requirements:

* Caller must have RESOLVER\_ROLE

### resolvePoliciesInBatch

```solidity
function resolvePoliciesInBatch(struct Policy.PolicyData[] policy, uint256[] payout) external
```

Resolves several policies paid by this contract and decreases the debt. See [{SignedQuoteRiskModule.resolvePolicy}](../riskmodule.md)

Requirements:

* Caller must have RESOLVER\_ROLE
