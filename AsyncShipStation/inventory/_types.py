from typing import TypedDict

from ..common import Fee, PaginationLink


class InventoryItem(TypedDict):
    sku: str
    on_hand: int
    allocated: int
    available: int
    average_cost: Fee
    inventory_warehouse_id: str
    inventory_location_id: str


class Inventory(TypedDict):
    inventory: list[InventoryItem]
    total: int
    page: int
    pages: int
    links: list[PaginationLink]


class Warehouse(TypedDict):
    inventory_warehouse_id: str
    name: str
    created_at: str
    updated_at: str


class Location(Warehouse):
    inventory_location_id: str


class WarehouseListResponse(TypedDict):
    inventory_warehouses: list[Warehouse]
    total: int
    page: int
    pages: int
    links: list[PaginationLink]


class LocationListResponse(TypedDict):
    inventory_locations: list[Location]
    total: int
    page: int
    pages: int
    links: list[PaginationLink]
