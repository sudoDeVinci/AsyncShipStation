from typing import TypedDict

from ..common import Dimensions, Fee, PaginatinatedResponse, Weight


class ProductCategory(TypedDict):
    product_category_id: int
    name: str


class ProductTag(TypedDict):
    tag_id: int
    name: str
    color: str


class ProductAlias(TypedDict):
    store_id: int
    sku_alias: str


class ProductBundleComponent(TypedDict):
    bundle_product_id: int
    component_product_id: int
    sku: str
    quantity: int
    active: bool


class Product(TypedDict):
    product_id: int
    name: str
    sku: str
    upc: str | None
    thumbnail_url: str | None
    price: Fee
    dimensions: Dimensions
    weight: Weight
    internal_notes: str | None
    fulfillment_sku: str | None
    created_date: str
    modify_date: str
    active: bool
    product_category: ProductCategory | None
    preset_category: str | None
    warehouse_location: str | None
    default_carrier_code: str | None
    default_service_code: str | None
    default_package_code: str | None
    default_intl_service_code: str | None
    default_intl_package_code: str | None
    default_confirmation: str | None
    default_intl_confirmation: str | None
    custom_description: str | None
    customs_value: float | None
    customs_tariff_no: str | None
    customs_country_code: str | None
    no_customs: bool
    tags: list[ProductTag] | None
    aliases: list[ProductAlias] | None
    product_type: str | None
    is_returnable: bool
    should_override_name: bool | None
    is_bundle: bool | None
    bundle_components: list[ProductBundleComponent] | None
    auto_split_option: str
    auto_split_custom_quantity: int | None


class ProductListResponse(PaginatinatedResponse):
    products: list[Product]
