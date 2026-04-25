from typing import NotRequired, TypedDict

from ..common import Address, Fee, PaginatinatedResponse
from ..common._types import Taggable


class Fulfillment(Taggable):
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


class FulfillmentGist(Taggable):
    shipment_id: str
    tracking_number: str
    carrier_code: str
    ship_date: NotRequired[str]
    notify_customer: NotRequired[bool]
    notify_order_source: NotRequired[bool]


class FulfillmentGistRequest(Taggable):
    fulfillments: list[FulfillmentGist]


class FulfillmentCreationResponse(Taggable):
    shipment_id: str
    shipment_number: str
    error_message: str | None


class BatchFulfillmentCreationResponse(Taggable):
    has_errors: bool
    fulfillments: list[FulfillmentCreationResponse]


class FulfillmentListResponse(PaginatinatedResponse):
    fulfillments: list[Fulfillment]