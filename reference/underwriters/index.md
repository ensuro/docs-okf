# Underwriters

* [IUnderwriter](overview.md) - Interface for contracts that validate policy inputs and convert them into the fields required to create a policy.
* [FullTrustedUW](fulltrusteduw.md) - Underwriter that just decodes what it receives; access validations are done on the RiskModule methods.
* [FullSignedUW](fullsigneduw.md) - Underwriter that decodes the input and requires it to be signed by an authorized account.
