from enum import Enum
from typing import Literal, TypedDict

from ..common import (
    URL,
    Address,
    Contact,
    DeliveryConfirmationMethods,
    DisplayFormatSchemes,
    Fee,
    Identifier,
    IncoTerms,
    LabelDownload,
    LabelFormats,
    LabelLayouts,
    LabelMetaData,
    Option,
    OrderSources,
    Package,
    PaginatinatedResponse,
    ShippingAddress,
    Tag,
    Weight,
)

LabelStatuses = Literal["processing", "completed", "error", "voided"]
ChargeEvents = Literal["carrier_default", "on_creation", "on_carrier_acceptance"]
PackageTypes = Literal["thick_envelope", "small_flat_rate_box", "large_package"]
TrackingStatuses = Literal["unknown", "in_transit", "error", "delivered"]
ShipmentContents = Literal[
    "merchandise", "documents", "gift", "returned_goods", "sample", "other"
]


class ShipmentContent(Enum):
    MERCHANDISE = "merchandise"
    DOCUMENTS = "documents"
    GIFT = "gift"
    RETURNED_GOODS = "returned_goods"
    SAMPLE = "sample"
    OTHER = "other"


class ChargeEvent(Enum):
    CARRIER_DEFAULT = "carrier_default"
    ON_CREATION = "on_creation"
    ON_CARRIER_ACCEPTANCE = "on_carrier_acceptance"


class LabelStatus(Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    VOIDED = "voided"


class PackageType(Enum):
    THICK_ENVELOPE = "thick_envelope"
    SMALL_FLAT_RATE_BOX = "small_flat_rate_box"
    LARGE_PACKAGE = "large_package"


class TrackingStatus(Enum):
    UNKNOWN = "unknown"
    IN_TRANSIT = "in_transit"
    ERROR = "error"
    DELIVERED = "delivered"


TrackingStatusCodes = Literal[
    "COLLECTION_FAILED",
    "AWAITING_DESPATCH",
    "COLLECTION_REQUESTED",
    "DESPATCHED",
    "ELEC_ADVICE_RECD_BY_CARRIER",
    "NOT_YET_RECEIVED_BY_CARRIER",
    "COLLECTION_MADE",
    "ATTEMPTED_DELIVERY",
    "ATTEMPTED_DELIVERY_2ND",
    "ATTEMPTED_DELIVERY_3RD",
    "COD_AMOUNT_NOT_PAID",
    "COD_AMOUNT_PAID",
    "CUSTOMER_CARDED",
    "CUSTOMER_IDENTIFICATION_FAILED",
    "INVALID_METHOD_OF_PAYMENT",
    "NO_ACCESS_TO_RECIPIENTS_ADDRESS",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "DELIVERED_DAMAGED",
    "DELIVERED_IN_PART",
    "DELIVERED_SPECIFIED_SAFE_PLACE",
    "DELIVERED_TO_ALTERNATIVE_DELIVERY_LOCATION",
    "DELIVERED_TO_NEIGHBOUR",
    "DELIVERED_TO_PO_BOX",
    "PARCEL_COLLECTED_FROM_PICKUP_POINT",
    "POST_TRANSIT_STATUS",
    "PROOF_OF_DELIVERY",
    "CANCELLED",
    "CANCELLED_BEFORE_DESPATCH",
    "CUSTOMER_MOVED",
    "HAZARDOUS_PROHIBITED",
    "NOT_COLLECTED_FROM_PICKUP_POINT",
    "NOT_DELIVERED",
    "NOT_DELIVERED_ADDRESSEE_DECEASED",
    "PARCEL_DAMAGED",
    "PARCEL_DISPOSED",
    "PARCEL_LOST",
    "PARCEL_OUTSIDE_OF_SERVICE_CAPABILITY",
    "REFUSED_BY_CUSTOMER",
    "RETURN_TO_SENDER",
    "ADDRESS_QUERY",
    "CARRIER_DELAYS",
    "CUSTOMS_CLEARED",
    "CUSTOMS_PROCESSING",
    "DELAYED_NOT_CARRIER",
    "DELIVERY_ARRANGED_WITH_RECIPIENT",
    "HELD_BY_CARRIER",
    "HELD_BY_CARRIER_FOR_CLEARANCE_PRE_PROCESSING",
    "HELD_BY_CUSTOMS",
    "HELD_BY_EXPORT_CUSTOMS",
    "HELD_BY_IMPORT_CUSTOMS",
    "HUB_SCAN_OUT",
    "IN_TRANSIT",
    "INCORRECT_DECLARATION",
    "INFORMATION",
    "MISSORTED",
    "PARCEL_OVER_LABELLED",
    "PARCEL_REPACKED",
    "PARCEL_UPDATE_NOTIFICATION_VIA_EMAIL",
    "PARCEL_UPDATE_NOTIFICATION_VIA_SMS",
    "RECEIVED_BY_CARRIER",
    "RECEIVED_LOCAL_DELIVERY_DEPOT",
    "ROUTING_ERROR",
    "SUB_CONTRACTOR_EVENT",
    "SUB_CONTRACTOR_RECEIVED",
    "RECD_BY_CARRIER_NO_ELEC_ADVICE",
    "AWAITING_ELECTRONIC_ADVICE",
    "AWAITING_COLLECTION_FROM_PICKUP_POINT",
    "COLLECT_AT_LOCAL_PO",
    "CUSTOMER_TO_COLLECT_FROM_CARRIER",
    "DELIVERED_TO_LOCKER_COLLECTION_POINT",
    "CARRIER_STATUS_NOT_MAPPED",
]


class TrackingStatusCode(Enum):
    COLLECTION_FAILED = "COLLECTION_FAILED"
    AWAITING_DESPATCH = "AWAITING_DESPATCH"
    COLLECTION_REQUESTED = "COLLECTION_REQUESTED"
    DESPATCHED = "DESPATCHED"
    ELEC_ADVICE_RECD_BY_CARRIER = "ELEC_ADVICE_RECD_BY_CARRIER"
    NOT_YET_RECEIVED_BY_CARRIER = "NOT_YET_RECEIVED_BY_CARRIER"
    COLLECTION_MADE = "COLLECTION_MADE"
    ATTEMPTED_DELIVERY = "ATTEMPTED_DELIVERY"
    ATTEMPTED_DELIVERY_2ND = "ATTEMPTED_DELIVERY_2ND"
    ATTEMPTED_DELIVERY_3RD = "ATTEMPTED_DELIVERY_3RD"
    COD_AMOUNT_NOT_PAID = "COD_AMOUNT_NOT_PAID"
    COD_AMOUNT_PAID = "COD_AMOUNT_PAID"
    CUSTOMER_CARDED = "CUSTOMER_CARDED"
    CUSTOMER_IDENTIFICATION_FAILED = "CUSTOMER_IDENTIFICATION_FAILED"
    INVALID_METHOD_OF_PAYMENT = "INVALID_METHOD_OF_PAYMENT"
    NO_ACCESS_TO_RECIPIENTS_ADDRESS = "NO_ACCESS_TO_RECIPIENTS_ADDRESS"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    DELIVERED_DAMAGED = "DELIVERED_DAMAGED"
    DELIVERED_IN_PART = "DELIVERED_IN_PART"
    DELIVERED_SPECIFIED_SAFE_PLACE = "DELIVERED_SPECIFIED_SAFE_PLACE"
    DELIVERED_TO_ALTERNATIVE_DELIVERY_LOCATION = (
        "DELIVERED_TO_ALTERNATIVE_DELIVERY_LOCATION"
    )
    DELIVERED_TO_NEIGHBOUR = "DELIVERED_TO_NEIGHBOUR"
    DELIVERED_TO_PO_BOX = "DELIVERED_TO_PO_BOX"
    PARCEL_COLLECTED_FROM_PICKUP_POINT = "PARCEL_COLLECTED_FROM_PICKUP_POINT"
    POST_TRANSIT_STATUS = "POST_TRANSIT_STATUS"
    PROOF_OF_DELIVERY = "PROOF_OF_DELIVERY"
    CANCELLED = "CANCELLED"
    CANCELLED_BEFORE_DESPATCH = "CANCELLED_BEFORE_DESPATCH"
    CUSTOMER_MOVED = "CUSTOMER_MOVED"
    HAZARDOUS_PROHIBITED = "HAZARDOUS_PROHIBITED"
    NOT_COLLECTED_FROM_PICKUP_POINT = "NOT_COLLECTED_FROM_PICKUP_POINT"
    NOT_DELIVERED = "NOT_DELIVERED"
    NOT_DELIVERED_ADDRESSEE_DECEASED = "NOT_DELIVERED_ADDRESSEE_DECEASED"
    PARCEL_DAMAGED = "PARCEL_DAMAGED"
    PARCEL_DISPOSED = "PARCEL_DISPOSED"
    PARCEL_LOST = "PARCEL_LOST"
    PARCEL_OUTSIDE_OF_SERVICE_CAPABILITY = "PARCEL_OUTSIDE_OF_SERVICE_CAPABILITY"
    REFUSED_BY_CUSTOMER = "REFUSED_BY_CUSTOMER"
    RETURN_TO_SENDER = "RETURN_TO_SENDER"
    ADDRESS_QUERY = "ADDRESS_QUERY"
    CARRIER_DELAYS = "CARRIER_DELAYS"
    CUSTOMS_CLEARED = "CUSTOMS_CLEARED"
    CUSTOMS_PROCESSING = "CUSTOMS_PROCESSING"
    DELAYED_NOT_CARRIER = "DELAYED_NOT_CARRIER"
    DELIVERY_ARRANGED_WITH_RECIPIENT = "DELIVERY_ARRANGED_WITH_RECIPIENT"
    HELD_BY_CARRIER = "HELD_BY_CARRIER"
    HELD_BY_CARRIER_FOR_CLEARANCE_PRE_PROCESSING = (
        "HELD_BY_CARRIER_FOR_CLEARANCE_PRE_PROCESSING"
    )
    HELD_BY_CUSTOMS = "HELD_BY_CUSTOMS"
    HELD_BY_EXPORT_CUSTOMS = "HELD_BY_EXPORT_CUSTOMS"
    HELD_BY_IMPORT_CUSTOMS = "HELD_BY_IMPORT_CUSTOMS"
    HUB_SCAN_OUT = "HUB_SCAN_OUT"
    IN_TRANSIT = "IN_TRANSIT"
    INCORRECT_DECLARATION = "INCORRECT_DECLARATION"
    INFORMATION = "INFORMATION"
    MISSORTED = "MISSORTED"
    PARCEL_OVER_LABELLED = "PARCEL_OVER_LABELLED"
    PARCEL_REPACKED = "PARCEL_REPACKED"
    PARCEL_UPDATE_NOTIFICATION_VIA_EMAIL = "PARCEL_UPDATE_NOTIFICATION_VIA_EMAIL"
    PARCEL_UPDATE_NOTIFICATION_VIA_SMS = "PARCEL_UPDATE_NOTIFICATION_VIA_SMS"
    RECEIVED_BY_CARRIER = "RECEIVED_BY_CARRIER"
    RECEIVED_LOCAL_DELIVERY_DEPOT = "RECEIVED_LOCAL_DELIVERY_DEPOT"
    ROUTING_ERROR = "ROUTING_ERROR"
    SUB_CONTRACTOR_EVENT = "SUB_CONTRACTOR_EVENT"
    SUB_CONTRACTOR_RECEIVED = "SUB_CONTRACTOR_RECEIVED"
    RECD_BY_CARRIER_NO_ELEC_ADVICE = "RECD_BY_CARRIER_NO_ELEC_ADVICE"
    AWAITING_ELECTRONIC_ADVICE = "AWAITING_ELECTRONIC_ADVICE"
    AWAITING_COLLECTION_FROM_PICKUP_POINT = "AWAITING_COLLECTION_FROM_PICKUP_POINT"
    COLLECT_AT_LOCAL_PO = "COLLECT_AT_LOCAL_PO"
    CUSTOMER_TO_COLLECT_FROM_CARRIER = "CUSTOMER_TO_COLLECT_FROM_CARRIER"
    DELIVERED_TO_LOCKER_COLLECTION_POINT = "DELIVERED_TO_LOCKER_COLLECTION_POINT"
    CARRIER_STATUS_NOT_MAPPED = "CARRIER_STATUS_NOT_MAPPED"


class LabelPackage(Package):
    tracking_number: str
    label_download: LabelDownload
    form_download: URL | None
    qr_code_download: URL | None
    paperless_download: URL | None
    sequence: int
    has_label_documents: bool
    has_form_documents: bool
    has_qr_code_documents: bool
    has_paperless_label_documents: bool
    alternative_identifiers: list[Identifier] | None


class RateDetails(TypedDict):
    rate_detail_type: str
    carrier_description: str
    carrier_billing_code: str
    carrier_memo: str
    amount: Fee


class Label(LabelMetaData):
    label_id: str
    status: LabelStatuses
    shipment_id: str
    external_shipment_id: str | None
    external_order_id: str | None
    created_at: str
    shipment_cost: Fee
    insurance_cost: Fee
    requested_comparison_amount: Fee
    tracking_number: str
    is_return_label: bool
    rma_number: str | None
    is_international: bool
    batch_id: str
    carrier_id: str
    charge_event: ChargeEvents
    service_code: str
    package_code: str
    voided: bool
    voided_at: str | None
    display_scheme: DisplayFormatSchemes
    trackable: bool
    label_image_id: str | None
    carrier_code: str
    confirmation: str
    tracking_status: TrackingStatuses
    label_download: LabelDownload
    form_download: URL | None
    qr_code_download: URL | None
    paperless_download: URL | None
    insurance_claim: URL | None
    packages: list[LabelPackage]
    alternative_identifiers: list[Identifier] | None
    rate_details: list[RateDetails]
    tracking_url: str | None
    ship_to: ShippingAddress


class LabelGist(TypedDict):
    validate_address: Literal["no_validation", "validate_only", "validate_and_clean"]
    label_layout: LabelLayouts
    label_format: LabelFormats
    label_download_type: Literal["url", "inline"]
    display_scheme: DisplayFormatSchemes


class LabelListResponse(PaginatinatedResponse):
    labels: list[Label]


class ShipmentPayment(TypedDict):
    payment_type: Literal["any", "cash", "cash_equivalent", "none"]
    payment_amount: Fee


class ShipmentItem(TypedDict):
    name: str
    sales_order_id: str | None
    sales_order_item_id: str | None
    quantity: int
    sku: str | None
    bundle_sku: str | None
    external_order_id: str | None
    external_order_item_id: str | None
    asin: str | None
    order_source_code: OrderSources
    item_id: str | None
    allocation_status: str | None
    image_url: str
    weight: Weight
    unit_price: float | None
    tax_amount: float | None
    shipping_amount: float | None
    inventory_location: str | None
    options: list[Option]
    product_id: str | None
    fulfillment_sku: str | None
    upc: str | None


class TaxIdentifier(TypedDict):
    taxable_entity_type: Literal["shipper", "recipient", "ior"]
    identifier_type: Literal[
        "vateori",
        "ssn",
        "ein",
        "tin",
        "ioss",
        "pan",
        "voec",
        "pccc",
        "oss",
        "passport",
        "abn",
        "ukims",
    ]
    issuing_authority: str
    value: str


class InvoiceAdditionalDetails(TypedDict):
    freight_charge: Fee
    insurance_charge: Fee
    discount: Fee
    estimated_import_charges: Fee
    other_charge: Fee
    other_charge_description: str


class InternationalShipmentOptions(TypedDict):
    contents: ShipmentContents  # default "merchandise"
    contents_explanations: str
    non_delivery: Literal["return_to_sender", "treat_as_abandoned"]
    terms_of_trade_code: IncoTerms
    decleration: str
    invoice_additional_details: InvoiceAdditionalDetails
    importer_of_record: Address


class FedexFreightOptions(TypedDict):
    shipper_load_and_count: str
    booking_confirmation: str


class WindsorFrameworkDetails(TypedDict):
    movement_indicator: Literal["c2c", "b2c", "c2b", "b2b"]
    not_at_risk: bool


class AdvancedShipmentOptions(TypedDict):
    bill_to_account: str | None
    bill_to_country_code: str | None
    bill_to_party: Literal["recipient", "third_party"]
    bill_to_postal_code: str | None
    contains_alcohol: bool  # default false
    delivered_duty_paid: bool  # default false
    dry_ice: bool  # default false
    dry_ice_weight: Weight | None
    non_machinable: bool  # default false
    saturday_delivery: bool  # default false
    fedex_freight: FedexFreightOptions
    use_ups_ground_freight_pricing: bool | None  # default null
    freight_class: str | None
    custom_field1: str | None
    custom_field2: str | None
    custom_field3: str | None
    origin_type: str | None
    additional_handling: bool | None  # default null
    shipper_release: bool | None  # default null
    collect_on_delivery: ShipmentPayment
    third_party_consignee: bool  # default false
    dangerous_goods: bool  # default false
    dangerous_goods_contact: Contact
    windsor_framework_details: WindsorFrameworkDetails
    ancillary_endorsements_option: str | None
    return_pickup_attempts: int | None
    own_document_upload: bool  # default false
    limited_quantity: bool  # default false
    event_notification: bool  # default false


class LabelShipment(TypedDict):
    carrier_id: str | None
    service_code: str | None
    requested_shipment_service: str | None
    shipping_rule_id: str | None
    external_order_id: str | None
    hold_until_date: str | None
    ship_by_date: str | None
    retail_rate: Fee | None
    store_id: str | None
    items: list[ShipmentItem]
    notes_from_buyer: str | None
    notes_for_gift: str | None
    is_gift: bool  # default false
    assigned_user: str | None
    amount_paid: Fee
    tax_paid: Fee
    zone: int | None
    display_scheme: DisplayFormatSchemes | None
    tax_identifiers: list[TaxIdentifier] | None
    external_shipment_id: str | None
    shipment_number: str | None
    ship_date: str | None
    ship_to: ShippingAddress
    ship_from: ShippingAddress
    warehouse_id: str | None
    return_to: ShippingAddress
    is_return: bool | None  # default false
    confirmation: DeliveryConfirmationMethods
    customs: InternationalShipmentOptions
    advanced_options: AdvancedShipmentOptions
    insurance_provider: Literal[
        "none", "shipsurance", "carrier", "third_party"
    ]  # default "none"
    tags: list[Tag]
    order_source_code: OrderSources
    packages: list[LabelPackage]
    comparison_rate_type: str | None


class TrackingEvent(TypedDict):
    occurred_at: str
    carrier_occurred_at: str
    description: str
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    company_name: str
    signer: str
    event_code: str
    carrier_detail_code: str | None
    status_code: TrackingStatusCodes
    status_detail_code: TrackingStatusCodes
    status_description: str
    status_detail_description: str
    carrier_status_code: str
    carrier_status_description: str
    latitude: float
    longitude: float
    proof_of_delivery_url: str


class TrackingInformation(TypedDict):
    tracking_number: str
    tracking_url: str
    status_code: TrackingStatusCodes
    status_detail_code: TrackingStatusCodes
    carrier_code: str
    carrier_id: int
    status_description: str
    status_detail_description: str
    carrier_status_code: str
    carrier_detail_code: str
    carrier_status_description: str
    ship_date: str
    estimated_delivery_date: str
    actual_delivery_date: str
    exception_description: str
    events: list[TrackingEvent]


class LabelVoidResponse(TypedDict):
    approved: bool
    message: str
    reason_code: Literal[
        "unknown",
        "unspecified",
        "validation_failed",
        "label_not_found_within_void_period",
        "label_already_used",
        "label_already_voided",
        "contact_carrier",
    ]
