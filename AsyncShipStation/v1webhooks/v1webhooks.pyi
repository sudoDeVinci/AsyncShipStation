from ..common import ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import (
    V1WebhookEventValues,
    V1WebhookListResponse,
    V1WebhookSubscriptionResult,
)

class V1WebhookPortal(ShipStationClient):
    @classmethod
    async def subscribe(
        cls: type["V1WebhookPortal"],
        connection: ShipStationConnection,
        event: V1WebhookEventValues,
        target_url: str,
        store_id: int | None = None,
        friendly_name: str | None = None,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | V1WebhookSubscriptionResult]: ...
    @classmethod
    async def unsubscribe(
        cls: type["V1WebhookPortal"],
        connection: ShipStationConnection,
        webhookId: int,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | None]: ...
    @classmethod
    async def all(
        cls: type["V1WebhookPortal"],
        connection: ShipStationConnection,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | V1WebhookListResponse]: ...
