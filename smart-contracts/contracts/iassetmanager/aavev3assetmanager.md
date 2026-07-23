---
type: Smart Contract
title: AAVEv3AssetManager
description: This is an implementation of the IAssetManager interface that deploys the funds into AAVE version 3 (also v2 available).
tags:
- smart-contracts
- asset-management
timestamp: '2022-09-30T10:23:13+00:00'
---

# AAVEv3AssetManager

This is an implementation of the [IAssetManager](overview.md) interface that deploys the funds into [AAVE](https://aave.com/) version 3 (also v2 available). Investment operations are deposits into AAVE, deinvestment ones are implemented as withdrawals.

Inherits from [LiquidityThresholdAssetManager](liquiditythresholdassetmanager.md), so it manages the liquid levels based on parametrized thresholds.

It's not part of the core Ensuro repository, more an extension with its [own repository](https://github.com/ensuro/aave-asset-manager).
