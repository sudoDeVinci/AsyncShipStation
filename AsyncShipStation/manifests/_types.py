from typing import TypedDict

from AsyncShipStation.common import URL, Error, PaginatinatedResponse


class Manifest(TypedDict):
    manifest_id: str
    form_id: str
    created_at: str
    ship_date: str
    shipments: int
    label_ids: list[str]
    warehouse_id: str
    submission_id: str
    carrier_id: str
    manifest_download: URL


class ManifestError(Error):
    label_id: str


class ManifestListResponse(PaginatinatedResponse):
    manifests: list[Manifest]
    manifest_request_id: str
    status: str
    request_id: str
    errors: list[ManifestError]
