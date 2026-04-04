from asyncio import gather
from asyncio import sleep as async_sleep
from typing import ClassVar, List, Literal, cast
from ..common import DisplayFormatSchemes, Endpoints, ErrorResponse, LabelFormats, LabelLayouts, ShipStationClient, ShipStationConnection
from ._types import ChargeEvents, Label, LabelListResponse, LabelShipment, LabelStatuses, LabelVoidResponse, TrackingInformation

class LabelPortal(ShipStationClient):
    _BATCH_POLL_INTERVAL: ClassVar[float] = 2.0
    _BATCH_POLL_TIMEOUT: ClassVar[float] = 20.0

    @classmethod
    async def list(cls: type['LabelPortal'], connection: ShipStationConnection, label_status: LabelStatuses | None = None, service_code: str | None = None, carrier_id: str | None = None, tracking_number: str | None = None, batch_id: str | None = None, rate_id: str | None = None, shipment_id: str | None = None, warehouse_id: str | None = None, created_at_start: str | None = None, created_at_end: str | None = None, page: int = 1, page_size: int = 25, sort_dir: Literal['asc', 'desc'] = 'desc', sort_by: Literal['created_at', 'modified_at'] = 'created_at') -> tuple[int, LabelListResponse | ErrorResponse]: ...

    @classmethod
    async def list_for_shipments(cls: type['LabelPortal'], connection: ShipStationConnection, shipment_ids: List[str]) -> tuple[int, LabelListResponse, list[ErrorResponse]]: ...

    @classmethod
    async def poll_label_until_ready(cls: type['LabelPortal'], connection: ShipStationConnection, label_id: str, timeout: float | None = None, interval: float | None = None) -> tuple[bool, Label | ErrorResponse]: ...

    @classmethod
    async def poll_labels_until_ready(cls: type['LabelPortal'], connection: ShipStationConnection, label_ids: List[str], timeout: float | None = None, interval: float | None = None) -> tuple[bool, List[Label] | List[ErrorResponse]]: ...

    @classmethod
    async def purchase(cls: type['LabelPortal'], connection: ShipStationConnection, shipment: LabelShipment, charge_event: ChargeEvents, outbound_label_id: str, validate_address: Literal['no_validation', 'validate_only', 'validate_and_clean'] = 'no_validation', label_download_type: Literal['url', 'inline'] = 'url', is_return_label: bool = False, rma_number: str | None = None, ship_to_service_point_id: str | None = None, ship_from_service_point_id: str | None = None, label_format: LabelFormats = 'pdf', display_scheme: DisplayFormatSchemes = 'label', label_layout: LabelLayouts = '4x6', label_image_id: str | None = None, test_label: bool = False) -> tuple[int, ErrorResponse | Label]: ...

    @classmethod
    async def purchase_with_rate_id(cls: type['LabelPortal'], connection: ShipStationConnection, rate_id: str, validate_address: Literal['no_validation', 'validate_only', 'validate_and_clean'] = 'no_validation', label_layout: LabelLayouts = '4x6', label_format: LabelFormats = 'pdf', label_download_type: Literal['url', 'inline'] = 'url', display_scheme: DisplayFormatSchemes = 'label') -> tuple[int, ErrorResponse | Label]: ...

    @classmethod
    async def purchase_with_shipment_id(cls: type['LabelPortal'], connection: ShipStationConnection, shipment_id: str, validate_address: Literal['no_validation', 'validate_only', 'validate_and_clean'] = 'no_validation', label_layout: LabelLayouts = '4x6', label_format: LabelFormats = 'pdf', label_download_type: Literal['url', 'inline'] = 'url', display_scheme: DisplayFormatSchemes = 'label') -> tuple[int, ErrorResponse | Label]: ...

    @classmethod
    async def get_by_id(cls: type['LabelPortal'], connection: ShipStationConnection, label_id: str, label_download_type: Literal['url', 'inline'] = 'url') -> tuple[int, ErrorResponse | Label]: ...

    @classmethod
    async def create_return_label(cls: type['LabelPortal'], connection: ShipStationConnection, label_id: str, charge_event: ChargeEvents, label_layout: LabelLayouts = '4x6', label_format: LabelFormats = 'pdf', label_download_type: Literal['url', 'inline'] = 'url', display_scheme: DisplayFormatSchemes = 'label', label_image_id: str | None = None) -> tuple[int, ErrorResponse | Label]: ...

    @classmethod
    async def get_tracking_information(cls: type['LabelPortal'], connection: ShipStationConnection, label_id: str) -> tuple[int, ErrorResponse | TrackingInformation]: ...

    @classmethod
    async def void_label(cls: type['LabelPortal'], connection: ShipStationConnection, label_id: str) -> tuple[int, ErrorResponse | LabelVoidResponse]: ...
