# Reference

* [PolicyPool](policypool.md) - The PolicyPool is the main contract that keeps track of active policies and receives the spending allowances.
* [EToken](etoken.md) - This is an ERC20 compatible contract that represents the capital of each liquidity provider in a given pool.
* [WEToken](wetoken.md) - Non-rebasing ERC-4626 wrapper for an eToken.
* [ILPWhitelist](ilpwhitelist/) - Whitelist contracts controlling who can provide liquidity.
* [Cooler](cooler/) - Optional component that handles the cooldown required before withdrawing from an eToken.
* [PremiumsAccount](premiumsaccount.md) - The risk modules are grouped in premiums accounts that keep track of the pure premiums (active and earned) their policies.
* [RiskModule](riskmodule.md) - Contract that manages the insurance products of the protocol, responsible for injecting policies and policy resolution.
* [Underwriters](underwriters/) - Contracts that validate, price and build the policies, plugged into a RiskModule.
