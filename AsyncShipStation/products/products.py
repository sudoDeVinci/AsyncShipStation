from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import ProductListResponse


class ProductPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type["ProductPortal"],
        connection: ShipStationConnection,
        sku: str | None = None,
        name: str | None = None,
        active: bool | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> tuple[int, ErrorResponse | ProductListResponse]:
        params = {
            "sku": sku,
            "name": name,
            "active": active,
            "page": page,
            "page_size": page_size,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f"{connection.v2_endpoint}/{Endpoints.PRODUCTS.value}"

        try:
            res = await connection.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                ProductListResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)
