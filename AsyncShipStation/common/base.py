from asyncio import Lock
from base64 import b64encode
from contextlib import asynccontextmanager
from dataclasses import dataclass
from hashlib import sha256
from json import JSONDecodeError, dump, dumps, load
from logging import Logger, getLogger
from pathlib import Path
from typing import Any, AsyncGenerator, ClassVar, Final, Generic, Literal, TypeVar, cast
from uuid import uuid4

from httpx import AsyncClient, Limits, Response
from httpx._types import HeaderTypes
from pydantic import EmailStr, HttpUrl, SecretStr

from ._types import ErrorResponse, Taggable

LOGGER: Logger = getLogger("AsyncShipStation")
VERSION: Final[str] = "0.2.0.9"
T = TypeVar("T")


class APIError(Exception):
    """
    Returned for local ShipStation responses such as during configuration.
    """

    __slots__ = ("status_code", "details")

    def __init__(self, status: int, detail: str | dict[str, object]):
        self.status_code = status
        self.details = detail

    def json(self) -> ErrorResponse:
        return cast(
            ErrorResponse,
            {
                "request_id": None,
                "errors": [
                    {
                        "error_source": "ShipStation",
                        "error_type": "integrations",
                        "error_code": self.status_code,
                        "message": self.details,
                    }
                ],
            },
        )

    def __str__(self) -> str:
        outdict = {
            "status_code": self.status_code,
            "details": self.json(),
        }
        return dumps(outdict, indent=4, ensure_ascii=False)

    @property
    def text(self) -> str:
        return self.__str__()

    @property
    def content(self) -> bytes:
        return self.__str__().encode("utf-8")


@dataclass(slots=True, frozen=True)
class ConnectionConfig:
    version: Literal["v1", "v2", "both"] = "v2"
    timeout: int = 500
    max_connections: int = 20
    max_keepalive_connections: int = 10
    http2: bool = False
    retries: int = 4
    user_agent: str = f"asyncShipStation/{VERSION}"
    v2_endpoint: str = "https://api.shipstation.com/v2"
    v2_mock_endpoint: str = "https://docs.shipstation.com/_mock/openapi/v2"
    v1_endpoint: str = "https://ssapi.shipstation.com"

    def __hash__(self: "ConnectionConfig") -> int:
        raw = f"{self.version}:{self.timeout}:{self.max_connections}:{self.max_keepalive_connections}:{self.user_agent}:{self.v2_endpoint}:{self.v1_endpoint}:{self.v2_mock_endpoint}:{self.retries}:{self.http2}"
        digest = int.from_bytes(
            sha256(raw.encode("utf-8")).digest()[:8], "big", signed=True
        )
        return -2 if digest == -1 else digest

    def __eq__(self: "ConnectionConfig", other: object) -> bool:
        if not isinstance(other, ConnectionConfig):
            return NotImplemented
        return (
            self.version == other.version
            and self.timeout == other.timeout
            and self.max_connections == other.max_connections
            and self.max_keepalive_connections == other.max_keepalive_connections
            and self.user_agent == other.user_agent
            and self.v2_endpoint == other.v2_endpoint
            and self.v1_endpoint == other.v1_endpoint
            and self.v2_mock_endpoint == other.v2_mock_endpoint
            and self.retries == other.retries
            and self.http2 == other.http2
        )


class ShipStationConnection:
    __slots__ = (
        "_v2_key",
        "_v1_key",
        "_v1_secret",
        "_v2_headers",
        "_v1_headers",
        "_v1_lock",
        "_v2_lock",
        "_v1_client",
        "_v2_client",
        "_v1_ref_count",
        "_v2_ref_count",
        "_v1_enabled",
        "_v2_enabled",
        "_pool_key",
        "_config",
        "_uid",
    )

    def __init__(
        self,
        v2_key: str | None = None,
        v1_key: str | None = None,
        v1_secret: str | None = None,
        config: ConnectionConfig | None = None,
    ) -> None:
        self._v2_key: SecretStr | None = SecretStr(v2_key) if v2_key else None
        self._v1_key: SecretStr | None = SecretStr(v1_key) if v1_key else None
        self._v1_secret: SecretStr | None = SecretStr(v1_secret) if v1_secret else None
        self._v1_enabled: bool = False
        self._v2_enabled: bool = False
        self._config: ConnectionConfig = config or ConnectionConfig()
        self._pool_key: int = self.hash(v2_key, v1_key, v1_secret, self._config)
        if self._v2_key:
            self._v2_headers: dict[str, str] = {
                "User-Agent": self._config.user_agent,
                "api-key": self._v2_key.get_secret_value(),
            }
            self._v2_enabled = True

        if v1_key and v1_secret:
            credentials = f"{v1_key}:{v1_secret}"
            encoded_credentials = b64encode(credentials.encode("utf-8")).decode("utf-8")
            self._v1_headers: dict[str, str] = {
                "User-Agent": self._config.user_agent,
                "Authorization": f"Basic {encoded_credentials}",
            }
            self._v1_enabled = True

        self._v1_lock: Lock = Lock()
        self._v2_lock: Lock = Lock()
        self._v1_client: AsyncClient | None = None
        self._v2_client: AsyncClient | None = None
        self._v1_ref_count: int = 0
        self._v2_ref_count: int = 0
        self._uid = uuid4().int

    async def start_v1(self: "ShipStationConnection") -> None:
        if not self._v1_enabled:
            raise APIError(400, "API v1 is not enabled for this connection.")
        async with self._v1_lock:
            if self._v1_client is None:
                self._v1_client = AsyncClient(
                    base_url=self._config.v1_endpoint,
                    headers=cast(HeaderTypes, self._v1_headers),
                    timeout=self._config.timeout,
                    http2=self._config.http2,  # Disable HTTP/2
                    limits=Limits(
                        max_connections=self._config.max_connections,
                        max_keepalive_connections=self._config.max_keepalive_connections,
                    ),
                )

            self._v1_ref_count += 1

    async def start_v2(self: "ShipStationConnection") -> None:
        if not self._v2_enabled:
            raise APIError(400, "API v2 is not enabled for this connection.")
        async with self._v2_lock:
            if self._v2_client is None:
                self._v2_client = AsyncClient(
                    base_url=self._config.v2_endpoint,
                    headers=cast(HeaderTypes, self._v2_headers),
                    timeout=self._config.timeout,
                    http2=self._config.http2,  # Disable HTTP/2
                    limits=Limits(
                        max_connections=self._config.max_connections,
                        max_keepalive_connections=self._config.max_keepalive_connections,
                    ),
                )
            self._v2_ref_count += 1

    async def start(
        self: "ShipStationConnection", version: Literal["v1", "v2", "both"] = "both"
    ) -> None:
        if version in ("v1", "both"):
            await self.start_v1()
        if version in ("v2", "both"):
            await self.start_v2()

    async def close(
        self: "ShipStationConnection",
        version: Literal["v1", "v2", "both"] = "both",
        force: bool = False,
    ) -> None:
        if version in ("v1", "both") and self._v1_enabled:
            async with self._v1_lock:
                self._v1_ref_count = max(0, self._v1_ref_count - 1)
                if self._v1_ref_count <= 0 or force:
                    self._v1_ref_count = 0
                    if self._v1_client is not None:
                        await self._v1_client.aclose()
                    self._v1_client = None

        if version in ("v2", "both") and self._v2_enabled:
            async with self._v2_lock:
                self._v2_ref_count = max(0, self._v2_ref_count - 1)
                if self._v2_ref_count <= 0 or force:
                    self._v2_ref_count = 0
                    if self._v2_client is not None:
                        await self._v2_client.aclose()
                    self._v2_client = None

    async def v2_request(
        self: "ShipStationConnection",
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: str,
        **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None],
    ) -> Response | APIError:
        if not self._v2_enabled:
            return APIError(400, "API v2 is not enabled for this connection.")
        self_start = False
        if self._v2_client is None:
            await self.start_v2()
            self_start = True
        if self._v2_client is None:
            return APIError(500, "HTTP client could not be initialized.")

        response = await self._v2_client.request(method, url, **kwargs)  # type: ignore[arg-type]

        if self_start:
            await self.close("v2")
        return response

    async def v1_request(
        self: "ShipStationConnection",
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: str,
        **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None],
    ) -> Response | APIError:
        self_start = False
        if self._v1_client is None:
            await self.start_v1()
            self_start = True
        if self._v1_client is None:
            return APIError(500, "HTTP client could not be initialized.")

        response = await self._v1_client.request(method, url, **kwargs)  # type: ignore[arg-type]

        if self_start:
            await self.close("v1")
        return response

    async def request(
        self: "ShipStationConnection",
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: str,
        version: Literal["v1", "v2"] = "v2",
        **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None],
    ) -> Response | APIError:
        if version == "v2":
            return await self.v2_request(method, url, **kwargs)
        elif version == "v1":
            return await self.v1_request(method, url, **kwargs)
        else:
            return APIError(400, f"Unsupported API version: {version}")

    @property
    def v2_key(self) -> SecretStr | None:
        return self._v2_key

    @property
    def v1_key(self) -> SecretStr | None:
        return self._v1_key

    @property
    def v1_secret(self) -> SecretStr | None:
        return self._v1_secret

    @property
    def v2_endpoint(self) -> str:
        return self._config.v2_endpoint

    @property
    def v1_endpoint(self) -> str:
        return self._config.v1_endpoint

    @property
    def v2_ref_count(self) -> int:
        return self._v2_ref_count

    @property
    def v1_ref_count(self) -> int:
        return self._v1_ref_count

    @property
    def ref_count(self) -> int:
        return self._v1_ref_count + self._v2_ref_count

    @property
    def uid(self) -> int:
        return self._uid

    @property
    def pool_key(self) -> int:
        return self._pool_key

    async def increment_v2_ref(self) -> None:
        async with self._v2_lock:
            self._v2_ref_count = max(0, self._v2_ref_count + 1)

    async def decrement_v2_ref(self) -> None:
        async with self._v2_lock:
            self._v2_ref_count = max(0, self._v2_ref_count - 1)
            if self._v2_ref_count == 0 and self._v2_client is not None:
                await self._v2_client.aclose()
                self._v2_client = None

    async def increment_v1_ref(self) -> None:
        async with self._v1_lock:
            self._v1_ref_count = max(0, self._v1_ref_count + 1)

    async def decrement_v1_ref(self) -> None:
        async with self._v1_lock:
            self._v1_ref_count = max(0, self._v1_ref_count - 1)
            if self._v1_ref_count == 0 and self._v1_client is not None:
                await self._v1_client.aclose()
                self._v1_client = None

    def __eq__(self: "ShipStationConnection", other: object) -> bool:
        if not isinstance(other, ShipStationConnection):
            return NotImplemented
        return (
            self._v2_key == other._v2_key
            and self._v1_key == other._v1_key
            and self._v1_secret == other._v1_secret
            and self._config == other._config
        )

    @staticmethod
    def hash(
        v2_key: str | None,
        v1_key: str | None,
        v1_secret: str | None,
        config: ConnectionConfig,
    ) -> int:
        raw = f"{v2_key or ''}:{v1_key or ''}:{v1_secret or ''}:{hash(config)}"
        digest = int.from_bytes(
            sha256(raw.encode("utf-8")).digest()[:8], "big", signed=True
        )
        return -2 if digest == -1 else digest

    def __hash__(self: "ShipStationConnection") -> int:
        return self._pool_key


class ShipStationClient:
    __slots__ = ()

    _physical_pool: ClassVar[dict[int, ShipStationConnection]] = {}
    """
    The pool of all connection objects, where the key is the hashed config value.
    """
    _virtual_pool: ClassVar[dict[int, int]] = {}
    """
    A dict of "virtual" addresses which map to the "physical" hashes of each value.
    This gives a layer of abstraction between the uuid provided to the user, and the
    actual physical hash of an object.
    """

    _pool_lock: ClassVar[Lock] = Lock()

    @staticmethod
    def _apply_identity_tag(
        payload: object,
        return_type: type[object],
    ) -> object:
        if isinstance(payload, dict):
            tagged = dict(payload)
            tagged["__kind__"] = return_type.__name__
            return tagged

        return payload

    @classmethod
    def validate_response(
        cls: type["ShipStationClient"],
        res: Response | APIError,
        accepted_statuses: tuple[int, ...],
        return_type: type[T],
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | T]:
        try:
            payload = cast(object, res.json())
        except JSONDecodeError as e:
            return cls.parse_unknown_exception(
                Exception(f"JSON decode error: {e}. Raw response: {res.text[:500]}")
            )

        if res.status_code not in accepted_statuses:
            if isinstance(payload, dict) and "errors" in payload:
                return res.status_code, cast(ErrorResponse, payload)
            raise APIError(res.status_code, cast(str | dict[str, object], payload))

        if identity:
            payload = cls._apply_identity_tag(payload, return_type)

        return res.status_code, cast(T, payload)

    @staticmethod
    def parse_unknown_exception(
        exception: Exception,
    ) -> tuple[Literal[500], ErrorResponse]:
        """
        Parses an unknown exception and returns a standardized error response.
        Args:
            exception (Exception): The exception to parse.
        Returns:
            tuple[Literal[500], ErrorResponse]: A tuple containing the status code and the error details.
        """
        return (
            500,
            cast(
                ErrorResponse,
                {
                    "request_id": None,
                    "errors": [
                        {
                            "error_source": "ShipStation",
                            "error_type": "integrations",
                            "error_code": "unknown",
                            "message": str(exception),
                        }
                    ],
                },
            ),
        )

    @classmethod
    async def evict_connection(cls: type["ShipStationClient"], uid: int) -> None:
        async with cls._pool_lock:
            physical_addr = cls._virtual_pool.get(uid, None)
            if not physical_addr:
                LOGGER.info(
                    f"evict_connection:::Could not find any connection with uuid {uid}"
                )
                return

            del cls._physical_pool[physical_addr]
            del cls._virtual_pool[uid]
            LOGGER.info(
                f"evict_connection:::Connection with uuid {uid} evicted from pool"
            )

    @classmethod
    async def _add_connection(
        cls: type["ShipStationClient"], connection: ShipStationConnection
    ) -> int:
        uid = connection.uid
        async with cls._pool_lock:
            cls._physical_pool[connection.pool_key] = connection
            cls._virtual_pool[uid] = connection.pool_key
            LOGGER.info(
                f"_add_connection:::Connection with uid {connection.uid} added to pool"
            )
            return uid

    @classmethod
    async def get_connection(
        cls: type["ShipStationClient"],
        uid: int | None = None,
        v2_key: str | None = None,
        v1_key: str | None = None,
        v1_secret: str | None = None,
        config: ConnectionConfig | None = None,
    ) -> ShipStationConnection | None:

        async with cls._pool_lock:
            if uid is not None:
                physical = cls._virtual_pool.get(uid, None)
                if physical is None:
                    LOGGER.info(
                        f"get_connection:::No connection object with uuid {uid} found."
                    )
                    return None
                return cls._physical_pool.get(physical, None)

            if config:
                physical = ShipStationConnection.hash(v2_key, v1_key, v1_secret, config)
                return cls._physical_pool.get(physical, None)

            return None

    @classmethod
    async def connect(
        cls: type["ShipStationClient"],
        uid: int | None = None,
        v2_key: str | None = None,
        v1_key: str | None = None,
        v1_secret: str | None = None,
        config: ConnectionConfig | None = None,
    ) -> ShipStationConnection:

        out: ShipStationConnection | None = await cls.get_connection(
            uid, v2_key, v1_key, v1_secret, config
        )
        if out is None:
            out = ShipStationConnection(v2_key, v1_key, v1_secret, config)
            uid = await cls._add_connection(out)
            LOGGER.info(f"configure:::New connection entry created with uid {uid}")

        return out

    @classmethod
    async def start(
        cls: type["ShipStationClient"],
        uid: int | None = None,
        v1_key: str | None = None,
        v1_secret: str | None = None,
        v2_key: str | None = None,
        connection: ShipStationConnection | None = None,
        config: ConnectionConfig | None = None,
        version: Literal["v1", "v2", "both"] = "both",
    ) -> ShipStationConnection:

        if version not in ("v1", "v2", "both"):
            raise ValueError(f"Unsupported version: {version}")

        if connection is not None:
            await connection.start(version)
            return connection

        connection = await cls.get_connection(uid, v2_key, v1_key, v1_secret, config)
        if connection is None:
            connection = await cls.connect(uid, v2_key, v1_key, v1_secret, config)

        if connection is None:
            raise ValueError(
                "Failed to create or retrieve a connection with the provided information."
            )

        await connection.start(version)
        return connection

    @classmethod
    async def close(
        cls: type["ShipStationClient"],
        v1_key: str | None = None,
        v1_secret: str | None = None,
        v2_key: str | None = None,
        connection: ShipStationConnection | None = None,
        uid: int | None = None,
        config: ConnectionConfig | None = None,
        version: Literal["v1", "v2", "both"] = "v2",
        force: bool = False,
    ) -> None:
        """
        Closes the asynchronous HTTP client session.

        Decrements the reference count and only actually closes the client
        when no more references remain. Pass ``force=True`` to close
        unconditionally, resetting the reference count to zero.
        """
        if version not in ("v1", "v2", "both"):
            raise ValueError(f"Unsupported version: {version}")

        conn = (
            connection
            if connection is not None
            else await cls.get_connection(uid, v2_key, v1_key, v1_secret, config)
        )

        if conn is None:
            raise ValueError(
                "No connection found to close. Provide a valid connection, uid, or credentials."
            )

        await conn.close(version, force=force)
        if conn.ref_count == 0:
            await cls.evict_connection(conn.uid)

    @classmethod
    @asynccontextmanager
    async def scoped_client(
        cls: type["ShipStationClient"],
        v1_key: str | None = None,
        v1_secret: str | None = None,
        v2_key: str | None = None,
        connection: ShipStationConnection | None = None,
        uid: int | None = None,
        config: ConnectionConfig | None = None,
        version: Literal["v1", "v2", "both"] = "v2",
        mock: bool = False,
    ) -> AsyncGenerator[ShipStationConnection | None, None]:
        connection = await cls.start(
            uid=uid,
            v1_key=v1_key,
            v1_secret=v1_secret,
            v2_key=v2_key,
            connection=connection,
            version=version,
            config=config,
        )

        try:
            yield connection
        finally:
            await cls.close(connection=connection, version=version)

    @classmethod
    async def request(
        cls: type["ShipStationClient"],
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: str,
        version: Literal["v1", "v2"] = "v2",
        connection: ShipStationConnection | None = None,
        uid: int | None = None,
        **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None],
    ) -> Response | APIError:
        if connection is None:
            if uid is None:
                raise ValueError(
                    "Either a connection or connection_hash must be provided."
                )
            connection = await cls.get_connection(uid=uid)
            if not connection:
                raise ValueError(
                    "No connection found for the provided hash. A connection must be started before making requests."
                )

        return await connection.request(method, url, version=version, **kwargs)


def write_json(fp: Path, data: dict[str, Any] | None) -> bool:
    """
    Writes a dictionary to a JSON file at the specified path.
    Args:
        fp (Path): The file path where the JSON data should be written.
        data (dict[str, Any] | None): The data to write to the JSON file. If None, no action is taken.
    Returns:
        bool: True if the data was written successfully, False otherwise.
    """
    if not data:
        LOGGER.warning(f"write_json:::No data to write to {fp}")
        return False

    try:
        with open(fp, "w") as f:
            dump(data, f, indent=4, ensure_ascii=False)
            LOGGER.info(f"write_json:::{fp} written to successfully")
            return True
    except (IOError, OSError) as err:
        LOGGER.error(f"write_json:::Failed to write data {err} to file {fp}")
        return False


def read_json(fp: Path) -> dict[str, Any] | None:
    """
    Reads a JSON file from the specified path and returns its content as a dictionary.
    Args:
        fp (Path): The file path from which to read the JSON data.
    Returns:
        dict[str, Any] | None: The data read from the JSON file as a dictionary, or None if the file does not exist or an error occurs.
    """
    if not fp.exists():
        LOGGER.warning(f"read_json:::File {fp} does not exist.")
        return None

    try:
        with open(fp, "r", encoding="utf-8") as f:
            data = load(f)
            LOGGER.info(f"read_json:::{fp} read successfully")
            return cast(dict[str, Any], data)
    except (IOError, OSError, JSONDecodeError) as err:
        LOGGER.error(f"read_json:::Failed to read data from {fp} with error: {err}")
        return None
