---
type: Smart Contract
title: Cooler
description: Implementation of the ICooler interface that holds the eTokens during the cooldown period, minting an NFT for each withdrawal request.
tags:
- smart-contracts
- liquidity
timestamp: '2026-10-16T00:00:00+00:00'
---

# Cooler

This contract handles the cooldown required before withdrawing eTokens. For each withdrawal request it mints an ERC721 NFT; the owner of the NFT is who receives the funds when the withdrawal is executed.

The value of the eTokens at the execution time can be higher or lower than the value at the scheduling time, due to earnings and losses during the cooldown period. If the resulting amount is lower, the LP (owner of the NFT) receives less. If the value is higher than the value at scheduling time, the LP receives only the value at scheduling time, and the difference is distributed to the remaining LPs of the eToken.

> **Source:** [Cooler.sol](https://github.com/ensuro/ensuro/blob/main/contracts/Cooler.sol) · **Full documentation:** [ensuro.readthedocs.io/en/latest/Cooler](https://ensuro.readthedocs.io/en/latest/Cooler/)

## Events

### WithdrawalRequested

```solidity
event WithdrawalRequested(IEToken indexed eToken, uint256 indexed tokenId, address indexed owner, uint40 when, ETKLib.Scale scaleAtRequest, uint256 amount)
```

Event emitted when a withdrawal is requested. A new NFT (the withdrawal position) is minted to the owner.

| Name           | Type           | Description                                                                  |
| -------------- | -------------- | ---------------------------------------------------------------------------- |
| eToken         | IEToken        | The eToken from which the withdrawal is being requested.                     |
| tokenId        | uint256        | The NFT id of the withdrawal position created.                               |
| owner          | address        | The owner initiating the withdrawal request.                                |
| when           | uint40         | The timestamp when the withdrawal can be executed.                          |
| scaleAtRequest | ETKLib.Scale   | The eToken scale at the time of the withdrawal request.                     |
| amount         | uint256        | The amount of eTokens being requested for withdrawal.                       |

### WithdrawalExecuted

```solidity
event WithdrawalExecuted(IEToken indexed eToken, uint256 indexed tokenId, address indexed receiver, uint256 amountRequested, uint256 amountWithdrawn)
```

Event emitted when a withdrawal is executed.

| Name            | Type    | Description                                              |
| --------------- | ------- | -------------------------------------------------------- |
| eToken          | IEToken | The eToken from which the withdrawal was processed.      |
| tokenId         | uint256 | The NFT id of the withdrawal position that was withdrawn. |
| receiver        | address | The address that received the withdrawn funds.          |
| amountRequested | uint256 | The original amount of eTokens requested for withdrawal. |
| amountWithdrawn | uint256 | The actual amount withdrawn to the receiver.            |

## External Methods

### scheduleWithdrawal

```solidity
function scheduleWithdrawal(IEToken eToken, uint40 when, uint256 amount) external returns (uint256 tokenId)
```

Schedules a withdrawal of `amount` eTokens from `eToken`, minting an NFT that represents the withdrawal position. `when == 0` uses the minimum cooldown period. If `amount == type(uint256).max`, the full balance of the caller is used.

| Name   | Type    | Description                                                                     |
| ------ | ------- | ------------------------------------------------------------------------------- |
| eToken | IEToken | The eToken from which to withdraw.                                              |
| when   | uint40  | The timestamp when the withdrawal becomes executable (`0` = minimum cooldown). |
| amount | uint256 | The amount of eTokens to withdraw.                                             |

| Name    | Type    | Description                                                    |
| ------- | ------- | -------------------------------------------------------------- |
| tokenId | uint256 | The NFT id of the token representing the withdrawal position. |

### scheduleWithdrawalWithPermit

```solidity
function scheduleWithdrawalWithPermit(IEToken eToken, uint40 when, uint256 amount, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external returns (uint256 tokenId)
```

Same as `scheduleWithdrawal`, but uses an EIP-2612 permit signature to approve the eTokens for gasless scheduling.

| Name     | Type    | Description                                                   |
| -------- | ------- | ------------------------------------------------------------- |
| eToken   | IEToken | The eToken from which to withdraw.                            |
| when     | uint40  | The timestamp when the withdrawal becomes executable.         |
| amount   | uint256 | The amount of eTokens to withdraw.                           |
| deadline | uint256 | The expiration timestamp for the permit signature.           |
| v        | uint8   | The recovery byte of the signature.                          |
| r        | bytes32 | The R component of the signature.                            |
| s        | bytes32 | The S component of the signature.                            |

| Name    | Type    | Description                                                    |
| ------- | ------- | -------------------------------------------------------------- |
| tokenId | uint256 | The NFT id of the token representing the withdrawal position. |

### executeWithdrawal

```solidity
function executeWithdrawal(uint256 tokenId) external
```

Executes a previously scheduled withdrawal after the cooldown period has elapsed. The position's NFT is burned and the funds are sent to its owner.

| Name    | Type    | Description                                                          |
| ------- | ------- | -------------------------------------------------------------------- |
| tokenId | uint256 | The NFT id of the withdrawal position to execute.                   |

### getCurrentValue

```solidity
function getCurrentValue(uint256 tokenId) external view returns (uint256)
```

Returns the current withdrawable value for a given withdrawal position.

### getWithdrawalRequestInfo

```solidity
function getWithdrawalRequestInfo(uint256 tokenId) external view returns (WithdrawalRequest memory)
```

Returns the information of a pending withdrawal request.

### pendingWithdrawals

```solidity
function pendingWithdrawals(IEToken eToken) external view returns (uint256)
```

See [ICooler-pendingWithdrawals](overview.md#pendingwithdrawals).

### cooldownPeriod

```solidity
function cooldownPeriod(IEToken eToken, address owner, uint256 amount) external view returns (uint40)
```

See [ICooler-cooldownPeriod](overview.md#cooldownperiod).
