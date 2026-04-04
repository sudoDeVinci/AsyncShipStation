from typing import List, Literal
from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import RateQueryResponse, Shipment, ShipmentCreationRequest, ShipmentCreationResponse, ShipmentListResponse, ShipmentStatuses, ShipmentTag

class ShipmentPortal(ShipStationClient):
    @classmethod
    async def list(cls: type['ShipmentPortal'], connection: ShipStationConnection, shipment_status: ShipmentStatuses | None = None, batch_id: str | None = None, pickup_id: str | None = None, created_at_start: str | None = None, created_at_end: str | None = None, modified_at_start: str | None = None, modified_at_end: str | None = None, sales_order_id: str | None = None, sort_dir: Literal['asc', 'desc'] = 'desc', shipment_number: str | None = None, ship_to_name: str | None = None, item_keyword: str | None = None, payment_date_start: str | None = None, payment_date_end: str | None = None, store_id: int | None = None, external_shipment_id: str | None = None, sort_by: Literal['modified_at', 'created_at'] | None = None, page: int = 1, page_size: int = 25) -> tuple[int, ShipmentListResponse | ErrorResponse]: ...

    @classmethod
    async def create(cls: type['ShipmentPortal'], connection: ShipStationConnection, shipments: List[ShipmentCreationRequest]) -> tuple[int, ShipmentCreationResponse | ErrorResponse]: ...

    @classmethod
    async def get_by_external_id(cls: type['ShipmentPortal'], connection: ShipStationConnection, external_shipment_id: str) -> tuple[int, Shipment | ErrorResponse]: ...

    @classmethod
    async def get_by_id(cls: type['ShipmentPortal'], connection: ShipStationConnection, shipment_id: str) -> tuple[int, Shipment | ErrorResponse]: ...

    @classmethod
    async def cancel_by_id(cls: type['ShipmentPortal'], connection: ShipStationConnection, shipment_id: str) -> tuple[int, None | ErrorResponse]: ...

    @classmethod
    async def get_rates(cls: type['ShipmentPortal'], connection: ShipStationConnection, shipment_id: str, created_at_start: str | None = None) -> tuple[int, RateQueryResponse | ErrorResponse]: ...

    @classmethod
    async def add_tag(cls: type['ShipmentPortal'], connection: ShipStationConnection, shipment_id: str, tag_name: str) -> tuple[int, ShipmentTag | ErrorResponse]: ...

    @classmethod
    async def remove_tag(cls: type['ShipmentPortal'], connection: ShipStationConnection, shipment_id: str, tag_name: str) -> tuple[int, None | ErrorResponse]: ...

__all__ = ['ShipmentPortal']
