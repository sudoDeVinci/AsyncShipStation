from typing import List

from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import V1MarketPlace, V1Store


class StorePortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type["StorePortal"],
        connection: ShipStationConnection,
        showInactive: bool | None = None,
        marketplaceId: int | None = None,
    ) -> tuple[int, ErrorResponse | List[V1Store]]:
        params = {
            "showInactive": showInactive,
            "marketplaceId": marketplaceId,
        }
        params = {k: v for k, v in params.items() if v is not None}
        endpoint = f"{connection.v1_endpoint}/{Endpoints.STORES.value}"
        res = await connection.request("GET", endpoint, "v1", params=params)  # type: ignore[arg-type]
        try:
            return cls.validate_response(res, (200,), list[V1Store])
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def list_marketplaces(
        cls: type["StorePortal"],
        connection: ShipStationConnection,
    ) -> tuple[int, ErrorResponse | List[V1MarketPlace]]:
        endpoint = f"{connection.v1_endpoint}/{Endpoints.STORES.value}/marketplaces"
        res = await connection.request("GET", endpoint, "v1")
        try:
            return cls.validate_response(res, (200,), list[V1MarketPlace])
        except Exception as e:
            return cls.parse_unknown_exception(e)
