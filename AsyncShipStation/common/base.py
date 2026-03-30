from asyncio import Lock
from base64 import b64encode
from contextlib import asynccontextmanager
from dataclasses import dataclass
from hashlib import sha256
from json import JSONDecodeError, dump, dumps, load
from logging import Logger, getLogger
from pathlib import Path
from typing import Any, AsyncGenerator, ClassVar, Literal, TypeVar, cast

from httpx import AsyncClient, Limits, Response
from httpx._types import HeaderTypes
from pydantic import EmailStr, HttpUrl

from ._types import ErrorResponse

LOGGER: Logger = getLogger("AsyncShipStation")
LOGGER.setLevel("INFO")

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
    version: Literal["v1", "v2"] = "v2"
    timeout = 30
    max_connections = 20
    max_keepalive_connections = 10
    http2 = False
    retries = 3
    user_agent = "asyncShipStation/2.0.0"
    v2_endpoint = "https://api.shipstation.com/v2"
    v2_mock_endpoint = "https://docs.shipstation.com/_mock/openapi/v2"
    v1_endpoint = "https://ssapi.shipstation.com"


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
    )

    def __init__(
        self,
        v2_key: str | None = None,
        v1_key: str | None = None,
        v1_secret: str | None = None,
        config: ConnectionConfig | None = None,
    ) -> None:

        self._v2_key: str | None = v2_key
        self._v1_key: str | None = v1_key
        self._v1_secret: str | None = v1_secret
        self._v1_enabled: bool = False
        self._v2_enabled: bool = False
        self._config: ConnectionConfig = config or ConnectionConfig()
        self._pool_key: int = self.hash(v2_key, v1_key, v1_secret)
        if self._v2_key:
            self._v2_headers: dict[str, str] = {
                "User-Agent": "asyncShipStation/1.0.0",
                "api-key": self._v2_key,
            }
            self._v2_enabled = True

        if v1_key and v1_secret:
            credentials = f"{v1_key}:{v1_secret}"
            encoded_credentials = b64encode(credentials.encode("utf-8")).decode("utf-8")
            self._v1_headers: dict[str, str] = {
                "User-Agent": "asyncShipStation/1.1.2",
                "Authorization": f"Basic {encoded_credentials}",
            }
            self._v1_enabled = True

        self._v1_lock: Lock = Lock()
        self._v2_lock: Lock = Lock()
        self._v1_client: AsyncClient | None = None
        self._v2_client: AsyncClient | None = None
        self._v1_ref_count: int = 0
        self._v2_ref_count: int = 0

    async def start_v1(self: "ShipStationConnection") -> None:
        if not self._v1_enabled:
            raise APIError(400, "API v1 is not enabled for this connection.")
        async with self._v1_lock:
            if self._v1_client is None:
                self._v1_client = AsyncClient(
                    base_url=self._config.v1_endpoint,
                    headers=cast(HeaderTypes, self._v1_headers),
                    timeout=30,
                    http2=False,  # Disable HTTP/2
                    limits=Limits(
                        max_connections=20,
                        max_keepalive_connections=10,
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
                    timeout=30,
                    http2=False,  # Disable HTTP/2
                    limits=Limits(
                        max_connections=20,
                        max_keepalive_connections=10,
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
    def v2_key(self) -> str | None:
        return self._v2_key

    @property
    def v1_key(self) -> str | None:
        return self._v1_key

    @property
    def v1_secret(self) -> str | None:
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
        )

    @staticmethod
    def hash(v2_key: str | None, v1_key: str | None, v1_secret: str | None) -> int:
        raw = f"{v2_key or ''}:{v1_key or ''}:{v1_secret or ''}"
        digest = int.from_bytes(
            sha256(raw.encode("utf-8")).digest()[:8], "big", signed=True
        )
        return -2 if digest == -1 else digest

    def __hash__(self: "ShipStationConnection") -> int:
        return self._pool_key


class ShipStationClient:
    __slots__ = ()

    _v2_endpoint: ClassVar[str] = "https://api.shipstation.com/v2"
    _v2_mock_endpoint: ClassVar[str] = "https://docs.shipstation.com/_mock/openapi/v2"
    _v1_endpoint: ClassVar[str] = "https://ssapi.shipstation.com"

    _pool: ClassVar[dict[int, ShipStationConnection]] = {}
    _pool_lock: ClassVar[Lock] = Lock()

    @classmethod
    def validate_response(
        cls: type["ShipStationClient"],
        res: Response | APIError,
        accepted_statuses: tuple[int, ...],
        return_type: type[T],
    ) -> tuple[int, ErrorResponse | T]:
        try:
            json = cast(str | dict[str, object], res.json())
        except JSONDecodeError as e:
            # Return raw response text for debugging
            return cls.parse_unknown_exception(
                Exception(f"JSON decode error: {e}. Raw response: {res.text[:500]}")
            )

        if res.status_code not in accepted_statuses:
            if "errors" in json:
                return res.status_code, cast(ErrorResponse, json)
            raise APIError(res.status_code, json)

        return res.status_code, cast(T, json)

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
    async def evict_connection(
        cls: type["ShipStationClient"], connection_hash: int
    ) -> None:
        async with cls._pool_lock:
            if connection_hash in cls._pool:
                del cls._pool[connection_hash]
                LOGGER.info(
                    f"evict_connection:::Connection with hash {connection_hash} evicted from pool"
                )

    @classmethod
    async def _add_connection(
        cls: type["ShipStationClient"], connection: ShipStationConnection
    ) -> None:
        async with cls._pool_lock:
            cls._pool[hash(connection)] = connection
            LOGGER.info(
                f"_add_connection:::Connection with hash {hash(connection)} added to pool"
            )

    @classmethod
    async def get_connection(
        cls: type["ShipStationClient"],
        v2_key: str | None = None,
        v1_key: str | None = None,
        v1_secret: str | None = None,
        connection_hash: int | None = None,
    ) -> ShipStationConnection | None:
        """
        Retrieves a ShipStationConnection from the pool based on the provided API keys.
        Args:
            v2_key (str): The API key for ShipStation API v2.
            v1_key (str | None): The API key for ShipStation API v1.
            v1_secret (str | None): The API secret for ShipStation API v1.
            connection_hash (int | None): An optional hash to look up a ShipStationConnection in the pool.
        Returns:
            ShipStationConnection | None: The retrieved ShipStationConnection if found, or None if no matching connection exists in the pool.
        """
        if connection_hash is not None:
            async with cls._pool_lock:
                return cls._pool.get(connection_hash, None)

        if not (v2_key or (v1_key and v1_secret)):
            raise ValueError("Insufficient credentials to identify a connection.")

        hashed = ShipStationConnection.hash(v2_key, v1_key, v1_secret)
        async with cls._pool_lock:
            return cls._pool.get(hashed, None)

    @classmethod
    async def configure(
        cls: type["ShipStationClient"],
        v2_key: str,
        v1_key: str | None = None,
        v1_secret: str | None = None,
    ) -> ShipStationConnection:
        """
        TODO: Rename to "connect"
        Configures the ShipStation client with the provided API key.
        Args:
            api_key (str): The API key for authenticating requests.
        """

        out: ShipStationConnection | None = await cls.get_connection(
            v2_key, v1_key, v1_secret
        )
        if out is None:
            out = ShipStationConnection(v2_key, v1_key, v1_secret)
            await cls._add_connection(out)
            LOGGER.info(
                f"configure:::New connection entry created with hash {out.pool_key}"
            )

        return out

    @classmethod
    async def start(
        cls: type["ShipStationClient"],
        v1_key: str | None = None,
        v1_secret: str | None = None,
        v2_key: str | None = None,
        connection: ShipStationConnection | None = None,
        connection_hash: int | None = None,
        version: Literal["v1", "v2", "both"] = "both",
    ) -> ShipStationConnection:
        """
        Retrieve and start a ShipStationConnection from the pool based on any provided conenction info.
        If a ``connection_hash`` is provided, the pool will be checked for a matching connection. If found, it will be started and returned.
        If no hash is provided but a ``connection`` object is, that connection will be started and returned.
        If neither of those are provided, the method will attempt to create a new connection using the provided credentials.
        Args:
            v1_key (str | None): The API key for ShipStation API v1.
            v1_secret (str | None): The API secret for ShipStation API v1.
            v2_key (str | None): The API key for ShipStation API v2.
            connection (ShipStationConnection | None): An optional ShipStationConnection object to start.
            connection_hash (int | None): An optional hash to look up a ShipStationConnection in the pool.
            version (Literal["v1", "v2", "both"]): The API version(s) to start the connection for. Defaults to "both".
        """
        if version not in ("v1", "v2", "both"):
            raise ValueError(f"Unsupported version: {version}")

        if connection is not None:
            await connection.start(version)
            return connection

        connection = await cls.get_connection(
            v2_key, v1_key, v1_secret, connection_hash
        )
        if connection is None:
            connection = await cls.configure(
                v2_key or "", v1_key or "", v1_secret or ""
            )

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
        connection_hash: int | None = None,
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
            else await cls.get_connection(v2_key, v1_key, v1_secret, connection_hash)
        )

        if conn is None:
            raise ValueError(
                "No connection found to close. Provide a valid connection, connection hash, or credentials."
            )

        await conn.close(version, force=force)
        if conn.ref_count == 0:
            await cls.evict_connection(hash(conn))

    @classmethod
    @asynccontextmanager
    async def scoped_client(
        cls: type["ShipStationClient"],
        v1_key: str | None = None,
        v1_secret: str | None = None,
        v2_key: str | None = None,
        connection: ShipStationConnection | None = None,
        connection_hash: int | None = None,
        version: Literal["v1", "v2", "both"] = "v2",
        mock: bool = False,
    ) -> AsyncGenerator[ShipStationConnection | None, None]:
        connection = await cls.start(
            v1_key=v1_key,
            v1_secret=v1_secret,
            v2_key=v2_key,
            connection=connection,
            connection_hash=connection_hash,
            version=version,
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
        connection_hash: int | None = None,
        **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None],
    ) -> Response | APIError:
        if connection is None:
            if not connection_hash:
                raise ValueError(
                    "Either a connection or connection_hash must be provided."
                )
            connection = await cls.get_connection(connection_hash=connection_hash)
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
