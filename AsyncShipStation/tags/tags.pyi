from typing import Literal

from ..common import ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import TagCreateResponse, TagInfo, TagListResponse

class TagsPortal(ShipStationClient):
    "Portal for interacting with the ShipStation Tags API (V2)."

    @classmethod
    async def all(
        cls: type["TagsPortal"],
        connection: ShipStationConnection,
        identity: bool = False,
    ) -> tuple[int, TagListResponse | ErrorResponse]: ...
    @classmethod
    async def create(
        cls: type["TagsPortal"],
        connection: ShipStationConnection,
        tag_name: str,
        color: (
            Literal[
                "red", "orange", "yellow", "green", "blue", "purple", "pink", "gray"
            ]
            | None
        ) = None,
        identity: bool = False,
    ) -> tuple[int, TagCreateResponse | ErrorResponse]: ...
    @classmethod
    async def delete(
        cls: type["TagsPortal"],
        connection: ShipStationConnection,
        tag_name: str,
        identity: bool = False,
    ) -> tuple[int, None | ErrorResponse]: ...
    @classmethod
    async def get_by_name(
        cls: type["TagsPortal"],
        connection: ShipStationConnection,
        tag_name: str,
        identity: bool = False,
    ) -> tuple[int, TagInfo | None | ErrorResponse]: ...

__all__ = ["TagsPortal"]
