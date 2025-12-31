from typing import cast

from ..common import (
    Endpoints,
    Error,
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
    ) -> tuple[int, bytes | Error]:
        endpoint = (
            f"{cls._endpoint}/{Endpoints.DOWNLOADS.value}/{dir}/{subdir}/{filename}"
        )
        params = {
            "download": download,
            "rotation": rotation,
        }

        try:
            res = await cls.request(
                "GET",
                endpoint,
                params=params,
                headers={"content-type": "application/pdf"},
            )
            if res.status_code != 200:
                if "error_code" in res.json():
                    return (
                        res.status_code,
                        cast(Error, res.json()),
                    )
                else:
                    raise Exception(f"Unexpected response: {res.json()}")

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

        return (res.status_code, res.content)
