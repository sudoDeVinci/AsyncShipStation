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


class InventoryWarehouse(TypedDict):
    inventory_warehouse_id: str
    name: str
    created_at: str
    updated_at: str


class InventoryLocation(InventoryWarehouse):
    inventory_location_id: str


class InventoryWarehouseListResponse(PaginatinatedResponse):
    inventory_warehouses: list[InventoryWarehouse]


class LocationListResponse(PaginatinatedResponse):
    inventory_locations: list[InventoryLocation]
