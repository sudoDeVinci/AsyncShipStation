from asyncio import Lock
from base64 import b64encode
from contextlib import asynccontextmanager
from json import JSONDecodeError, dump, dumps, load
from logging import Logger, getLogger
from os import makedirs
from pathlib import Path
from typing import Any, AsyncGenerator, Final, Literal, TypeVar, cast

from dotenv import load_dotenv
from httpx import AsyncClient, Limits, Response
from httpx._types import HeaderTypes
from pydantic import EmailStr, HttpUrl

from ._types import ErrorResponse

LOGGER: Logger = getLogger(__name__)
LOGGER.setLevel("INFO")

load_dotenv()
CWD: Path = Path(__file__).parent.parent.resolve()
CACHE_DIR: Path = CWD / "__cache__"
makedirs(CACHE_DIR, exist_ok=True)

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
                        "errors_type": "integrations",
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
    def content(self) -> bytes:
        return self.__str__().encode("utf-8")


class ShipStationClient:
    __slots__ = ()

    _api_key_v2: str | None = None
    _api_key_v1: str | None = None
    _api_secret: str | None = None
    _v2_endpoint: Final[str] = "https://api.shipstation.com/v2"
    _v1_endpoint: Final[str] = "https://ssapi.shipstation.com"
    _v1_headers = {"User-Agent": "asyncShipStation/1.0.0"}
    _v2_headers = {"User-Agent": "asyncShipStation/1.0.0"}
    _v1_client: AsyncClient | None = None
    _v2_client: AsyncClient | None = None
    _v1_connection_lock: Lock = Lock()
    _v2_connection_lock: Lock = Lock()

    @classmethod
    def validate_response(
        cls: type["ShipStationClient"],
        res: Response | APIError,
        accepted_statuses: tuple[int, ...],
        return_type: type[T],
    ) -> tuple[int, ErrorResponse | T]:
        """
        Validates the HTTP response from the ShipStation API.
        Args:
            res (Response | APIError): The response object or APIError to validate.
            accepted_statuses (tuple[int, ...]): A tuple of accepted HTTP status codes.
        Returns:
            tuple[int, ErrorResponse | T]: A tuple containing the status code and either an error dict or a response.

        Raises:
            APIError: If the response status code is not in the accepted statuses.
        """
        json = cast(str | dict[str, object], res.json())
        if res.status_code not in accepted_statuses:
            if "errors" in json:
                return res.status_code, cast(ErrorResponse, json)

            raise APIError(
                res.status_code,
                json,
            )

        return res.status_code, cast(T, json)

    @classmethod
    def parse_unknown_exception(
        cls: type["ShipStationClient"], exception: Exception
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
    def configure(
        cls: type["ShipStationClient"],
        v2_key: str,
        v1_key: str | None = None,
        v1_secret: str | None = None,
    ) -> None:
        """
        Configures the ShipStation client with the provided API key.
        Args:
            api_key (str): The API key for authenticating requests.
        """
        cls._api_key_v2 = v2_key
        cls._api_key_v1 = v1_key
        cls._api_secret = v1_secret
        cls._v2_headers["api-key"] = v2_key

        if v1_key and v1_secret:
            credentials = f"{v1_key}:{v1_secret}"
            encoded_credentials = b64encode(credentials.encode("utf-8")).decode("utf-8")
            cls._v1_headers["Authorization"] = f"Basic {encoded_credentials}"

    @classmethod
    async def start(
        cls: type["ShipStationClient"], version: Literal["v1", "v2"] = "v2"
    ) -> None:
        """
        Initializes the asynchronous HTTP client session.
        """
        if version == "v2":
            async with cls._v2_connection_lock:
                if cls._v2_client is None:
                    cls._v2_client = AsyncClient(
                        base_url=cls._v2_endpoint,
                        headers=cast(HeaderTypes, cls._v2_headers),
                        timeout=30,
                        http2=False,  # Disable HTTP/2
                        limits=Limits(
                            max_connections=20,
                            max_keepalive_connections=10,
                        ),
                    )

        elif version == "v1":
            async with cls._v1_connection_lock:
                if cls._v1_client is None:
                    cls._v1_client = AsyncClient(
                        base_url=cls._v1_endpoint,
                        headers=cast(HeaderTypes, cls._v1_headers),
                        timeout=30,
                        http2=False,  # Disable HTTP/2
                        limits=Limits(
                            max_connections=20,
                            max_keepalive_connections=10,
                        ),
                    )

        else:
            raise ValueError(f"Unsupported version: {version}")

    @classmethod
    async def close(
        cls: type["ShipStationClient"], version: Literal["v1", "v2"] = "v2"
    ) -> None:
        """
        Closes the asynchronous HTTP client session.
        """
        if version == "v2":
            async with cls._v2_connection_lock:
                if cls._v2_client is not None:
                    await cls._v2_client.aclose()
                    cls._v2_client = None

        elif version == "v1":
            async with cls._v1_connection_lock:
                if cls._v1_client is not None:
                    await cls._v1_client.aclose()
                    cls._v1_client = None

        else:
            raise ValueError(f"Unsupported version: {version}")

    @classmethod
    @asynccontextmanager
    async def scoped_client(
        cls: type["ShipStationClient"],
        version: Literal["v1", "v2"] = "v2",
    ) -> AsyncGenerator[AsyncClient, None]:
        """
        Asynchronous context manager for the HTTP client session.
        Yields:
            AsyncClient: The asynchronous HTTP client session.
        """
        await cls.start(version)
        client = cls._v2_client if version == "v2" else cls._v1_client
        try:
            yield client  # type: ignore
        finally:
            await cls.close(version)

    @classmethod
    async def request(
        cls: type["ShipStationClient"],
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: str,
        version: Literal["v1", "v2"] = "v2",
        **kwargs: dict[str, str | int | bool | EmailStr | HttpUrl | None],
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
        client = cls._v2_client if version == "v2" else cls._v1_client
        if client is None:
            await cls.start(version)

        if client is None:
            return APIError(500, "HTTP client could not be initialized.")

        response = await client.request(method, url, **kwargs)  # type: ignore[arg-type]

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
            return cast(dict[str, Any], data)
    except (IOError, OSError, JSONDecodeError) as err:
        LOGGER.error(f"read_json:::Failed to read data from {fp} with error: {err}")
        return None
