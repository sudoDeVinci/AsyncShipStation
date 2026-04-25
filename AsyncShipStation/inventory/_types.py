from typing import TypedDict

from ..common import Fee, PaginatinatedResponse
from ..common._types import Taggable


class InventoryItem(Taggable):
    sku: str
    on_hand: int
    allocated: int
    available: int
    average_cost: Fee
    inventory_warehouse_id: str
    inventory_location_id: str


class Inventory(PaginatinatedResponse):
    inventory: list[InventoryItem]


class InventoryWarehouse(Taggable):
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