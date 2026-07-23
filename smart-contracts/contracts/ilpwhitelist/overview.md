---
type: Smart Contract
title: ILPWhitelist
description: Optional component that controls which liquidity providers can deposit into an eToken.
tags:
- smart-contracts
- whitelist
timestamp: '2022-09-28T10:10:54-03:00'
---

# ILPWhitelist

This is an optional component. If present it controls which Liquidity Providers can deposit or transfer their _eTokens_.

Each _eToken_ has a `whitelist` parameter that if not null, points to a contract following this interface. Several _eTokens_ can share the same whitelist contract or they can different ones.

## External Methods

### acceptsDeposit

```solidity
function acceptsDeposit(contract IEToken etoken, address provider, uint256 amount) external view returns (bool)
```

Indicates whether or not a liquidity provider can do a deposit in an eToken.

| Name     | Type             | Description                                                          |
| -------- | ---------------- | -------------------------------------------------------------------- |
| etoken   | contract IEToken | The eToken (see {EToken}) where the provider wants to deposit money. |
| provider | address          | The address of the liquidity provider (user) that wants to deposit   |
| amount   | uint256          | The amount of the deposit                                            |

| Name | Type | Description                                          |
| ---- | ---- | ---------------------------------------------------- |
| [0]  | bool | true if `provider` deposit is accepted, false if not |

### acceptsTransfer

```solidity
function acceptsTransfer(contract IEToken etoken, address providerFrom, address providerTo, uint256 amount) external view returns (bool)
```

Indicates whether or not the eTokens can be transferred from `providerFrom` to `providerTo`

| Name         | Type             | Description                                                            |
| ------------ | ---------------- | ---------------------------------------------------------------------- |
| etoken       | contract IEToken | The eToken (see {EToken}) that the LPs have the intention to transfer. |
| providerFrom | address          | The current owner of the tokens                                        |
| providerTo   | address          | The destination of the tokens if the transfer is accepted              |
| amount       | uint256          | The amount of tokens to be transferred                                 |

| Name | Type | Description                                               |
| ---- | ---- | --------------------------------------------------------- |
| [0]  | bool | true if the transfer operation is accepted, false if not. |
