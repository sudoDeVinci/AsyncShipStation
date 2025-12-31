from typing import NotRequired, TypedDict

from ..common import Fee, PaginationLink


class Address(TypedDict):
    name: str
    company_name: str | None
    email: str | None
    phone: str | None
    address_line1: str
    address_line2: str | None
    address_line3: str | None
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str


class Fulfillment(TypedDict):
    fulfillment_id: str
    shipment_id: str
    shipment_number: str
    user_id: str
    tracking_number: str
    created_at: str
    ship_date: str
    voided_at: str | None
    delivered_at: str | None
    fulfillment_carrier_friendly_name: str
    fulfillment_provider_id: str | None
    fulfillment_provider_friendly_name: str | None
    fulfillment_provider_code: str | None
    fulfillment_service_code: str | None
    fulfillment_fee: Fee
    void_requested: bool
    voided: bool
    order_source_notified: bool
    notification_error_message: str | None
    ship_to: Address


class FulfillmentGist(TypedDict):
    shipment_id: str
    tracking_number: str
    carrier_code: str
    ship_date: NotRequired[str]
    notify_customer: NotRequired[bool]
    notify_order_source: NotRequired[bool]


class FulfillmentGistRequest(TypedDict):
    fulfillments: list[FulfillmentGist]


class FulfillmentCreationResponse(TypedDict):
    shipment_id: str
    shipment_number: str
    error_message: str | None


class BatchFulfillmentCreationResponse(TypedDict):
    has_errors: bool
    fulfillments: list[FulfillmentCreationResponse]


class FulfillmentListResponse(TypedDict):
    fulfillments: list[Fulfillment]
    page: int
    pages: int
    total: int
    links: PaginationLink
