---
type: Smart Contract
title: ICooler
description: Optional component that defines the cooldown required before withdrawing funds from an eToken.
tags:
- smart-contracts
- liquidity
timestamp: '2026-10-16T00:00:00+00:00'
---

# ICooler

This is an optional component. If present, it controls the cooldown period that must elapse before funds can be withdrawn from an eToken.

Each _eToken_ has a `cooler` parameter that, if not null, points to a contract following this interface. Several eTokens can share the same cooler contract. When a cooler is set, withdrawals can't be executed immediately: they must be scheduled and then executed once the cooldown period has passed.

> **Source:** [ICooler.sol](https://github.com/ensuro/ensuro/blob/main/contracts/interfaces/ICooler.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/interfaces/ICooler](https://ensuro.readthedocs.io/en/latest/interfaces/ICooler/)

## External Methods

### pendingWithdrawals

```solidity
function pendingWithdrawals(IEToken eToken) external view returns (uint256)
```

Returns the amount of pending (scheduled) withdrawals for a given eToken.

| Name   | Type    | Description                       |
| ------ | ------- | --------------------------------- |
| eToken | IEToken | The eToken contract to query.     |

| Name | Type    | Description                           |
| ---- | ------- | ------------------------------------- |
| \[0] | uint256 | The amount in `currency()` pending.   |

### cooldownPeriod

```solidity
function cooldownPeriod(IEToken eToken, address owner, uint256 amount) external view returns (uint40)
```

Returns the cooldown period in seconds required for a withdrawal in a given eToken.

| Name   | Type    | Description                              |
| ------ | ------- | ---------------------------------------- |
| eToken | IEToken | The eToken contract to query.            |
| owner  | address | The owner of the tokens to withdraw.     |
| amount | uint256 | The amount requested to withdraw.        |

| Name | Type   | Description                    |
| ---- | ------ | ------------------------------ |
| \[0] | uint40 | The cooldown period in seconds |
