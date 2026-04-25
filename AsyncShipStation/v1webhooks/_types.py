from typing import Literal, TypedDict
from ..common._types import Taggable

V1WebhookEventValues = Literal[
    "ORDER_NOTIFY",
    "ITEM_ORDER_NOTIFY",
    "SHIP_NOTIFY",
    "ITEM_SHIP_NOTIFY",
    "FULFILLMENT_SHIPPED",
    "FULFILLMENT_REJECTED",
]


class V1WebhookSubscriptionResult(Taggable):
    id: int


class V1WebhookGist(Taggable):
    resource_url: str
    resource_type: V1WebhookEventValues


class V1Webhook(Taggable):
    IsLabelAPIHook: bool
    WebHookID: int
    SellerID: int
    StoreID: int
    HookType: V1WebhookEventValues
    MessageFormat: str
    Url: str
    Name: str
    BulkCopyBatchID: int | None
    BulkCopyRecordID: int | None
    Active: bool
    WebhookLogs: list[dict[str, str | int | bool | None]]
    Seller: str | None
    Store: str | None


class V1WebhookListResponse(Taggable):
    webhooks: list[V1Webhook]