from typing import Sequence, cast

from ..common import Endpoints, Error, ErrorResponse, Header, ShipStationClient
from ._types import Webhook, WebhookEventValues


class WebhookPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
        webhook_id: str | None = None,
        event: WebhookEventValues | None = None,
        headers: Sequence[Header] | None = None,
        name: str | None = None,
        store_id: int | None = None,
    ) -> tuple[int, list[Webhook] | ErrorResponse]:
        """
        List all webhooks.

        Returns:
            tuple[int, list[Webhook] | ErrorResponse]: A tuple containing the status code and either a list of webhooks or an error response.
        """

        params = {
            "webhook_id": webhook_id,
            "event": event,
            "headers": headers,
            "name": name,
            "store_id": store_id,
        }

        endpoint = f"{cls.v2_endpoint}/{Endpoints.WEBHOOKS.value}"

        try:
            res = await cls.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(res, (200,), list[Webhook])

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create(
        cls: type[ShipStationClient],
        name: str,
        event: WebhookEventValues,
        url: str,
        headers: Sequence[Header] | None = None,
        store_id: int | None = None,
    ) -> tuple[int, Webhook | ErrorResponse]:

        payload = {
            "name": name,
            "event": event,
            "url": url,
            "headers": headers,
            "store_id": store_id,
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        endpoint = f"{cls.v2_endpoint}/{Endpoints.WEBHOOKS.value}"

        try:
            res = await cls.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(res, (200,), Webhook)

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type[ShipStationClient],
        webhook_id: str,
    ) -> tuple[int, Webhook | ErrorResponse]:

        endpoint = f"{cls.v2_endpoint}/{Endpoints.WEBHOOKS.value}/{webhook_id}"

        try:
            res = await cls.request("GET", endpoint)

            return cls.validate_response(res, (200,), Webhook)

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def delete_by_id(
        cls: type[ShipStationClient],
        webhook_id: str,
    ) -> tuple[int, None | ErrorResponse]:

        endpoint = f"{cls.v2_endpoint}/{Endpoints.WEBHOOKS.value}/{webhook_id}"

        try:
            res = await cls.request("DELETE", endpoint)

            return cls.validate_response(res, (204,), type(None))

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def update_by_id(
        cls: type[ShipStationClient],
        webhook_id: str,
        name: str | None = None,
        url: str | None = None,
        headers: Sequence[Header] | None = None,
    ) -> tuple[int, None | ErrorResponse]:

        payload = {
            "name": name,
            "url": url,
            "headers": headers,
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        if not payload:
            return 400, cast(
                ErrorResponse,
                {
                    "errors": [
                        cast(
                            Error,
                            {
                                "error_source": "order_source",
                                "error_type": "business_rules",
                                "error_code": "field_value_required",
                                "message": "At least one of 'name', 'url', or 'headers' must be provided for update.",
                            },
                        )
                    ],
                    "request_id": None,
                },
            )

        endpoint = f"{cls.v2_endpoint}/{Endpoints.WEBHOOKS.value}/{webhook_id}"

        try:
            res = await cls.request("PUT", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(res, (204,), type(None))

        except Exception as e:
            return cls.parse_unknown_exception(e)


__all__ = ("WebhookPortal",)
