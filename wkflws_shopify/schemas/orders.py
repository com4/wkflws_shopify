from datetime import datetime
from decimal import Decimal
import enum
from typing import Optional

from pydantic import BaseModel, Field

from . import customer as customer_m  # aliased to fix conflict with `customer` fields.


class CancelReason(str, enum.Enum):
    """Reasons for a Shopify order to be cancelled."""

    customer = "customer"


class LineItemTax(BaseModel):
    """Represents tax information for a line item (taxable_lines)."""

    #: description of the tax
    title: str
    #: amount added to the order
    price: Decimal
    #: the rate of the tax (i.e. rate * 100.0 = tax percentage)
    rate: Decimal
    #: Whether the channel that submitted the tax line is liable for remitting. A value
    #: of null indicates unknown liability for the tax line.
    channel_liable: Optional[bool] = None


class LineItem(BaseModel):
    """Represent a line item of an order."""

    #: id of the line item.
    id_: int = Field(alias="id")
    #: price of item before discounts.
    price: Decimal
    #: id of the product. can be None if the product was deleted later
    product_id: Optional[int]
    #: number of products ordered
    quantity: int
    #: whether the item requires shipping
    requires_shipping: bool
    #: Stock Keeping Unit
    sku: str
    #: Description of the product (e.g. T-shirt)
    title: str
    #: Variant identifier
    variant_id: int
    #: Description of the variant  (e.g. Blue)
    variant_title: str
    #: name of the supplier
    vendor: str
    #: Is the item a gift card. If it is taxes and shipping do not apply
    gift_card: bool
    #: Total discount amount
    total_discount: Decimal
    #: all/any taxes applied to this line item
    tax_lines: list[LineItemTax] = []


class Order(BaseModel):
    """Represent an Order.

    This is loosely based on the Shopify Order object api v2022-10.
    """

    # https://shopify.dev/api/admin-rest/2022-04/resources/order

    #: This is the id used for the API. This is different from order_number the shop
    #: uses.
    api_id: int = Field(alias="id")
    billing_address: customer_m.Address
    #: Whether the customer consented to recieve email updates from the shop.
    buyer_accepts_marketing: bool = False
    #: the reason the order was cancelled
    cancel_reason: Optional[CancelReason]  # Shopify seems to always pass this.
    #: date and time the order was cancelled. None if the order was not cancelled.
    cancelled_at: Optional[datetime]
    #: unique token for the cart associated with this order.
    cart_token: str
    #: unique token for the checkout associated with this order.
    checkout_token: str
    #: date and time when the order was closed. None if the order is not closed.
    closed_at: Optional[datetime]
    #: date and time when the order was created.
    created_at: datetime
    #: ISO 4217 three-letter code of the shop's currency.
    currency: str
    #: The current total discounts after edits, returns, refunds.
    current_total_discounts: Decimal
    #: The current total price after edits, returns, refunds.
    current_total_price: Decimal
    #: The current subtotal price after edits, returns, refunds.
    current_subtotal_price: Decimal
    #: The current total tax after edits, returns, refunds.
    current_total_tax: Decimal
    #: An order may not have a customer if it was created through the Shopify POS
    customer: Optional[customer_m.Customer] = None
    #: the customer's email address
    email: str
    #: URL of the page the user landed when they entered the shop
    landing_site: Optional[str] = None
    #: Information about the items ordered
    line_items: list[LineItem] = []
    #: name of the order
    name: str
    #: note attached by the shop owner to the order
    note: Optional[str] = None
    #: The order's position in the shop's count of orders starting at 1.
    number: int
    #: The order 's position in the shop's count of orders starting at 1001.
    order_number: int
    #: Customer's phone for receiving SMS.
    phone: Optional[str] = None
    #: Currency that was displayed to the customer.
    presentment_currency: str
    #: processed date time displayed on orders
    processed_at: datetime
    #: Site which referred the customer.
    referring_site: Optional[str] = None
    #: Mailing address where orders will be shipped
    shipping_address: customer_m.Address
    #: price after discounts but before shipping,taxes (see taxes_included),etc
    subtotal_price: Decimal
    #: tags attached to the order as CSV
    tags: str = ""
    #: whether taxes are included in the subtotal
    taxes_includes: bool = False
    #: whether this is a test order
    test: bool = False
    #: unique value when referencing this order
    token: str
    #: total amount of discounts applied to the order
    total_discounts: Decimal
    #: total amount of all line items in the shop's default currency
    total_line_items_price: Decimal
    #: total amount left to be paid
    total_outstanding: Decimal
    #: Sum of line items, discounts taxes, etc.
    total_price: Decimal
    #: Sum of taxes
    total_tax: Decimal
    #: Sum of tips
    total_tip_received: Decimal
    #: Total shipping weight in grams
    total_weight: int
    #: Date time of last update to this order
    updated_at: datetime
    #: URL to the order status
    order_status_url: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
