from typing import cast

from ..common import (
    Endpoints,
    ErrorResponse,
    ShipStationClient,
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
    async def list_carriers(
        cls: type[ShipStationClient],
    ) -> tuple[int, CarrierListResponse | ErrorResponse]:
        endpoint = f"{cls._v2_endpoint}/{Endpoints.CARRIERS}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200, 207),
                CarrierListResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type[ShipStationClient], carrier_id: str
    ) -> tuple[int, Carrier | ErrorResponse]:
        endpoint = f"{cls._v2_endpoint}/{Endpoints.CARRIERS}/{carrier_id}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200,),
                Carrier,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_options(
        cls: type[ShipStationClient], carrier_id: str
    ) -> tuple[int, ErrorResponse | AdvancedCarrierOptionList]:
        endpoint = f"{cls._v2_endpoint}/{Endpoints.CARRIERS}/{carrier_id}/options"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200,),
                AdvancedCarrierOptionList,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_packages(
        cls: type[ShipStationClient], carrier_id: str
    ) -> tuple[int, ErrorResponse | PackageList]:
        endpoint = f"{cls._v2_endpoint}/{Endpoints.CARRIERS}/{carrier_id}/packages"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200,),
                PackageList,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_services(
        cls: type[ShipStationClient], carrier_id: str
    ) -> tuple[int, ErrorResponse | ServiceList]:
        endpoint = f"{cls._v2_endpoint}/{Endpoints.CARRIERS}/{carrier_id}/services"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )

            return cls.validate_response(
                res,
                (200,),
                ServiceList,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)
