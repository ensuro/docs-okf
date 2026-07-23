---
type: Smart Contract
title: IAssetManager
description: Asset managers are contracts that can be plugged into a reserve (eTokens or PremiumsAccounts).
tags:
- smart-contracts
- asset-management
timestamp: '2025-04-16T15:35:04+00:00'
---

# IAssetManager

Asset managers are contracts that can be plugged into a reserve (eTokens or PremiumsAccounts). They have the responsibility of managing the assets of the contract and reinvesting them in other DeFi protocols to generate additional yields. `IAssetManager` defines the interface of these asset managers that can later have several implementations diverging mostly in where the funds are invested and in how much of the funds are invested and how much remains as liquid funds in the reserve contract.

They operate in the context of the reserves, behind specific functions that use _delegatecalls_ to the asset manager interface. In a way, the assets managers aren't itself contracts, but instead, they are code chunks that are plugged into the reserve contract.

## Events

### MoneyInvested

```solidity
event MoneyInvested(uint256 amount)
```

Event emitted when funds are removed from Reserve liquidity and invested in the investment strategy.

| Name   | Type    | Description         |
| ------ | ------- | ------------------- |
| amount | uint256 | The amount invested |

### MoneyDeinvested

```solidity
event MoneyDeinvested(uint256 amount)
```

Event emitted when funds are deinvested from the investment strategy and returned to the reserve as liquid funds.

| Name   | Type    | Description            |
| ------ | ------- | ---------------------- |
| amount | uint256 | The amount de-invested |

### EarningsRecorded

```solidity
event EarningsRecorded(int256 earnings)
```

Event emitted when investment yields are accounted in the reserve.

| Name     | Type   | Description                                                                                                                  |
| -------- | ------ | ---------------------------------------------------------------------------------------------------------------------------- |
| earnings | int256 | The amount of earnings generated since last record. It's positive in the case of earnings or negative when there are losses. |

## External Methods

### connect

```solidity
function connect() external
```

Function called when an asset manager is plugged into a reserve. Useful for initialization tasks.

### rebalance

```solidity
function rebalance() external
```

Gives the opportunity to the asset manager to rebalance the funds between those that are kept liquid in the reserve balance and those that are invested. Called with delegatecall by the reserve from the external function rebalance (see {Reserve-rebalance}).

Events:

* Emits {MoneyInvested} or {MoneyDeinvested}

### recordEarnings

```solidity
function recordEarnings() external returns (int256)
```

Gives the opportunity to the asset manager to rebalance the funds between those that are kept liquid in the reserve balance and those that are invested. Called with delegatecall by the reserve from the external function rebalance (see {Reserve-rebalance}).

Events:

* Emits {MoneyInvested} or {MoneyDeinvested}

### refillWallet

```solidity
function refillWallet(uint256 paymentAmount) external returns (uint256)
```

Refills the reserve balance with enough money to do a payment. Called from the reserve when a payment needs to be made and there's no enough liquid balance (`currency().balanceOf(reserve) < paymentAmount`)

Events:

* Emits {MoneyDeinvested} with the amount transferred to the liquid balance.

| Name          | Type    | Description                                                                                                                                                                                                                                                           |
| ------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| paymentAmount | uint256 | The total amount of the payment that needs to be made. If this function is called, it's because paymentAmount > balanceOf(reserve). The minimum amount that needs to be transferred to the reserve is `paymentAmount - balanceOf(reserve)`, but it can transfer more. |

| Name | Type    | Description                           |
| ---- | ------- | ------------------------------------- |
| \[0] | uint256 | Returns the actual amount transferred |

### deinvestAll

```solidity
function deinvestAll() external returns (int256)
```

Deinvests all the funds transfer all the assets to the liquid balance. Called from the reserve when the asset manager is unplugged.

Events:

* Emits {MoneyDeinvested} with the amount transferred to the liquid balance.
* Emits {EarningsRecorded} with the amount of earnings since earnings were recorded last time.

| Name | Type   | Description                                                                       |
| ---- | ------ | --------------------------------------------------------------------------------- |
| \[0] | int256 | Returns the earnings or losses (negative) since last time earnings were recorded. |
