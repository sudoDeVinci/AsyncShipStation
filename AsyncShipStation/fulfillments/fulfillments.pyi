from typing import List, Literal

from ..common import ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import (
    BatchFulfillmentCreationResponse,
    FulfillmentGist,
    FulfillmentListResponse,
)

class FulfillmentPortal(ShipStationClient):
    @classmethod
    async def where(
        cls: type["FulfillmentPortal"],
        connection: ShipStationConnection,
        ship_to_name: str | None,
        ship_to_country_code: str | None,
        shipment_number: str | None,
        shipment_id: str | None,
        fulfillment_id: str | None,
        batch_id: str | None,
        order_source_id: str | None,
        fulfillment_provider_code: str | None,
        tracking_number: str | None,
        ship_date_start: str | None,
        ship_date_end: str | None,
        create_date_start: str | None,
        create_date_end: str | None,
        page: int = 1,
        page_size: int = 25,
        sort_dir: Literal["asc", "desc"] = "asc",
        sort_by: Literal["created_at", "modified_at", "shipped_at"] = "created_at",
        identity: bool = False,
    ) -> tuple[int, FulfillmentListResponse | ErrorResponse]: ...
    @classmethod
    async def create(
        cls: type["FulfillmentPortal"],
        connection: ShipStationConnection,
        fulfillments: List[FulfillmentGist],
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | BatchFulfillmentCreationResponse]: ...
