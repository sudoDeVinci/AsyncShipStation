from typing import TypedDict

from ..common import Dimensions, DisplayFormatSchemes, Error
from ..common._types import Taggable


class Service(Taggable):
    carrier_id: str
    carrier_code: str
    service_code: str
    name: str
    domestic: bool
    international: bool
    is_multi_package_supported: bool
    is_return_supported: bool
    display_schemes: list[DisplayFormatSchemes]


class ServiceList(Taggable):
    services: list[Service]


class PackageGist(Taggable):
    package_id: str
    package_code: str
    name: str
    dimensions: Dimensions
    description: str | None


class PackageList(Taggable):
    packages: list[PackageGist]


class AdvancedCarrierOption(Taggable):
    name: str
    default_value: str | None
    description: str


class AdvancedCarrierOptionList(Taggable):
    options: list[AdvancedCarrierOption]


class Carrier(Taggable):
    allows_returns: bool
    carrier_id: str
    carrier_code: str
    account_number: str
    requires_funded_amount: bool
    balance: float
    nickname: str
    friendly_name: str
    funding_source_id: str | None
    primary: bool
    has_multi_package_supporting_services: bool
    supports_label_messages: bool
    disabled_by_billing_plan: bool
    services: list[Service]
    packages: list[PackageGist]
    options: list[AdvancedCarrierOption]
    send_rates: bool
    supports_user_managed_rates: bool


class CarrierListResponse(Taggable):
    carriers: list[Carrier]
    request_id: str
    errors: list[Error]