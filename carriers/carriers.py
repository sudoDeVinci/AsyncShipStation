from typing import Literal, cast

from ..common._types import Endpoints, Error  # type: ignore[import-not-found]
from ..common.base import (  # type: ignore[import-not-found]
    API_ENDPOINT,
    ShipStationClient,
)
from ._types import Carrier, CarrierListResponse


class Carriers(ShipStationClient):
    @classmethod
    async def list_carriers(
        cls: type["Carriers"],
    ) -> tuple[int, CarrierListResponse | Error]:
        """
        Retrieves a list of carriers associated with the account.

        Returns:
            CarrierListResponse: A dictionary containing the list of carriers and related information.
        """
        endpoint = f"{API_ENDPOINT}{Endpoints.CARRIERS}"

        try:
            res = await cls.request("GET", endpoint)
            json = res.json()
            if res.status_code not in (200, 207):
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))

                else:
                    raise Exception(f"Unexpected error format: {json}")
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

        return (res.status_code, cast(CarrierListResponse, json))
