from asyncio import Lock
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Any, ClassVar, Literal, TypeVar
from httpx import Response
from pydantic import EmailStr, HttpUrl
from ._types import ErrorResponse
LOGGER: Logger
T = TypeVar('T')

class APIError(Exception):
    __slots__ = ('status_code', 'details')
    status_code: int
    details: str | dict[str, object]

    def __init__(self, status: int, detail: str | dict[str, object]) -> None: ...

    def json(self) -> ErrorResponse: ...

    def __str__(self) -> str: ...

    @property
    def text(self) -> str: ...

    @property
    def content(self) -> bytes: ...

@dataclass(slots=True, frozen=True)
class ConnectionConfig:
    version: Literal['v1', 'v2'] = 'v2'
    timeout: int = 500
    max_connections: int = 20
    max_keepalive_connections: int = 10
    http2: bool = False
    retries: int = 4
    user_agent: str = 'asyncShipStation/2.0.0'
    v2_endpoint: str = 'https://api.shipstation.com/v2'
    v2_mock_endpoint: str = 'https://docs.shipstation.com/_mock/openapi/v2'
    v1_endpoint: str = 'https://ssapi.shipstation.com'

class ShipStationConnection:
    __slots__ = ('_v2_key', '_v1_key', '_v1_secret', '_v2_headers', '_v1_headers', '_v1_lock', '_v2_lock', '_v1_client', '_v2_client', '_v1_ref_count', '_v2_ref_count', '_v1_enabled', '_v2_enabled', '_pool_key', '_config')

    def __init__(self, v2_key: str | None = None, v1_key: str | None = None, v1_secret: str | None = None, config: ConnectionConfig | None = None) -> None: ...

    async def start_v1(self) -> None: ...

    async def start_v2(self) -> None: ...

    async def start(self, version: Literal['v1', 'v2', 'both'] = 'both') -> None: ...

    async def close(self, version: Literal['v1', 'v2', 'both'] = 'both', force: bool = False) -> None: ...

    async def v2_request(self, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'], url: str, **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None]) -> Response | APIError: ...

    async def v1_request(self, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'], url: str, **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None]) -> Response | APIError: ...

    async def request(self, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'], url: str, version: Literal['v1', 'v2'] = 'v2', **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None]) -> Response | APIError: ...

    @property
    def v2_key(self) -> str | None: ...

    @property
    def v1_key(self) -> str | None: ...

    @property
    def v1_secret(self) -> str | None: ...

    @property
    def v2_endpoint(self) -> str: ...

    @property
    def v1_endpoint(self) -> str: ...

    @property
    def v2_ref_count(self) -> int: ...

    @property
    def v1_ref_count(self) -> int: ...

    @property
    def ref_count(self) -> int: ...

    @property
    def pool_key(self) -> int: ...

    async def increment_v2_ref(self) -> None: ...

    async def decrement_v2_ref(self) -> None: ...

    async def increment_v1_ref(self) -> None: ...

    async def decrement_v1_ref(self) -> None: ...

    def __eq__(self, other: object) -> bool: ...

    @staticmethod
    def hash(v2_key: str | None, v1_key: str | None, v1_secret: str | None) -> int: ...

    def __hash__(self) -> int: ...

class ShipStationClient:
    __slots__ = ()
    _v2_endpoint: ClassVar[str]
    _v2_mock_endpoint: ClassVar[str]
    _v1_endpoint: ClassVar[str]
    _pool: ClassVar[dict[int, ShipStationConnection]]
    _pool_lock: ClassVar[Lock]

    @classmethod
    def validate_response(cls, res: Response | APIError, accepted_statuses: tuple[int, ...], return_type: type[T]) -> tuple[int, ErrorResponse | T]: ...

    @staticmethod
    def parse_unknown_exception(exception: Exception) -> tuple[Literal[500], ErrorResponse]: ...

    @classmethod
    async def evict_connection(cls, connection_hash: int) -> None: ...

    @classmethod
    async def _add_connection(cls, connection: ShipStationConnection) -> None: ...

    @classmethod
    async def get_connection(cls, v2_key: str | None = None, v1_key: str | None = None, v1_secret: str | None = None, connection_hash: int | None = None) -> ShipStationConnection | None: ...

    @classmethod
    async def configure(cls, v2_key: str, v1_key: str | None = None, v1_secret: str | None = None) -> ShipStationConnection: ...

    @classmethod
    async def start(cls, v1_key: str | None = None, v1_secret: str | None = None, v2_key: str | None = None, connection: ShipStationConnection | None = None, connection_hash: int | None = None, version: Literal['v1', 'v2', 'both'] = 'both') -> ShipStationConnection: ...

    @classmethod
    async def close(cls, v1_key: str | None = None, v1_secret: str | None = None, v2_key: str | None = None, connection: ShipStationConnection | None = None, connection_hash: int | None = None, version: Literal['v1', 'v2', 'both'] = 'v2', force: bool = False) -> None: ...

    @classmethod
    def scoped_client(cls, v1_key: str | None = None, v1_secret: str | None = None, v2_key: str | None = None, connection: ShipStationConnection | None = None, connection_hash: int | None = None, version: Literal['v1', 'v2', 'both'] = 'v2', mock: bool = False) -> AbstractAsyncContextManager[ShipStationConnection | None]: ...

    @classmethod
    async def request(cls, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'], url: str, version: Literal['v1', 'v2'] = 'v2', connection: ShipStationConnection | None = None, connection_hash: int | None = None, **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None]) -> Response | APIError: ...

def write_json(fp: Path, data: dict[str, Any] | None) -> bool: ...

def read_json(fp: Path) -> dict[str, Any] | None: ...
