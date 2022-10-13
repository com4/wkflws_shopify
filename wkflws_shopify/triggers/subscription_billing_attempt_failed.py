import json
import sys
from typing import Any


async def subscription_billing_attempt_failed(
    data: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    """Trigger after Shopify fails to bill for a subscription.

    Args:
        data: The message payload
        context: Contextual information about the workflow being executed.
    """
    # all data preparation is completed by the trigger's event handler.
    return data


if __name__ == "__main__":  # pragma: no cover
    import asyncio

    try:
        message = json.loads(sys.argv[1])
    except IndexError:
        raise ValueError("missing required `message` argument") from None

    try:
        context = json.loads(sys.argv[2])
    except IndexError:
        raise ValueError("missing `context` argument") from None

    output = asyncio.run(subscription_billing_attempt_failed(message, context))

    if output is None:
        sys.exit(1)

    print(json.dumps(output))
