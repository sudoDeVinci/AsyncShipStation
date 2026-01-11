from typing import List, Literal

from ..common import Endpoints, ErrorResponse, ShipStationClient
from ._types import (
    RateQueryResponse,
    Shipment,
    ShipmentCreationRequest,
    ShipmentCreationResponse,
    ShipmentListResponse,
    ShipmentStatuses,
    ShipmentTag,
)


class ShipmentPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
        shipment_status: ShipmentStatuses | None = None,
        batch_id: str | None = None,
        pickup_id: str | None = None,
        created_at_start: str | None = None,
        created_at_end: str | None = None,
        modified_at_start: str | None = None,
        modified_at_end: str | None = None,
        sales_order_id: str | None = None,
        sort_dir: Literal["asc", "desc"] = "desc",
        shipment_number: str | None = None,
        ship_to_name: str | None = None,
        item_keyword: str | None = None,
        payment_date_start: str | None = None,
        payment_date_end: str | None = None,
        store_id: int | None = None,
        external_shipment_id: str | None = None,
        sort_by: Literal["modified_at", "created_at"] | None = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[int, ShipmentListResponse | ErrorResponse]:
        params = {
            "shipment_status": shipment_status,
            "batch_id": batch_id,
            "pickup_id": pickup_id,
            "created_at_start": created_at_start,
            "created_at_end": created_at_end,
            "modified_at_start": modified_at_start,
            "modified_at_end": modified_at_end,
            "sales_order_id": sales_order_id,
            "sort_dir": sort_dir,
            "shipment_number": shipment_number,
            "ship_to_name": ship_to_name,
            "item_keyword": item_keyword,
            "payment_date_start": payment_date_start,
            "payment_date_end": payment_date_end,
            "store_id": store_id,
            "external_shipment_id": external_shipment_id,
            "sort_by": sort_by,
            "page": page,
            "page_size": page_size,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f"{cls._v2_endpoint}/{Endpoints.SHIPMENTS.value}"

        try:
            res = await cls.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                ShipmentListResponse,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create(
        cls: type[ShipStationClient], shipments: List[ShipmentCreationRequest]
    ) -> tuple[int, ErrorResponse, ShipmentCreationResponse]:
        raise NotImplementedError("Shipment creation is not yet implemented.")

    @classmethod
    async def get_by_external_id(
        cls: type[ShipStationClient], external_shipment_id: str
    ) -> tuple[int, ErrorResponse, Shipment]:
        raise NotImplementedError("Get shipment by external ID is not yet implemented.")

    @classmethod
    async def get_by_id(
        cls: type[ShipStationClient], shipment_id: str
    ) -> tuple[int, ErrorResponse, Shipment]:
        raise NotImplementedError("Get shipment by ID is not yet implemented.")

    @classmethod
    async def cancel_by_id(
        cls: type[ShipStationClient], shipment_id: str
    ) -> tuple[int, ErrorResponse, None]:
        raise NotImplementedError("Cancel shipment by ID is not yet implemented.")

    @classmethod
    async def get_rates(
        cls: type[ShipStationClient], shipment_id: str
    ) -> tuple[int, ErrorResponse, RateQueryResponse]:
        raise NotImplementedError("Get shipment rates is not yet implemented.")

    @classmethod
    async def add_tag(
        cls: type[ShipStationClient], shipment_id: str, tag_name: str
    ) -> tuple[int, ErrorResponse, ShipmentTag]:
        raise NotImplementedError("Add tag to shipment is not yet implemented.")


__all__ = ["ShipmentPortal"]
