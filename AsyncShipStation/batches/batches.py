from typing import List, Literal, cast

from ..common import (
    DisplayFormatScheme,
    Endpoints,
    Error,
    LabelFormats,
    LabelLayouts,
    ShipStationClient,
)
from ._types import (
    Batch,
    BatchListResponse,
    BatchProcessErrorResponse,
    BatchStatuses,
    ProcessLabel,
)


class BatchPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
        status: BatchStatuses | None = None,
        batch_number: str | None = None,
        sort_by: Literal["ship_date", "processed_at", "created_at"] | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_dir: Literal["asc", "desc"] = "desc",
    ) -> tuple[int, BatchListResponse | Error]:
        """
        List the batches associated with your ShipStation account.
        https://docs.shipstation.com/openapi/batches/list_batches#batches/list_batches/request

        Args:
            status (BatchStatuses): Filter batches by their status.
            batch_number (str): Filter batches by their batch number.
            sort_by (Literal["ship_date", "processed_at", "created_at"]): The field to sort the results by.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of results per page. Defaults to 25.
            sort_dir (Literal["asc", "desc"], optional): The direction to sort the results. Defaults to "desc".

        Returns:
            tuple[int, BatchListResponse | Error]: A tuple containing the status code and either a BatchListResponse or an Error.
        """
        params = {
            "status": status,
            "batch_number": batch_number,
            "sort_by": sort_by,
            "page": page,
            "page_size": page_size,
            "sort_dir": sort_dir,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
                params=params,  # type: ignore[arg-type]
            )
            json = res.json()
            if res.status_code != 200:
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))

                raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(BatchListResponse, json))

    @classmethod
    async def create(
        cls: type[ShipStationClient],
        external_batch_id: str | None,
        shipment_ids: List[str] | None,
        rate_ids: List[str] | None,
        batch_notes: str | None = None,
        process_labels: ProcessLabel | None = None,
    ) -> tuple[int, Batch | Error]:
        """
        Create a new batch in your ShipStation account.
        https://docs.shipstation.com/openapi/batches/create_batch#batches/create_batch/request

        Args:
            external_batch_id (str): An external identifier for the batch.
            shipment_ids (list[str]): A list of shipment IDs to include in the batch.
            rate_ids (list[str] | None): A list of rate IDs to use for the shipments in the batch.
            batch_notes (str, optional): Notes for the batch. Defaults to "".

        Returns:
            tuple[int, Batch | Error]: A tuple containing the status code and either a Batch or an Error.
        """
        payload = {
            "external_batch_id": external_batch_id,
            "shipment_ids": shipment_ids,
            "rate_ids": rate_ids,
            "batch_notes": batch_notes,
            "process_labels": process_labels,
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}"

        try:
            res = await cls.request(
                "POST",
                endpoint,
                json=payload,  # type: ignore[arg-type]
            )
            json = res.json()
            if res.status_code not in (200, 207):
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))

                raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(Batch, json))

    @classmethod
    async def get_by_external_id(
        cls: type[ShipStationClient], external_batch_id: str
    ) -> tuple[int, Batch | Error]:
        """
        Retrieve a batch by its external ID.
        https://docs.shipstation.com/openapi/batches/get_batch_by_external_id#batches/get_batch_by_external_id/request

        Args:
            external_batch_id (str): The external ID of the batch to retrieve.

        Returns:
            tuple[int, Batch | Error]: A tuple containing the status code and either a Batch or an Error.
        """
        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}/external_batch_id/{external_batch_id}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )
            json = res.json()
            if res.status_code != 200:
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))

                raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(Batch, json))

    @classmethod
    async def get_by_id(
        cls: type[ShipStationClient],
        batch_id: str,
    ) -> tuple[int, Batch | Error]:
        """
        Retrieve a batch by its ID.
        https://docs.shipstation.com/openapi/batches/get_batch#batches/get_batch/request

        Args:
            batch_id (str): The ID of the batch to retrieve.

        Returns:
            tuple[int, Batch | Error]: A tuple containing the status code and either a Batch or an Error.
        """
        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}/{batch_id}"

        try:
            res = await cls.request(
                "GET",
                endpoint,
            )
            json = res.json()
            if res.status_code != 200:
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))
                raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(Batch, json))

    @classmethod
    async def delete_by_id(
        cls: type[ShipStationClient],
        batch_id: str,
    ) -> tuple[int, None | Error]:
        """
        Delete a batch by its ID.
        https://docs.shipstation.com/openapi/batches/delete_batch#batches/delete_batch/request

        Args:
            batch_id (str): The ID of the batch to delete.

        Returns:
            tuple[int, None | Error]: A tuple containing the status code and either None or an Error.
        """
        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}/{batch_id}"

        try:
            res = await cls.request(
                "DELETE",
                endpoint,
            )
            if res.status_code != 204:
                json = res.json()
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))
                raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, None)

    @classmethod
    async def archive_by_id(
        cls: type[ShipStationClient],
        batch_id: str,
    ) -> tuple[int, None | Error]:
        """
        Archive a batch by its ID.
        https://docs.shipstation.com/openapi/batches/archive_batch#batches/archive_batch/request

        Args:
            batch_id (str): The ID of the batch to archive.

        Returns:
            tuple[int, None | Error]: A tuple containing the status code and either None or an Error.
        """
        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}/{batch_id}"

        try:
            res = await cls.request(
                "PUT",
                endpoint,
            )
            if res.status_code != 204:
                json = res.json()
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))
                raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, None)

    @classmethod
    async def add_to_batch(
        cls: type[ShipStationClient],
        batch_id: str,
        external_batch_id: str,
        batch_notes: str | None = None,
        shipment_ids: List[str] | None = None,
        rate_ids: List[str] | None = None,
        process_labels: ProcessLabel | None = None,
    ) -> tuple[int, None | Error]:
        """
        Add shipments to an existing batch.
        https://docs.shipstation.com/openapi/batches/add_to_batch#batches/add_to_batch/request

        Args:
            batch_id (str): The ID of the batch to which shipments will be added.
            external_batch_id (str): An external identifier for the batch.
            batch_notes (str): Notes for the batch.
            shipment_ids (list[str]): A list of shipment IDs to add to the batch.
            rate_ids (list[str]): A list of rate IDs to use for the shipments in the batch.
            process_labels (ProcessLabels): Instructions for processing labels for the shipments.

        Returns:
            tuple[int, None | Error]: A tuple containing the status code and either None or an Error.
        """
        payload = {
            "external_batch_id": external_batch_id,
            "batch_notes": batch_notes,
            "shipment_ids": shipment_ids,
            "rate_ids": rate_ids,
            "process_labels": process_labels,
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}/{batch_id}/add"

        try:
            res = await cls.request(
                "POST",
                endpoint,
                json=payload,  # type: ignore[arg-type]
            )
            if res.status_code != 204:
                json = res.json()
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))
                raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, None)

    @classmethod
    async def get_batch_errors(
        cls: type[ShipStationClient],
        batch_id: str,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[int, BatchProcessErrorResponse | Error]:
        params = {
            "page": page,
            "page_size": page_size,
        }

        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}/{batch_id}/errors"

        try:
            res = await cls.request(
                "GET",
                endpoint,
                params=params,  # type: ignore[arg-type]
            )
            json = res.json()
            if res.status_code != 200:
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))
                else:
                    raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, cast(BatchProcessErrorResponse, json))

    @classmethod
    async def process_batch_id_labels(
        cls: type[ShipStationClient],
        batch_id: str,
        label_layout: LabelLayouts = "4x6",
        label_format: LabelFormats = "pdf",
        display_scheme: DisplayFormatScheme = "label",
        ship_date: str | None = None,
    ) -> tuple[int, None | Error]:
        """
        Process labels for a batch by its ID.
        https://docs.shipstation.com/openapi/batches/process_batch_labels#batches/process_batch_labels/request

        Args:
            batch_id (str): The ID of the batch to process labels for.
            ship_date (str): The ship date for the labels.
            label_layout (BatchLabelLayouts, optional): The layout of the labels. Defaults to "4x6".
            label_format (BatchLabelFormats, optional): The format of the labels. Defaults to "pdf".
            display_scheme (DisplayFormatScheme, optional): The display scheme for the labels. Defaults to "label".
        """
        payload: dict[str, object] = {
            "label_layout": label_layout,
            "label_format": label_format,
            "display_scheme": display_scheme,
        }

        if ship_date is not None:
            payload["ship_date"] = ship_date

        endpoint = (
            f"{cls._endpoint}/{Endpoints.BATCHES.value}/{batch_id}/process/labels"
        )

        try:
            res = await cls.request(
                "POST",
                endpoint,
                json=payload,
            )
            if res.status_code != 204:
                json = res.json()
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))
                else:
                    raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, None)

    @classmethod
    async def remove_from_batch(
        cls: type[ShipStationClient],
        batch_id: str,
        shipment_ids: List[str] | None = None,
        rate_ids: List[str] | None = None,
    ) -> tuple[int, None | Error]:
        params: dict[str, object] = {}
        if shipment_ids is not None:
            params["shipment_ids"] = shipment_ids
        if rate_ids is not None:
            params["rate_ids"] = rate_ids

        if not params:
            return (
                400,
                cast(
                    Error,
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": "invalid_request",
                        "message": "At least one of shipment_ids or rate_ids must be provided.",
                    },
                ),
            )

        endpoint = f"{cls._endpoint}/{Endpoints.BATCHES.value}/{batch_id}/remove"

        try:
            res = await cls.request(
                "POST",
                endpoint,
                json=params,
            )
            if res.status_code != 204:
                json = res.json()
                if "error_code" in json:
                    return (res.status_code, cast(Error, json))
                else:
                    raise Exception(f"Unexpected response: {json}")
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

        return (res.status_code, None)
