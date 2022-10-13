"""Define trigger listener for Shopify's subscription_billing_attempt/failed webhook."""
import json
from typing import Any, Optional
from uuid import uuid4


from wkflws.events import Event
from wkflws.exceptions import WkflwExecutionException
from wkflws.http import http_method, Request, Response
from wkflws.logging import getLogger
from wkflws.triggers.webhook import WebhookTrigger

from . import schemas
from .. import __identifier__, __version__


async def process_webhook_request(
    request: Request,
    response: Response,
) -> Optional[Event]:
    """Accept and process a Pandadoc webhook request returning an event."""
    # logger = getLogger(f"{__identifier__}.triggers.process_webhook_request")

    metadata: dict[str, str] = {}
    metadata.update(request.headers)

    data = json.loads(request.body)

    # This is in subscription_billing_attempt/*; maybe others.
    identifier = str(data.get("idempotency_key", uuid4()))

    return Event(identifier, metadata, data)


async def accept_event(event: Event) -> tuple[Optional[str], dict[str, Any]]:
    """Accept and process data from the event bus."""
    logger = getLogger(f"{__identifier__}.triggers.accept_event")

    event_type = event.metadata.get("x-shopify-topic", None)

    # shopify should always return a dictionary as the payload. (also this makes the
    # type checker happy.)
    if not isinstance(event.data, dict):
        raise WkflwExecutionException("Unexpected data type for event")

    if event_type == "subscription_billing_attempt/failed":
        data = schemas.SubscriptionBillingAttempt(**event.data)

        return (
            "wkflws_shopify.triggers.subscription_billing_attempt_failed",
            data.dict(by_alias=True),
        )
    else:
        logger.warning(
            f"Event type '{event_type}' not supported in event id "
            f"{event.identifier}"
        )
        return None, {}


webhook = WebhookTrigger(
    client_identifier=__identifier__,
    client_version=__version__,
    process_func=accept_event,
    routes=(
        (
            (http_method.POST,),
            "/shopify/webhook/",
            process_webhook_request,
        ),
    ),
)
