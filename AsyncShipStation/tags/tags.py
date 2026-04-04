from typing import Literal, cast

from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import (
    TagCreateResponse,
    TagInfo,
    TagListResponse,
)


class TagsPortal(ShipStationClient):
    """Portal for interacting with the ShipStation Tags API (V2)."""

    @classmethod
    async def all(
        cls: type["TagsPortal"],
        connection: ShipStationConnection,
    ) -> tuple[int, TagListResponse | ErrorResponse]:
        """
        List all tags in the account.
        https://docs.shipstation.com/openapi/tags/list_tags

        Returns:
            Tuple of status code and TagListResponse or ErrorResponse
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.TAGS.value}"

        try:
            res = await connection.request("GET", endpoint)

            return cls.validate_response(
                res,
                (200,),
                TagListResponse,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create(
        cls: type["TagsPortal"],
        connection: ShipStationConnection,
        tag_name: str,
        color: (
            Literal[
                "red",
                "orange",
                "yellow",
                "green",
                "blue",
                "purple",
                "pink",
                "gray",
            ]
            | None
        ) = None,
    ) -> tuple[int, TagCreateResponse | ErrorResponse]:
        """
        Create a new tag.
        https://docs.shipstation.com/openapi/tags/create_tag

        Args:
            tag_name: The name of the tag to create
            color: Optional color for the tag

        Returns:
            Tuple of status code and TagCreateResponse or ErrorResponse
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.TAGS.value}/{tag_name}"

        try:
            res = await connection.request(
                "POST",
                endpoint,
                params={"color": color} if color is not None else None,  # type: ignore[arg-type]
            )

            return cls.validate_response(
                res,
                (200, 201),
                TagCreateResponse,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def delete(
        cls: type["TagsPortal"],
        connection: ShipStationConnection,
        tag_name: str,
    ) -> tuple[int, None | ErrorResponse]:
        """
        Delete a tag by name.
        https://docs.shipstation.com/openapi/tags/delete_tag

        Args:
            tag_name: The name of the tag to delete

        Returns:
            Tuple of status code and None (on success) or ErrorResponse
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.TAGS.value}/{tag_name}"

        try:
            res = await connection.request("DELETE", endpoint)

            if res.status_code == 204:
                return (res.status_code, None)

            return cls.validate_response(
                res,
                (204,),
                type(None),
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_name(
        cls: type["TagsPortal"],
        connection: ShipStationConnection,
        tag_name: str,
    ) -> tuple[int, TagInfo | None | ErrorResponse]:
        """
        Get a tag by name by listing all tags and filtering.

        Note: The V2 API doesn't have a direct get-by-name endpoint,
        so this lists all tags and filters locally.

        Args:
            tag_name: The name of the tag to find

        Returns:
            Tuple of status code and TagInfo (if found), None (if not found), or ErrorResponse
        """
        status_code, response = await cls.all(connection)

        if status_code != 200:
            return (status_code, response)  # type: ignore[return-value]

        # Cast response to TagListResponse since we know it's successful
        tag_list: TagListResponse = response  # type: ignore[assignment]

        for tag in tag_list.get("tags", []):
            if tag.get("name") == tag_name:
                return (status_code, tag)

        return (
            404,
            cast(
                ErrorResponse,
                {
                    "error": "Tag not found",
                    "message": f"Tag '{tag_name}' not found",
                    "code": 404,
                    "type": "not_found",
                },
            ),
        )


__all__ = ["TagsPortal"]
