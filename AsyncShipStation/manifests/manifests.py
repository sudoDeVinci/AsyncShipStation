from ..common import Endpoints, ErrorResponse, ShipStationClient
from ._types import Manifest, ManifestListResponse


class ManifestsPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
        label_ids: list[str] | None = None,
        warehouse_id: str | None = None,
        ship_date_start: str | None = None,
        ship_date_end: str | None = None,
        created_at_start: str | None = None,
        created_at_end: str | None = None,
        carrier_id: str | None = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[int, ErrorResponse | ManifestListResponse]:
        """Get a list of manifests.

        Args:
            label_ids (list[str] | None, optional): Filter by label IDs. Defaults to None.
            warehouse_id (str | None, optional): Filter by warehouse ID. Defaults to None.
            ship_date_start (str | None, optional): Filter by ship date start. Defaults to None.
            ship_date_end (str | None, optional): Filter by ship date end. Defaults to None.
            created_at_start (str | None, optional): Filter by created at start. Defaults to None.
            created_at_end (str | None, optional): Filter by created at end. Defaults to None.
            carrier_id (str | None, optional): Filter by carrier ID. Defaults to None.
            page (int, optional): Page number. Defaults to 1.
            page_size (int, optional): Page size. Defaults to 25.

        Returns:
            tuple[int, ErrorResponse | ManifestListResponse]: Status code and either an ErrorResponse or ManifestListResponse.
        """
        params = {
            "label_ids": label_ids,
            "warehouse_id": warehouse_id,
            "ship_date_start": ship_date_start,
            "ship_date_end": ship_date_end,
            "created_at_start": created_at_start,
            "created_at_end": created_at_end,
            "carrier_id": carrier_id,
            "page": page,
            "page_size": page_size,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f"{cls._v2_endpoint}/{Endpoints.MANIFESTS.value}"

        try:
            res = await cls.request("GET", endpoint, params=params)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                ManifestListResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create(
        cls: type[ShipStationClient],
    ) -> tuple[int, ErrorResponse, ManifestListResponse]:
        """Create a new manifest.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError("This method is not yet implemented.")

    @classmethod
    async def get_by_id(
        cls: type[ShipStationClient], manifest_id: str
    ) -> tuple[int, ErrorResponse, Manifest]:
        """Get a manifest by its ID.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError("This method is not yet implemented.")
