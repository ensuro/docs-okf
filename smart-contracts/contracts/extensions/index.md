The extensions are contracts used to support particular use cases. They operate outside of the protocol and have their [own repository](https://github.com/ensuro/ensuro-extensions).

# Documents

* [ERC4626CashFlowLender](erc4626cashflowlender.md) - Implements the ERC-4626 standard tracking how much liquidity was provided by each LP.
* [ETokensBundleVault](etokensbundlevault.md) - ERC-4626 vault that invests in several eTokens with fixed allocations.
* [MultiStrategyERC4626](multistrategyerc4626.md) - ERC4626 vault that invests/deinvests using a pluggable IInvestStrategy on each deposit/withdraw.
