---
type: Smart Contract
title: MultiStrategyERC4626
description: ERC4626 vault that invests/deinvests using a pluggable IInvestStrategy on each deposit/withdraw.
tags:
- smart-contracts
- extensions
timestamp: '2024-07-31T19:36:40+00:00'
---

# MultiStrategyERC4626

ERC4626 vault that invests/deinvests using a pluggable IInvestStrategy on each deposit/withdraw.

The vault requires permission to deposit/withdraw (not transfer). The owner of the shares must have LP\_ROLE.

Code available at [https://github.com/ensuro/vaults/blob/main/contracts/MultiStrategyERC4626.sol](https://github.com/ensuro/vaults/blob/main/contracts/MultiStrategyERC4626.sol)

In that repository, you can find the investment strategies implemented.
