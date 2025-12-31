from typing import Literal, cast

from ..common import (
    Endpoints,
    Error,
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
        sku: str,
        inventory_warehouse_id: str,
        inventory_location_id: str,
        group_by: Literal["warehouse", "location"],
        page_size: int,
    ) -> tuple[int, Error | Inventory]:
        params = {
            "sku": sku,
            "inventory_warehouse_id": inventory_warehouse_id,
            "inventory_location_id": inventory_location_id,
            "group_by": group_by,
            "page_size": page_size,
        }

        endpoint = f"{cls._endpoint}/{Endpoints.INVENTORY.value}"

        try:
            response = await cls.request("GET", endpoint, params=params)

            if response.status_code != 200:
                if "error_code" in response.json():
                    return response.status_code, cast(Error, response.json())

                raise Exception(
                    f"Unexpected response: {response.status_code} - {response.json()}"
                )

        except Exception as e:
            return (
                500,
                cast(
                    Error,
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": "unknown",
                        "message": str(e),
                    },
                ),
            )

        return response.status_code, cast(Inventory, response.json())

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
    ) -> tuple[int, Error | None]:
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

        endpoint = f"{cls._endpoint}/{Endpoints.INVENTORY.value}"

        try:
            response = await cls.request("POST", endpoint, json=payload)

            if response.status_code != 204:
                if "error_code" in response.json():
                    return response.status_code, cast(Error, response.json())

                raise Exception(
                    f"Unexpected response: {response.status_code} - {response.json()}"
                )

        except Exception as e:
            return (
                500,
                cast(
                    Error,
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": "unknown",
                        "message": str(e),
                    },
                ),
            )

        return response.status_code, None

    @classmethod
    async def list_warehouses(
        cls: type[ShipStationClient], page_size: int
    ) -> tuple[int, Error | WarehouseListResponse]:
        params = {"page_size": page_size}
        endpoint = f"{cls._endpoint}/{Endpoints.INVENTORY_WAREHOUSES.value}"

        try:
            response = await cls.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            if response.status_code != 200:
                if "error_code" in response.json():
                    return response.status_code, cast(Error, response.json())

                raise Exception(
                    f"Unexpected response: {response.status_code} - {response.json()}"
                )
        except Exception as e:
            return (
                500,
                cast(
                    Error,
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": "unknown",
                        "message": str(e),
                    },
                ),
            )

        return response.status_code, cast(WarehouseListResponse, response.json())

    @classmethod
    async def create_warehouse(
        cls: type[ShipStationClient], name: str
    ) -> tuple[int, Error | Warehouse]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def get_warehouse_by_id(
        cls: type[ShipStationClient], inventory_warehouse_id: str
    ) -> tuple[int, Error | Warehouse]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def update_warehouse_name(
        cls: type[ShipStationClient],
        inventory_warehouse_id: str,
        name: str,
    ) -> tuple[int, Error | None]:
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def delete_warehouse(
        cls: type[ShipStationClient],
        inventory_warehouse_id: str,
        remove_inventory: Literal["0", "1"],
    ) -> tuple[int, Error | None]:
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
    ) -> tuple[int, Error | LocationListResponse]:
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
    ) -> tuple[int, Error | Warehouse]:
        """
        POST a new inventory location.
        /v2/inventory_locations
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def get_location_by_id(
        cls: type[ShipStationClient], inventory_location_id: str
    ) -> tuple[int, Error | Location]:
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
    ) -> tuple[int, Error | None]:
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
    ) -> tuple[int, Error | None]:
        """
        DELETE an inventory location.
        /v2/inventory_locations/{inventory_location_id}?remove_inventory={remove_inventory}

        Args:
            inventory_location_id (str): The ID of the inventory location to delete.
            remove_inventory (str): If 1, remove all inventory from the location before deleting it. If 0 or missing and the location has On Hand inventory, the request will fail.
        """
        raise NotImplementedError("This method is not yet implemented.")
