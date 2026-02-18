from typing import cast

from ..common import Endpoints, ErrorResponse, ShipStationClient
from ._types import Warehouse, WarehouseListResponse


class WarehousePortal(ShipStationClient):
    """Portal for interacting with the ShipStation Warehouses API (V2)."""

    @classmethod
    async def list(
        cls: type["WarehousePortal"],
    ) -> tuple[int, WarehouseListResponse | ErrorResponse]:
        """
        Retrieve a list of warehouses associated with the account.
        https://docs.shipstation.com/openapi/warehouses/list_warehouses

        Returns:
            Tuple of status code and WarehouseListResponse or ErrorResponse
        """
        endpoint = f"{cls.v2_endpoint}/{Endpoints.WAREHOUSES.value}"

        try:
            res = await cls.request("GET", endpoint)

            return cls.validate_response(
                res,
                (200,),
                WarehouseListResponse,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type["WarehousePortal"],
        warehouse_id: str,
    ) -> tuple[int, Warehouse | ErrorResponse]:
        """
        Retrieve warehouse data based on the warehouse ID.
        https://docs.shipstation.com/openapi/warehouses/get_warehouse_by_id

        Args:
            warehouse_id: The warehouse ID to retrieve

        Returns:
            Tuple of status code and Warehouse or ErrorResponse
        """
        endpoint = f"{cls.v2_endpoint}/{Endpoints.WAREHOUSES.value}/{warehouse_id}"

        try:
            res = await cls.request("GET", endpoint)

            return cls.validate_response(
                res,
                (200,),
                Warehouse,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_name(
        cls: type["WarehousePortal"],
        warehouse_name: str,
    ) -> tuple[int, Warehouse | ErrorResponse]:
        """
        Retrieve warehouse data based on the warehouse name. Since there is no direct endpoint to get a warehouse by name,
        we first call the list() endpoint, then filter the results by the given name.

        Args:
            warehouse_name: The name of the warehouse to retrieve

        Returns:
            Tuple of status code and Warehouse or ErrorResponse
        """
        status, warehouses = await cls.list()
        if status != 200:
            return status, cast(ErrorResponse, warehouses)

        warehouselist = cast(WarehouseListResponse, warehouses)
        for warehouse in warehouselist["warehouses"]:
            if warehouse["name"] == warehouse_name:
                return status, warehouse

        return cls.parse_unknown_exception(
            Exception(f"Warehouse with name '{warehouse_name}' not found.")
        )


__all__ = ["WarehousePortal"]
