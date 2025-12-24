from typing import TypedDict

from ..common._types import Fee, PaginationLink  # type: ignore[import-not-found]


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
