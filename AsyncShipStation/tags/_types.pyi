from typing import TypedDict

class TagInfo(TypedDict):
    'A tag in ShipStation V2 API.'
    tag_id: int
    name: str
    color: str

class TagListResponse(TypedDict):
    'Response from listing tags.'
    tags: list[TagInfo]

class TagCreateResponse(TypedDict):
    'Response from creating a tag.'
    tag_id: int
    name: str
    color: str

class TagDeleteResponse(TypedDict):
    'Response from deleting a tag.'
    ...
