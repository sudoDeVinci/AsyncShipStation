from typing import Literal, TypedDict

from ..common import (
    Error,
    Fee,
    Package,
    PaginatinatedResponse,
    Quantity,
    ShippingAddress,
    Tag,
)
from ..labels import LabelShipment, ShipmentItem

ShipmentStatuses = Literal["pending", "processing", "label_purchased", "cancelled"]


class Shipment(LabelShipment):
    shipment_id: str


class ShipmentListResponse(PaginatinatedResponse):
    shipments: list[Shipment]


class DangerousGood(TypedDict):
    id_number: str | None
    shipping_name: str | None
    technical_name: str | None
    product_class: str | None
    product_class_subsidiary: str | None
    packahging_group: Literal["i", "ii", "iii"]
    dangerous_amount: Quantity
    quantity: int
    packaging_instruction: str | None
    packaging_instruction_section: Literal[
        "section_1", "section_2", "section_1a", "section_1b"
    ]
    packaging_type: str | None
    transport_mean: str
    transport_category: str | None
    regulation_authority: str | None
    regulation_level: Literal[
        "lightly_regulated",
        "fully_regulated",
        "limited_quantities",
        "excepted_quantity",
    ]
    radioactive: bool | None
    reportable_quantity: bool | None
    tunnel_code: str | None
    additional_description: str | None


class Product(TypedDict):
    description: str
    quantity: int
    value: Fee
    weight: Fee
    harmonized_tariff_code: str | None
    country_of_origin: str | None
    unit_of_measure: str | None
    sku: str | None
    sku_description: str | None
    mid_code: str | None
    product_url: str | None
    vat_rate: float | None
    dangerous_goods: list[DangerousGood]


class ShipmentPackage(Package):
    package_name: str
    products: list[Product]


class ShipmentCreationRequest(TypedDict):
    validate_address: Literal["no_validation", "validate_only", "validate_and_clean"]
    external_shipment_id: str | None
    carrier_id: str | None
    create_sales_order: bool
    store_id: str | None
    notes_from_buyer: str | None
    notes_for_gift: str | None
    is_gift: bool
    zone: int | None
    display_scheme: str | None
    assigned_user: str | None
    shipment_status: str
    amount_paid: Fee
    shipping_paid: Fee
    tax_paid: Fee
    ship_to: ShippingAddress
    ship_from: ShippingAddress
    items: list[ShipmentItem]
    packages: list[ShipmentPackage]


class ShipmentCreationResponse(TypedDict):
    has_errors: bool
    shipments: list[Shipment]


class ShippingRate(TypedDict):
    rate_id: str
    rate_type: Literal["check", "shipment"]
    carrier_id: str
    shipping_amount: Fee
    insurance_amount: Fee
    confirmation_amount: Fee
    other_amount: Fee
    requested_comparison_amount: Fee
    tax_amount: Fee
    zone: int | None
    package_type: str | None
    delivery_days: int | None
    guaranteed_service: bool
    estimated_delivery_date: str
    carrier_delivery_days: str
    ship_date: str
    negatiated_rate: bool
    service_type: str
    service_code: str
    traclable: bool
    carrier_code: str
    carrier_nickname: str
    carrier_friendly_name: str
    validation_status: Literal["valid", "invalid", "unknown", "has_warnings"]
    warning_messages: list[str]
    error_messages: list[str]


class RateQueryResponse(TypedDict):
    rates: list[ShippingRate]
    invalid_rates: list[ShippingRate]
    rate_request_id: str
    shipment_id: str
    created_at: str
    status: str
    errors: list[Error]


class ShipmentTag(Tag):
    shipment_id: str
