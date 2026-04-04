from ..common import ErrorResponse, ShipStationClient, ShipStationConnection, V1Address
from ._types import V1Warehouse

class V1WarehousePortal(ShipStationClient):
    '\n    In the API, the endpoint is called warehouse, but the process actually\n    affects Ship From locations on the application side of operations.\n    '

    @classmethod
    async def delete_by_id(cls, connection: ShipStationConnection, warehouseId: int) -> tuple[int, ErrorResponse | dict[str, str]]: ...

    @classmethod
    async def get_by_id(cls, connection: ShipStationConnection, warehouseId: int) -> tuple[int, ErrorResponse | V1Warehouse]: ...

    @classmethod
    async def get_by_name(cls, connection: ShipStationConnection, warehouseName: str) -> tuple[int, ErrorResponse | V1Warehouse]: ...

    @classmethod
    async def list(cls, connection: ShipStationConnection) -> tuple[int, ErrorResponse | list[V1Warehouse]]: ...

    @classmethod
    async def create(cls, connection: ShipStationConnection, originAddress: V1Address, warehouseName: str | None = None, returnAddress: V1Address | None = None, isDefault: bool = False) -> tuple[int, ErrorResponse | V1Warehouse]: ...

__all__ = ['V1WarehousePortal', 'V1Warehouse']
