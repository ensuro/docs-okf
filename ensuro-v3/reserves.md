---
type: Concept
title: Reserves
description: The funds received by the protocol, such as liquidity provider deposits or premiums, are stored in reserves.
tags:
- smart-contracts
- reserves
timestamp: '2022-09-27T16:33:37+00:00'
---

# Reserves

The funds received by the protocol, such as liquidity provider deposits or premiums, are stored in _reserves_. A _reserve_ is a base contract that holds assets (USDC). We have two types of reserves: [eTokens](liquidity-pools.md) and [Premiums Accounts](premiums-accounts.md).

Each reserve might have an asset management strategy to get additional returns from the managed assets. This strategy, an additional implementation contract that runs with _delegatecall_, will invest the reserves' funds to get the returns and should be able to de-invest them when needed.

> **Note:** An **asset management strategy** can be something as simple as a contract that deposits the USDC in AAVE, accruing the interests. When the funds are needed, the contract withdraws them from AAVE.
>
> Other more aggressive or complex asset management strategies can be implemented, including using ERC-4626 vaults or asset management protocols like Enzyme Finance.

The returns coming from the asset management strategy will be treated differently depending on the specific reserve:

* **ETokens**: the yields of the asset management strategy generate an increase in the total supply, distributing the yield to all the LPs in proportion to their share of the liquidity pool.
* **Premiums Accounts**: in this case, the yields will have a treatment similar to the earned pure premiums precedence [explained here](premiums-accounts.md#pure-premiums). 

## Cash Movements

| Operation     | In/Out   | Source/Target                                                                                                                                                                        |
| ------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| deposit       | In       | eToken                                                                                                                                                                               |
| withdraw      | Out      | eToken                                                                                                                                                                               |
| newPolicy     | In       | <ul><li>Ensuro Treasury</li><li>Partner</li><li>Premiums Account</li><li>Junior eToken</li><li>Senior eToken</li></ul><p>See <a href="policy.md#premium-split">Premium Split</a></p> |
| resolvePolicy | Out      | <ol><li>Premiums Account</li><li>Junior eToken</li><li>Senior eToken</li></ol><p>See <a href="premiums-accounts.md#pure-premiums">precedence order</a>.</p>                          |
| expirePolicy  | Internal | [Internal loan repayment](liquidity-pools.md#internal-loan-repayment) from Premiums Account --> eToken                                                                               |
