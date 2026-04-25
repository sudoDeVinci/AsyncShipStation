from ..common import (
    ErrorResponse,
    LabelFormats,
    ShipStationClient,
    ShipStationConnection,
)
from ..labels import Label
from ._types import DownloadError

def create_packing_slip_page(order_id: str | None) -> bytes: ...

class DownloadPortal(ShipStationClient):
    @classmethod
    async def download_file(
        cls: type["DownloadPortal"],
        connection: ShipStationConnection,
        dir: str,
        subdir: str,
        filename: str,
        download: str = "string",
        rotation: int = 0,
        identity: bool = False,
    ) -> tuple[int, bytes | ErrorResponse]: ...
    @classmethod
    async def download_packing_slip(
        cls: type["DownloadPortal"],
        connection: ShipStationConnection,
        label: Label,
        dtype: LabelFormats = "pdf",
        identity: bool = False,
    ) -> tuple[int, bytes | ErrorResponse]: ...
    @classmethod
    async def download_packing_slips(
        cls: type["DownloadPortal"],
        connection: ShipStationConnection,
        labels: list[Label],
        dtype: LabelFormats = "pdf",
        include_dummy_slips: bool = True,
        timeout: int | None = None,
        interval: int = 2,
        identity: bool = False,
    ) -> tuple[int, tuple[bytes, list[DownloadError]]]: ...
