from typing import cast

from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import Warehouse, WarehouseListResponse


class WarehousePortal(ShipStationClient):
    @classmethod
    async def where(
        cls: type["WarehousePortal"],
        connection: ShipStationConnection,
        identity: bool = False,
    ) -> tuple[int, WarehouseListResponse | ErrorResponse]:
        endpoint = f"{connection.v2_endpoint}/{Endpoints.WAREHOUSES.value}"
        try:
            res = await connection.request("GET", endpoint)
            return cls.validate_response(
                res,
                (200,),
                WarehouseListResponse,
                identity=identity,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type["WarehousePortal"],
        connection: ShipStationConnection,
        warehouse_id: str,
        identity: bool = False,
    ) -> tuple[int, Warehouse | ErrorResponse]:
        endpoint = (
            f"{connection.v2_endpoint}/{Endpoints.WAREHOUSES.value}/{warehouse_id}"
        )
        try:
            res = await connection.request("GET", endpoint)
            return cls.validate_response(
                res,
                (200,),
                Warehouse,
                identity=identity,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_name(
        cls: type["WarehousePortal"],
        connection: ShipStationConnection,
        warehouse_name: str,
        identity: bool = False,
    ) -> tuple[int, Warehouse | ErrorResponse]:
        status, warehouses = await cls.where(connection)
        if status != 200:
            return status, cast(ErrorResponse, warehouses)
        warehouselist = cast(WarehouseListResponse, warehouses)
        for warehouse in warehouselist["warehouses"]:
            if warehouse["name"] == warehouse_name:
                return status, warehouse
        return cls.parse_unknown_exception(
            Exception(f"Warehouse with name '{warehouse_name}' not found.")
        )
