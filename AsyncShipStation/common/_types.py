from enum import Enum
from typing import Literal, TypedDict

from pydantic import EmailStr, HttpUrl, PastDatetime

JSONDict = dict[str, str | int | bool | EmailStr | HttpUrl | PastDatetime | None]


class Endpoints(Enum):
    BATCHES = "batches"
    CARRIERS = "carriers"
    DOWNLOADS = "downloads"
    FULFILLMENTS = "fulfillments"
    INVENTORY = "inventory"
    INVENTORY_WAREHOUSES = "inventory_warehouses"
    INVENTORY_LOCATIONS = "inventory_locations"
    ORDERS = "orders"


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


DisplayFormatScheme = Literal[
    "label", "qr_code", "label_and_qr_code", "paperless", "label_and_paperless"
]

LabelLayouts = Literal["4x6", "letter"]


class LabelLayout(Enum):
    LAYOUT_4X6 = "4x6"
    LAYOUT_LETTER = "letter"


LabelFormats = Literal["pdf", "zpl", "png"]


class LabelFormat(Enum):
    PDF = "pdf"
    ZPL = "zpl"
    PNG = "png"


class URL(TypedDict):
    href: str
    type: str | None


class LabelDownload(TypedDict):
    href: str
    pdf: str
    png: str
    zpl: str


class Label(TypedDict):
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


class Dimensions(TypedDict):
    unit: Literal["inch", "centimeters"]  # default "inch"
    length: float
    width: float
    height: float


class Fee(TypedDict):
    amount: float
    currency: str
