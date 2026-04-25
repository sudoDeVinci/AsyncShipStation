from typing import Literal, NotRequired

from ..common import Header, Taggable

WebhookEventValues = Literal[
    "batch",
    "carrier_connected",
    "order_source_refresh_complete",
    "rate",
    "report_complete",
    "sales_orders_imported",
    "track",
    "batch_processed_v2",
    "fulfillment_rejected_v2",
    "fulfillment_shipped_v2",
    "label_created_v2",
    "shipment_created_v2",
    "track_event_v2",
]

class Webhook(Taggable, total=True):
    webhook_id: NotRequired[str]
    url: str
    event: WebhookEventValues
    headers: list[Header]
    name: str
    store_id: str
