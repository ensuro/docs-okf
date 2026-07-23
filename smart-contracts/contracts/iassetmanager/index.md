# Documents

* [IAssetManager](overview.md) - Asset managers are contracts that can be plugged into a reserve (eTokens or PremiumsAccounts).
* [LiquidityThresholdAssetManager](liquiditythresholdassetmanager.md) - This is an abstract implementation of the IAssetManager interface that implements a liquidity strategy based on thresholds.
* [ERC4626AssetManager](erc4626assetmanager.md) - This contract inherits from LiquidityThresholdAssetManager, deploying the funds into an ERC-4626 compatible vault.
* [AAVEv3AssetManager](aavev3assetmanager.md) - This is an implementation of the IAssetManager interface that deploys the funds into AAVE version 3 (also v2 available).
