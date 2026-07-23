---
type: Concept
title: Asset Management
description: The Reserve contracts hold assets that can be invested to get additional returns.
tags:
- smart-contracts
- asset-management
timestamp: '2024-07-31T19:36:40+00:00'
---

# Asset Management

The [Reserve](reserves.md) contracts hold assets that can be invested to get additional returns. The investment strategy is implemented by [IAssetManager](contracts/iassetmanager/overview.md) contracts that are plugged into the reserve contracts and execute different investments, always prioritizing safety and liquidity.

So far, all the strategies involve keeping some funds liquid (as USDC) in the reserve contract and investing the remaining funds. The logic (implemented in the [LiquidityThresholdAssetManager](contracts/iassetmanager/liquiditythresholdassetmanager.md) abstract contract) uses parametrized thresholds to decide when to invest some liquid funds into the specific investment strategy or when to de-invest funds and leave them liquid in the reserve contract. 

It is important to mention that we always choose **highly liquid** investment strategies, so this movement of funds between funds liquid in the reserve and funds invested in other protocols is not driven by liquidity needs, but instead to **avoid the gas costs** we would have if we had 100% of the funds invested.

Each of the reserves can have a different asset management strategy, or not have one, in that case, 100% of the funds are liquid in the contract. 

In June 2024 we implemented a [MultiStrategyERC4626](contracts/extensions/multistrategyerc4626.md) (MSV), a vault contract that diversifies the funds into different protocols, like AAVEv3, CompoundV3, and Mountain Protocol (USDM). Through the [ERC4626AssetManager](contracts/iassetmanager/erc4626assetmanager.md), most of the reserves deploy funds into the MSV, getting shares of the vault. The funds, invested in the different protocols accrue yields that increase the value of the vault and, thus the values of the shares. This single MSV allows us to have a diversified investment strategy without having to fragment the liquidity into different contracts.
