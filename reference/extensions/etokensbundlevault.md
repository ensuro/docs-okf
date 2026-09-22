---
type: Smart Contract
title: ETokensBundleVault
description: ERC-4626 vault that invests in several eTokens with fixed allocations.
tags:
- smart-contracts
- extensions
timestamp: '2024-03-06T19:26:15+00:00'
---

# ETokensBundleVault

ERC-4626 vault that invests in several eTokens with fixed allocations.

## **Roles**

The roles and functions of the contract are as follows:

| Role                     | Description                                                      | Methods Accessible                                                                                            |
| ------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| ADMIN\_ROLE              | Adds and removes underlying eTokens.                             | <ul><li>addEToken: Adds a new underlying eToken.</li><li>removeEToken: Removes an underlying eToken</li></ul> |
| CHANGE\_PERCENTAGE\_ROLE | Changes allocation percentages for eTokens.                      | <ul><li>changePercentages: Changes allocation percentages for eTokens.</li></ul>                              |
| REORDER\_ROLE            | Swaps the order of underlying eTokens.                           | <ul><li>reorderETokens: Swaps order of underlying eTokens.</li></ul>                                          |
| REBALANCER\_ROLE         | Moves funds between underlying eTokens for rebalancing purposes. | <ul><li>rebalance: Moves funds between underlying eTokens.</li></ul>                                          |

This contract does not use Access Manager as an access control solution. It has its own [access control ](https://docs.openzeppelin.com/contracts/5.x/api/access)mechanism.
