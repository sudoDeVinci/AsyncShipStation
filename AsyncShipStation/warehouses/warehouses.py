from ..common import Endpoints, ErrorResponse, ShipStationClient
from ._types import Warehouse, WarehouseListResponse


class WarehousePortal(ShipStationClient):
    """Portal for interacting with the ShipStation Warehouses API (V2)."""

    @classmethod
    async def list(
        cls: type[ShipStationClient],
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
        cls: type[ShipStationClient],
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


__all__ = ["WarehousePortal"]
