from re import Pattern
from re import match as re_match
from typing import List, Literal, cast

from ..common import (
    Endpoints,
    ErrorResponse,
    ShipStationClient,
    ShipStationConnection,
)
from ._types import (
    RateQueryResponse,
    Shipment,
    ShipmentCreationRequest,
    ShipmentCreationResponse,
    ShipmentFilterResult,
    ShipmentListResponse,
    ShipmentStatuses,
    ShipmentTag,
)


class ShipmentPortal(ShipStationClient):
    @classmethod
    async def where(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        shipment_status: ShipmentStatuses | None = None,
        batch_id: str | None = None,
        pickup_id: str | None = None,
        created_at_start: str | None = None,
        created_at_end: str | None = None,
        modified_at_start: str | None = None,
        modified_at_end: str | None = None,
        sales_order_id: str | None = None,
        sort_dir: Literal["asc", "desc"] = "desc",
        shipment_number: str | None = None,
        ship_to_name: str | None = None,
        item_keyword: str | None = None,
        payment_date_start: str | None = None,
        payment_date_end: str | None = None,
        store_id: int | None = None,
        external_shipment_id: str | None = None,
        sort_by: Literal["modified_at", "created_at"] | None = None,
        page: int = 1,
        page_size: int = 25,
        identity: bool = False,
    ) -> tuple[int, ShipmentListResponse | ErrorResponse]:
        """
        Get a list of shipments.
        https://docs.shipstation.com/openapi/shipments/list_shipments

        Args:
            connection: The ShipStationConnection to use for the request.
            shipment_status: Filter by shipment status (pending, processing, label_purchased, cancelled)
            batch_id: Filter by batch ID
            pickup_id: Filter by pickup ID
            created_at_start: Filter by creation date start (ISO 8601)
            created_at_end: Filter by creation date end (ISO 8601)
            modified_at_start: Filter by modification date start (ISO 8601)
            modified_at_end: Filter by modification date end (ISO 8601)
            sales_order_id: Filter by sales order ID
            sort_dir: Sort direction (asc or desc)
            shipment_number: Filter by shipment number
            ship_to_name: Filter by recipient name
            item_keyword: Filter by item keyword
            payment_date_start: Filter by payment date start
            payment_date_end: Filter by payment date end
            store_id: Filter by store ID
            external_shipment_id: Filter by external shipment ID
            sort_by: Sort by field (modified_at or created_at)
            page: Page number (default 1)
            page_size: Results per page (default 25)

        Returns:
            Tuple of status code and ShipmentListResponse or ErrorResponse
        """
        params = {
            "shipment_status": shipment_status,
            "batch_id": batch_id,
            "pickup_id": pickup_id,
            "created_at_start": created_at_start,
            "created_at_end": created_at_end,
            "modified_at_start": modified_at_start,
            "modified_at_end": modified_at_end,
            "sales_order_id": sales_order_id,
            "sort_dir": sort_dir,
            "shipment_number": shipment_number,
            "ship_to_name": ship_to_name,
            "item_keyword": item_keyword,
            "payment_date_start": payment_date_start,
            "payment_date_end": payment_date_end,
            "store_id": store_id,
            "external_shipment_id": external_shipment_id,
            "sort_by": sort_by,
            "page": page,
            "page_size": page_size,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f"{connection.v2_endpoint}/{Endpoints.SHIPMENTS.value}"

        try:
            res = await connection.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                ShipmentListResponse,
                identity=identity,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        shipments: List[ShipmentCreationRequest],
        identity: bool = False,
    ) -> tuple[int, ShipmentCreationResponse | ErrorResponse]:
        """
        Create one or more shipments.
        https://docs.shipstation.com/openapi/shipments/create_shipments

        Args:
            connection: The ShipStationConnection to use for the request.
            shipments: List of shipment creation requests

        Returns:
            Tuple of status code and ShipmentCreationResponse or ErrorResponse
        """
        payload = {
            "shipments": shipments,
        }

        endpoint = f"{connection.v2_endpoint}/{Endpoints.SHIPMENTS.value}"

        try:
            res = await connection.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200, 207),
                ShipmentCreationResponse,
                identity=identity,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_external_id(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        external_shipment_id: str,
        identity: bool = False,
    ) -> tuple[int, Shipment | ErrorResponse]:
        """
        Retrieve a shipment by its external ID.
        https://docs.shipstation.com/openapi/shipments/get_shipment_by_external_id

        Args:
            connection: The ShipStationConnection to use for the request.
            external_shipment_id: The external shipment ID

        Returns:
            Tuple of status code and Shipment or ErrorResponse
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.SHIPMENTS.value}/external_shipment_id/{external_shipment_id}"

        try:
            res = await connection.request("GET", endpoint)

            return cls.validate_response(
                res,
                (200,),
                Shipment,
                identity=identity,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        shipment_id: str,
        identity: bool = False,
    ) -> tuple[int, Shipment | ErrorResponse]:
        """
        Retrieve a shipment by its ID.
        https://docs.shipstation.com/openapi/shipments/get_shipment_by_id

        Args:
            connection: The ShipStationConnection to use for the request.
            shipment_id: The shipment ID (e.g., se-12345678)

        Returns:
            Tuple of status code and Shipment or ErrorResponse
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.SHIPMENTS.value}/{shipment_id}"

        try:
            res = await connection.request("GET", endpoint)

            return cls.validate_response(
                res,
                (200,),
                Shipment,
                identity=identity,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_sku(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        sku: Pattern[str] | str,
        identity: bool = False,
        limit: int = 10,
        page_size: int = 25,
        page: int = 1,
    ) -> tuple[int, ShipmentFilterResult | ErrorResponse]:
        """
        Retrieve shipments that contain items matching a SKU pattern.

        Args:
            connection: The ShipStationConnection to use for the request.
            sku: A regex pattern or exact string to match against item SKUs in shipments.
        """

        outputs: list[Shipment] = []
        page = max(1, page)
        page_size = max(1, min(1000, page_size))
        page_offset = 0
        page_number = 1
        sufficient = False
        while not sufficient:
            page_number = page + page_offset
            status_code, shipments_response = await cls.where(
                connection, page=page_number, identity=identity, page_size=page_size
            )

            if status_code != 200:
                return (status_code, cast(ErrorResponse, shipments_response))

            if shipments_response.get("__kind__", None) != "ShipmentListResponse":
                return (status_code, cast(ErrorResponse, shipments_response))

            shipments = cast(list[Shipment], shipments_response.get("shipments", None))

            for shipment in shipments:
                for item in shipment["items"]:
                    item_sku = item.get("sku", "")
                    if not item_sku:
                        continue
                    if re_match(pattern=sku, string=item_sku):
                        outputs.append(shipment)

                    if len(outputs) >= limit:
                        sufficient = True
                        break

                if len(outputs) >= limit:
                    sufficient = True
                    break

            page_offset += 1

        out: ShipmentFilterResult = {
            "shipments": outputs,
            "page_stop": page_number,
            "pages": max(1, page_offset),
        }
        if identity:
            out["__kind__"] = "ShipmentFilterResult"
        return (200, out)

    @classmethod
    async def cancel_by_id(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        shipment_id: str,
        identity: bool = False,
    ) -> tuple[int, None | ErrorResponse]:
        """
        Cancel a shipment by its ID.
        https://docs.shipstation.com/openapi/shipments/cancel_shipments

        Note: You can only cancel a shipment if it hasn't been labeled yet.
        Once a label has been purchased, you must void the label instead.

        Args:
            connection: The ShipStationConnection to use for the request.
            shipment_id: The shipment ID to cancel

        Returns:
            Tuple of status code and None (on success) or ErrorResponse
        """
        endpoint = (
            f"{connection.v2_endpoint}/{Endpoints.SHIPMENTS.value}/{shipment_id}/cancel"
        )

        try:
            res = await connection.request("PUT", endpoint)

            if res.status_code == 204:
                return (res.status_code, None)

            return cls.validate_response(
                res,
                (204,),
                type(None),
                identity=identity,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_rates(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        shipment_id: str,
        created_at_start: str | None = None,
        identity: bool = False,
    ) -> tuple[int, RateQueryResponse | ErrorResponse]:
        """
        Get shipping rates for a shipment.
        https://docs.shipstation.com/openapi/shipments/list_shipment_rates

        Args:
            connection: The ShipStationConnection to use for the request.
            shipment_id: The shipment ID to get rates for
            created_at_start: Optional filter for rates created after this date (ISO 8601)

        Returns:
            Tuple of status code and RateQueryResponse or ErrorResponse
        """
        params: dict[str, object] = {}
        if created_at_start is not None:
            params["created_at_start"] = created_at_start

        endpoint = (
            f"{connection.v2_endpoint}/{Endpoints.SHIPMENTS.value}/{shipment_id}/rates"
        )

        try:
            res = await connection.request(
                "GET",
                endpoint,
                params=params if params else None,  # type: ignore[arg-type]
            )

            return cls.validate_response(
                res,
                (200,),
                RateQueryResponse,
                identity=identity,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def add_tag(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        shipment_id: str,
        tag_name: str,
        identity: bool = False,
    ) -> tuple[int, ShipmentTag | ErrorResponse]:
        """
        Add a tag to a shipment.
        https://docs.shipstation.com/openapi/shipments/tag_shipment

        Args:
            connection: The ShipStationConnection to use for the request.
            shipment_id: The shipment ID to tag
            tag_name: The name of the tag to add

        Returns:
            Tuple of status code and ShipmentTag or ErrorResponse
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.SHIPMENTS.value}/{shipment_id}/tags/{tag_name}"

        try:
            res = await connection.request("POST", endpoint)

            return cls.validate_response(
                res,
                (200, 201),
                ShipmentTag,
                identity=identity,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def remove_tag(
        cls: type["ShipmentPortal"],
        connection: ShipStationConnection,
        shipment_id: str,
        tag_name: str,
        identity: bool = False,
    ) -> tuple[int, None | ErrorResponse]:
        """
        Remove a tag from a shipment.
        https://docs.shipstation.com/openapi/shipments/untag_shipment

        Args:
            connection: The ShipStationConnection to use for the request.
            shipment_id: The shipment ID
            tag_name: The name of the tag to remove

        Returns:
            Tuple of status code and None (on success) or ErrorResponse
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.SHIPMENTS.value}/{shipment_id}/tags/{tag_name}"

        try:
            res = await connection.request("DELETE", endpoint)

            if res.status_code == 204:
                return (res.status_code, None)

            return cls.validate_response(
                res,
                (204,),
                type(None),
                identity=identity,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)


__all__ = ["ShipmentPortal"]
