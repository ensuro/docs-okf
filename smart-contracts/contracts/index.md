# Contract References

* [PolicyPool](policypool.md) - The PolicyPool is the main contract that keeps track of active policies and receives the spending allowances.
* [EToken](etoken.md) - This is an ERC20 compatible contract that represents the capital of each liquidity provider in a given pool.
* [RiskModule](riskmodule.md) - Abstract contract that manages the insurance products of the protocol, responsible for pricing and resolution of policies.
* [PremiumsAccount](premiumsaccount.md) - The risk modules are grouped in premiums accounts that keep track of the pure premiums (active and earned) their policies.
* [AccessManager](accessmanager.md) - Contract that manages the access control permissions for governance actions.
* [iassetmanager](iassetmanager/) - Asset management strategy contracts for the protocol's reserves.
* [ilpwhitelist](ilpwhitelist/) - Whitelist contracts controlling who can provide liquidity.
* [extensions](extensions/) - Contracts supporting particular use cases, operating outside the core protocol.
