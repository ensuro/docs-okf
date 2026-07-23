---
type: API Reference
title: Pricing API
description: This API is used for policy pricing, creation, resolution, replacement and cancellation.
tags:
- api
- pricing
- reference
timestamp: '2026-07-20T17:31:34-03:00'
spec: assets/openapi/pricing-api.yaml
---

# Pricing API

You should have received a partner-specific URL and credentials to use this API. If you didn't, please contact our support team to set up the required services and credentials.

> **Note:** The bundled specification ([assets/openapi/pricing-api.yaml](../assets/openapi/pricing-api.yaml)) is the newest copy archived from the former GitBook site, but it is known to be incomplete: the documented `POST /example/cancel-policy` operation is missing from it. See the [migration log](../log.md).

# Endpoints

| Method | Path | Summary |
| --- | --- | --- |
| POST | `/example` | Create a new quote |
| OPTIONS | `/example` | Get information about this instance |
| POST | `/example/quote` | Create a new quote |
| POST | `/example/new-policy` | Create a new policy |
| POST | `/example/resolve-policy` | Resolve a policy |
| POST | `/example/replace-policy` | Replace a policy |

# Signatures

For policy creation, resolution, replacement and cancellation the body of the request must be signed.

There's two options available for signing:

* Symmetric: a shared secret will be provided and it has to be used to compute an hmac digest. The digest must be sent in the `X-Ensuro-Signature` of the request.
* Asymmetric: An authorized ethereum account is used to sign the body of the message. This method is safer because only the partner has access to the private key and it does not need to be sent over the internet ever. The signature is computed following the [EIP191](https://eips.ethereum.org/EIPS/eip-191) standard. It must be sent in the `X-EIP191-Signature` header of the request.

Only one of the methods must be used, and "Asymmetric" is the preferred one.

See [our samples repository](https://github.com/ensuro/ensuro-samples-js#webhooks-for-creation-and-resolution) for a js example of how to use each one.

# Citations

[1] [Pricing API OpenAPI specification](../assets/openapi/pricing-api.yaml)
