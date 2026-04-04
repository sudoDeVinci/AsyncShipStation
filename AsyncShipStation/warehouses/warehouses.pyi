from typing import cast
from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import Warehouse, WarehouseListResponse

class WarehousePortal(ShipStationClient):
    @classmethod
    async def list(cls: type['WarehousePortal'], connection: ShipStationConnection) -> tuple[int, WarehouseListResponse | ErrorResponse]: ...

    @classmethod
    async def get_by_id(cls: type['WarehousePortal'], connection: ShipStationConnection, warehouse_id: str) -> tuple[int, Warehouse | ErrorResponse]: ...

    @classmethod
    async def get_by_name(cls: type['WarehousePortal'], connection: ShipStationConnection, warehouse_name: str) -> tuple[int, Warehouse | ErrorResponse]: ...
