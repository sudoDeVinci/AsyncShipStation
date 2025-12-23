from typing import List, Literal, cast

from ..common._types import Endpoints, Error  # type: ignore[import-not-found, misc]
from ..common.base import (  # type: ignore[import-not-found, misc]
    API_ENDPOINT,
    ShipStationClient,
)
from ._types import (  # type: ignore[import-not-found, misc]
    BatchFulfillmentCreationResponse,
    FulfillmentGist,
    FulfillmentGistRequest,
    FulfillmentListResponse,
)


class Fulfillment(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
        ship_to_name: str,
        ship_to_country_code: str,
        shipment_number: str,
        shipment_id: str,
        fulfillment_id: str,
        batch_id: str,
        order_source_id: str,
        fulfillment_provider_code: str,
        tracking_number: str,
        ship_date_start: str,
        ship_date_end: str,
        create_date_start: str,
        create_date_end: str,
        page: int = 1,
        page_size: int = 25,
        sort_dir: Literal["asc", "desc"] = "asc",
        sort_by: Literal["created_at", "modified_at", "shipped_at"] = "created_at",
    ) -> tuple[int, FulfillmentListResponse | Error]:
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

        endpoint = f"{API_ENDPOINT}/{Endpoints.FULFILLMENTS}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
                json=data,
            )
            if res.status_code != 200:
                if "error_code" in res.json():
                    return (
                        res.status_code,
                        cast(Error, res.json()),
                    )
                else:
                    raise Exception(f"Unexpected response: {res.json()}")

        except Exception as e:
            return (
                500,
                cast(
                    Error,
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": "unknown",
                        "message": str(e),
                    },
                ),
            )

        return (res.status_code, cast(FulfillmentListResponse, res.json()))

    @classmethod
    async def create(
        cls: type[ShipStationClient],
        fulfillments: List[FulfillmentGist],
    ) -> tuple[int, Error | BatchFulfillmentCreationResponse]:
        """
        Create one or more fulfillments by marking shipments as shipped with tracking information.
        This will notify customers and marketplaces according to your configuration.
        """

        data: FulfillmentGistRequest = {"fulfillments": fulfillments}

        endpoint = f"{API_ENDPOINT}/{Endpoints.FULFILLMENTS}"

        try:
            res = await cls.request(
                "POST",
                endpoint,
                json=data,
            )
            if res.status_code != 200:
                if "error_code" in res.json():
                    return (
                        res.status_code,
                        cast(Error, res.json()),
                    )
                else:
                    raise Exception(f"Unexpected response: {res.json()}")

        except Exception as e:
            return (
                500,
                cast(
                    Error,
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": "unknown",
                        "message": str(e),
                    },
                ),
            )

        return (res.status_code, cast(BatchFulfillmentCreationResponse, res.json()))
