from typing import Literal, cast

from ..common import (
    Endpoints,
    ErrorResponse,
    Fee,
    ShipStationClient,
)
from ._types import (
    Inventory,
    Location,
    LocationListResponse,
    Warehouse,
    WarehouseListResponse,
)


class InventoryPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
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

        endpoint = f"{cls._v2_endpoint}/{Endpoints.INVENTORY.value}"

        try:
            res = await cls.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                Inventory,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def update(
        cls: type[ShipStationClient],
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

        endpoint = f"{cls._v2_endpoint}/{Endpoints.INVENTORY.value}"

        try:
            res = await cls.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

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
        cls: type[ShipStationClient], page_size: int = 25, page: int = 1
    ) -> tuple[int, ErrorResponse | WarehouseListResponse]:
        params = {"page_size": page_size, "page": page}
        endpoint = f"{cls._v2_endpoint}/{Endpoints.INVENTORY_WAREHOUSES.value}"

        try:
            res = await cls.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                WarehouseListResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create_warehouse(
        cls: type[ShipStationClient], name: str
    ) -> tuple[int, ErrorResponse | Warehouse]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def get_warehouse_by_id(
        cls: type[ShipStationClient], inventory_warehouse_id: str
    ) -> tuple[int, ErrorResponse | Warehouse]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def update_warehouse_name(
        cls: type[ShipStationClient],
        inventory_warehouse_id: str,
        name: str,
    ) -> tuple[int, ErrorResponse | None]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def delete_warehouse(
        cls: type[ShipStationClient],
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
        cls: type[ShipStationClient],
        page_size: int,
    ) -> tuple[int, ErrorResponse | LocationListResponse]:
        """
        GET a list of inventory locations.
        /v2/inventory_locations?page_size={page_size}
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def create_new_location(
        cls: type[ShipStationClient],
        name: str,
        inventory_warehouse_id: str,
    ) -> tuple[int, ErrorResponse | Warehouse]:
        """
        POST a new inventory location.
        /v2/inventory_locations
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def get_location_by_id(
        cls: type[ShipStationClient], inventory_location_id: str
    ) -> tuple[int, ErrorResponse | Location]:
        """
        GET an inventory location by its ID.
        /v2/inventory_locations/{inventory_location_id}
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def update_location_name(
        cls: type[ShipStationClient],
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
        cls: type[ShipStationClient],
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
