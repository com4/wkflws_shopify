from datetime import datetime
from decimal import Decimal
import enum
from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    """Represent a physical address."""

    address1: str
    address2: str
    city: str
    #: The name of the region (for example, province, state, or prefecture).
    province: str
    province_code: str
    zip: str  # Shopify calls this zip
    country: str
    #: The two-letter country code (ISO 3166-1 format)
    country_code: str
    latitude: Optional[str] = None  # Shopify provides a string
    longitude: Optional[str] = None  # Shopify provides a string
    #: full name associated with the address (e.g. billing contact, shipping recipient)
    name: Optional[str] = None
    #: first name associated with the address
    first_name: Optional[str] = None
    #: last name associated with the address
    last_name: Optional[str] = None
    #: phone number associated with the address
    phone: Optional[str] = None
    #: company associated with the address
    company: Optional[str] = None


class MarketingConsent(BaseModel):
    """Respresents information about a user's consent to email marketing."""

    #: The state (status) of the user's consent
    state: str
    #: Level of opt-in
    #: 1. Single opt-in
    #: 2. Single opt-in with notification
    #: 3. Confirmed opt-in
    #: See https://www.m3aawg.org/sites/default/files/document/M3AAWG_Senders_BCP_Ver3-2015-02.pdf
    opt_in_level: str
    #: Date time when the consent was received (or consent information was sent)
    consent_updated_at: Optional[datetime] = None


class SMSMarketingConsent(MarketingConsent):
    """Represents information about a user's consent to SMS marketing."""

    #: The source the consent was collected from
    consent_collected_from: str


class CustomerStatus(str, enum.Enum):
    """Represent the status (state) of a customer's account with a shop."""

    disabled = "disabled"
    enabled = "enabled"
    invited = "invited"
    declined = "declined"


class Customer(BaseModel):
    """Represent a customer."""

    #: A list of up to 10 of the last used addresses
    addresses: list[Address] = []
    #: Currency the customer used when they paid for their last order. Defaults to
    #: shop's currency.
    currency: str
    #: ISO-8601 date time when the customer was created
    created_at: datetime
    #: The default address of the customer
    default_address: Address
    #: Unique email address of the customer
    email: str
    #: The customer has consented to receiveing email marketing
    email_marketing_consent: Optional[MarketingConsent] = None
    first_name: str
    id: int
    last_name: str
    #: ID of the last order placed by this customer
    last_order_id: Optional[int] = None
    #: Name of the last order placed by this customer
    last_order_name: Optional[str] = None
    #: phone number
    phone: Optional[str] = None
    #: Information about the customer's consent to email marketing.
    sms_marketing_consent: Optional[SMSMarketingConsent] = None
    #: State (status) of the account
    #: (default disabled, choices: invited, enabled, declined)
    state: str = "enabled"
    #: tags a shop owner has attached to the customer. CSV
    tags: str = ""
    tax_exempt: bool = False
    total_spent: Decimal = Decimal("0.0")
    #: whether the user has verified their email
    verified_email: bool = False
