from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
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
    ) -> tuple[int, ErrorResponse | V1WebhookSubscriptionResult]:
        payload = {
            "event": event,
            "target_url": target_url,
            "store_id": store_id,
            "friendly_name": friendly_name,
        }
        endpoint = f"{connection.v1_endpoint}/{Endpoints.V1WEBHOOKS.value}/subscribe"
        try:
            res = await connection.request("POST", endpoint, "v2", json=payload)  # type: ignore[arg-type]
            return cls.validate_response(res, (200, 201), V1WebhookSubscriptionResult)
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def unsubscribe(
        cls: type["V1WebhookPortal"],
        connection: ShipStationConnection,
        webhookId: int,
    ) -> tuple[int, ErrorResponse | None]:
        endpoint = f"{connection.v1_endpoint}/{Endpoints.V1WEBHOOKS.value}/{webhookId}"
        try:
            res = await connection.request("DELETE", endpoint, "v1")
            return cls.validate_response(res, (200, 201), type(None))
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def all(
        cls: type["V1WebhookPortal"],
        connection: ShipStationConnection,
    ) -> tuple[int, ErrorResponse | V1WebhookListResponse]:
        endpoint = f"{connection.v1_endpoint}/{Endpoints.V1WEBHOOKS.value}"
        try:
            res = await connection.request("GET", endpoint, "v1")
            return cls.validate_response(res, (200, 201), V1WebhookListResponse)
        except Exception as e:
            return cls.parse_unknown_exception(e)
