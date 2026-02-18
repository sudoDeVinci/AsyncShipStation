from typing import cast

from ..common import Endpoints, ErrorResponse, ShipStationClient, V1Address
from ._types import V1Warehouse


class V1WarehousePortal(ShipStationClient):
    """
    In the API, the endpoint is called warehouse, but the process actually affects Ship From locations on the application side of operations.
    """

    @classmethod
    async def delete_by_id(
        cls: type["V1WarehousePortal"],
        warehouseId: int,
    ) -> tuple[int, ErrorResponse | dict[str, str]]:

        endpoint = f"{cls._v1_endpoint}/{Endpoints.WAREHOUSES.value}/{warehouseId}"

        try:
            res = await cls.request("DELETE", endpoint, "v1")
            return cls.validate_response(
                res,
                (200, 204),
                dict[str, str],
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type["V1WarehousePortal"],
        warehouseId: int,
    ) -> tuple[int, ErrorResponse | V1Warehouse]:

        endpoint = f"{cls._v1_endpoint}/{Endpoints.WAREHOUSES.value}/{warehouseId}"

        try:
            res = await cls.request("GET", endpoint, "v1")
            return cls.validate_response(
                res,
                (200, 201),
                V1Warehouse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_name(
        cls: type["V1WarehousePortal"],
        warehouseName: str,
    ) -> tuple[int, ErrorResponse | V1Warehouse]:
        """
        Get a warehouse from the V1 endpoint. There is no way to directly get warehouses by their name,
        so we first call the list() endpoint, then filter the results by the given name.

        Args:
            warehouseName (str): The name of the warehouse to retrieve.

        Returns:
            tuple[int, ErrorResponse | V1Warehouse]: A tuple containing the HTTP status code and either an ErrorResponse or a V1Warehouse object.
        """

        status, warehouses = await cls.list()
        if status not in (200, 201):
            return status, cast(ErrorResponse, warehouses)

        warehouselist = cast(list[V1Warehouse], warehouses)
        for warehouse in warehouselist:
            if warehouse["warehouseName"] == warehouseName:
                return status, warehouse

        return cls.parse_unknown_exception(
            Exception(f"Warehouse with name '{warehouseName}' not found.")
        )

    @classmethod
    async def list(
        cls: type["V1WarehousePortal"],
    ) -> tuple[int, ErrorResponse | list[V1Warehouse]]:

        endpoint = f"{cls._v1_endpoint}/{Endpoints.WAREHOUSES.value}"

        try:
            res = await cls.request("GET", endpoint, "v1")
            return cls.validate_response(
                res,
                (200, 201),
                list[V1Warehouse],
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create(
        cls: type["V1WarehousePortal"],
        originAddress: V1Address,
        warehouseName: str | None = None,
        returnAddress: V1Address | None = None,
        isDefault: bool = False,
    ) -> tuple[int, ErrorResponse | V1Warehouse]:

        payload = {
            "warehouseName": warehouseName,
            "originAddress": originAddress,
            "returnAddress": returnAddress,
            "isDefault": isDefault,
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        endpoint = f"{cls._v1_endpoint}/{Endpoints.WAREHOUSES.value}/createwarehouse"

        try:
            res = await cls.request("POST", endpoint, "v1", json=payload)  # type: ignore[arg-type]
            return cls.validate_response(
                res,
                (200, 201),
                V1Warehouse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)


__all__ = ["V1WarehousePortal", "V1Warehouse"]
