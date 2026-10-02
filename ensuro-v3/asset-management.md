---
type: Concept
title: Asset Management
description: The Reserve contracts hold assets that can be invested to get additional returns.
tags:
- smart-contracts
- asset-management
timestamp: '2026-09-22T00:00:00+00:00'
---

# Asset Management

The [Reserve](reserves.md) contracts hold assets that can be invested to get additional returns. Each reserve can be assigned a _yield vault_, an [ERC-4626](https://eips.ethereum.org/EIPS/eip-4626) compatible contract that invests the delegated funds into other DeFi protocols, always prioritizing safety and liquidity.

Each of the reserves can have a different yield vault, or not have one, in which case 100% of the funds remain liquid in the contract.

## Yield vault

The yield vault used for most of the reserves is a [MultiStrategyVault](https://github.com/ensuro/vaults) (MSV), which diversifies the funds across several investment strategies. The funds invested in the different strategies accrue yields that increase the value of the vault and, therefore, the value of the shares held by each reserve. This single vault allows us to have a diversified investment strategy without fragmenting the liquidity into different contracts.

## Rebalancing

In previous versions, the rebalancing logic (how much of the funds remain liquid and how much is invested) was implemented in the asset management contracts themselves, using parametrized thresholds.

In v3 this logic is no longer implemented on-chain. Instead, an operative account holding the [YIELD_REBALANCER_ROLE](roles.md#operative-roles) moves funds between the liquid reserve and the yield vault (`depositIntoYieldVault` / `withdrawFromYieldVault`) according to the liquidity needs. Keeping some funds liquid instead of 100% invested avoids the gas costs of withdrawing from the vaults on every liquidity need.

## Allocation dashboard

The current allocation of the funds across the investment strategies is published on a live dashboard at [assets.ensuro.co](https://assets.ensuro.co/).
