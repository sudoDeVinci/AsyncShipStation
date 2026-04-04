from typing import cast

from ..carriers import PackageGist, PackageList
from ..common import (
    Dimensions,
    Endpoints,
    ErrorResponse,
    ShipStationClient,
    ShipStationConnection,
)


class CustomPackagePortal(ShipStationClient):
    @classmethod
    async def create(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
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

        endpoint = f"{connection.v2_endpoint}/{Endpoints.PACKAGES.value}"

        try:
            res = await connection.request("POST", endpoint, json=payload)  # type: ignore[arg-type]
            return cls.validate_response(res, (200, 207, 201), PackageGist)
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def all(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
    ) -> tuple[int, PackageList | ErrorResponse]:
        """
        List your package types to get a response with an array of all the available custom packaging available in your account.
        """

        endpoint = f"{connection.v2_endpoint}/{Endpoints.PACKAGES.value}"

        try:
            res = await connection.request("GET", endpoint)
            return cls.validate_response(res, (200,), PackageList)
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
        package_id: str,
    ) -> tuple[int, PackageGist | ErrorResponse]:
        """
        Retrieve a custom package by its ID.
        To obtain details about a specific custom package, like its dimensions and description, you'll use the GET method with the /v2/packages endpoint and the package_id.

        Args:
            package_id (str): The ID of the package to retrieve.

        Returns:
            tuple[int, PackageGist | ErrorResponse]: A tuple containing the HTTP status code and the package details or an error response.
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.PACKAGES.value}/{package_id}"

        try:
            res = await connection.request("GET", endpoint)
            return cls.validate_response(res, (200,), PackageGist)
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def update(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
        package_id: str,
        new_values: PackageGist,
    ) -> tuple[int, None | ErrorResponse]:
        """
        You can update the individual properties of your custom packages using the PUT method with the /v2/packages endpoint and the package_id.
        You'll need to include all the same properties in the request body as when you defined the custom package, with any new values for the properties you'd like to update.

        Args:
            package_id (str): The ID of the package to update.
            new_values (PackageGist): The new values for the package properties.

        Returns:
            tuple[int, None | ErrorResponse]: A tuple containing the HTTP status code and an error response if any.
        """

        endpoint = f"{connection.v2_endpoint}/{Endpoints.PACKAGES.value}/{package_id}"
        try:
            res = await connection.request("PUT", endpoint, json=new_values)  # type: ignore[arg-type]
            return cls.validate_response(res, (200,), type(None))
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def delete(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
        package_id: str,
    ) -> tuple[int, None | ErrorResponse]:
        """
        You can delete a custom package using the DELETE method with the /v2/packages endpoint and the package_id.
        Deleting a package will not disassociate it from any shipments. It will merely stop being available for use with future shipments and it will will no longer be included in the list packages response.
        You will need the package_id of the custom package you wish to delete.

        Args:
            package_id (str): The ID of the package to delete.

        Returns:
            tuple[int, None | ErrorResponse]: A tuple containing the HTTP status code and an error response if any.
        """

        endpoint = f"{connection.v2_endpoint}/{Endpoints.PACKAGES.value}/{package_id}"
        try:
            res = await connection.request("DELETE", endpoint)
            return cls.validate_response(res, (204,), type(None))
        except Exception as e:
            return cls.parse_unknown_exception(e)


__all__ = ["CustomPackagePortal"]
