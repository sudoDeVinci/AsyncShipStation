from ..common import Endpoints, ErrorResponse, ShipStationClient
from ._types import Webhook


class WebhookPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
    ) -> tuple[int, list[Webhook] | ErrorResponse]:
        """
        List all webhooks.

        Returns:
            tuple[int, list[Webhook] | ErrorResponse]: A tuple containing the status code and either a list of webhooks or an error response.
        """

        endpoint = f"{cls.v2_endpoint}/{Endpoints.WEBHOOKS.value}"

        try:
            res = await cls.request("GET", endpoint)

            return cls.validate_response(res, (200,), list[Webhook])

        except Exception as e:
            return cls.parse_unknown_exception(e)


__all__ = ("WebhookPortal",)
