from typing import TypedDict
from ..common._types import Taggable


class TagInfo(Taggable):
    """A tag in ShipStation V2 API."""

    tag_id: int
    name: str
    color: str


class TagListResponse(Taggable):
    """Response from listing tags."""

    tags: list[TagInfo]


class TagCreateResponse(Taggable):
    """Response from creating a tag."""

    tag_id: int
    name: str
    color: str


class TagDeleteResponse(Taggable):
    """Response from deleting a tag."""

    pass  # Empty response on successful deletion
