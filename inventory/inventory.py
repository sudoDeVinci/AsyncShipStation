from typing import Literal, cast

from ..common._types import (  # type: ignore[import-not-found, misc]
    Endpoints,
    Error,
    Fee,
)
from ..common.base import (  # type: ignore[import-not-found, misc]
    API_ENDPOINT,
    ShipStationClient,
)
from ._types import Inventory  # type: ignore[import-not-found, misc]


class InventoryPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
        sku: str,
        inventory_warehouse_id: str,
        inventory_location_id: str,
        group_by: Literal["warehouse", "location"],
        page_size: int,
    ) -> tuple[int, Error | Inventory]:
        params = {
            "sku": sku,
            "inventory_warehouse_id": inventory_warehouse_id,
            "inventory_location_id": inventory_location_id,
            "group_by": group_by,
            "page_size": page_size,
        }

        endpoint = f"{API_ENDPOINT}/{Endpoints.INVENTORY.value}"

        try:
            response = await cls.request("GET", endpoint, params=params)

            if response.status_code != 200:
                if "error_code" in response.json():
                    return response.status_code, cast(Error, response.json())

                raise Exception(
                    f"Unexpected response: {response.status_code} - {response.json()}"
                )

        except Exception as e:
            return (
                500,
                cast(
                    Error,
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": "unknown",
                        "message": str(e),
                    },
                ),
            )

        return response.status_code, cast(Inventory, response.json())

    @classmethod
    async def update(
        cls: type[ShipStationClient],
        transaction_type: Literal["increment", "decrement", "adjust", "modify"],
        inventory_location_id: str,
        sku: str,
        quantity: int,
        cost: Fee | None,
        condition: Literal["sellable", "damaged", "expired", "qa_hold"] | None = None,
        lot: str | None = None,
        usble_start_date: str | None = None,
        usable_end_date: str | None = None,
        effective_at: str | None = None,
        reason: str | None = None,
        notes: str | None = None,
        new_inventory_location_id: str | None = None,
        new_cost: Fee | None = None,
        new_condition: (
            Literal["sellable", "damaged", "expired", "qa_hold"] | None
        ) = None,
    ) -> tuple[int, Error | None]:
        payload = {
            "transaction_type": transaction_type,
            "inventory_location_id": inventory_location_id,
            "sku": sku,
            "quantity": quantity,
        }
        optionals = {
            "cost": cost,
            "condition": condition,
            "lot": lot,
            "usable_start_date": usble_start_date,
            "usable_end_date": usable_end_date,
            "effective_at": effective_at,
            "reason": reason,
            "notes": notes,
            "new_inventory_location_id": new_inventory_location_id,
            "new_cost": new_cost,
            "new_condition": new_condition,
        }

        if transaction_type in ("adjust", "modify"):
            filtered = {k: v for k, v in optionals.items() if v is not None}
            payload.update(filtered)

        endpoint = f"{API_ENDPOINT}/{Endpoints.INVENTORY.value}"

        try:
            response = await cls.request("POST", endpoint, json=payload)

            if response.status_code != 204:
                if "error_code" in response.json():
                    return response.status_code, cast(Error, response.json())

                raise Exception(
                    f"Unexpected response: {response.status_code} - {response.json()}"
                )

        except Exception as e:
            return (
                500,
                cast(
                    Error,
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": "unknown",
                        "message": str(e),
                    },
                ),
            )

        return response.status_code, None
