from typing import TypedDict

from ..common import Dimensions, Error


class Service(TypedDict):
    carrier_id: str
    carrier_code: str
    service_code: str
    name: str
    domestic: bool
    international: bool
    is_multi_package_supported: bool


class ServiceList(TypedDict):
    services: list[Service]


class PackageGist(TypedDict):
    package_id: str
    package_code: str
    name: str
    dimensions: Dimensions
    description: str


class PackageList(TypedDict):
    packages: list[PackageGist]


class AdvancedCarrierOption(TypedDict):
    name: str
    default_value: str
    description: str


class AdvancedCarrierOptionList(TypedDict):
    options: list[AdvancedCarrierOption]


class Carrier(TypedDict):
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


class CarrierListResponse(TypedDict):
    carriers: list[Carrier]
    request_id: str
    errors: list[Error]
