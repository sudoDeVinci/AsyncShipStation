from typing import cast

from ..common import (
    Endpoints,
    Error,
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
    ) -> tuple[int, CarrierListResponse | Error]:
        endpoint = f"{cls._endpoint}/{Endpoints.CARRIERS}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )
            json = res.json()
            if res.status_code not in (200, 207):
                if "error_code" in json:
                    return (
                        res.status_code,
                        cast(Error, json),
                    )
                else:
                    raise Exception(f"Unexpected response: {json}")
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

    @classmethod
    async def get_by_id(
        cls: type[ShipStationClient], carrier_id: str
    ) -> tuple[int, Carrier | Error]:
        endpoint = f"{cls._endpoint}/{Endpoints.CARRIERS}/{carrier_id}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )
            json = res.json()
            if res.status_code != 200:
                if "error_code" in json:
                    return (
                        res.status_code,
                        cast(Error, json),
                    )
                else:
                    raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(Carrier, json))

    @classmethod
    async def get_options(
        cls: type[ShipStationClient], carrier_id: str
    ) -> tuple[int, Error | AdvancedCarrierOptionList]:
        endpoint = f"{cls._endpoint}/{Endpoints.CARRIERS}/{carrier_id}/options"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )
            json = res.json()
            if res.status_code != 200:
                if "error_code" in json:
                    return (
                        res.status_code,
                        cast(Error, json),
                    )
                else:
                    raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(AdvancedCarrierOptionList, json))

    @classmethod
    async def get_packages(
        cls: type[ShipStationClient], carrier_id: str
    ) -> tuple[int, Error | PackageList]:
        endpoint = f"{cls._endpoint}/{Endpoints.CARRIERS}/{carrier_id}/packages"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )
            json = res.json()
            if res.status_code != 200:
                if "error_code" in json:
                    return (
                        res.status_code,
                        cast(Error, json),
                    )
                else:
                    raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(PackageList, json))

    @classmethod
    async def get_services(
        cls: type[ShipStationClient], carrier_id: str
    ) -> tuple[int, Error | ServiceList]:
        endpoint = f"{cls._endpoint}/{Endpoints.CARRIERS}/{carrier_id}/services"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )
            json = res.json()
            if res.status_code != 200:
                if "error_code" in json:
                    return (
                        res.status_code,
                        cast(Error, json),
                    )
                else:
                    raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(ServiceList, json))
