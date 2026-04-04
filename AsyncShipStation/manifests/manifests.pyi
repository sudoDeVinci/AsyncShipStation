from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import Manifest, ManifestListResponse

class ManifestsPortal(ShipStationClient):
    @classmethod
    async def list(cls: type['ManifestsPortal'], connection: ShipStationConnection, label_ids: list[str] | None = None, warehouse_id: str | None = None, ship_date_start: str | None = None, ship_date_end: str | None = None, created_at_start: str | None = None, created_at_end: str | None = None, carrier_id: str | None = None, page: int = 1, page_size: int = 25) -> tuple[int, ErrorResponse | ManifestListResponse]: ...

    @classmethod
    async def create(cls: type['ManifestsPortal'], connection: ShipStationConnection) -> tuple[int, ErrorResponse, ManifestListResponse]: ...

    @classmethod
    async def get_by_id(cls: type['ManifestsPortal'], connection: ShipStationConnection, manifest_id: str) -> tuple[int, ErrorResponse, Manifest]: ...
