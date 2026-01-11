from typing import List, Literal, cast

from ..common import (
    Endpoints,
    ErrorResponse,
    ShipStationClient,
)
from ._types import (
    BatchFulfillmentCreationResponse,
    FulfillmentGist,
    FulfillmentGistRequest,
    FulfillmentListResponse,
)


class FulfillmentPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
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
    ) -> tuple[int, FulfillmentListResponse | ErrorResponse]:
        data = {
            "ship_to_name": ship_to_name,
            "ship_to_country_code": ship_to_country_code,
            "shipment_number": shipment_number,
            "shipment_id": shipment_id,
            "fulfillment_id": fulfillment_id,
            "batch_id": batch_id,
            "order_source_id": order_source_id,
            "fulfillment_provider_code": fulfillment_provider_code,
            "tracking_number": tracking_number,
            "ship_date_start": ship_date_start,
            "ship_date_end": ship_date_end,
            "create_date_start": create_date_start,
            "create_date_end": create_date_end,
            "page": page,
            "page_size": page_size,
            "sort_dir": sort_dir,
            "sort_by": sort_by,
        }

        data = {k: v for k, v in data.items() if v is not None}

        endpoint = f"{cls._v2_endpoint}/{Endpoints.FULFILLMENTS.value}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
                params=data,  # type: ignore[arg-type]
            )

            return cls.validate_response(
                res,
                (200,),
                FulfillmentListResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create(
        cls: type[ShipStationClient],
        fulfillments: List[FulfillmentGist],
    ) -> tuple[int, ErrorResponse | BatchFulfillmentCreationResponse]:
        """
        Create one or more fulfillments by marking shipments as shipped with tracking information.
        This will notify customers and marketplaces according to your configuration.
        """

        data: FulfillmentGistRequest = {"fulfillments": fulfillments}

        endpoint = f"{cls._v2_endpoint}/{Endpoints.FULFILLMENTS.value}"

        try:
            res = await cls.request(
                "POST",
                endpoint,
                json=data,  # type: ignore[arg-type]
            )

            return cls.validate_response(
                res,
                (200,),
                BatchFulfillmentCreationResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)
