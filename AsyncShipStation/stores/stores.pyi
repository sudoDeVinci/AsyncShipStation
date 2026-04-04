from typing import List

from ..common import ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import V1MarketPlace, V1Store

class StorePortal(ShipStationClient):
    @classmethod
    async def all(
        cls: type["StorePortal"],
        connection: ShipStationConnection,
        showInactive: bool | None = None,
        marketplaceId: int | None = None,
    ) -> tuple[int, ErrorResponse | List[V1Store]]: ...
    @classmethod
    async def list_marketplaces(
        cls: type["StorePortal"], connection: ShipStationConnection
    ) -> tuple[int, ErrorResponse | List[V1MarketPlace]]: ...
