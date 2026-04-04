from typing import Sequence, cast
from ..common import Endpoints, Error, ErrorResponse, Header, ShipStationClient, ShipStationConnection
from ._types import Webhook, WebhookEventValues

class WebhookPortal(ShipStationClient):
    @classmethod
    async def list(cls: type['WebhookPortal'], connection: ShipStationConnection, webhook_id: str | None = None, event: WebhookEventValues | None = None, headers: Sequence[Header] | None = None, name: str | None = None, store_id: int | None = None) -> tuple[int, list[Webhook] | ErrorResponse]: ...

    @classmethod
    async def create(cls: type['WebhookPortal'], connection: ShipStationConnection, name: str, event: WebhookEventValues, url: str, headers: Sequence[Header] | None = None, store_id: int | None = None) -> tuple[int, Webhook | ErrorResponse]: ...

    @classmethod
    async def get_by_id(cls: type['WebhookPortal'], connection: ShipStationConnection, webhook_id: str) -> tuple[int, Webhook | ErrorResponse]: ...

    @classmethod
    async def delete_by_id(cls: type['WebhookPortal'], connection: ShipStationConnection, webhook_id: str) -> tuple[int, None | ErrorResponse]: ...

    @classmethod
    async def update_by_id(cls: type['WebhookPortal'], connection: ShipStationConnection, webhook_id: str, name: str | None = None, url: str | None = None, headers: Sequence[Header] | None = None) -> tuple[int, None | ErrorResponse]: ...

__all__ = ('WebhookPortal',)
