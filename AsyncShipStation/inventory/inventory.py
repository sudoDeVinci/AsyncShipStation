from typing import Literal, cast

from ..common import (
    Endpoints,
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
    ) -> tuple[int, ErrorResponse | Inventory]:
        params = {
            "sku": sku,
            "inventory_warehouse_id": inventory_warehouse_id,
            "inventory_location_id": inventory_location_id,
            "group_by": group_by,
            "page_size": page_size,
            "page": page,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f"{connection.v2_endpoint}/{Endpoints.INVENTORY.value}"

        try:
            res = await connection.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                Inventory,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

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
    ) -> tuple[int, ErrorResponse | None]:
        payload = {
            "transaction_type": transaction_type,
            "inventory_location_id": inventory_location_id,
            "sku": sku,
            "quantity": quantity,
        }
        optionals = {
            "cost": cost,
            "condition": condition,
            "lot": lot,
            "usable_start_date": usble_start_date,
            "usable_end_date": usable_end_date,
            "effective_at": effective_at,
            "reason": reason,
            "notes": notes,
            "new_inventory_location_id": new_inventory_location_id,
            "new_cost": new_cost,
            "new_condition": new_condition,
        }

        if transaction_type in ("adjust", "modify"):
            filtered = {k: v for k, v in optionals.items() if v is not None}
            payload.update(filtered)

        endpoint = f"{connection.v2_endpoint}/{Endpoints.INVENTORY.value}"

        try:
            res = await connection.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            if res.status_code == 204:
                return res.status_code, None

            status_code, result = cls.validate_response(
                res,
                (204,),
                type(None),
            )
            return status_code, cast(ErrorResponse, result)
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def list_warehouses(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        page_size: int = 25,
        page: int = 1,
    ) -> tuple[int, ErrorResponse | InventoryWarehouseListResponse]:
        params = {"page_size": page_size, "page": page}
        endpoint = f"{connection.v2_endpoint}/{Endpoints.INVENTORY_WAREHOUSES.value}"

        try:
            res = await connection.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                InventoryWarehouseListResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create_warehouse(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        name: str,
    ) -> tuple[int, ErrorResponse | InventoryWarehouse]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def get_warehouse_by_id(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_warehouse_id: str,
    ) -> tuple[int, ErrorResponse | InventoryWarehouse]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def update_warehouse_name(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_warehouse_id: str,
        name: str,
    ) -> tuple[int, ErrorResponse | None]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def delete_warehouse(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_warehouse_id: str,
        remove_inventory: Literal["0", "1"],
    ) -> tuple[int, ErrorResponse | None]:
        f"""
        GET a warehouse by its ID.
        /v2/inventory_warehouses/{inventory_warehouse_id}?remove_inventory={remove_inventory}'

        Parameters:
            inventory_warehouse_id (str): The ID of the warehouse to delete.
            remove_inventory (str): If 1, remove all inventory from the warehouse before deleting it. If 0 or missing and the warehouse has On Hand inventory, the request will fail.
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def list_locations(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        page_size: int,
    ) -> tuple[int, ErrorResponse | LocationListResponse]:
        """
        GET a list of inventory locations.
        /v2/inventory_locations?page_size={page_size}
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def create_new_location(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        name: str,
        inventory_warehouse_id: str,
    ) -> tuple[int, ErrorResponse | InventoryWarehouse]:
        """
        POST a new inventory location.
        /v2/inventory_locations
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def get_location_by_id(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_location_id: str,
    ) -> tuple[int, ErrorResponse | InventoryLocation]:
        """
        GET an inventory location by its ID.
        /v2/inventory_locations/{inventory_location_id}
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def update_location_name(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_location_id: str,
        name: str,
    ) -> tuple[int, ErrorResponse | None]:
        """
        PUT an inventory location's name.
        /v2/inventory_locations/{inventory_location_id}
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def delete_location(
        cls: type["InventoryPortal"],
        connection: ShipStationConnection,
        inventory_location_id: str,
        remove_inventory: Literal["0", "1"],
    ) -> tuple[int, ErrorResponse | None]:
        """
        DELETE an inventory location.
        /v2/inventory_locations/{inventory_location_id}?remove_inventory={remove_inventory}

        Args:
            inventory_location_id (str): The ID of the inventory location to delete.
            remove_inventory (str): If 1, remove all inventory from the location before deleting it. If 0 or missing and the location has On Hand inventory, the request will fail.
        """
        raise NotImplementedError("This method is not yet implemented.")
