from logging import getLogger
from typing import Any

from pydantic import BaseModel, ValidationError

from .. import __identifier__
from ..http import make_http_request, HttpError
from ..schemas.orders import Order


class ParameterSchema(BaseModel):
    """Represent the possible Parameters that can be passed to the node."""

    order_id: int


class ContextSchema(BaseModel):
    """Represent the required context variables."""

    #: the FQDN of the store front. e.g. heyhorse.myshopify.com
    myshopify_domain: str
    #: the authentication token to access the order api via REST
    shopify_token: str


async def get_order(
    message: dict[str, Any],
    _context: dict[str, Any],
) -> dict[str, Any]:
    """Retrieve a single order from Shopify."""
    logger = getLogger(f"{__identifier__}.get_order")
    logger.setLevel(10)
    try:
        parameters = ParameterSchema(**message)
    except ValidationError:
        raise

    try:
        context = ContextSchema(**_context)
    except ValidationError:
        raise

    # Query shopify for the order
    try:
        ret_val = make_http_request(
            logger,
            myshopify_domain=context.myshopify_domain,
            api_path=f"/orders/{parameters.order_id}.json",
            api_token=context.shopify_token,
            method="GET",
        )
    except HttpError:
        raise

    order = Order(**ret_val.json()["order"])

    # Construct a standard reply

    return order.dict(by_alias=True)
