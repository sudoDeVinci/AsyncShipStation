from typing import Literal

from ..common import (
    DisplayFormatSchemes,
    Endpoints,
    ErrorResponse,
    LabelFormats,
    LabelLayouts,
    ShipStationClient,
)
from ._types import (
    ChargeEvents,
    Label,
    LabelListResponse,
    LabelShipment,
    LabelStatuses,
    LabelVoidResponse,
    TrackingInformation,
)


class LabelPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
        label_status: LabelStatuses | None = None,
        service_code: str | None = None,
        carrier_id: str | None = None,
        tracking_number: str | None = None,
        batch_id: str | None = None,
        rate_id: str | None = None,
        shipment_id: str | None = None,
        warehouse_id: str | None = None,
        created_at_start: str | None = None,
        created_at_end: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_dir: Literal["asc", "desc"] = "desc",
        sort_by: Literal["created_at", "modified_at"] = "created_at",
    ) -> tuple[int, LabelListResponse | ErrorResponse]:
        """
        This method returns a list of labels that you've created. You can optionally filter the results as well as control their sort order and the number of results returned at a time.

        By default all labels are returned 25 at a time, starting with the most recently created ones. You can combine multiple filter options to narrow-down the results. For example, if you only want your UPS labels for your east coast warehouse you could query by both warehouse_id and carrier_id.

        Args:
            label_status (LabelStatuses | None, optional): Filter results by label status. Defaults to None.
            service_code (str | None, optional): Filter results by service code. Defaults to None.
            carrier_id (str | None, optional): Filter results by carrier ID. Defaults to None.
            tracking_number (str | None, optional): Filter results by tracking number. Defaults to None.
            batch_id (str | None, optional): Filter results by batch ID. Defaults to None.
            rate_id (str | None, optional): Filter results by rate ID. Defaults to None.
            shipment_id (str | None, optional): Filter results by shipment ID. Defaults to None.
            warehouse_id (str | None, optional): Filter results by warehouse ID. Defaults to None.
            created_at_start (str | None, optional): Filter results by creation date start (ISO 8601 format). Defaults to None.
            created_at_end (str | None, optional): Filter results by creation date end (ISO 8601 format). Defaults to None.
            page (int, optional): The page number of results to return. Defaults to 1.
            page_size (int, optional): The number of results to return per page. Defaults to 25.
            sort_dir (Literal["asc", "desc"], optional): The direction to sort the results. Defaults to "desc".
            sort_by (Literal["created_at", "modified_at"], optional): The field to sort the results by. Defaults to "created_at".

        Returns:
            tuple[int, LabelListResponse | ErrorResponse]: A tuple containing the HTTP status code and either
        """
        params = {
            "label_status": label_status,
            "service_code": service_code,
            "carrier_id": carrier_id,
            "tracking_number": tracking_number,
            "batch_id": batch_id,
            "rate_id": rate_id,
            "shipment_id": shipment_id,
            "warehouse_id": warehouse_id,
            "created_at_start": created_at_start,
            "created_at_end": created_at_end,
            "page": page,
            "page_size": page_size,
            "sort_dir": sort_dir,
            "sort_by": sort_by,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f"{cls._v2_endpoint}/{Endpoints.LABELS.value}"

        try:
            res = await cls.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                LabelListResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def purchase(
        cls: type[ShipStationClient],
        shipment: LabelShipment,
        charge_event: ChargeEvents,
        outbound_label_id: str,
        validate_address: Literal[
            "no_validation", "validate_only", "validate_and_clean"
        ] = "no_validation",
        label_download_type: Literal["url", "inline"] = "url",
        is_return_label: bool = False,
        rma_number: str | None = None,
        ship_to_service_point_id: str | None = None,
        ship_from_service_point_id: str | None = None,
        label_format: LabelFormats = "pdf",
        display_scheme: DisplayFormatSchemes = "label",
        label_layout: LabelLayouts = "4x6",
        label_image_id: str | None = None,
        test_label: bool = False,
    ) -> tuple[int, ErrorResponse | Label]:
        """
        This method allows you to purchase a shipping and print a label for a given shipment. You can specify various options such as the charge event, label format, and whether it's a return label.

        Args:
            shipment (Shipment): The shipment details for which the label is to be purchased.
            charge_event (ChargeEvents): The event that will trigger the charge for the label.
            outbound_label_id (str): The ID of the outbound label.
            validate_address (Literal["no_validation", "validate_only", "validate_and_clean"], optional): Address validation option. Defaults to "no_validation".
            label_download_type (Literal["url", "inline"], optional): The format in which the label will be downloaded. Defaults to "url".
            is_return_label (bool, optional): Indicates if the label is a return label. Defaults to False.
            rma_number (str | None, optional): The RMA number for return labels. Defaults to None.
            ship_to_service_point_id (str | None, optional): Service point ID for shipping to. Defaults to None.
            ship_from_service_point_id (str | None, optional): Service point ID for shipping from. Defaults to None.
            label_format (LabelFormats, optional): The format of the label. Defaults to "pdf".
            display_scheme (DisplayFormatSchemes, optional): The display scheme for the label. Defaults to "label".
            label_layout (LabelLayouts, optional): The layout of the label. Defaults to "4x6".
            label_image_id (str | None, optional): The image ID for the label. Defaults to None.
            test_label (bool, optional): Indicates if this is a test label. Defaults to False.

        Returns:
            tuple[int, ErrorResponse | Label]: A tuple containing the HTTP status code and either an ErrorResponse or the purchased Label.
        """
        payload = {
            "shipment": shipment,
            "charge_event": charge_event,
            "outbound_label_id": outbound_label_id,
            "validate_address": validate_address,
            "label_download_type": label_download_type,
            "is_return_label": is_return_label,
            "rma_number": rma_number,
            "ship_to_service_point_id": ship_to_service_point_id,
            "ship_from_service_point_id": ship_from_service_point_id,
            "label_format": label_format,
            "display_scheme": display_scheme,
            "label_layout": label_layout,
            "label_image_id": label_image_id,
            "test_label": test_label,
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        endpoint = f"{cls._v2_endpoint}/{Endpoints.LABELS.value}"

        try:
            res = await cls.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                Label,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def purchase_with_rate_id(
        cls: type[ShipStationClient],
        rate_id: str,
        validate_address: Literal[
            "no_validation", "validate_only", "validate_and_clean"
        ] = "no_validation",
        label_layout: LabelLayouts = "4x6",
        label_format: LabelFormats = "pdf",
        label_download_type: Literal["url", "inline"] = "url",
        display_scheme: DisplayFormatSchemes = "label",
    ) -> tuple[int, ErrorResponse | Label]:
        """
        When retrieving rates for shipments using the /rates endpoint, the returned information contains a rate_id property that can be used to generate a label without having to refill in the shipment information repeatedly

        Args:
            rate_id (str): The ID of the rate to be used for purchasing the label.
            validate_address (Literal["no_validation", "validate_only", "validate_and_clean"], optional): Address validation option. Defaults to "no_validation".
            label_layout (LabelLayouts, optional): The layout of the label. Defaults to "4x6".
            label_format (LabelFormats, optional): The format of the label. Defaults to "pdf".
            label_download_type (Literal["url", "inline"], optional): The format in which the label will be downloaded. Defaults to "url".
            display_scheme (DisplayFormatSchemes, optional): The display scheme for the label. Defaults to "label".

        Returns:
            tuple[int, ErrorResponse | Label]: A tuple containing the HTTP status code and either an ErrorResponse or the purchased Label.
        """
        payload = {
            "validate_address": validate_address,
            "label_layout": label_layout,
            "label_format": label_format,
            "label_download_type": label_download_type,
            "display_scheme": display_scheme,
        }

        endpoint = f"{cls._v2_endpoint}/{Endpoints.LABELS.value}/rates/{rate_id}"

        try:
            res = await cls.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                Label,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def purchase_with_shipment_id(
        cls: type[ShipStationClient],
        shipment_id: str,
        validate_address: Literal[
            "no_validation", "validate_only", "validate_and_clean"
        ] = "no_validation",
        label_layout: LabelLayouts = "4x6",
        label_format: LabelFormats = "pdf",
        label_download_type: Literal["url", "inline"] = "url",
        display_scheme: DisplayFormatSchemes = "label",
    ) -> tuple[int, ErrorResponse | Label]:
        """
        Purchase a label using a shipment ID that has already been created with the desired address and package info.

        Args:
            shipment_id (str): The ID of the shipment to be used for purchasing the label.
            validate_address (Literal["no_validation", "validate_only", "validate_and_clean"], optional): Address validation option. Defaults to "no_validation".
            label_layout (LabelLayouts, optional): The layout of the label. Defaults to "4x6".
            label_format (LabelFormats, optional): The format of the label. Defaults to "pdf".
            label_download_type (Literal["url", "inline"], optional): The format in which the label will be downloaded. Defaults to "url".
            display_scheme (DisplayFormatSchemes, optional): The display scheme for the label. Defaults to "label".

        Returns:
            tuple[int, ErrorResponse | Label]: A tuple containing the HTTP status code and either an ErrorResponse or the purchased Label.
        """
        payload = {
            "validate_address": validate_address,
            "label_layout": label_layout,
            "label_format": label_format,
            "label_download_type": label_download_type,
            "display_scheme": display_scheme,
        }

        endpoint = f"{cls._v2_endpoint}/{Endpoints.LABELS.value}/shipment/{shipment_id}"

        try:
            res = await cls.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                Label,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type[ShipStationClient],
        label_id: str,
        label_download_type: Literal["url", "inline"] = "url",
    ) -> tuple[int, ErrorResponse | Label]:
        """
        This method retrieves the details of a specific label using its unique ID.

        Args:
            label_id (str): The unique identifier of the label to be retrieved.
            label_download_type (Literal["url", "inline"], optional): The format in which the label was downloaded. Defaults to "url".
        Returns:
            tuple[int, ErrorResponse | Label]: A tuple containing the HTTP status code and either an ErrorResponse or the requested Label.
        """
        endpoint = f"{cls._v2_endpoint}/{Endpoints.LABELS.value}/{label_id}?label_download_type={label_download_type}"

        try:
            res = await cls.request("GET", endpoint)

            return cls.validate_response(
                res,
                (200,),
                Label,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create_return_label(
        cls: type[ShipStationClient],
        label_id: str,
        charge_event: ChargeEvents,
        label_layout: LabelLayouts = "4x6",
        label_format: LabelFormats = "pdf",
        label_download_type: Literal["url", "inline"] = "url",
        display_scheme: DisplayFormatSchemes = "label",
        label_image_id: str | None = None,
    ) -> tuple[int, ErrorResponse | Label]:
        """
        Create a return label for a previously created outbound label.
        The return label will automatically swap the ship to and ship from addresses from the original label.

        Args:
            label_id (str): The ID of the outbound label for which the return label is to be created.
            charge_event (ChargeEvents): The event that will trigger the charge for the return label.
            label_layout (LabelLayouts, optional): The layout of the label. Defaults to "4x6".
            label_format (LabelFormats, optional): The format of the label. Defaults to "pdf".
            label_download_type (Literal["url", "inline"], optional): The format in which the label will be downloaded. Defaults to "url".
            display_scheme (DisplayFormatSchemes, optional): The display scheme for the label. Defaults to "label".
            label_image_id (str | None, optional): The image ID for the label. Defaults to None.

        Returns:
            tuple[int, ErrorResponse | Label]: A tuple containing the HTTP status code and either an ErrorResponse or the created return Label.
        """

        payload = {
            "charge_event": charge_event,
            "label_layout": label_layout,
            "label_format": label_format,
            "label_download_type": label_download_type,
            "display_scheme": display_scheme,
            "label_image_id": label_image_id,
        }

        endpoint = f"{cls._v2_endpoint}/{Endpoints.LABELS.value}/{label_id}/return"

        try:
            res = await cls.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                Label,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_tracking_information(
        cls: type[ShipStationClient],
        label_id: str,
    ) -> tuple[int, ErrorResponse | TrackingInformation]:
        endpoint = f"{cls._v2_endpoint}/{Endpoints.LABELS.value}/{label_id}/track"

        try:
            res = await cls.request("GET", endpoint)

            return cls.validate_response(
                res,
                (200,),
                TrackingInformation,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def void_label(
        cls: type[ShipStationClient],
        label_id: str,
    ) -> tuple[int, ErrorResponse | LabelVoidResponse]:
        endpoint = f"{cls._v2_endpoint}/{Endpoints.LABELS.value}/{label_id}/void"

        try:
            res = await cls.request("PUT", endpoint)

            return cls.validate_response(
                res,
                (200,),
                LabelVoidResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)
