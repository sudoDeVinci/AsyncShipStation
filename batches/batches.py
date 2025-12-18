from typing import Literal, cast

from requests import get

from ..common._types import (  # type: ignore[import-not-found]
    Endpoints,
    Error,
    ShipPortal,
)
from ..common.base import API_ENDPOINT, req  # type: ignore[import-not-found]
from ._types import (
    BatchLabelFormat,
    BatchLabelFormats,
    BatchLabelLayout,
    BatchLabelLayouts,
    BatchListResponse,
    BatchStatus,
    BatchStatuses,
)


class BatchPortal(ShipPortal):
    async def list_batches(
        cls: "BatchPortal",
        status: BatchStatuses,
        batch_number: str,
        sort_by: Literal["ship_date", "processed_at", "created_at"],
        page: int = 1,
        page_size: int = 25,
        sort_dir: Literal["asc", "desc"] = "desc",
    ) -> BatchListResponse | Error:
        params = {
            "status": status,
            "batch_number": batch_number,
            "sort_by": sort_by,
            "page": page,
            "page_size": page_size,
            "sort_dir": sort_dir,
        }
        endpoint = f"{API_ENDPOINT}/{Endpoints.BATCHES}"

        try:
            res = await req(
                fn=get,
                url=endpoint,
                params=params,
            )
            json = res.json()
            if res.status_code == 200:
                return cast(BatchListResponse, json)
            else:
                if "error_code" in json:
                    return cast(Error, json)
                else:
                    raise Exception(f"Unexpected response: {json}")
        except Exception as e:
            return cast(
                Error,
                {
                    "error_source": "ShipStation",
                    "error_type": "integrations",
                    "error_code": "unknown",
                    "message": str(e),
                },
            )
