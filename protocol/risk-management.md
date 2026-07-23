---
type: Guide
title: Risk Management
description: Liquidity Providers and Policyholders are at the heart of Ensuro’s business model.
tags:
- risk-management
timestamp: '2023-05-11T15:16:03+00:00'
---

# Risk Management

Liquidity Providers and Policyholders are at the heart of Ensuro’s business model. The former protects the latter, providing supplementary capital to pay unexpected losses (solvency capital). Ensuro makes a concentrated effort to guarantee the safety of Liquidity Providers assets as well as Policyholders continuous protections, both from an IT and a risk-management standpoint. Ensuro commits to the highest standards in reinsurance risk management following the European Union’s Solvency II directives.

### Architecture Shield

Ensuro leverages its architecture to protect LPs capital whilst offering solvency to policyholders. The protocol comprises of four pools; the first two need to be completely drained before any loss can impact the third and fourth, where the LPs’ capital is stored. These pools are:

* **Won Premium pool**: this pool contains the pure premiums of all expired policies. 
* **Active Premium pool**: this pool contains the pure premiums of all currently active policies. 
* **SCR pool (Junior tranche)**: this pool collects the solvency capital of the active policies. It represents the LPs’ capital exposed to insurance risk and returns. This first tranche of the SCR is usually calibrated to be able to cover the losses in 70%/80% of the scenarios.
* **SCR pool (Senior tranche)**: this second tranche of the solvency capital covers for more extreme scenarios. The solvency capital is calibrated in accordance with Bermuda's Solvency Capital Requirements (99.5%), a risk-based approach endorsed by a variety of international regulatory and standard setting bodies including, most recently, Bermuda's enhanced commercial insurance regime reaching full equivalence with Solvency II.

Before disbursing the LPs’ capital locked in the SCR pool, both the Won Premium pool and the Active Premium pool must be fully depleted. As mentioned, policies are priced incorporating a conservative factor called '_margin of conservatism_' or MoC. This parameter increases the pure premium having the effect of increasing both the Won and Active Premium pool, shielding the SCR pool. The MoC is monitored in real-time, and can be increased as deemed necessary.

Further details on the order in which solvency reserves are used can be found [here](../smart-contracts/premiums-accounts.md#pure-premiums).
