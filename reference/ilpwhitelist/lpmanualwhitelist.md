---
type: Smart Contract
title: LPManualWhitelist
description: Implementation of the ILPWhitelist interface that stores, per provider, whether each operation is whitelisted, with configurable defaults.
tags:
- smart-contracts
- whitelist
timestamp: '2026-10-16T00:00:00+00:00'
---

# LPManualWhitelist

This is an implementation of the [ILPWhitelist](overview.md) interface that stores manually, for each provider, the status of each operation (deposit, withdraw, send transfer and receive transfer). Each operation can be `whitelisted`, `blacklisted` or `undefined` (meaning "use the default"). The defaults are stored at the `address(0)` entry.

To whitelist an address, an authorized user calls `whitelistAddress(provider, newStatus)`.

> **Source:** [LPManualWhitelist.sol](https://github.com/ensuro/ensuro/blob/main/contracts/LPManualWhitelist.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/LPManualWhitelist](https://ensuro.readthedocs.io/en/latest/LPManualWhitelist/)

## Parameters

The default status (`address(0)` entry) is used for every provider whose operation isn't explicitly set. Each of its fields takes one of `undefined`, `whitelisted` or `blacklisted`.

| Field           | Type           | Description                                          |
| --------------- | -------------- | ---------------------------------------------------- |
| deposit         | WhitelistOptions | Default status for deposits.                       |
| withdraw        | WhitelistOptions | Default status for withdrawals.                    |
| sendTransfer    | WhitelistOptions | Default status for sending transfers.              |
| receiveTransfer | WhitelistOptions | Default status for receiving transfers.            |

## Events

### LPWhitelistStatusChanged

```solidity
event LPWhitelistStatusChanged(address provider, WhitelistStatus whitelisted)
```

Event emitted when the whitelist status for a provider (or the defaults entry at `address(0)`) is updated.

| Name        | Type             | Description                                                              |
| ----------- | ---------------- | ------------------------------------------------------------------------ |
| provider    | address          | The provider whose status was changed. `address(0)` denotes the defaults. |
| whitelisted | WhitelistStatus  | The new status stored for the provider.                                  |

## External Methods

### whitelistAddress

```solidity
function whitelistAddress(address provider, WhitelistStatus calldata newStatus) external
```

Sets a custom whitelist status for `provider`. Fields may be `undefined` to indicate "use defaults".

| Name      | Type            | Description                                                       |
| --------- | --------------- | ----------------------------------------------------------------- |
| provider  | address         | The LP address whose status will be updated. Must be non-zero.    |
| newStatus | WhitelistStatus | The status to store for `provider`.                               |

### getWhitelistDefaults

```solidity
function getWhitelistDefaults() external view returns (WhitelistStatus memory)
```

Returns the default whitelist status stored at the `address(0)` entry.

### Other methods

The `acceptsDeposit`, `acceptsWithdrawal`, `acceptsTransfer` and `acceptsOperation` methods are inherited from the [ILPWhitelist](overview.md) interface.
