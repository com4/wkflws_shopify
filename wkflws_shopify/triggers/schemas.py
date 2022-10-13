from typing import Optional

from pydantic import BaseModel, Field


class SubscriptionBillingAttempt(BaseModel):
    """Describes a failed billing attempt on a subscription."""

    order_id: int
    admin_graphql_api_order_id: str = Field(alias="graphql_order_id")
    subscription_contract_id: int
    admin_graphql_api_subscription_contract_id: str = Field(
        alias="graphql_subscription_contract_id"
    )
    ready: bool
    error_message: Optional[str] = None
    error_code: Optional[str] = None

    class Config:
        # allows the admin_graphql_api_* fields to be populated by the Shopify payload
        # and be translated to the alias on output (via `.dict(by_alias=True)`)
        allow_population_by_field_name = True
