# wkflws_shopify
This node provides triggers and actions for interacting with a Shopify store front.

## wkflws_shopify.triggers.subscription_billing_attempt_failed
Trigger for when a billing attempt has failed on a recurring subscription.

### Example Output
```json
{
  "order_id": 1,
  "graphql_order_id": "gid://shopify/Order/1",
  "subscription_contract_id": 9998878778,
  "graphql_subscription_contract_id": "gid://shopify/SubscriptionContract/9998878778",
  "ready": true,
  "error_message": null,
  "error_code": null
}
```

## wkflws_shopify.get_order
Retrieve a single order from Shopify.

### Context Properties
The following context properties are required for this node.

| name | type | description |
|-|-|-|
| `myshopify_domain` | `str` | the FQDN of the store front. e.g. `heyhorse.myshopify.com` |
| `shopify_token` | `str` | the authentication token to access the order api via REST. |

### Parameters

| name | required | type |description |
|-|-|-|-|
| `order_id` | ✅ | `int` | the id of the order to retrieve |

### Example Input
```json
{
  "order_id": 1
}
```

### Example Output
```json
```
