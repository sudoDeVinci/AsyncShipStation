from enum import Enum
from typing import Literal, TypedDict

from ..common._types import Endpoints, ShipPortal

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


BatchLabelLayouts = Literal["4x6", "letter"]


class BatchLabelLayout(Enum):
    LAYOUT_4X6 = "4x6"
    LAYOUT_LETTER = "letter"


BatchLabelFormats = Literal["pdf", "zpl", "png"]
class BatchLabelFormat(Enum):
    PDF = "pdf"
    ZPL = "zpl"
    PNG = "png"


class Batch(TypedDict):
    label_layout: BatchLabelLayouts
    label_format: BatchLabelFormats
    batch_id: str
    batch_number: str
    external_batch_id: str
    batch_notes: str
    created_at: str
    processed_at: str
    errors: int


class BatchListResponse(TypedDict):
    batches: list[dict]
    total: int
    page: int
    pages: int
    links: dict
