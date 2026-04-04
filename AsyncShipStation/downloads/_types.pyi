from ..common import ErrorResponse

class DownloadError(ErrorResponse, total=False):
    external_shipment_id: str | None
    external_order_id: str | None
    error: ErrorResponse
