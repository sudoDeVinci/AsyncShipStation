from asyncio import Lock
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Any, ClassVar, Final, Literal, TypeVar

from httpx import Response
from pydantic import EmailStr, HttpUrl

from ._types import ErrorResponse

LOGGER: Logger
VERSION: Final[str]
T = TypeVar("T")

class APIError(Exception):
    __slots__ = ("status_code", "details")
    status_code: int
    details: str | dict[str, object]

    def __init__(self, status: int, detail: str | dict[str, object]) -> None: ...
    def json(self) -> ErrorResponse: ...
    def __str__(self) -> str: ...
    @property
    def text(self) -> str: ...
    @property
    def content(self) -> bytes: ...

class RateLimitError(APIError):
    __slots__ = ("status_code", "details", "retry_after")
    retry_after: float | None

    def __init__(
        self,
        status: int,
        detail: str | dict[str, object],
        retry_after: float | None,
    ) -> None: ...

@dataclass(slots=True, frozen=True)
class ConnectionConfig:
    version: Literal["v1", "v2"] = "v2"
    timeout: int = 60
    max_connections: int = 20
    max_keepalive_connections: int = 10
    http2: bool = False
    retries: int = 4
    user_agent: str = "asyncShipStation/2.0.0"
    v2_endpoint: str = "https://api.shipstation.com/v2"
    v2_mock_endpoint: str = "https://docs.shipstation.com/_mock/openapi/v2"
    v1_endpoint: str = "https://ssapi.shipstation.com"
