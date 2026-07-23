---
type: Concept
title: Liquidity pools
description: The solvency to cover the potential losses does not simply come from the premiums.
tags:
- smart-contracts
- liquidity
timestamp: '2023-06-20T18:28:11+00:00'
---

# Liquidity pools

The solvency to cover the potential losses does not simply come from the premiums. The additional capital is supplied by investors (liquidity providers) with the expectation of getting returns.

These returns come from the premiums (as cost of capital for the funds locked as solvency capital) and are available for the liquidity providers as a continuous interest rate.

Each liquidity pool (a.k.a. _eToken_) is linked to specific risks and has a part of the capital locked as solvency capital of active policies.

> **Note:** **eTokens == Liquidity pool**
>
> In the context of Ensuro, _eToken_ and _liquidity pool_ are synonyms. We choose the term _eToken_ by analogy with [AAVE's aTokens](https://docs.aave.com/developers/tokens/atoken). As AAVE's aTokens, the eTokens are pegged 1:1 to the value of the supplied asset. In AAVE, the yield comes from lending; in Ensuro, it comes from locking the funds as solvency capital.

## Utilization rate

The liquidity pools have a given amount of capital (also called _**total supply**_) originating from deposits and earnings. At any point, a fraction of that capital is used as solvency capital for active policies. We call this capital _**scr**_.

The relation between the _scr_ and the _total supply_ is called the _**utilization rate**_.

$$
utilizationRate = scr / totalSupply
$$

Different operations in a liquidity pool affect the scr and totalSupply, and, consequently, the utilization rate.

## SCR / Token interest rate

When a new policy is sold, part of the liquidity of a pool is locked as SCR,  and a [cost of capital](policy.md#junior-and-senior-cost-of-capital) is paid from the premium and generates an interest rate paid to the pool.

Every chunk of capital that's locked can have a different interest rate. The eToken keeps track of the _scrInterestRate_ doing a weighted average:

$$
newScrIR = (scrIR * oldScr + policy.scr * policy.IR) / (oldScr + policy.scr)
$$

And when a policy expires, and the capital is no longer locked:

$$
newScrIR = (scrIR * oldScr - policy.scr * policy.IR) / (oldScr - policy.scr)
$$

But given not all the capital of the pool is locked as SCR, the yield rate of the pool can't be the scrInterestRate, but instead should be multiplied by the utilization rate:

$$
tokenInterestRate = scrInterestRate * utilizationRate
$$

This token interest rate is the factor that will scale the total supply with time, growing at this interest rate.

$$
ts_t = ts_0*(1 + tIR* Δt) = ts_0*(1 + scrIR * UR_0* Δt)
$$

> **Note:** **A numeric example**
>
> Initially, the eToken has a total supply (TS)=$ 100, no scr, so UR = 0%.
>
> 1. January 1st: New Policy comes in, locks $ 30 at 10% for six months. CoC = 1.5 will be disbursed over six months. scr = $ 30, UR=30%, scrIR=10%, tIR=3%.
> 2. April 1st: New Policy comes in, locks $ 40 at 20% for six months. CoC = 4 disbursed over six months. scr = 70, TS=100\*(1 + .03\*3/12)=100.75, UR = 70 / 100.75 \~ 69.5%, scrIR = 15.71%, tIR=10.9%
> 3. July 1st: policy #1 expires. TS=100.75\*(1 + .109\*3/12)=103.5, scr = 40, scrIR=20%, UR=40/103.5=38.6%, tIR=7.7%
> 4. October 1st: policy #2 expires, TS=103.5\*(1+.077\*3/12)=105.5, scr=scrIR=UR=0

### Why progressive disbursing if the CoC is paid upfront with the premiums?

Progressive disbursing of the cost of capital allows us to have a dynamic capital pool where liquidity providers can jump in and out and get returns proportional to their share and the utilization rate of the pool at every point in time.

## Operations

### Deposit

Any user can deposit liquidity in the pools (USDC). For regulatory reasons, in some cases, we might require the user to be whitelisted after going through a KYC process.

The user provides an amount X of the underlying asset (e.g., USDC) and receives the same amount in eTokens. From that point onwards, the user's balance will grow at a rate defined by the _token interest rate, as_ explained above.

Deposits increase the _total supply_ without affecting the _scr_, decreasing the _utilization rate_ and the _token interest rate_ and diluting the LPs' yield. The parameter `minUtilizationRate` allows setting a limit in this dilution, rejecting deposits if they leave the utilization rate under this value.

### Withdrawal

Any liquidity provider can issue a withdrawal transaction at any point, converting their _eTokens_ one-to-one to the underlying asset (e.g., USDC). The withdrawable funds of the pool limit the amount that LPs can withdraw:

$$
totalWithdrawable = totalSupply - scr * liquidityRequirement
$$

> **Note:** **liquidityRequirement** is a parameter supported by the eTokens that's 1.0 by default. In some cases, a governance decision can increase it, for example, to increase the amounts locked if we need to lock the yields until the policies expire. Usually, it will be 1.0.

So, the user will be able to withdraw the minimum between his balance and the _totalWithdrawable_ of the pool.

This operation decreases the total supply without affecting the scr, thus increasing the utilization rate.

### Lock

When a policy is sold and requires solvency covered by the pool, the eToken receives lock requests from other protocol components ([PremiumsAccount](contracts/premiumsaccount.md)). These lock requests specify the amount to lock and the interest rate that LPs will receive.

This operation increases the scr, modifies the [scr interest rate and token interest rate](liquidity-pools.md#scr-token-interest-rate), and increases the utilization rate.

The parameter _maxUtilizationRate_ allows defining a limit on the utilization rate, rejecting lock requests if they leave the utilization rate above this value.

### Unlock

When policies expire or are resolved (with or without payout), the eToken receives an unlock request from other protocol components ([PremiumsAccount](contracts/premiumsaccount.md)). These requests specify the amount to unlock and the paid interest rate.

This operation decreases the scr, modifies the [scr interest rate and token interest rate](liquidity-pools.md#scr-token-interest-rate), and decreases the utilization rate.

Besides the amount and the interest rate, the unlock request receives a third parameter specifying a discrete adjustment. This discrete adjustment will modify the totalSupply, either by accelerating the accrual of the CoC or by fixing an excess in the disbursement.

Adjustments reconcile the fact that a precise amount of CoC has been received when the funds were locked, and those funds are disbursed progressively. The original schedule for this disbursement assumes that the policy will be active for its entire expected duration (i.e., until its expiration date). However, this is not always the case, as the policy might be resolved days or minutes before the expected expiration date. The adjustment takes care of solving this miscalculation. See more about this in the [adjustment note here](policy-lifecycle.md#resolution-with-payout).

### Internal loan

The solvency capital provided by the eTokens won't be touched most of the time when the losses are equal to or less than expected. But when losses exceed expectations, the funds in the eToken will be used to cover the losses.

These funds will be given as an internal loan between the eToken (lender) and the PremiumsAccount (borrower). They will be repaid in the future when/if the losses are less than expected and the PremiumsAccount has a surplus.

The loan comes with interests defined in the _poolLoanInterestRate_ parameter.

This operation decreases the total supply producing a negative return to the LPs.

### Internal loan repayment

When policies expire without a claim, if the PremiumsAccount has an outstanding debt with the eToken, it repays it with the _pure premium_ of the expired policy. This operation is repeated for each expired policy until all the debt has been repaid.

This operation increases the total supply producing a positive return to the LPs.

### Operation Summary

| Operation | SCR | Total Supply | Utilization Rate | Limits |
| --- | --- | --- | --- | --- |
| deposit | = | ↑ | ↓ | minUtilizationRate |
| withdraw | = | ↓ | ↑ | utilizationRate < 100% |
| lock | ↑ | = | ↑ | maxUtilizationRate |
| unlock | ↓ | = | ↓ | none |
| internalLoan | = | ↓ | ↓ | totalSupply or fundsAvailable |
| repayLoan | = | ↑ | ↑ | none |
