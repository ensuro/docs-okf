---
type: Concept
title: Reserves
description: The funds received by the protocol, such as liquidity provider deposits or premiums, are stored in reserves.
tags:
- smart-contracts
- reserves
timestamp: '2026-09-22T00:00:00+00:00'
---

# Reserves

The funds received by the protocol, such as liquidity provider deposits or premiums, are stored in _reserves_. A _reserve_ is a base contract that holds assets (USDC). We have two types of reserves: [eTokens](liquidity-pools.md) and [Premiums Accounts](premiums-accounts.md).

Each reserve can be assigned a _yield vault_, an ERC-4626 contract that invests the reserve's funds to get additional returns and can de-invest them when needed. See the [Asset Management](asset-management.md) page for the details.

The returns coming from the yield vault will be treated differently depending on the specific reserve:

* **ETokens**: the yields of the yield vault generate an increase in the total supply, distributing the yield to all the LPs in proportion to their share of the liquidity pool.
* **Premiums Accounts**: in this case, the yields will have a treatment similar to the earned pure premiums precedence [explained here](premiums-accounts.md#pure-premiums).

## Cash Movements

| Operation     | In/Out   | Source/Target |
| ------------- | -------- | --- |
| deposit       | In       | eToken |
| withdraw      | Out      | eToken |
| newPolicy     | In       | <ul><li>Ensuro Treasury</li><li>Partner</li><li>Premiums Account</li><li>Junior eToken</li><li>Senior eToken</li></ul><br>See [Premium Split](policy.md#premium-split) |
| replacePolicy | In       | <ul><li>Ensuro Treasury</li><li>Partner</li><li>Premiums Account</li><li>Junior eToken</li><li>Senior eToken</li></ul><br>Receives the delta of each premium component (see [Premium Split](policy.md#premium-split)) |
| cancelPolicy  | Out      | <ul><li>Junior eToken</li><li>Senior eToken</li><li>Pure Premium</li></ul><br>The flows depend on the refund amounts (see [Policy cancellation](policy-lifecycle.md#policy-cancellation)) |
| resolvePolicy | Out      | <ol><li>Premiums Account</li><li>Junior eToken</li><li>Senior eToken</li></ol><br>See [precedence order](premiums-accounts.md#pure-premiums) |
| repayLoan     | Internal | Premiums Account --> eToken |
