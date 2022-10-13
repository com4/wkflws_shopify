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
{
  "id": 48829967047,
  "billing_address": {
    "address1": "123 Fake Street",
    "address2": "",
    "city": "Oak Lawn",
    "province": "Illinois",
    "province_code": "IL",
    "zip": "60453",
    "country": "United States",
    "country_code": "US",
    "latitude": "41.725390",
    "longitude": "-87.750750",
    "name": "John Smith",
    "first_name": "John",
    "last_name": "Smith",
    "phone": "(555) 123-4567",
    "company": ""
  },
  "buyer_accepts_marketing": True,
  "cancel_reason": None,
  "cancelled_at": None,
  "cart_token": "68da1ff222b115cf342211fbf182d5fc",
  "checkout_token": "8292bbb46d35c9587f9b50a34bdce5e5",
  "closed_at": None,
  "created_at": "2022-10-13T14:15:00-04:00",
  "currency": "USD",
  "current_total_discounts": "20.00",
  "current_total_price": "570.08",
  "current_subtotal_price": "479.99",
  "current_total_tax": "0.00",
  "customer": {
    "addresses": [],
    "currency": "USD",
    "created_at": "2022-06-28T16:00:44-04:00",
    "default_address": {
      "address1": "123 Fake Street",
      "address2": "",
      "city": "Oak Lawn",
      "province": "Illinois",
      "province_code": "IL",
      "zip": "60453",
      "country": "United States",
      "country_code": "US",
      "latitude": null,
      "longitude": null,
      "name": "John Smith",
      "first_name": "John",
      "last_name": "Smith",
      "phone": "(555) 123-4567",
      "company": ""
    },
    "email": "jsmith@gmail.com",
    "email_marketing_consent": {
      "state": "subscribed",
      "opt_in_level": "single_opt_in",
      "consent_updated_at": None
    },
    "first_name": "John",
    "id": 7913927416923,
    "last_name": "Smith",
    "last_order_id": 6869967970482,
    "last_order_name": "22520",
    "phone": None,
    "sms_marketing_consent": None,
    "state": "enabled",
    "tags": "",
    "tax_exempt": False,
    "total_spent": "814.37",
    "verified_email": True
  },
  "email": "jsmith@gmail.com",
  "landing_site": "/?utm_medium=store-directory&utm_source=summersizzle",
  "line_items": [
    {
      "id": 62103096238871,
      "price": "499.99",
      "product_id": 8672033808842,
      "quantity": 1,
      "requires_shipping": True,
      "sku": "MM-7482",
      "title": "MultiMaster Tool",
      "variant_id": 8766203028238,
      "variant_title": "",
      "vendor": "CLOSEOUT",
      "gift_card": False,
      "total_discount": "0.00",
      "tax_lines": []
    }
  ],
  "name": "22520",
  "note": None,
  "number": 21520,
  "order_number": 22520,
  "phone": None,
  "presentment_currency": "USD",
  "processed_at": "2022-10-13T14:14:58-04:00",
  "referring_site": "",
  "shipping_address": {
    "address1": "123 Fake Street",
    "address2": "",
    "city": "Oak Lawn",
    "province": "Illinois",
    "province_code": "IL",
    "zip": "60453",
    "country": "United States",
    "country_code": "US",
    "latitude": "41.725390",
    "longitude": "-87.750750",
    "name": "John Smith",
    "first_name": "John",
    "last_name": "Smith",
    "phone": "(555) 123-4567",
    "company": ""
  },
  "subtotal_price": "479.99",
  "tags": "",
  "taxes_includes": False,
  "test": False,
  "token": "a36beeb6d4d334ee3078eb9b564858bc",
  "total_discounts": "20.00",
  "total_line_items_price": "499.99",
  "total_outstanding": "0.00",
  "total_price": "570.08",
  "total_tax": "0.00",
  "total_tip_received": "0.00",
  "total_weight": 36287,
  "updated_at": "2022-10-13T14:16:16-04:00",
  "order_status_url": "https://hey.horse/8019189128/orders/a36beeb6d4d334ee3078eb9b564858bc/authenticate?key=c61f1b3c528e953b99bd189278ab7d5e"
}
```
