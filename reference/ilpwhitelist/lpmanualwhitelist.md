---
type: Smart Contract
title: LPManualWhitelist
description: This is an implementation of the ILPWhitelist interface that just has a mapping (address - bool) indicating whether or not a liquidity provider with a given address is whitelisted.
tags:
- smart-contracts
- whitelist
timestamp: '2024-03-06T19:26:15+00:00'
---

# LPManualWhitelist

This is an implementation of the [ILPWhitelist](overview.md) interface that just has a mapping (address -> bool) indicating whether or not a liquidity provider with a given address is whitelisted.

All the addresses are blacklisted by default. To whitelist an address, an authorized user with the LP\_WHITELIST component role needs to call `whitelistAddress(provider, whitelisted)`.

## **Component roles**

The specific roles and functions of the contract are as follows:

| Role | Global* | Description | Methods Accessible |
| --- | --- | --- | --- |
| LP_WHITELIST_ROLE | ✗ | Whitelist or un-whitelist addresses manually. | [whitelistAddress](lpmanualwhitelist.md#whitelistaddress): Adds or removes provider addresses from the whitelist manually. |
| LP_WHITELIST_ADMIN | ✗ | Manages the LP whitelisting system. | setWhitelistDefaults: Set the default whitelist status for LP addresses. |

( \* ) Global means that the role can be delegated to a user at the protocol level (for all components) or only for a specific component. Non-global roles can only be granted for a specific component.

## Events

### LPWhitelisted

```solidity
event LPWhitelisted(address provider, bool whitelisted)
```

| Name        | Type    | Description                              |
| ----------- | ------- | ---------------------------------------- |
| provider    | address | The address to be whitelisted.           |
| whitelisted | bool    | If `true`, the provider was whitelisted. |

## External Methods

### whitelistAddress

```solidity
function whitelistAddress(address provider, bool whitelisted) external
```
