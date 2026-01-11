from typing import cast

from ..common import (
    Endpoints,
    ErrorResponse,
    ShipStationClient,
)


class DownloadPortal(ShipStationClient):
    @classmethod
    async def download_file(
        cls: type[ShipStationClient],
        dir: str,
        subdir: str,
        filename: str,
        download: str,
        rotation: int = 0,
    ) -> tuple[int, bytes | ErrorResponse]:
        endpoint = (
            f"{cls._v2_endpoint}/{Endpoints.DOWNLOADS.value}/{dir}/{subdir}/{filename}"
        )
        params = {
            "download": download,
            "rotation": rotation,
        }

        try:
            res = await cls.request(
                "GET",
                endpoint,
                params=params,  # type: ignore[arg-type]
                headers={"content-type": "application/pdf"},
            )
            if res.status_code != 200:
                json = res.json()
                if "errors" in json:
                    return (res.status_code, cast(ErrorResponse, json))
                raise Exception(f"Unexpected response: {json}")

        except Exception as e:
            return cls.parse_unknown_exception(e)

        return (res.status_code, res.content)
