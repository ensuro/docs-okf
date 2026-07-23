---
type: Concept
title: Governance
description: Ensuro leverages Multisig and Timelock contracts to provide transparency and security for the protocol.
tags:
- smart-contracts
- governance
timestamp: '2024-03-13T20:16:37+00:00'
---

# Governance

Ensuro leverages Multisig and Timelock contracts to provide transparency and security for the protocol.

No major changes to the protocol will ever be made without first going through an internal vetting process that requires sign-off from several senior staff members and a public announcement with an appropriate warning period enforced by a [TimelockController smart contract](https://docs.openzeppelin.com/contracts/4.x/api/governance#TimelockController).

### Timelocks

Timelocks require a change to be published on the blockchain in advance. The timelock enforces a minimum waiting period for execution once the change has been proposed, and only authorized accounts or contracts can propose changes.

The Timelock contracts currently in use in Ensuro are these:

| Name | Delegated roles | Min. Delay | Authorized proposers |
| --- | --- | --- | --- |
| [ADMIN_TL](https://polygonscan.com/address/0xc0D3EcAcEBE2A8f2268D3FAE616f9DD1B94e81a2) | DEFAULT_ADMIN_ROLE<br>LEVEL1_ROLE<br>LEVEL2_ROLE | 4 days | ADMINS_MULTISIG |
| [LEVEL2_TL](https://polygonscan.com/address/0x371d67Ee31f6bfcDF13C7fa0CC9cC2C7080Ac666) | LEVEL2_ROLE<br>LP_WHITELIST_ADMIN_ROLE_ADMIN | 18 hours | ADMINS_MULTISIG |
| [OPERATIONAL_TL](https://polygonscan.com/address/0x76934cd2648594488a1378AC769D639933623D2a) | WITHDRAW_WON_PREMIUMS_ROLE<br>RESOLVER_ROLE_ADMIN<br>POLICY_CREATOR_ROLE_ADMIN | 6 hours | ADMINS_MULTISIG |

Each timelock acts as its own admin, and proposals can be executed by one of several company EOAs once they've been scheduled and the lock time has elapsed.

No accounts, besides the Timelock contracts enumerated here, are granted the `DEFAULT_ADMIN`, `LEVEL1` or `LEVEL2` roles at the protocol level. 

Some of the RiskModules have the `LEVEL1` and `LEVEL2` component-specific roles delegated directly to a Multisig in some cases to allow for faster product repricing. This exception depends on the agreement with the risk partner that the RiskModule belongs to and the maturity of the product.

### Multisigs

| Name | Description | Members |
| --- | --- | --- |
| [ADMINS_MULTISIG](https://app.safe.global/settings/setup?safe=matic:0xCfcd29CD20B6c64A4C0EB56e29E5ce3CD69336D2) | Main admin multisig.<br><br>Requires at least 3 signatures from senior staff.<br><br>Permissions:<br>Propose transactions on [timelocks](governance.md#timelocks)<br>[LEVEL3_ROLE](roles.md) at protocol level<br>[LEVEL2_ROLE](roles.md) on some RiskModules<br>Role admin on [PRICER_ROLE](contracts/riskmodule.md)<br>DEFAULT_ADMIN_ROLE and GUARDIAN_ROLE on some [Peripheral contracts](../audits.md#peripheral-contracts) (mainly [CashflowLenders](contracts/extensions/erc4626cashflowlender.md)) | [Colin McQueen (CFO)](https://www.linkedin.com/in/colin-mcqueen-55454b13/)<br>[Gabriel Parrondo (CISO)](https://www.linkedin.com/in/gnpar/)<br>[Gian Giacomo della Torre (CRO)](https://www.linkedin.com/in/gian-giacomo-della-torre/)<br>[Guillermo Narvaja (CTO)](https://www.linkedin.com/in/guillermonarvaja/)<br>[Luca Mungo (CSO)](https://www.linkedin.com/in/luca-mungo-a26278103/)<br>[Marco Mirabella (CEO)](https://www.linkedin.com/in/marco-mirabella/) |
| [GUARDIAN_TEAM_1](https://app.safe.global/settings/setup?safe=matic:0x2f8CD0Dc0393139E1AFAED51F629F77A7dfB955d) | Emergency operations multisig 1. <br><br>Requires approval from all members.<br><br>Used for emergency protocol pausing or unpausing.<br><br>Permissions:<br>[GUARDIAN_ROLE](roles.md) at protocol level | [Gabriel Parrondo (CISO)](https://www.linkedin.com/in/gnpar/)<br>[Marco Mirabella (CEO)](https://www.linkedin.com/in/marco-mirabella/) |
| [GUARDIAN_TEAM_2](https://app.safe.global/settings/setup?safe=matic:0x89735E8f678Fe72A31402d04595d36044b80909B) | Emergency operations multisig 2. <br><br>Requires approval from all members.<br><br>Used for emergency protocol pausing or unpausing.<br><br>Permissions:<br>[GUARDIAN_ROLE](roles.md) at protocol level | [Colin McQueen (CFO)](https://www.linkedin.com/in/colin-mcqueen-55454b13/)<br>[Guillermo Narvaja (CTO)](https://www.linkedin.com/in/guillermonarvaja/) |

### Transaction signing

All members of the multisigs must use secure hardware wallets or isolated environments for signing transactions. This is audited internally as part of our compliance program with the Bermuda Monetary Authority.

Transactions are signed using [Safe Wallet Multisigs](https://safe.global/) as documented above.

All critical transactions, such as upgrades or major parameter changes, must require at least 3 different senior staff members to sign.

### Restricted Executor

In some cases, we have integrated our monitoring system (Ensuro Forta Bot, Forta feeds, Openzeppelin Defender sentinels and internal transaction monitoring) into our automated incident response.

This requires a service account to have the ability to instantly pause the protocol in reaction to some alerts.

Given that our GUARDIAN\_ROLE, which is the one used for pausing, can also unpause and upgrade contracts, we have created an intermediate contract called [Restricted Executor ](https://github.com/ensuro/restricted-executor?tab=readme-ov-file)that allows us to delegate a single operation instead of a full role.

| Name                                                                                               | Permissions                                                                                                                             | Authorized operations                                                                                                                                |
| -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [RESTRICTED\_EXECUTOR](https://polygonscan.com/address/0x174F4498aF0a5102234Ad24d16Ed6E698E48Fa65) | <ul><li><a href="roles.md">GUARDIAN_ROLE</a> on specific <a href="contracts/premiumsaccount.md">PremiumsAccount</a> contracts</li></ul> | <ul><li>pause() authorized to an <a href="https://polygonscan.com/address/0x11Ca23Ef7d05fF86EECd8FE8324f35693bd27Cc9">operational EOA</a>.</li></ul> |
