from ..common import (
    Endpoints,
    ErrorResponse,
    ShipStationClient,
    ShipStationConnection,
)
from ._types import (
    AdvancedCarrierOptionList,
    Carrier,
    CarrierListResponse,
    PackageList,
    ServiceList,
)


class CarrierPortal(ShipStationClient):
    @classmethod
    async def all(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        identity: bool = False,
    ) -> tuple[int, CarrierListResponse | ErrorResponse]:
        endpoint = f"{connection.v2_endpoint}/{Endpoints.CARRIERS.value}"

        try:
            res = await connection.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200, 207),
                CarrierListResponse,
                identity=identity,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        carrier_id: str,
        identity: bool = False,
    ) -> tuple[int, Carrier | ErrorResponse]:
        endpoint = f"{connection.v2_endpoint}/{Endpoints.CARRIERS.value}/{carrier_id}"

        try:
            res = await connection.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200,),
                Carrier,
                identity=identity,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_options(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        carrier_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | AdvancedCarrierOptionList]:
        endpoint = (
            f"{connection.v2_endpoint}/{Endpoints.CARRIERS.value}/{carrier_id}/options"
        )

        try:
            res = await connection.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200,),
                AdvancedCarrierOptionList,
                identity=identity,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_packages(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        carrier_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | PackageList]:
        endpoint = (
            f"{connection.v2_endpoint}/{Endpoints.CARRIERS.value}/{carrier_id}/packages"
        )

        try:
            res = await connection.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200,),
                PackageList,
                identity=identity,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_services(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        carrier_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | ServiceList]:
        endpoint = (
            f"{connection.v2_endpoint}/{Endpoints.CARRIERS.value}/{carrier_id}/services"
        )

        try:
            res = await connection.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200,),
                ServiceList,
                identity=identity,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)
