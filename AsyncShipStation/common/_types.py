from enum import Enum
from typing import Literal, NotRequired, TypedDict

from pydantic import EmailStr, HttpUrl

JSONDict = dict[str, str | int | bool | EmailStr | HttpUrl | None]


class Endpoints(Enum):
    BATCHES = "batches"
    CARRIERS = "carriers"
    DOWNLOADS = "downloads"
    FULFILLMENTS = "fulfillments"
    INVENTORY = "inventory"
    INVENTORY_WAREHOUSES = "inventory_warehouses"
    INVENTORY_LOCATIONS = "inventory_locations"
    ORDERS = "orders"
    LABELS = "labels"
    MANIFESTS = "manifests"
    PRODUCTS = "products"
    SHIPMENTS = "shipments"


ErrorSources = Literal["carrier", "order_source", "ShipStation"]


class ErrorSource(Enum):
    CARRIER = "carrier"
    ORDER_SOURCE = "order_source"
    SHIPSTATION = "ShipStation"


ErrorTypes = Literal[
    "account_status",
    "business_rules",
    "validation",
    "security",
    "system",
    "integrations",
]


class ErrorType(Enum):
    ACCOUNT_STATUS = "account_status"
    BUSINESS_RULES = "business_rules"
    VALIDATION = "validation"
    SECURITY = "security"
    SYSTEM = "system"
    INTEGRATIONS = "integrations"


ErrorCodes = Literal[
    "auto_fund_not_supported",
    "batch_cannot_be_modified",
    "carrier_conflict",
    "carrier_disconnected",
    "carrier_not_connected",
    "carrier_not_supported",
    "confirmation_not_supported",
    "default_warehouse_cannot_be_deleted",
    "field_conflict",
    "field_value_required",
    "forbidden",
    "identifier_conflict",
    "identifiers_must_match",
    "insufficient_funds",
    "invalid_address",
    "invalid_billing_plan",
    "invalid_field_value",
    "invalid_identifier",
    "invalid_status",
    "invalid_string_length",
    "label_images_not_supported",
    "meter_failure",
    "order_source_not_active",
    "rate_limit_exceeded",
    "refresh_not_supported",
    "request_body_required",
    "return_label_not_supported",
    "settings_not_supported",
    "subscription_inactive",
    "terms_not_accepted",
    "tracking_not_supported",
    "trial_expired",
    "unauthorized",
    "unknown",
    "unspecified",
    "verification_failure",
    "warehouse_conflict",
    "webhook_event_type_conflict",
    "customs_items_required",
    "incompatible_paired_labels",
    "invalid_charge_event",
    "invalid_object",
    "no_rates_returned",
]


class ErrorCode(Enum):
    AUTO_FUND_NOT_SUPPORTED = "auto_fund_not_supported"
    BATCH_CANNOT_BE_MODIFIED = "batch_cannot_be_modified"
    CARRIER_CONFLICT = "carrier_conflict"
    CARRIER_DISCONNECTED = "carrier_disconnected"
    CARRIER_NOT_CONNECTED = "carrier_not_connected"
    CARRIER_NOT_SUPPORTED = "carrier_not_supported"
    CONFIRMATION_NOT_SUPPORTED = "confirmation_not_supported"
    DEFAULT_WAREHOUSE_CANNOT_BE_DELETED = "default_warehouse_cannot_be_deleted"
    FIELD_CONFLICT = "field_conflict"
    FIELD_VALUE_REQUIRED = "field_value_required"
    FORBIDDEN = "forbidden"
    IDENTIFIER_CONFLICT = "identifier_conflict"
    IDENTIFIERS_MUST_MATCH = "identifiers_must_match"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    INVALID_ADDRESS = "invalid_address"
    INVALID_BILLING_PLAN = "invalid_billing_plan"
    INVALID_FIELD_VALUE = "invalid_field_value"
    INVALID_IDENTIFIER = "invalid_identifier"
    INVALID_STATUS = "invalid_status"
    INVALID_STRING_LENGTH = "invalid_string_length"
    LABEL_IMAGES_NOT_SUPPORTED = "label_images_not_supported"
    METER_FAILURE = "meter_failure"
    ORDER_SOURCE_NOT_ACTIVE = "order_source_not_active"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    REFRESH_NOT_SUPPORTED = "refresh_not_supported"
    REQUEST_BODY_REQUIRED = "request_body_required"
    RETURN_LABEL_NOT_SUPPORTED = "return_label_not_supported"
    SETTINGS_NOT_SUPPORTED = "settings_not_supported"
    SUBSCRIPTION_INACTIVE = "subscription_inactive"
    TERMS_NOT_ACCEPTED = "terms_not_accepted"
    TRACKING_NOT_SUPPORTED = "tracking_not_supported"
    TRIAL_EXPIRED = "trial_expired"
    UNAUTHORIZED = "unauthorized"
    UNKNOWN = "unknown"
    UNSPECIFIED = "unspecified"
    VERIFICATION_FAILURE = "verification_failure"
    WAREHOUSE_CONFLICT = "warehouse_conflict"
    WEBHOOK_EVENT_TYPE_CONFLICT = "webhook_event_type_conflict"
    CUSTOMS_ITEMS_REQUIRED = "customs_items_required"
    INCOMPATIBLE_PAIRED_LABELS = "incompatible_paired_labels"
    INVALID_CHARGE_EVENT = "invalid_charge_event"
    INVALID_OBJECT = "invalid_object"
    NO_RATES_RETURNED = "no_rates_returned"


DisplayFormatSchemes = Literal[
    "label", "qr_code", "label_and_qr_code", "paperless", "label_and_paperless"
]


class DisplayFormatScheme(Enum):
    LABEL = "label"
    QR_CODE = "qr_code"
    LABEL_AND_QR_CODE = "label_and_qr_code"
    PAPERLESS = "paperless"
    LABEL_AND_PAPERLESS = "label_and_paperless"


LabelLayouts = Literal["4x6", "letter"]


class LabelLayout(Enum):
    LAYOUT_4X6 = "4x6"
    LAYOUT_LETTER = "letter"


LabelFormats = Literal["pdf", "zpl", "png"]


class LabelFormat(Enum):
    PDF = "pdf"
    ZPL = "zpl"
    PNG = "png"


OrderSources = Literal[
    "amazon_ca",
    "amazon_us",
    "brightpearl",
    "channel_advisor",
    "cratejoy",
    "ebay",
    "etsy",
    "jane",
    "groupon_goods",
    "magento",
    "paypal",
    "seller_active",
    "shopify",
    "stitch_labs",
    "squarespace",
    "three_dcart",
    "tophatter",
    "walmart",
    "woo_commerce",
    "volusion",
]


class OrderSource(Enum):
    AMAZON_CA = "amazon_ca"
    AMAZON_US = "amazon_us"
    BRIGHTPEARL = "brightpearl"
    CHANNEL_ADVISOR = "channel_advisor"
    CRATEJOY = "cratejoy"
    EBAY = "ebay"
    ETSY = "etsy"
    JANE = "jane"
    GROUPON_GOODS = "groupon_goods"
    MAGENTO = "magento"
    PAYPAL = "paypal"
    SELLER_ACTIVE = "seller_active"
    SHOPIFY = "shopify"
    STITCH_LABS = "stitch_labs"
    SQUARESPACE = "squarespace"
    THREE_DCART = "three_dcart"
    TOPHATTER = "tophatter"
    WALMART = "walmart"
    WOO_COMMERCE = "woo_commerce"
    VOLUSION = "volusion"


DeliveryConfirmationMethods = Literal[
    "none",
    "delivery",
    "signature",
    "adult_signature",
    "direct_signature",
    "delivery_mailed",
    "verbal_confirmation",
]


class DeliveryConfirmationMethod(Enum):
    NONE = "none"
    DELIVERY = "delivery"
    SIGNATURE = "signature"
    ADULT_SIGNATURE = "adult_signature"
    DIRECT_SIGNATURE = "direct_signature"
    DELIVERY_MAILED = "delivery_mailed"
    VERBAL_CONFIRMATION = "verbal_confirmation"


IncoTerms = Literal[
    "exwfca",
    "cpt",
    "cip",
    "dpu",
    "dap",
    "ddp",
    "fas",
    "fob",
    "cfr",
    "cif",
    "ddu",
    "daf",
    "deq",
    "des",
]


class IncoTerm(Enum):
    EXWFCA = "exwfca"
    CPT = "cpt"
    CIP = "cip"
    DPU = "dpu"
    DAP = "dap"
    DDP = "ddp"
    FAS = "fas"
    FOB = "fob"
    CFR = "cfr"
    CIF = "cif"
    DDU = "ddu"
    DAF = "daf"
    DEQ = "deq"
    DES = "des"


class URL(TypedDict):
    href: str
    type: str | None


class LabelDownload(TypedDict):
    href: str
    pdf: str
    png: str
    zpl: str


class LabelMetaData(TypedDict):
    ship_date: str
    label_layout: LabelLayouts  # default "4x6"
    label_format: LabelFormats  # default "pdf"


class PaperlessDownload(TypedDict):
    href: str
    instructions: str | None  # default is None
    handoff_code: str | None  # default is None


class PaginationLink(TypedDict):
    first: URL
    last: URL
    prev: URL | None  # default is None
    next: URL | None  # default is None


class Error(TypedDict):
    error_source: ErrorSources
    errors_type: ErrorTypes
    error_code: ErrorCodes
    message: str


class ErrorResponse(TypedDict):
    errors: list[Error]
    request_id: str | None


class Dimensions(TypedDict):
    unit: Literal["inch", "centimeters"]  # default "inch"
    length: float
    width: float
    height: float


class Fee(TypedDict):
    amount: float
    currency: str


class Weight(TypedDict):
    value: float
    unit: Literal["pound", "ounce", "gram", "kilogram"]


class Identifier(TypedDict):
    type: str
    value: str


class Option(TypedDict):
    name: str
    value: str


class Quantity(TypedDict):
    amount: int  # default 0
    unit: str | None


class Tag(TypedDict):
    name: str


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


class LabelMessages(TypedDict):
    reference1: str | None
    reference2: str | None
    reference3: str | None


class Package(TypedDict):
    package_id: str
    package_code: str
    weight: Weight
    dimensions: Dimensions
    insured_value: NotRequired[Fee]
    label_messages: LabelMessages
    external_package_id: str
    content_description: str | None


class PaginatinatedResponse(TypedDict):
    total: int
    page: int
    pages: int
    links: PaginationLink


class Contact(TypedDict):
    name: str
    phone: str


class ShippingAddress(Address):
    address_residential_indicator: Literal["unknown", "yes", "no"]
    instructions: str | None
    geolocation: list[Identifier]
