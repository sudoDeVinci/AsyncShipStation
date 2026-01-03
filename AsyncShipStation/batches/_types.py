from enum import Enum
from typing import Literal, TypedDict

from ..common import (
    URL,
    DisplayFormatScheme,
    Error,
    LabelDownload,
    LabelFormats,
    LabelLayouts,
    LabelMetaData,
    PaginatinatedResponse,
    PaginationLink,
    PaperlessDownload,
)

BatchStatuses = Literal[
    "open",
    "queued",
    "processing",
    "completed",
    "completed_with_errors",
    "archived",
    "notifying",
    "invalid",
]


class BatchStatus(Enum):
    OPEN = "open"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    ARCHIVED = "archived"
    NOTIFYING = "notifying"
    INVALID = "invalid"


class BatchLabel(LabelMetaData):
    display_scheme: DisplayFormatScheme  # default "label"


class ProcessLabel(BatchLabel):
    create_batch_and_process_labels: bool


class Batch(TypedDict):
    label_layout: LabelLayouts
    label_format: LabelFormats
    batch_id: str
    batch_number: str
    external_batch_id: str
    batch_notes: str
    created_at: str
    processed_at: str
    errors: int
    process_errors: list[Error]
    warnings: int
    completed: int
    forms: int
    count: int
    batch_shipments_url: URL
    batch_labels_url: URL
    batch_errors_url: URL
    label_download: LabelDownload
    form_download: URL
    paperless_download: PaperlessDownload
    status: BatchStatuses


class BatchListResponse(PaginatinatedResponse):
    batches: list[Batch]


class BatchResponseError(TypedDict):
    error: str
    shipment_id: str
    external_shipment_id: str


class BatchProcessErrorResponse(PaginationLink):
    errors: list[BatchResponseError]  # default is []
    links: PaginationLink
