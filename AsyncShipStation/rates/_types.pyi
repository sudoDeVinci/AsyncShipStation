from enum import Enum
from typing import Literal, NotRequired, Required

from ..common import (
    DeliveryConfirmationMethods,
    Dimensions,
    Error,
    Fee,
    Package,
    ShippingAddress,
    Tag,
    Taggable,
    Weight,
)
from ..shipments import Shipment

RateTypes = Literal["check", "shipment"]
RateResponseStatuses = Literal["working", "completed", "partial", "error"]
ValidationStatuses = Literal["valid", "invalid", "unknown", "has_warnings"]

class RateType(Enum):
    CHECK = "check"
    SHIPMENT = "shipment"

class RateResponseStatus(Enum):
    WORKING = "working"
    COMPLETED = "completed"
    PARTIAL = "partial"
    ERROR = "error"

class ValidationStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    UNKNOWN = "unknown"
    HAS_WARNINGS = "has_warnings"

class Rate(Taggable):
    "A shipping rate returned by the API."

    rate_id: str
    rate_type: RateTypes
    carrier_id: str
    shipping_amount: Fee
    insurance_amount: Fee
    confirmation_amount: Fee
    other_amount: Fee
    requested_comparison_amount: Fee | None
    tax_amount: Fee | None
    zone: int | None
    package_type: str | None
    delivery_days: int | None
    guaranteed_service: bool
    estimated_delivery_date: str | None
    carrier_delivery_days: str | None
    ship_date: str
    negotiated_rate: bool
    service_type: str
    service_code: str
    trackable: bool
    carrier_code: str
    carrier_nickname: str
    carrier_friendly_name: str
    validation_status: ValidationStatuses
    warning_messages: list[str]
    error_messages: list[str]

class RateEstimate(Taggable):
    "A rate estimate (without full shipment details)."

    rate_type: RateTypes
    carrier_id: str
    shipping_amount: Fee
    insurance_amount: Fee
    confirmation_amount: Fee
    other_amount: Fee
    tax_amount: Fee | None
    zone: int | None
    package_type: str | None
    delivery_days: int | None
    guaranteed_service: bool
    estimated_delivery_date: str | None
    carrier_delivery_days: str | None
    ship_date: str
    negotiated_rate: bool
    service_type: str
    service_code: str
    trackable: bool
    carrier_code: str
    carrier_nickname: str
    carrier_friendly_name: str
    validation_status: ValidationStatuses
    warning_messages: list[str]
    error_messages: list[str]

class RatesResponse(Taggable):
    "Response from the rates information endpoint."

    rates: list[Rate]
    invalid_rates: list[Rate]
    rate_request_id: str
    shipment_id: str
    created_at: str
    status: RateResponseStatuses
    errors: list[Error]

class RateRequestOptions(Taggable, total=False):
    "Options for a rate request."

    carrier_ids: list[str]
    package_types: NotRequired[list[str]]
    service_codes: NotRequired[list[str]]
    calculate_tax_amount: NotRequired[bool]
    preferred_currency: NotRequired[str]
    is_return: NotRequired[bool]

class RateEstimateOptions(Taggable, total=False):
    "Options for a rate estimate request."

    from_country_code: str
    from_postal_code: str
    from_city_locality: str
    from_state_province: str
    to_country_code: str
    to_postal_code: str
    to_city_locality: str
    to_state_province: str
    weight: Weight
    dimensions: Dimensions
    confirmation: DeliveryConfirmationMethods
    address_residential_indicator: Literal["unknown", "yes", "no"]
    ship_date: str

class RateEstimateByCarrierIds(RateEstimateOptions, total=False):
    "Options for a rate estimate request."

    carrier_ids: Required[list[str]]

class RateEstimateByCarrierId(RateEstimateOptions, total=False):
    "Options for a rate estimate request."

    carrier_id: Required[str]

class CalculateRatesRequest(Taggable, total=False):
    "Request body for calculating rates."

    shipment_id: str
    shipment: NotRequired[Shipment]
    rate_options: RateRequestOptions

class CalculateRatesResponse(Taggable):
    "Response from calculate rates endpoint."

    shipment_id: str
    carrier_id: str | None
    service_code: str | None
    external_order_id: str | None
    ship_date: str | None
    created_at: str
    modified_at: str
    shipment_status: str
    ship_to: ShippingAddress
    ship_from: ShippingAddress
    warehouse_id: str | None
    return_to: ShippingAddress | None
    confirmation: str
    insurance_provider: str
    tags: list[Tag]
    packages: list[Package]
    total_weight: Weight
    rate_response: RatesResponse
