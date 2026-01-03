from typing import TypedDict

from ..common import Fee, PaginatinatedResponse


class InventoryItem(TypedDict):
    sku: str
    on_hand: int
    allocated: int
    available: int
    average_cost: Fee
    inventory_warehouse_id: str
    inventory_location_id: str


class Inventory(PaginatinatedResponse):
    inventory: list[InventoryItem]


class Warehouse(TypedDict):
    inventory_warehouse_id: str
    name: str
    created_at: str
    updated_at: str


class Location(Warehouse):
    inventory_location_id: str


class WarehouseListResponse(PaginatinatedResponse):
    inventory_warehouses: list[Warehouse]


class LocationListResponse(PaginatinatedResponse):
    inventory_locations: list[Location]
