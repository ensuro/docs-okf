---
type: Smart Contract
title: WEToken
description: Non-rebasing ERC-4626 wrapper for an Ensuro eToken with static balances.
tags:
- smart-contracts
- liquidity
timestamp: '2026-10-16T00:00:00+00:00'
---

# WEToken

This contract wraps the rebasing [eToken](etoken.md) into a non-rebasing ERC-4626 vault token with static balances. 1 WEToken (share) is worth 1 eToken at the eToken's initial scale; as the eToken accrues yield, each WEToken becomes redeemable for more eTokens.

It can optionally freeze accounts that the underlying eToken's whitelist doesn't allow to send transfers. When the eToken has a [whitelist](ilpwhitelist/overview.md), the frozen state acts as a cache of the whitelist decision, and this contract's address must be whitelisted.

> **Source:** [WEToken.sol](https://github.com/ensuro/ensuro/blob/main/contracts/WEToken.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/WEToken](https://ensuro.readthedocs.io/en/latest/WEToken/)

## Events

### AccountFrozen

```solidity
event AccountFrozen(address indexed account, bool frozen)
```

Event emitted when an account is frozen or unfrozen.

| Name    | Type    | Description                                  |
| ------- | ------- | -------------------------------------------- |
| account | address | The account that was frozen or unfrozen.     |
| frozen  | bool    | `true` if frozen, `false` if unfrozen.       |

## External Methods

### deposit / mint / withdraw / redeem

The contract implements the standard ERC-4626 methods to wrap eTokens into WETokens:

```solidity
function deposit(uint256 assets, address receiver) external returns (uint256)
function mint(uint256 shares, address receiver) external returns (uint256)
function withdraw(uint256 assets, address receiver, address owner) external returns (uint256)
function redeem(uint256 shares, address receiver, address owner) external returns (uint256)
```

Deposits transfer eTokens from the caller and mint WETokens; withdrawals and redemptions burn WETokens and transfer the corresponding eTokens. Positions owned by a frozen account can't be moved (transfers and burns are blocked).

### setFrozen

```solidity
function setFrozen(address user, bool frozen_) external
```

Freezes or unfreezes an account. When the eToken has a whitelist, the call is validated against it: freezing requires the whitelist to reject the user's send transfer, and unfreezing requires it to accept.

Some state is exposed through public getters: `freezer()` returns the authorized freezer (or `address(0)` for open-freeze mode) and `frozen(address)` returns whether an account is frozen.
