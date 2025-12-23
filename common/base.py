from contextlib import asynccontextmanager
from json import JSONDecodeError, dump, load
from logging import Logger, getLogger
from os import environ, makedirs
from pathlib import Path
from threading import Lock
from typing import Any, AsyncGenerator, Literal, cast

from dotenv import load_dotenv  # type: ignore
from httpx import AsyncClient, Response
from httpx._types import HeaderTypes

LOGGER: Logger = getLogger(__name__)
LOGGER.setLevel("INFO")

load_dotenv()
CWD: Path = Path(__file__).parent.resolve()
CACHE_DIR: Path = CWD / "__cache__"
makedirs(CACHE_DIR, exist_ok=True)

CACHE_LOCK: Lock = Lock()
API_ENDPOINT = "https://api.shipstation.com/v2"

API_KEY: str | None = None

try:
    assert load_dotenv(
        verbose=True,
    ), "Failed to load variables from .env file"

    API_KEY = environ.get("API_KEY", None)

    assert API_KEY is not None, "API_KEY must be set in environment variables."

except (AssertionError, AttributeError, OSError) as err:
    LOGGER.error(f"Error during global configuration:::{err}")


class APIError(Exception):
    """
    Returned for local ShipStation responses such as during configuration.
    """

    __slots__ = ("status_code", "details")

    def __init__(self, status: int, detail: str | dict[str, object]):
        self.status_code = status
        self.details = detail

    def json(self) -> dict[str, object]:
        return {"status_code": self.status_code, "detail": self.details}

    @property
    def content(self) -> bytes:
        return str(self.details).encode("utf-8")


class ShipStationClient:
    __slots__ = ()

    _api_key = API_KEY
    _endpoint = API_ENDPOINT
    _headers: HeaderTypes = {
        "User-Agent": "asyncShipStation/1.0.0",
        "api-key": API_KEY if API_KEY else "",
    }
    _client: AsyncClient | None = None
    _connection_lock: Lock = Lock()

    @classmethod
    async def start(
        cls: type["ShipStationClient"],
    ) -> None:
        """
        Initializes the asynchronous HTTP client session.
        """
        with cls._connection_lock:
            if cls._client is None:
                cls._client = AsyncClient(
                    base_url=cast(str, cls._endpoint),
                    headers=cls._headers,
                    timeout=30,
                )

    @classmethod
    async def close(
        cls: type["ShipStationClient"],
    ) -> None:
        """
        Closes the asynchronous HTTP client session.
        """
        with cls._connection_lock:
            if cls._client is not None:
                await cls._client.aclose()
                cls._client = None

    @classmethod
    @asynccontextmanager
    async def scoped_client(
        cls: type["ShipStationClient"],
    ) -> AsyncGenerator[AsyncClient, None]:
        """
        Asynchronous context manager for the HTTP client session.
        Yields:
            AsyncClient: The asynchronous HTTP client session.
        """
        await cls.start()
        try:
            yield cls._client  # type: ignore
        finally:
            await cls.close()

    @classmethod
    async def request(
        cls: type["ShipStationClient"],
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: str,
        **kwargs,
    ) -> Response | APIError:
        """
        Makes an asynchronous HTTP request to the ShipStation API.
        Args:
            method (str): The HTTP method to use (e.g., 'GET', 'POST').
            url (str): The endpoint URL to which the request will be made.
            **kwargs: Additional keyword arguments to pass to the request.
        Returns:
            Response: The response object returned by the request.
        Raises:
            RequestError: If an error occurs while making the request.
        """
        if cls._client is None:
            await cls.start()

        if cls._client is None:
            raise APIError(500, "HTTP client could not be initialized.")

        response = await cls._client.request(method, url, **kwargs)

        # Handle rate limiting - return as error to match union pattern
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "60")
            return APIError(
                429,
                {
                    "error": "rate_limit_exceeded",
                    "retry_after": retry_after,
                    "message": f"Rate limited. Retry after {retry_after}s",
                },
            )

        return response


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
            return data
    except (IOError, OSError, JSONDecodeError) as err:
        LOGGER.error(f"read_json:::Failed to read data from {fp} with error: {err}")
        return None
