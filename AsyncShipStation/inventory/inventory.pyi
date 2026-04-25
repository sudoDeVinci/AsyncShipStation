from typing import Literal

from ..common import (
    ErrorResponse,
    Fee,
    ShipStationClient,
    ShipStationConnection,
)
from ._types import (
    Inventory,
    InventoryLocation,
    InventoryWarehouse,
    InventoryWarehouseListResponse,
    LocationListResponse,
)

class InventoryPortal(ShipStationClient):
    @classmethod
    async def where(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        sku: str | None = None,
        inventory_warehouse_id: str | None = None,
        inventory_location_id: str | None = None,
        group_by: Literal["warehouse", "location"] | None = None,
        page_size: int = 25,
        page: int = 1,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | Inventory]: ...
    @classmethod
    async def update(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        transaction_type: Literal["increment", "decrement", "adjust", "modify"],
        inventory_location_id: str,
        sku: str,
        quantity: int,
        cost: Fee | None,
        condition: Literal["sellable", "damaged", "expired", "qa_hold"] | None = None,
        lot: str | None = None,
        usble_start_date: str | None = None,
        usable_end_date: str | None = None,
        effective_at: str | None = None,
        reason: str | None = None,
        notes: str | None = None,
        new_inventory_location_id: str | None = None,
        new_cost: Fee | None = None,
        new_condition: (
            Literal["sellable", "damaged", "expired", "qa_hold"] | None
        ) = None,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | None]: ...
    @classmethod
    async def list_warehouses(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        page_size: int = 25,
        page: int = 1,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | InventoryWarehouseListResponse]: ...
    @classmethod
    async def create_warehouse(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        name: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | InventoryWarehouse]: ...
    @classmethod
    async def get_warehouse_by_id(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_warehouse_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | InventoryWarehouse]: ...
    @classmethod
    async def update_warehouse_name(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_warehouse_id: str,
        name: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | None]: ...
    @classmethod
    async def delete_warehouse(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_warehouse_id: str,
        remove_inventory: Literal["0", "1"],
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | None]: ...
    @classmethod
    async def list_locations(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        page_size: int,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | LocationListResponse]: ...
    @classmethod
    async def create_new_location(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        name: str,
        inventory_warehouse_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | InventoryWarehouse]: ...
    @classmethod
    async def get_location_by_id(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_location_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | InventoryLocation]: ...
    @classmethod
    async def update_location_name(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_location_id: str,
        name: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | None]: ...
    @classmethod
    async def delete_location(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_location_id: str,
        remove_inventory: Literal["0", "1"],
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | None]: ...
