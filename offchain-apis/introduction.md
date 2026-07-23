---
type: Guide
title: Introduction
description: We provide RESTful APIs to our partners for easier integration.
tags:
- api
- integration
timestamp: '2026-07-20T17:31:34-03:00'
---

# Introduction

We provide RESTful APIs to our partners for easier integration. The actions that can be performed through our APIs are:

* Create a new policy
* Resolve an existing policy
* Replace an existing policy
* Cancel an existing policy
* Get the pricing and optionally obtain a signature to create a policy onchain
* Query policy details

Some of these operations are asynchronous, so partners can also set up to receive callback notifications with the results of the operations.

## Quickstart Guide

Integrating with our APIs is really simple. The first step is on our end, setting up the necessary services and credentials. Once that's done you'll get four things:

* A URL for the pricing API
* An API key
* A signing secret
* The address of your risk module

You'll need all of these to properly integrate.

### Your first call to our service: pricing a policy

On your first call you'll just need the URL and the API key. This endpoint will price a policy without creating or signing anything:

#### Shell

```sh
curl --request POST \
  --url "$URL/quote?unsigned" \
  --header 'Content-Type: application/application/json' \
  --header 'X-API-Key: $API_KEY' \
  --data '{"payout": "100.98","expiration": "2024-12-31T21:36:07.211025Z","data": {"pricing": "general"}}'
```

#### Python

```python
import requests
import json

URL = "..."
API_KEY = "secret"

data = {"pricing": "general"}

response = requests.post(
    f"{URL}/quote",
    headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    params={"unsigned": True},
    data=json.dumps({"payout": "100.98", "expiration": "2024-12-31T21:36:07.211025Z", "data": data}),
)

print(json.dumps(response.json(), indent=2))
```

#### NodeJS

```javascript
const axios = require("axios");

const URL = "...";
const API_KEY = "secret";

async function printQuote() {
  const data = {
    pricing: "Bedwin",
    blissid: "c5629d49-cd6f-4ccc-8a58-b46637988e51",
  };

  const response = await axios({
    method: "post",
    url: `${URL}/quote`,
    headers: { "X-API-Key": API_KEY, "Content-Type": "application/json" },
    params: { unsigned: true },
    data: { payout: "100.98", expiration: "2024-12-31T21:36:07.211025Z", data },
  });

  console.log(response.data);
}

printQuote()
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
```

Notice that the specific parameters that you need to send on the call will depend on the pricing structure and settings, you should've received more specific instructions about what to include in the `data` object.

Some parameters will always be required:

* `payout` is the policy's max payout in USD.
* `expiration` is the policy's expiration. The example uses a UTC timestamp, but you can pick the timezone that's better for your business.

The response will look something like this:

```
{
  bucket_id: 'general',
  contract_address: '0x0d175CB042dd6997ac37588954Fc5A7b8bab5615',
  data_hash: '0x469428e566ecf36d57bc13cd75446eec1cf36c2b89ddc2d4e610280ed607ae03',
  ensuro_id: '5921344226728579096291186784487329498769731945547014779449079388463409114627',
  expiration: 1735680967,
  loss_prob: '0.0436',
  premium: null,
  premium_details: {
    ensuro_commission: '0.692791',
    jr_coc: '2.130666',
    minimum_premium: '9.822071',
    pure: '5.50341',
    sr_coc: '1.495204'
  },
  quote_id: 'c5629d49-cd6f-4ccc-8a58-b46637988e51',
  valid_until: 1716311048
}
```

You can check the API reference for a detailed description of each, but the most important ones are:

* `ensuro_id`: this will be the policy ID on our system, it identifies each policy univocally across our protocol.
* `loss_prob`: this is the loss probability assigned to the policy. When testing out your integration you should validate that this loss probability matches the pricing set forth for the product.
* `premium_details` : this is a breakdown of the premium as per the current pricing.

If you remove the `unsigned` parameter from the call to `/quote` you will get an additional field with the `signature` for the quote. With this signature you can call our smart contract to create a policy.

### Creating a policy

Although you can obtain signed quotes and use those to create policies on the blockchain, it's more practical to just create the policies directly by calling our API.

To do this, you'll have to sign the body of your request using an HMAC signature.

#### Shell

```sh
URL="..."
API_KEY="secret"
SIGN_SECRET="T0pS3cret"

body='{"payout": "100.98", "expiration": "2024-12-31T14:21:55+00:00", "data": {"pricing": "general"}}'
signature=$(echo -n "$body" | openssl dgst -sha256 -hmac "$SIGN_SECRET" | sed 's/^.*= //')

curl --request POST \
  --url "$URL/new-policy" \
  --header 'Content-Type: application/json' \
  --header "X-API-Key: $API_KEY" \
  --header "X-Ensuro-Signature: $signature" \
  --data "$body"
```

#### Python

```python
import requests
import json
import hmac
from hashlib import sha256

URL = "..."
API_KEY = "secret"
SIGN_SECRET = "T0pS3cret"

data = {"pricing": "general"}

raw_request = json.dumps(
    {
        "payout": "100.98",
        "expiration": "2024-12-31T21:36:07.211025Z",
        "data": data,
    }
).encode("utf-8")
digest = hmac.new(bytes(SIGN_SECRET, "utf-8"), msg=raw_request, digestmod=sha256).hexdigest()
response = requests.post(
    f"{URL}/new-policy",
    headers={
        "X-API-Key": API_KEY,
        "X-Ensuro-Signature": digest,
        "Content-Type": "application/json",
    },
    data=raw_request,
)

print(json.dumps(response.json(), indent=2))
```

#### NodeJS

```javascript
const axios = require("axios");
const { createHmac } = require("crypto");

const URL = "...";
const API_KEY = "secret";
const SIGN_SECRET = "T0pS3cret";

async function createNewPolicy() {
  const data = { pricing: "general" };
  const body = {
    payout: "100.98",
    expiration: "2024-12-31T21:36:07.211025Z",
    data,
  };
  const jsonBody = JSON.stringify(body);

  const signature = createHmac("sha256", SIGN_SECRET)
    .update(jsonBody)
    .digest("hex");

  const response = await axios({
    method: "post",
    url: `${URL}/new-policy`,
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
      "X-Ensuro-Signature": signature,
    },
    data: jsonBody,
  });

  console.log(response.data);
}

createNewPolicy()
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });

```

> **Note:** The returned object will be the same as when calling `/quote`. You should take note of the `ensuro_id` because you'll need it to resolve policies later on.

### Resolving a policy

You can resolve a policy with any payout up to the max payout established on policy creation. This transfers the payout to the policy owner and releases the rest of the locked capital for use in other policies.

Here as well you'll need to sign the body of the request.

#### Shell

```sh
URL="..."
API_KEY="secret"
SIGN_SECRET="T0pS3cret"

body='{"payout": "100.98", "ensuro_id": "5921344226728579096291186784487329498769731945547014779449079388463409114627"}'
signature=$(echo -n "$body" | openssl dgst -sha256 -hmac "$SIGN_SECRET" | sed 's/^.*= //')

curl --request POST \
  --url "$URL/resolve-policy" \
  --header 'Content-Type: application/json' \
  --header "X-API-Key: $API_KEY" \
  --header "X-Ensuro-Signature: $signature" \
  --data "$body"

```

#### Python

```python
import requests
import json
import hmac
from hashlib import sha256

URL = "..."
API_KEY = "secret"
SIGN_SECRET = "T0pS3cret"

raw_request = json.dumps(
    {
        "payout": "100.98",
        "ensuro_id": "5921344226728579096291186784487329498769731945547014779449079388463409114627",
    }
).encode("utf-8")
digest = hmac.new(bytes(SIGN_SECRET, "utf-8"), msg=raw_request, digestmod=sha256).hexdigest()
response = requests.post(
    f"{URL}/resolve-policy",
    headers={
        "X-API-Key": API_KEY,
        "X-Ensuro-Signature": digest,
        "Content-Type": "application/json",
    },
    data=raw_request,
)

print(json.dumps(response.json(), indent=2))
```

#### NodeJS

```javascript
const axios = require("axios");
const { createHmac } = require("crypto");

const URL = "...";
const API_KEY = "secret";
const SIGN_SECRET = "T0pS3cret";

async function resolvePolicy() {
  const body = {
    payout: "100.98",
    ensuro_id: "5921344226728579096291186784487329498769731945547014779449079388463409114627",
  };
  const jsonBody = JSON.stringify(body);

  const signature = createHmac("sha256", SIGN_SECRET)
    .update(jsonBody)
    .digest("hex");

  const response = await axios({
    method: "post",
    url: `${URL}/resolve-policy`,
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
      "X-Ensuro-Signature": signature,
    },
    data: jsonBody,
  });

  console.log(response.data);
}

resolvePolicy()
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });

```

You should get a 200 response with this json content:

```json
{"status":"QUEUED"}
```

And the policy should get resolved on the blockchain shortly afterward.

As you can see, all operations done through our API are asynchronous. You should set up your own HTTP endpoint where you can receive [notifications about the status of the operations](notification-webhooks.md).

### Replacing a policy

You can replace an active policy with a new one. This is useful when the policy parameters need to be updated (e.g. changed payout or expiration). The old policy is marked as replaced and a new policy is created with the updated parameters.

The replacement policy must have a payout greater than or equal to the original policy's payout, and an expiration greater than or equal to the original policy's expiration.

The request body includes all the same fields as creating a policy, plus the `old_ensuro_id` of the policy being replaced. You'll need to sign the body of the request.

#### Shell

```sh
URL="..."
API_KEY="secret"
SIGN_SECRET="T0pS3cret"

body='{"payout": "120.50", "expiration": "2024-12-31T14:21:55+00:00", "data": {"pricing": "general"}, "old_ensuro_id": "5921344226728579096291186784487329498769731945547014779449079388463409114627"}'
signature=$(echo -n "$body" | openssl dgst -sha256 -hmac "$SIGN_SECRET" | sed 's/^.*= //')

curl --request POST \
  --url "$URL/replace-policy" \
  --header 'Content-Type: application/json' \
  --header "X-API-Key: $API_KEY" \
  --header "X-Ensuro-Signature: $signature" \
  --data "$body"
```

#### Python

```python
import requests
import json
import hmac
from hashlib import sha256

URL = "..."
API_KEY = "secret"
SIGN_SECRET = "T0pS3cret"

data = {"pricing": "general"}

raw_request = json.dumps(
    {
        "payout": "120.50",
        "expiration": "2024-12-31T21:36:07.211025Z",
        "data": data,
        "old_ensuro_id": "5921344226728579096291186784487329498769731945547014779449079388463409114627",
    }
).encode("utf-8")
digest = hmac.new(bytes(SIGN_SECRET, "utf-8"), msg=raw_request, digestmod=sha256).hexdigest()
response = requests.post(
    f"{URL}/replace-policy",
    headers={
        "X-API-Key": API_KEY,
        "X-Ensuro-Signature": digest,
        "Content-Type": "application/json",
    },
    data=raw_request,
)

print(json.dumps(response.json(), indent=2))
```

#### NodeJS

```javascript
const axios = require("axios");
const { createHmac } = require("crypto");

const URL = "...";
const API_KEY = "secret";
const SIGN_SECRET = "T0pS3cret";

async function replacePolicy() {
  const data = { pricing: "general" };
  const body = {
    payout: "120.50",
    expiration: "2024-12-31T21:36:07.211025Z",
    data,
    old_ensuro_id: "5921344226728579096291186784487329498769731945547014779449079388463409114627",
  };
  const jsonBody = JSON.stringify(body);

  const signature = createHmac("sha256", SIGN_SECRET)
    .update(jsonBody)
    .digest("hex");

  const response = await axios({
    method: "post",
    url: `${URL}/replace-policy`,
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
      "X-Ensuro-Signature": signature,
    },
    data: jsonBody,
  });

  console.log(response.data);
}

replacePolicy()
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });

```

> **Note:** The response will be the same as when calling `/new-policy`. The old policy will have its status set to `"replaced"` and the new policy will be created with the updated parameters.

### Canceling a policy

You can cancel an active policy. This will mark the policy as cancelled and refund the applicable portions of the premium (pure premium, jr coc, and sr coc).

The refund values returned by the API may be `MAXUINT256` (2**256-1). This means that the max undisbursed cost of capital (jr coc and sr coc) at the time of execution will be refunded, rather than a fixed amount calculated at request time.

The request body only requires the `ensuro_id` of the policy to cancel. You'll need to sign the body of the request.

#### Shell

```sh
URL="..."
API_KEY="secret"
SIGN_SECRET="T0pS3cret"

body='{"ensuro_id": "5921344226728579096291186784487329498769731945547014779449079388463409114627"}'
signature=$(echo -n "$body" | openssl dgst -sha256 -hmac "$SIGN_SECRET" | sed 's/^.*= //')

curl --request POST \
  --url "$URL/cancel-policy" \
  --header 'Content-Type: application/json' \
  --header "X-API-Key: $API_KEY" \
  --header "X-Ensuro-Signature: $signature" \
  --data "$body"
```

#### Python

```python
import requests
import json
import hmac
from hashlib import sha256

URL = "..."
API_KEY = "secret"
SIGN_SECRET = "T0pS3cret"

raw_request = json.dumps(
    {
        "ensuro_id": "5921344226728579096291186784487329498769731945547014779449079388463409114627",
    }
).encode("utf-8")
digest = hmac.new(bytes(SIGN_SECRET, "utf-8"), msg=raw_request, digestmod=sha256).hexdigest()
response = requests.post(
    f"{URL}/cancel-policy",
    headers={
        "X-API-Key": API_KEY,
        "X-Ensuro-Signature": digest,
        "Content-Type": "application/json",
    },
    data=raw_request,
)

print(json.dumps(response.json(), indent=2))
```

#### NodeJS

```javascript
const axios = require("axios");
const { createHmac } = require("crypto");

const URL = "...";
const API_KEY = "secret";
const SIGN_SECRET = "T0pS3cret";

async function cancelPolicy() {
  const body = {
    ensuro_id: "5921344226728579096291186784487329498769731945547014779449079388463409114627",
  };
  const jsonBody = JSON.stringify(body);

  const signature = createHmac("sha256", SIGN_SECRET)
    .update(jsonBody)
    .digest("hex");

  const response = await axios({
    method: "post",
    url: `${URL}/cancel-policy`,
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
      "X-Ensuro-Signature": signature,
    },
    data: jsonBody,
  });

  console.log(response.data);
}

cancelPolicy()
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });

```

> **Note:** The response will contain the `ensuro_id`, a `refunds` object with the refunded amounts for each component (`pure_premium`, `jr_coc`, `sr_coc`), and a `signature` for the cancellation.

### Currency and Forex handling

By default, all policies are priced in USD. However, partners can send payouts in other currencies if supported by our configuration. Currency conversion is handled automatically by our system.

The currency field can be included at the same level as payout and expiration. If currency is not provided, it is assumed to be USD.

#### Supported currencies

Each API instance supports a specific set of currencies, as defined in the agreed pricing configuration.

If a currency is supported, it will be automatically converted to USD. If a currency is not supported, the request will be rejected.

If you're unsure which currencies are available for your integration, please refer to your pricing configuration or contact us.

#### Conversion process

When a non-USD currency is used, the system must account for potential fluctuations in the exchange rate between the moment a policy is created and when it is resolved. To do this:

1. The payout is converted to USD using the current rate.
2. Two adjustment factors are applied: max appreciation and expected appreciation

This mechanism exists because exchange rates can change over time. As a result, the USD value of a payout at resolution time may be higher than it was at creation time. For example, a policy created for 150,000 JPY might initially convert to 970 USD, but later, due to exchange rate movements, the same 150,000 JPY could be equivalent to 1,000 USD. If the policy’s maximum payout were fixed at 970 USD, it would not be possible to fully resolve the policy and pay the claim.

To prevent this, the system increases the maximum payout using the max appreciation factor, ensuring that the policy can always be fully resolved even if exchange rates move unfavorably. At the same time, the premium is not arbitrarily increased: it is calculated using the expected appreciation, which reflects a more realistic estimate of currency movement.

As a result, the final payout (max payout) is determined using the max appreciation, while the premium is calculated based on the expected appreciation.

**Example**

The behavior described above can vary depending on the configuration of expected and max appreciation.

Given:

* payout = 100 EUR
* EUR/USD = 1.1
* expected = 1.0
* max = 1.1

Then:

* Converted payout = 110 USD
* Final payout (max payout) = 110 × 1.1 = 121 USD
* Premium is calculated based on the converted payout (110 USD)

If the exchange rate moves unfavorably (for example, if 100 EUR becomes worth more in USD at resolution time), the policy can still be fully resolved because the max payout was increased.
