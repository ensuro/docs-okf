---
type: Smart Contract
title: ERC4626AssetManager
description: This contract inherits from LiquidityThresholdAssetManager, deploying the funds into an ERC-4626 compatible vault.
tags:
- smart-contracts
- asset-management
timestamp: '2022-09-27T16:33:37+00:00'
---

# ERC4626AssetManager

This contract inherits from LiquidityThresholdAssetManager, deploying the funds into an [ERC-4626](https://eips.ethereum.org/EIPS/eip-4626) compatible vault.

It receives the `vault` as a constructor parameter that's stored as an immutable attribute. 

Implements the required [inheritance methods](liquiditythresholdassetmanager.md#inheriting) by deposits and withdrawals from the vault.
