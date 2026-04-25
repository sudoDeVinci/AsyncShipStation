from ..common import ErrorResponse, ShipStationClient, ShipStationConnection, V1Address
from ._types import V1Warehouse

class V1WarehousePortal(ShipStationClient):
    """
    In the API, the endpoint is called warehouse, but the process actually
    affects Ship From locations on the application side of operations.
    """

    @classmethod
    async def delete_by_id(
        cls: type["V1WarehousePortal"],
        connection: ShipStationConnection,
        warehouseId: int,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | dict[str, str]]: ...
    @classmethod
    async def get_by_id(
        cls: type["V1WarehousePortal"],
        connection: ShipStationConnection,
        warehouseId: int,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | V1Warehouse]: ...
    @classmethod
    async def get_by_name(
        cls: type["V1WarehousePortal"],
        connection: ShipStationConnection,
        warehouseName: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | V1Warehouse]: ...
    @classmethod
    async def where(
        cls: type["V1WarehousePortal"],
        connection: ShipStationConnection,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | list[V1Warehouse]]: ...
    @classmethod
    async def create(
        cls: type["V1WarehousePortal"],
        connection: ShipStationConnection,
        originAddress: V1Address,
        warehouseName: str | None = None,
        returnAddress: V1Address | None = None,
        isDefault: bool = False,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | V1Warehouse]: ...

__all__ = ["V1WarehousePortal", "V1Warehouse"]
