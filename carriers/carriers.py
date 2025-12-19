from typing import Literal, cast

from requests import delete, get, post, put

from ..common._types import (  # type: ignore[import-not-found]
    Endpoints,
    Error,
    ShipPortal,
)
from ..common.base import API_ENDPOINT, req  # type: ignore[import-not-found]
from ._types import Carrier, CarrierListResponse


class Carriers(ShipPortal): ...
