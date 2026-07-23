---
type: Concept
title: Roles and permissions
description: The protocol uses OpenZeppelin's AccessControl mechanism.
tags:
- smart-contracts
- roles
- governance
timestamp: '2024-03-13T20:03:33+00:00'
---

# Roles and permissions

The protocol uses [OpenZeppelin's AccessControl](https://docs.openzeppelin.com/contracts/4.x/api/access#AccessControl) mechanism. The roles and delegations are managed by the [AccesManager](contracts/accessmanager.md) smart contract.

In some operations, both global roles and component roles are accepted. [Component roles](contracts/accessmanager.md#component-roles) are special roles that are restricted to a specific component (eToken, RiskModule, or PremiumsAccount).

## Common Roles

These roles are defined at the protocol level and are used across its components. They form the core of the access control structure.

| Role | Description | Methods accessible |
| --- | --- | --- |
| **LEVEL1_ROLE** | High impact changes like upgrades or other critical operations. | [unpause](roles.md#pause-unpause): Pauses the smart contract.<br>[upgrade](roles.md#upgrade): Upgrade to the smart contract implementation. |
| **LEVEL2_ROLE** | Mid-impact changes like changing some parameters. | - |
| **LEVEL3_ROLE** | Low-impact changes like changing some parameters up to given percentage (tweaks). | - |
| **GUARDIAN_ROLE** | For emergency operations oriented to protect the protocol in case of attacks or hacking. | [pause](roles.md#pause-unpause): Pauses the smart contract.<br>[unpause](roles.md#pause-unpause): Unpause the smart contract.<br>[upgrade](roles.md#upgrade): Upgrade the smart contract implementation. |
| **DEFAULT_ADMIN_ROLE** | By default, it is the admin role for all roles, which means that only accounts with this role will be able to grant or revoke other roles. See  [OpenZeppelin's documentation](https://docs.openzeppelin.com/contracts/4.x/access-control) for additional details. | grantRole: Grants a role to an account.<br>revokeRole: Revokes  a role to an account.<br>grantComponentRole: Assigns the specified role to the specified account within the component identified by the address component.<br>setComponentRoleAdmin: Sets the component-role admin for a specific component or for any component within the contract. |

## Component roles

Besides the general use roles described above, each contract can have its own defined roles for specific operations. For components of the protocol these roles are called [Component Roles](contracts/accessmanager.md#component-roles) and a detailed description of each can be found in each contract's documentation:

* [EToken](contracts/etoken.md#roles)
* [RiskModule](contracts/riskmodule.md)
* [PremiumsAccount](contracts/premiumsaccount.md#roles)
* [AccessManager](contracts/accessmanager.md#component-roles)
* [LPManualWhiteList](contracts/ilpwhitelist/lpmanualwhitelist.md#component-roles)

## Common Operations

### Upgrade

Ensuro contracts are upgradeable, following the [UUPS](https://eips.ethereum.org/EIPS/eip-1822) pattern and implemented based on [OpenZeppelin implementation](https://docs.openzeppelin.com/contracts/4.x/api/proxy#UUPSUpgradeable). 

Only users with the roles **LEVEL1\_ROLE** or **GUARDIAN\_ROLE** can execute upgrades. For global contracts such as PolicyPool and AccessManager, the role granted has to be global. For other components it can be a component role.

### Pause / Unpause

Also, most of the contracts support `pause()` and `unpause()` operations. The behavior changes from one contract to the other, but in general, most of the critical operations are rejected when the contract is paused. Check the source code for more details.

Only users with the role **GUARDIAN\_ROLE** can pause contracts. To resume (unpause) a contract, the transaction needs to be executed by a user with either **GUARDIAN\_ROLE** or **LEVEL1\_ROLE**_._

###
