---
type: Guide
title: Callback notifications
description: These callbacks are made from Ensuro's system back to partner's systems to notify about events on policies. It's mainly used for asynchronous policy creation/resolution/cancellation/replacement
tags:
- api
- webhooks
timestamp: '2026-07-21T16:30:11+00:00'
---

# Callback notifications

To get notifications from our system you will need to provide an HTTPS endpoint that will receive the notifications.

## Retry policy

The endpoint must reply with a status code of 200. Any response status 4xx or 5xx will be considered a rejected message and will be retried later. If the endpoint does not reply within 10 seconds the message will be considered rejected and retried again later.

The first retry is done after 30 seconds, then doubled each time the request fails up to a max delay of 10 minutes. After 10 retries the notification will not be retried anymore.

## Robustness principle and idempotency

You must implement an [idempotent consumer](https://microservices.io/patterns/communication-style/idempotent-consumer.html) to receive notifications from our system.

This means that we guarantee at-least-once delivery, but provide no guarantees about:

* Repeated messages: your system must gracefully handle receiving the same notification twice. For instance, if you receive a `policy/resolved` notification twice, you can just ignore the second notification by returning a 200 status code without further processing.
* Out of order messages: because of the retry policy, you may receive messages in a different order than they were generated. Your system must not expect notification messages in a specific order.

Besides idempotency, you should apply the [robustness principle](https://en.wikipedia.org/wiki/Robustness_principle) when designing your events receiver:

> Be conservative in what you send, be liberal in what you accept

We may add new fields to the notification payload as the protocol evolves, your system should pick what it needs from the payload and simply ignore everything else, instead of failing if a new field is added.

This, of course, only refers to backwards compatible changes like adding new fields. Any backwards-incompatible changes will be rolled out with previous coordination to avoid breaking stuff.

## Notification signature

Notifications will be signed by Ensuro. You should verify this signature to make sure the notification really comes from Ensuro. No other authentication method is supported.

To verify the signature you'll need to recalculate the signature on your end and verify that it matches the signature present in the `X-Ensuro-Signature` header. Here's how to do that:

#### Python

```python
import hmac
from hashlib import sha256

def check_signature(raw_body: bytes, signature: str, sign_secret: str) -> bool:
    """Check HMAC signature

    Arguments:
      - raw_body: the signed message as bytes
      - signature: the signature received along with the message
      - sign_secret: the secret used for signing

    Returns: True if signature checks out, False otherwise.

    Examples:
    >>> check_signature(b"hello world", "500f38dc7f0b1b86b6911e95cb1ad56bb13409937302e1c0f31f5ab1c397d5b6", "T0pS3cret")
    True

    >>> check_signature(b"hello world", "ff73b9fbfcd2454daa91ad3c232c65090713b18651cb5c0c4f39d57ccc87d4bb", "T0pS3cret")
    False
    """
    calculated_digest = hmac.new(bytes(sign_secret, "utf-8"), msg=raw_body, digestmod=sha256).hexdigest()

    return calculated_digest.lower() == signature.lower()
```

#### NodeJS

```javascript
/**
 * Checks that the signature is correct
 * @param {String} rawBody The raw body of the request
 * @param {String} signature The signature to verify
 * @param {String} signSecret The signing secret
 * @returns {Boolean} true if the signature is valid, false otherwise
 */
function checkSignature(rawBody, signature, signSecret) {
  const calculated_signature = createHmac("sha256", signSecret)
    .update(rawBody)
    .digest("hex");
  return calculated_signature === signature;
}
```

You must take the raw body as received from the network, without any additional decoding or processing. This is a common error in NodeJS:

```javascript
const express = require("express");
const app = express();
const port = 3000;

const SIGN_SECRET = "T0pS3cret";

app.use(express.json());

app.post("/notify", (req, res) => {
  const signature = req.get("X-Ensuro-Signature");
  const body = JSON.stringify(req.body); // BAD, don't do this

  if (!checkSignature(body, signature, SIGN_SECRET)) {
    res.status(403).send("Invalid signature");
    return;
  }

  // Process the request
});

app.listen(port, () => {
  console.log(`App started on port ${port}`);
});
```

By first decoding the JSON payload and then encoding it again as JSON you may be modifying the body and the signature will not match. You should instead do something like this:

```javascript
const express = require("express");
const app = express();
const port = 3000;

const SIGN_SECRET = "T0pS3cret";

app.use(
  express.json({
    verify: (req, res, buf) => {
      if (!checkSignature(buf, req.get("X-Ensuro-Signature"), SIGN_SECRET)) {
        throw new Error("Invalid signature");
      }
    },
  })
);

app.post("/notify", (req, res) => {
  // Process the request

  res.send("OK");
});

app.listen(port, () => {
  console.log(`App started on port ${port}`);
});
```

If you aren't using ExpressJS you should check your framework's documentation to find out how to get the raw body of the request for signature validation.

## Notifications

Error notifications will have JSON content with the following structure:

```json
{
    "type": ...
    "data": ...
    "error_detail": ...
}
```

Success notifications will have the following structure:

```json
{
    "type": ...
    "policy": ...
}
```

### Policy Creation

When a policy is successfully created a notification like this one will be sent:

```json
{
    "type": "policy/creation",
    "policy": {
        "actual_payout": null,
        "custom_data": {},
        "ensuro_commission": "9.333260",
        "ensuro_id": "55290711940124341656440333382658655728151858290221369410762348674130909154134",
        "events": [
            {
                "event_type": "creation",
                "log_index": 1,
                "timestamp": "2023-06-28T22:00:00",
                "tx_hash": "0xa1d76042cee072e73778122da8191aeb69c029cd780b67623281fac295945bc7"
            }
        ],
        "expiration": "2023-07-01T19:00:01Z",
        "id": 12,
        "jr_coc": "0.373269",
        "jr_scr": "67.713540",
        "loss_prob": "0.098000000000000000",
        "partner_commission": "0.000000",
        "payout": "1000.200000",
        "premium": "142.363804",
        "pure_premium": "132.326460",
        "quote": null,
        "rm": "/api/riskmodules/0x7A3D6f180ABDAA8C35949a48Cd590bA1c06CDF33/",
        "sr_coc": "0.330815",
        "sr_scr": "120.024000",
        "start": "2023-06-28T22:15:40Z",
        "status": "active",
        "url": "/api/policies/3352/"
    }
}
```

Note the `events` array that holds the creation transaction event.

### Policy resolution

When a policy is successfully resolved a notification like this one will be sent:

```json
{
    "type": "policy/resolution",
    "policy": {
        "actual_payout": "71.350000",
        "custom_data": {},
        "ensuro_commission": "9.333260",
        "ensuro_id": "55290711940124341656440333382658655728151858290221369410762348674130909154134",
        "events": [
            {
                "event_type": "creation",
                "log_index": 1,
                "timestamp": "2023-06-28T22:00:00",
                "tx_hash": "0xa1d76042cee072e73778122da8191aeb69c029cd780b67623281fac295945bc7"
            },
            {
                "event_type": "resolution",
                "log_index": 2,
                "timestamp": "2023-06-28T22:15:00Z",
                "tx_hash": "0x40652b64a9f82212c3113f78f9b47c54a7c261495877d6176585b8b160d99632"
            }
        ],
        "expiration": "2023-07-01T19:14:45Z",
        "id": 13,
        "jr_coc": "0.373269",
        "jr_scr": "67.713540",
        "loss_prob": "0.098000000000000000",
        "partner_commission": "0.000000",
        "payout": "1000.200000",
        "premium": "142.363804",
        "pure_premium": "132.326460",
        "quote": null,
        "rm": "/api/riskmodules/0x7A3D6f180ABDAA8C35949a48Cd590bA1c06CDF33/",
        "sr_coc": "0.330815",
        "sr_scr": "120.024000",
        "start": "2023-06-28T22:15:40Z",
        "status": "customer_won",
        "url": "/api/policies/3352/"
    }
}
```

Note the `events` array that now holds the resolution transaction. Another important field to notice is the `actual_payout` which holds the amount for which the policy was resolved, as opposed to the `payout` field that holds the policy's original max payout.

### Failed policy creation notification

When a policy's creation has an unrecoverable error a notification like the following will be sent:

```json
{
    "type": "policy/creation/failed",
    "error_detail": "execution reverted: Policy exceeds max duration",
    "data": {
        "quote": {
            "data": {
                "internalId": "78fb131b-95f9-4d9d-bc20-f29ea1952631"
            },
            "data_hash": "0x5bd832fcafbbbc0c96769b60bc52aaaece5a3f79b02255c94f1aaf2806385e6a",
            "ensuro_id": "55290711940124341656440333382658655728151858290221369410762348674130909154134",
            "loss_prob": "0.098",
            "payout": "1000.2",
            "policy_expiration": 1735335367,
            "premium": null,
            "quote_id": "78fb131b-95f9-4d9d-bc20-f29ea1952631",
            "risk_module": "0x7a3d6f180abdaa8c35949a48cd590ba1c06cdf33",
            "valid_until": 1688071049
        },
        "signature": {
            "hash": "0xe78aceeecf645ce31115a891f2386a4c91f11a40526bfe6c829846cb5d6ce829",
            "r": "0xb244fb8ac61181044de43332dc5aae339aa568c474070d4fbf7491837b432777",
            "vs": "0xd168c60a655ae7c6d64229ca466de342cab5308fe257b9a360039acd103bd0f0"
        }
    }
}
```

The data is the same that you received when calling the `new-policy` endpoint to request the policy creation.

### Failed policy resolution notification

When a policy's resolution has an unrecoverable error a notification like the following will be sent:

```json
{
    "type": "policy/resolution/failed",
    "error_detail": "execution reverted: Policy not found",
    "data": {
        "ensuro_id": "55290711940124341656440333382658655728151858290221369410762348674130909154134",
        "payout": "10000",
        "policy": {
            "id": 12,
            "url": "https://offchain-v2.ensuro.co/api/policies/12/",
            "ensuro_id": "55290711940124341656440333382658655728151858290221369410762348674130909154134",
            "rm": "https://offchain-v2.ensuro.co/api/riskmodules/0x7A3D6f180ABDAA8C35949a48Cd590bA1c06CDF33/",
            "quote": null,
            "premium": "2.191125",
            "payout": "28.980000",
            "loss_prob": "0.052000000000000000",
            "jr_scr": "2.022804",
            "sr_scr": "4.057200",
            "pure_premium": "2.034396",
            "ensuro_commission": "0.143710",
            "partner_commission": "0.000000",
            "jr_coc": "0.006500",
            "sr_coc": "0.006519",
            "start": "2023-06-27T19:00:10Z",
            "expiration": "2023-06-29T12:00:00Z",
            "status": "customer_won",
            "actual_payout": "28.980000",
            "events": [
                {
                    "tx_hash": "0xa1d76042cee072e73778122da8191aeb69c029cd780b67623281fac295945bc7",
                    "timestamp": "2023-06-27T19:47:10Z",
                    "event_type": "creation",
                    "log_index": 11
                },
                {
                    "tx_hash": "0x40652b64a9f82212c3113f78f9b47c54a7c261495877d6176585b8b160d99632",
                    "timestamp": "2023-06-28T18:35:50Z",
                    "event_type": "resolution",
                    "log_index": 3
                }
            ]
        }
    }
}
```

In this example the policy resolution failed because the policy is already resolved.

### Policy Cancellation

When a policy is successfully cancelled a notification like this one will be sent:

```json
{
    "type": "policy/cancellation",
    "policy": {
        "custom_data": {},
        "premium": "11.088408",
        "refund_data": {
            "pure_premium_refund": "8.181301",
            "jr_coc_refund": "0.296398",
            "sr_coc_refund": "0.244912"
        },
        "replaces": null,
        "jr_scr": "12.536699",
        "ensuro_id": "67812604429973654391505078897904107021838970640758236538653164245079165055139",
        "loss_prob": "0.032907384368209150",
        "start": "2026-04-01T11:37:35Z",
        "bucket_id_hash": "0x19b4828aecf8cdc773574017daba4bef95cd6c33bcb1b1672af99e8c0e2b6342",
        "id": 25,
        "rm": "/api/riskmodules/0x95eC92eE7539D2Fe38f68d593f1451fa88452891/",
        "partner_commission": "0.000000",
        "updated_at": "2026-06-27T01:34:23.256090Z",
        "ensuro_commission": "1.008037",
        "expiration": "2026-07-31T14:00:00Z",
        "events": [
            {
                "event_type": "creation",
                "log_index": 328,
                "tx_hash": "0x11280a0d2c19a6a010907d584b6d38eb2a677cae62596257e97e1ffe71d0428d",
                "timestamp": "2026-04-01T11:37:35Z"
            },
            {
                "event_type": "cancellation",
                "log_index": 467,
                "tx_hash": "0x08291cfd46277fa0f630f0747efb1f0c2956fca6dee62cd7e2217c3c073ccfb8",
                "timestamp": "2026-06-27T01:34:11Z"
            }
        ],
        "replaced_by": null,
        "quote": {
            "bucket_id": "Brushfire",
            "data": {},
            "quote_id": "e82c1038-24e9-4680-bd5b-f39d04cf1cbd",
            "url": "/api/quotes/203/",
            "data_hash": "0xe8b6d5974aa7cb21ce30763bf4e0aa7f465d5d95397aa64d7a2a2deab21130a3",
            "valid_until": "2026-04-06T10:52:09Z",
            "payout": "207.180000"
        },
        "url": "/api/policies/25/",
        "sr_coc": "0.859221",
        "status": "cancelled",
        "payout": "207.180000",
        "sr_scr": "20.718000",
        "jr_coc": "1.039849",
        "actual_payout": "0.000000",
        "pure_premium": "8.181301"
    }
}
```

The `refund_data` field contains the amounts refunded for each component (pure premium, jr coc, sr coc). The `events` array now includes a `cancellation` event with its corresponding transaction hash and timestamp.

### Failed policy cancellation notification

When a policy's cancellation has an unrecoverable error a notification like the following will be sent:

```json
{
    "type": "policy/cancellation/failed",
    "data": {
        "cancellation": {
            "policy_data": {
                "ensuro_id": "55618312493875190273648915273846192736451827364519273645192736451927364519273",
                "payout": "2500.000000",
                "jr_scr": "1200.000000",
                "sr_scr": "600.000000",
                "loss_prob": "0.034200000000000000",
                "pure_premium": "85.500000",
                "ensuro_commission": "12.500000",
                "partner_commission": "8.750000",
                "jr_coc": "22.300000",
                "sr_coc": "11.150000",
                "start": 1718265600,
                "expiration": 1718870400
            },
            "refunds": {
                "pure_premium": "42.750000",
                "jr_coc": "11.150000",
                "sr_coc": "5.575000"
            }
        },
        "signature": {
            "hash": "0x3a8e7b2c1d4f5e6a9b0c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7",
            "r": "0x7f6e5d4c3b2a109887766554433221100ffeeddccbbaa9988776655443322110",
            "vs": "0x11223344556677889900112233445566778899aabbccddeeff00112233445566",
            "type": "classic"
        },
        "ensuro_id": "55618312493875190273648915273846192736451827364519273645192736451927364519273",
        "pure_premium_refund": "42.750000",
        "jr_coc_refund": "11.150000",
        "sr_coc_refund": "5.575000"
    },
    "error_detail": "PolicyAlreadyExpired(uint256 policyId)"
}
```

The `data` field contains the original cancellation request including the policy data, refund amounts, and the signature. The `error_detail` field indicates the reason the cancellation failed.

### Policy Replacement

When a policy is successfully replaced by a new one a notification like this one will be sent:

```json
{
    "type": "policy/replacement",
    "policy": {
        "partner_commission": "0.000000",
        "sr_coc": "0.098004",
        "actual_payout": null,
        "jr_scr": "1.856000",
        "start": "2026-07-07T20:32:59Z",
        "expiration": "2026-07-19T19:00:00Z",
        "updated_at": "2026-07-17T21:46:29.351753Z",
        "url": "/api/policies/34319/",
        "status": "replaced",
        "sr_scr": "3.200000",
        "jr_coc": "0.113685",
        "premium": "1.711257",
        "replaced_by": "/api/policies/38289/",
        "quote": {
            "url": "/api/quotes/34458/",
            "valid_until": "2026-07-17T18:43:19Z",
            "bucket_id": "Brushfire.short",
            "quote_id": "068c8d9d-6e45-49ae-80b3-a34a07f09b9e",
            "data": {},
            "data_hash": "0x15d363adc1df08c72d196720345fd9be5cb7bfeea5204961b8bea1b27f95ca44",
            "payout": "32.000000"
        },
        "refund_data": null,
        "pure_premium": "1.344000",
        "id": 34319,
        "custom_data": {},
        "ensuro_commission": "0.155568",
        "replaces": null,
        "events": [
            {
                "log_index": 707,
                "timestamp": "2026-07-07T20:32:59Z",
                "tx_hash": "0x670111d9261360ab1acf254ed74754bd0117fe95a8b2e87b4ae78eff3c43fc55",
                "event_type": "creation"
            },
            {
                "event_type": "replacement",
                "tx_hash": "0xda6340bb82e2372e7b774b939cee35a101510ee18cfbe8f2b1a9fe0c31c30fbf",
                "log_index": 183,
                "timestamp": "2026-07-17T21:45:59Z"
            }
        ],
        "loss_prob": "0.035000000000000000",
        "ensuro_id": "67812604429973654391505078897904107021838970640791551677583465526901792426564",
        "rm": "/api/riskmodules/0x95eC92eE7539D2Fe38f68d593f1451fa88452891/",
        "bucket_id_hash": "0xf70829454d09d7d43e477eb35740c6a838e38b8867261572d7b356d9082e8855",
        "payout": "32.000000"
    }
}
```

The `replaced_by` field contains the URL of the new policy that replaced this one. The `events` array includes a `replacement` event with the corresponding transaction hash. The policy's `status` is set to `"replaced"`.

### Failed policy replacement notification

When a policy's replacement has an unrecoverable error a notification like the following will be sent:

```json
{
    "type": "policy/replacement/failed",
    "data": {
        "old_ensuro_id": "104165209084408127675421213904488324566295479272568976442517413012439276373189",
        "new_policy": {
            "quote": {
                "quote_id": "ed98cf2f-1474-4319-b205-671c8ee80067",
                "data": {},
                "risk_module": "0xe64b6B463c3B3Cb3475fb940B64Ef6f946D6F460",
                "premium_details": {
                    "ensuro_commission": "0.272482",
                    "pure": "2.352000",
                    "sr_coc": "0.230142",
                    "minimum_premium": "2.997304",
                    "jr_coc": "0.142680"
                },
                "params": {
                    "ensuro_coc_fee": "0.1",
                    "jr_coll_ratio": "0.10",
                    "jr_roc": "0.250000000000000000",
                    "moc": "1.2",
                    "ensuro_pp_fee": "0.1",
                    "sr_roc": "0.233884",
                    "coll_ratio": "0.20"
                },
                "loss_prob": "0.035000000000000000",
                "data_hash": "0xfe09dd5deef04f5269490302b060a2c07e9b73338dcd4b18f4480d18b0ac64aa",
                "valid_until": 1784749472,
                "payout": "56.000000",
                "ensuro_id": "104165209084408127675421213904488324566295479272579078779240038076489451463850",
                "bucket_id": "Brushfire",
                "premium": null,
                "policy_expiration": 1789858800
            },
            "signature": {
                "type": "full",
                "hash": "0x83fa840b57ad4f5747cb80cd2be0fb890e94370ca583ea56ed71552d172a0e6a",
                "vs": "0xd800624f54b02cd5feb73df0f3ccecb02a2c83f498ed0c96e6524d4f7c19e6ba",
                "r": "0x604f6f1cc190cbda270c6a496531672c903008d4d4f11fd3d08e8abf25626c87"
            }
        },
        "old_policy": {
            "partner_commission": "0.000000",
            "sr_coc": "0.341610",
            "id": 352136,
            "pure_premium": "1.936203",
            "actual_payout": null,
            "jr_scr": "3.663797",
            "start": "2026-03-25T19:59:25Z",
            "expiration": "2026-09-19T23:00:00Z",
            "ensuro_commission": "0.272481",
            "status": "active",
            "sr_scr": "5.600000",
            "url": "https://offchain-v2.ensuro.co/api/policies/352136/",
            "jr_coc": "0.446997",
            "loss_prob": "0.028812547325078279",
            "ensuro_id": "104165209084408127675421213904488324566295479272568976442517413012439276373189",
            "rm": "https://offchain-v2.ensuro.co/api/riskmodules/0xe64b6B463c3B3Cb3475fb940B64Ef6f946D6F460/",
            "premium": "2.997291",
            "quote": "https://offchain-v2.ensuro.co/api/quotes/374167/",
            "payout": "56.000000"
        }
    },
    "error_detail": "execution reverted: New policy must be greater or equal than old policy"
}
```

The `data` field contains both the `old_policy` that was being replaced and the `new_policy` with its quote and signature. The `error_detail` field indicates the reason the replacement failed.
