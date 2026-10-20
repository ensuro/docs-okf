---
type: Smart Contract
title: ILPWhitelist
description: Optional component that controls which liquidity providers can deposit into an eToken.
tags:
- smart-contracts
- whitelist
timestamp: '2026-10-16T00:00:00+00:00'
---

# ILPWhitelist

This is an optional component. If present it controls which Liquidity Providers can deposit, withdraw or transfer their _eTokens_.

Each _eToken_ has a `whitelist` parameter that if not null, points to a contract following this interface. Several _eTokens_ can share the same whitelist contract or they can different ones.

> **Source:** [ILPWhitelist.sol](https://github.com/ensuro/ensuro/blob/main/contracts/interfaces/ILPWhitelist.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/interfaces/ILPWhitelist](https://ensuro.readthedocs.io/en/latest/interfaces/ILPWhitelist/)

## External Methods

### acceptsOperation

```solidity
function acceptsOperation(IEToken etoken, address provider, Operation operation) external view returns (bool)
```

Returns whether `provider` is allowed to perform `operation` (one of `deposit`, `withdraw`, `sendTransfer`, `receiveTransfer`) on `etoken`.

| Name      | Type      | Description                                                          |
| --------- | --------- | -------------------------------------------------------------------- |
| etoken    | IEToken   | The eToken (see [EToken](../etoken.md)) where the operation is checked. |
| provider  | address   | The address of the liquidity provider (user).                        |
| operation | Operation | The operation to check.                                              |

| Name | Type | Description                                          |
| ---- | ---- | ---------------------------------------------------- |
| \[0] | bool | true if the operation is accepted, false if not.     |

### acceptsDeposit

```solidity
function acceptsDeposit(IEToken etoken, address provider, uint256 amount) external view returns (bool)
```

Indicates whether or not a liquidity provider can do a deposit in an eToken.

| Name     | Type    | Description                                                          |
| -------- | ------- | -------------------------------------------------------------------- |
| etoken   | IEToken | The eToken (see [EToken](../etoken.md)) where the provider wants to deposit money. |
| provider | address | The address of the liquidity provider (user) that wants to deposit   |
| amount   | uint256 | The amount of the deposit                                            |

| Name | Type | Description                                          |
| ---- | ---- | ---------------------------------------------------- |
| \[0] | bool | true if `provider` deposit is accepted, false if not |

### acceptsWithdrawal

```solidity
function acceptsWithdrawal(IEToken etoken, address provider, uint256 amount) external view returns (bool)
```

Indicates whether or not a liquidity provider can withdraw from an eToken.

| Name     | Type    | Description                                                          |
| -------- | ------- | -------------------------------------------------------------------- |
| etoken   | IEToken | The eToken (see [EToken](../etoken.md)) where the provider wants to withdraw money. |
| provider | address | The address of the liquidity provider (user) that wants to withdraw  |
| amount   | uint256 | The amount of the withdrawal                                         |

| Name | Type | Description                                            |
| ---- | ---- | ------------------------------------------------------ |
| \[0] | bool | true if `provider` withdrawal is accepted, false if not |

### acceptsTransfer

```solidity
function acceptsTransfer(IEToken etoken, address providerFrom, address providerTo, uint256 amount) external view returns (bool)
```

Indicates whether or not the eTokens can be transferred from `providerFrom` to `providerTo`.

| Name         | Type    | Description                                                            |
| ------------ | ------- | ---------------------------------------------------------------------- |
| etoken       | IEToken | The eToken (see [EToken](../etoken.md)) that the LPs have the intention to transfer. |
| providerFrom | address | The current owner of the tokens                                        |
| providerTo   | address | The destination of the tokens if the transfer is accepted              |
| amount       | uint256 | The amount of tokens to be transferred                                 |

| Name | Type | Description                                               |
| ---- | ---- | --------------------------------------------------------- |
| \[0] | bool | true if the transfer operation is accepted, false if not. |
