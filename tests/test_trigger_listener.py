import json

import pytest
from wkflws.events import Event
from wkflws.exceptions import WkflwExecutionException
from wkflws.http import Request, Response

from wkflws_shopify.triggers import listener

SUBSCRIPTION_BILLING_FAIL_PAYLOAD = """{
  "id": null,
  "admin_graphql_api_id": null,
  "idempotency_key": "9a453d81-d41d-403e-806f-714dee215ff9",
  "order_id": 1,
  "admin_graphql_api_order_id": "gid://shopify/Order/1",
  "subscription_contract_id": 9998878778,
  "admin_graphql_api_subscription_contract_id": "gid://shopify/SubscriptionContract/9998878778",
  "ready": true,
  "error_message": null,
  "error_code": null
}"""  # noqa

MYSHOPIFY_DOMAIN = "heyhorse.myshopify.com"
SHOPIFY_API_VERSION = "2022-10"


def get_request_headers(shopify_topic: str) -> dict[str, str]:
    """Generate a header payload for the provided shopify topic."""
    return {
        "x-shopify-topic": shopify_topic,
        "x-shopify-shop-domain": MYSHOPIFY_DOMAIN,
        "x-shopify-api-version": SHOPIFY_API_VERSION,
        "x-shopify-webhook-id": "daea8817-0caf-420a-8d03-615277bf5b6a",
    }


async def test_process_webhook_request():
    """Verify the values from a webhook call are expected."""
    headers = get_request_headers("subscription_billing_attempt/failed")
    request = Request(
        "https://wkfl.ws/shopify/webhook/",
        headers,
        SUBSCRIPTION_BILLING_FAIL_PAYLOAD,
    )
    response = Response()

    event = await listener.process_webhook_request(request, response)

    assert event is not None, "Expected a valid event"

    data = json.loads(SUBSCRIPTION_BILLING_FAIL_PAYLOAD)

    assert event.identifier == data["idempotency_key"]
    for header, value in headers.items():
        assert (
            header in event.metadata
        ), f"Missing expected metadata from header: {header}"
        assert (
            event.metadata[header] == value
        ), f"Unexpected value for header {header}: {event.metadata[header]} != {value}"

    assert json.dumps(event.data, sort_keys=True) == json.dumps(
        data, sort_keys=True
    ), "Expecting unaltered payload"


async def test_accept_event__subscription_billing_attempt_failed():
    """Verify subscription_billing_attempt/failed calls the correct node."""
    metadata = get_request_headers("subscription_billing_attempt/failed")
    orig_data = json.loads(SUBSCRIPTION_BILLING_FAIL_PAYLOAD)
    event = Event(
        identifier="abc123",
        metadata=metadata,
        data=orig_data,
    )

    node, data = await listener.accept_event(event)

    assert (
        node == "wkflws_shopify.triggers.subscription_billing_attempt_failed"
    ), "Unexpected node returned for trigger."

    assert len(data.keys()) == 7, (
        "Unexpected number of fields in response. Tests need to be updated to account "
        "for the changes."
    )
    assert data["order_id"] == orig_data["order_id"], "Unexpected change to order_id"
    assert (
        data["graphql_order_id"] == orig_data["admin_graphql_api_order_id"]
    ), "Unexpected change to graphql_order_id"
    assert (
        data["subscription_contract_id"] == orig_data["subscription_contract_id"]
    ), "Unexpected change to subscription_contract_id"
    orig_graphql_sub_id = orig_data["admin_graphql_api_subscription_contract_id"]
    assert (
        data["graphql_subscription_contract_id"] == orig_graphql_sub_id
    ), "Unexpected change to graphql_subscription_contract_id"
    assert data["ready"] == orig_data["ready"], "Unexpected change to ready"
    assert (
        data["error_message"] == orig_data["error_message"]
    ), "Unexpected change to error_message"
    assert (
        data["error_code"] == orig_data["error_code"]
    ), "Unexpected change to error_code"


async def test_accept_event__unknown_event_type():
    """Test for an unknown event type."""
    metadata = get_request_headers("shopify_topic/unknown")
    orig_data = {}
    event = Event(
        identifier="abc123",
        metadata=metadata,
        data=orig_data,
    )

    node, data = await listener.accept_event(event)

    assert node is None, "Expecting no node returned."
    assert len(data.keys()) == 0, "Expecting no data returned."


async def test_accept_event__invalid_payload():
    """Verify checking against an unknown payload."""
    metadata = get_request_headers("shopify_topic/unknown")
    orig_data = list(dict())
    event = Event(
        identifier="abc123",
        metadata=metadata,
        data=orig_data,
    )

    with pytest.raises(WkflwExecutionException):
        await listener.accept_event(event)
