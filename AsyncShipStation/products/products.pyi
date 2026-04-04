from ..common import ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import ProductListResponse

class ProductPortal(ShipStationClient):
    @classmethod
    async def where(
        cls: type["ProductPortal"],
        connection: ShipStationConnection,
        sku: str | None = None,
        name: str | None = None,
        active: bool | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> tuple[int, ErrorResponse | ProductListResponse]: ...
