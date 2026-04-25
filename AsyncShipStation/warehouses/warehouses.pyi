from ..common import ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import Warehouse, WarehouseListResponse

class WarehousePortal(ShipStationClient):
    @classmethod
    async def where(
        cls: type["WarehousePortal"],
        connection: ShipStationConnection,
        identity: bool = False,
    ) -> tuple[int, WarehouseListResponse | ErrorResponse]: ...
    @classmethod
    async def get_by_id(
        cls: type["WarehousePortal"],
        connection: ShipStationConnection,
        warehouse_id: str,
        identity: bool = False,
    ) -> tuple[int, Warehouse | ErrorResponse]: ...
    @classmethod
    async def get_by_name(
        cls: type["WarehousePortal"],
        connection: ShipStationConnection,
        warehouse_name: str,
        identity: bool = False,
    ) -> tuple[int, Warehouse | ErrorResponse]: ...
