from asyncio import sleep as async_sleep
from typing import ClassVar, List, Literal, cast
from ..common import DisplayFormatSchemes, Endpoints, ErrorResponse, LabelFormats, LabelLayouts, ShipStationClient, ShipStationConnection
from ._types import Batch, BatchListResponse, BatchProcessErrorResponse, BatchStatuses, ProcessLabel

class BatchPortal(ShipStationClient):
    _BATCH_POLL_INTERVAL: ClassVar[float] = 2.0
    _BATCH_POLL_TIMEOUT: ClassVar[float] = 20.0

    @classmethod
    async def list(cls: type['BatchPortal'], connection: ShipStationConnection, status: BatchStatuses | None = None, batch_number: str | None = None, sort_by: Literal['ship_date', 'processed_at', 'created_at'] | None = None, page: int = 1, page_size: int = 25, sort_dir: Literal['asc', 'desc'] = 'desc') -> tuple[int, BatchListResponse | ErrorResponse]: ...

    @classmethod
    async def _poll_batch_until_ready(cls: type['BatchPortal'], connection: ShipStationConnection, batch_id: str, process_labels: bool = False, timeout: float | None = None, interval: float | None = None) -> tuple[bool, Batch | ErrorResponse]: ...

    @classmethod
    async def create(cls: type['BatchPortal'], connection: ShipStationConnection, external_batch_id: str | None, shipment_ids: List[str] | None, rate_ids: List[str] | None = None, batch_notes: str | None = None, process_labels: ProcessLabel | None = None, timeout: float | None = None, interval: float | None = None) -> tuple[int, Batch | ErrorResponse]: ...

    @classmethod
    async def get_by_external_id(cls: type['BatchPortal'], connection: ShipStationConnection, external_batch_id: str) -> tuple[int, Batch | ErrorResponse]: ...

    @classmethod
    async def get_by_batch_number(cls: type['BatchPortal'], connection: ShipStationConnection, batch_number: str, page: int = 1, page_size: int = 25) -> tuple[int, Batch | ErrorResponse]: ...

    @classmethod
    async def get_by_id(cls: type['BatchPortal'], connection: ShipStationConnection, batch_id: str) -> tuple[int, Batch | ErrorResponse]: ...

    @classmethod
    async def delete_by_id(cls: type['BatchPortal'], connection: ShipStationConnection, batch_id: str) -> tuple[int, None | ErrorResponse]: ...

    @classmethod
    async def archive_by_id(cls: type['BatchPortal'], connection: ShipStationConnection, batch_id: str) -> tuple[int, None | ErrorResponse]: ...

    @classmethod
    async def add_to_batch(cls: type['BatchPortal'], connection: ShipStationConnection, batch_id: str, external_batch_id: str, batch_notes: str | None = None, shipment_ids: List[str] | None = None, rate_ids: List[str] | None = None, process_labels: ProcessLabel | None = None) -> tuple[int, None | ErrorResponse]: ...

    @classmethod
    async def get_batch_errors(cls: type['BatchPortal'], connection: ShipStationConnection, batch_id: str, page: int = 1, page_size: int = 25) -> tuple[int, BatchProcessErrorResponse | ErrorResponse]: ...

    @classmethod
    async def process_batch_id_labels(cls: type['BatchPortal'], connection: ShipStationConnection, batch_id: str, label_layout: LabelLayouts = '4x6', label_format: LabelFormats = 'pdf', display_scheme: DisplayFormatSchemes = 'label', ship_date: str | None = None) -> tuple[int, None | ErrorResponse]: ...

    @classmethod
    async def remove_from_batch(cls: type['BatchPortal'], connection: ShipStationConnection, batch_id: str, shipment_ids: List[str] | None = None, rate_ids: List[str] | None = None) -> tuple[int, None | ErrorResponse]: ...
