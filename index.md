---
okf_version: "0.1"
title: Introduction
description: Ensuro is a blockchain protocol that provides capital coverage for insurance risks.
type: Guide
tags:
  - introduction
  - protocol
---

Ensuro is a blockchain protocol that provides capital coverage for insurance risks.

Insurance risks are composed of sets of policies purchased by customers (policyholders) to obtain a refund if they experience a loss. In the context of the Ensuro protocol, we define an insurance risk as a random variable between 0 and the maximum payout defined in the corresponding policy. From the point of view of the protocol, this payment is referred to as a _loss_.

The main objective of Ensuro is to guarantee that the protocol will be able to cover the losses for the risks taken. The amount of capital required to cover the potential losses up to the desired confidence interval (typically 99.5%) is calculated externally by our quantitative team. The outcome of this computation is the _collateralization ratio_ parameter which, when multiplied by the maximum payout of each policy, results in the amount of capital to lock (_solvency capital)_.

The solvency capital comes from two sources:

- **Pure premiums**: the part of the premium equal to the "risk" random variable estimated mean (i.e., to the expected losses), paid by the policyholder.
- **SCR**: the rest of the solvency capital (unexpected losses), required to cover the risks with a given _confidence level_, is locked from the _eTokens_ (or _liquidity pools_).

## ETokens

The _eTokens_ are capital pools where investors (_liquidity providers_ or _LPs_) can deposit capital using stablecoins (USDC). In doing so, they accept their capital to be used as solvency capital for the risks taken by the protocol. In exchange for this exposure, they receive a return in the form of a continuous interest rate paid from the premiums as _Cost of Capital_. This cost is proportional to the SCR's amount, the policy's duration, and the interest rate of the specific risk.

Each _eToken_ will have a total amount of capital (_total supply_) provided by LPs plus the returns, and a fraction of that capital will be used as solvency capital (SCR) of active policies. The relation between _scr_ and _total supply_ is called _utilization rate_.

Liquidity providers can jump out from the liquidity pools (eTokens) at any point as far as the _total supply_ after their withdrawal is greater than the _scr_ (leaving _utilization rate_ under 100%).

There are different eTokens, each one exposed to a different set of risks. The _Junior eTokens_ are linked to a specific portfolio (PremiumsAccount) and are exposed to the first tranche of unexpected losses; Junior eTokens are the first hit when pure premiums are exhausted. The _Senior eTokens_ are linked to different policy portfolios and are used only after both pure premiums and junior capital are exhausted.

## Risk Modules

The risk taken, represented by the policies, is managed by _risk modules_ that are smart contracts plugged into the protocol. Each _risk module_ represents an Ensuro partner and a specific insurance product. They have two main responsibilities:

- **policy injection and pricing**: they receive the transactions to create new policies. They validate the price using a trusted party or by some specific calculation.
- **policy resolution**: validating the conditions in which the event triggering the policy is met and the amount of payout. This resolution can also be sourced from a trusted party or based on some input like an oracle.

Besides the logic related to policy pricing and resolution, each risk module stores several parameters of the specific insurance product: collateralization ratios, fees, return on solvency capital, exposure limits, and maximum policy duration, MoC.

## Documentation

- [Liquidity Providers](liquidity-providers/) — FAQ, pools overview and onboarding process
- [Risk Partners](risk-partners/) — FAQ, onboarding process and product flow
- [Deployments](deployments/) — Addresses of deployed smart contracts
- [Audits](audits/) — Security audit reports
- [Smart Contracts](smart-contracts/) — Architecture, concepts and reference docs
- [Offchain APIs](offchain-apis/) — REST APIs for partner integrations
- [Frontend](frontend/) — Security and monitoring
- [Legal & Compliance](legal/) — Legal and compliance documents
