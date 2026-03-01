from ..common import Endpoints, ErrorResponse, ShipStationClient
from ._types import (
    V1WebhookEventValues,
    V1WebhookListResponse,
    V1WebhookSubscriptionResult,
)


class V1WebhookPortal(ShipStationClient):
    @classmethod
    async def subscribe(
        cls: type["V1WebhookPortal"],
        event: V1WebhookEventValues,
        target_url: str,
        store_id: int | None = None,
        friendly_name: str | None = None,
    ) -> tuple[int, ErrorResponse | V1WebhookSubscriptionResult]:
        """ """
        payload = {
            "event": event,
            "target_url": target_url,
            "store_id": store_id,
            "friendly_name": friendly_name,
        }

        endpoint = f"{cls._v1_endpoint}/{Endpoints.V1WEBHOOKS.value}/subscribe"

        try:
            res = await cls.request("POST", endpoint, "v2", json=payload)  # type: ignore[arg-type]

            return cls.validate_response(res, (200, 201), V1WebhookSubscriptionResult)

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def unsubscribe(
        cls: type["V1WebhookPortal"],
        webhookId: int,
    ) -> tuple[int, ErrorResponse | None]:
        """ """
        endpoint = f"{cls._v1_endpoint}/{Endpoints.V1WEBHOOKS.value}/{webhookId}"

        try:
            res = await cls.request("DELETE", endpoint, "v1")

            return cls.validate_response(
                res,
                (200, 201),
                type(None),
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def list(
        cls: type["V1WebhookPortal"],
    ) -> tuple[int, ErrorResponse | V1WebhookListResponse]:
        """ """
        endpoint = f"{cls._v1_endpoint}/{Endpoints.V1WEBHOOKS.value}"

        try:
            res = await cls.request("GET", endpoint, "v1")

            return cls.validate_response(res, (200, 201), V1WebhookListResponse)

        except Exception as e:
            return cls.parse_unknown_exception(e)


__all__ = ("V1WebhookPortal",)
