import io
from asyncio import gather
from base64 import b64encode
from io import BytesIO
from typing import cast
from urllib.parse import parse_qs, urlparse

from pypdf import PdfReader, PdfWriter

from ..common import (
    Endpoints,
    ErrorResponse,
    LabelFormats,
    ShipStationClient,
)
from ..labels import Label


class DownloadPortal(ShipStationClient):
    @classmethod
    async def download_file(
        cls: type["DownloadPortal"],
        dir: str,
        subdir: str,
        filename: str,
        download: str = "string",
        rotation: int = 0,
    ) -> tuple[int, bytes | ErrorResponse]:
        endpoint = (
            f"{cls.v2_endpoint}/{Endpoints.DOWNLOADS.value}/{dir}/{subdir}/{filename}"
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

    @classmethod
    async def download_packing_slip(
        cls: type["DownloadPortal"], label: Label, dtype: LabelFormats = "pdf"
    ) -> tuple[int, bytes | ErrorResponse]:

        links = label["label_download"]
        pdf_href = links.get("pdf", links.get("href", None))

        try:
            if not pdf_href:
                raise Exception("Label download not found")

            parsed = urlparse(pdf_href)
            path_parts = parsed.path.split("/")
            filename_part = path_parts[-1]
            subdir_part = path_parts[-2]
            dir_part = path_parts[-3]

        except Exception as e:
            return cls.parse_unknown_exception(e)

        return await cls.download_file(dir_part, subdir_part, filename_part)

    @classmethod
    async def download_packing_slips(
        cls: type["DownloadPortal"], labels: list[Label], dtype: LabelFormats = "pdf"
    ) -> tuple[int, bytes | list[ErrorResponse]]:

        print(f"Downloading {len(labels)} packing slips")
        try:
            slips = await gather(
                *[cls.download_packing_slip(label, dtype) for label in labels]
            )

            writer = PdfWriter()
            errors = []
            for stat, slip in slips:
                if stat not in (200, 201):
                    if isinstance(slip, dict):
                        errors.append(cast(ErrorResponse, slip))
                    continue
                if not isinstance(slip, bytes):
                    errors.append(
                        {"status": stat, "message": "Failed to download packing slip"}
                    )
                    continue

                slip_pdf = PdfReader(BytesIO(slip))
                for page in slip_pdf.pages:
                    writer.add_page(page)

            out = BytesIO()
            writer.write(out)

            if errors:
                return 400, errors

            if out.tell() == 0:
                raise ValueError("No packing slips were downloaded")

            return 200, out.getvalue()

        except Exception as e:
            return [cls.parse_unknown_exception(e)]
