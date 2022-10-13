import uuid

from wkflws_shopify.triggers import subscription_billing_attempt_failed as sbaf


async def test_subscription_billing_attempt_failed():
    """Test data is returned from failed billing attempt."""
    data = {"a": str(uuid.uuid4())}
    result = await sbaf.subscription_billing_attempt_failed(data, {})

    assert len(data.keys()) == 1, "Unexpected data returned."
    assert (
        data is result
    ), "Expected result of node to be exactly the data that was provided."
