from typing import Literal, cast

from ..common._types import (  # type: ignore[import-not-found]
    Endpoints,
    Error,
    ShipPortal,
)
from ..common.base import API_ENDPOINT, req  # type: ignore[import-not-found]
from ._types import Carrier, CarrierListResponse


class Carriers(ShipPortal): ...
