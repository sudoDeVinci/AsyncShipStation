from typing import cast

from ..common import (
    Dimensions,
    Endpoints,
    ErrorResponse,
    PackageGist,
    ShipStationClient,
)
from ._types import PackageListResponse


class CustomPackagePortal(ShipStationClient):
    @classmethod
    async def create(
        cls: type[ShipStationClient],
        name: str,
        package_code: str,
        dimensions: Dimensions,
        package_id: str | None = None,
        description: str | None = None,
    ) -> tuple[int, PackageGist | ErrorResponse]:
        """
        You can define as many package types as you need, each with their own name, package code, and set of dimensions.
        If you have your own custom packaging with specific dimensions that you use frequently
        (either in place of or in addition to carrier-defined packages), you might find it helpful to define those custom
        package types to use more easily in your shipments. You can then simply include the package_code property in your
        shipment object, instead of the individual dimension properties.

        Args:
            name (str): Max 50 characters. Any custom name you choose to help identify the package.
            package_code (str): Max 50 characters. This is the code you will use in your shipment objects. Each custom package must add the prefix custom_ to the package_code or the request will be rejected with a HTTP 400, Bad Request status.
            dimensions (Dimensions): The dimensions of the package type.
            description (str | None): Max 255 characters. Any custom description you choose to help identify the package.
            package_id (str | None): Max 50 characters. This is the ID you will use in your shipment objects. Each custom package must add the prefix custom_ to the package_id or the request will be rejected with a HTTP 400, Bad Request status.
        Returns:

        """

        if not package_code.startswith("custom_"):
            package_code = f"custom_{package_code}"

        payload_items = {
            "name": name,
            "package_code": package_code,
            "dimensions": dimensions,
            "package_id": package_id,
            "description": description,
        }

        payload: PackageGist = cast(
            PackageGist, {k: v for k, v in payload_items.items() if v is not None}
        )

        endpoint = f"{cls.v2_endpoint}/{Endpoints.PACKAGES.value}"

        try:
            res = await cls.request("POST", endpoint, json=payload)  # type: ignore[arg-type]
            return cls.validate_response(res, (200, 207, 201), PackageGist)
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def list(
        cls: type[ShipStationClient],
    ) -> tuple[int, PackageListResponse | ErrorResponse]:
        """
        List your package types to get a response with an array of all the available custom packaging available in your account.
        """

        endpoint = f"{cls.v2_endpoint}/{Endpoints.PACKAGES.value}"

        try:
            res = await cls.request("GET", endpoint)
            return cls.validate_response(res, (200,), PackageListResponse)
        except Exception as e:
            return cls.parse_unknown_exception(e)


__all__ = ["CustomPackagePortal"]
