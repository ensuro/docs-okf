---
type: Smart Contract
title: AccessManager
description: Contract that manages the access control permissions for governance actions.
tags:
- smart-contracts
- core
- governance
timestamp: '2022-09-29T09:24:00-03:00'
---

# AccessManager

This contract the access control permissions for the governance actions.

It's created before the PolicyPool contract and it's an immutable attribute of it. The access permissions of all the different components of the protocol are stored and managed by this contract.

The contract is basically an [OpenZeppelin AccessControl](https://docs.openzeppelin.com/contracts/4.x/api/access#AccessControl) contract, with some additional functions for computing _component roles_ and helper functions.

## Component Roles

The contract has the function `getComponentRole(component, role)` that derives a new role by mixing the address of the component and the role (a bytes32 hash).

`getComponent(component, role) = bytes32(bytes20(component)) ^ role`

Then, for example, if we want to grant the role LEVEL2_ROLE (hash `0xa82e22387fca439f316d78ca566f383218ab8ae1b3e830178c9c82cbd16749c0)`but just on eToken with the address `0x161d203D2BF64A71324C4583491a5C7f1FE2839C` we compute the new role that will be: `0xbe330205543c09ee03213d491f75644d0749097db3e830178c9c82cbd16749c0`and we grant that role. This way a user can have a given role restricted to a specific component.

## External Methods

### hasComponentRole

```solidity
function hasComponentRole(address component, bytes32 role, address account, bool alsoGlobal) external view returns (bool)
```

Tells if a user has been granted a given role for a component.

| Name       | Type    | Description                                                                                                                           |
| ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| component  | address | The component where this role will apply                                                                                              |
| role       | bytes32 | A role such as `keccak256("LEVEL1_ROLE")` that's global                                                                               |
| account    | address | The user address for who we want to verify the permission                                                                             |
| alsoGlobal | bool    | If true, it will return if the users has either the component role, or the role itself. If false, only the component role is accepted |

| Name | Type | Description                                  |
| ---- | ---- | -------------------------------------------- |
| [0]  | bool | Whether the user has or not any of the roles |

### checkRole

```solidity
function checkRole(bytes32 role, address account) external view
```

Checks if a user has been granted a given role and reverts if it doesn't.

| Name    | Type    | Description                                               |
| ------- | ------- | --------------------------------------------------------- |
| role    | bytes32 | A role such as `keccak256("LEVEL1_ROLE")` that's global   |
| account | address | The user address for who we want to verify the permission |

### checkRole2

```solidity
function checkRole2(bytes32 role1, bytes32 role2, address account) external view
```

Checks if a user has been granted any of the two roles specified and reverts if it doesn't.

| Name    | Type    | Description                                                     |
| ------- | ------- | --------------------------------------------------------------- |
| role1   | bytes32 | A role such as `keccak256("LEVEL1_ROLE")` that's global         |
| role2   | bytes32 | Another role such as `keccak256("GUARDIAN_ROLE")` that's global |
| account | address | The user address for who we want to verify the permission       |

### checkComponentRole

```solidity
function checkComponentRole(address component, bytes32 role, address account, bool alsoGlobal) external view
```

Checks if a user has been granted a given component role and reverts if it doesn't.

| Name       | Type    | Description                                                                                                                             |
| ---------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| component  | address |                                                                                                                                         |
| role       | bytes32 | A role such as `keccak256("LEVEL1_ROLE")` that's global                                                                                 |
| account    | address | The user address for who we want to verify the permission                                                                               |
| alsoGlobal | bool    | If true, it will accept not only the component role, but also the (global) `role` itself. If false, only the component role is accepted |

### checkComponentRole2

```solidity
function checkComponentRole2(address component, bytes32 role1, bytes32 role2, address account, bool alsoGlobal) external view
```

Checks if a user has been granted any of the two component roles specified and reverts if it doesn't.

| Name       | Type    | Description                                                                                                                     |
| ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------- |
| component  | address |                                                                                                                                 |
| role1      | bytes32 | A role such as `keccak256("LEVEL1_ROLE")` that's global                                                                         |
| role2      | bytes32 | Another role such as `keccak256("GUARDIAN_ROLE")` that's global                                                                 |
| account    | address | The user address for who we want to verify the permission                                                                       |
| alsoGlobal | bool    | If true, it will accept not only the component roles, but also the global ones. If false, only the component roles are accepted |
