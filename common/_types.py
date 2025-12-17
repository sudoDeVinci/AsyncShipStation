from __future__ import annotations

from abc import ABCMeta
from enum import Enum

from pydantic import EmailStr, HttpUrl, PastDatetime

JSONDict = dict[str, str | int | bool | EmailStr | HttpUrl | PastDatetime | None]


class ShipPortal(ABCMeta): ...


class Endpoints(Enum):
    BATCHES = "/v2/batches/"


class ErrorMessage:
    """
    Represents an error message with a code and description.

    Attributes:
        code (int): The error code.
        message (str): A description of the error.
        endpoint (str | None): The API endpoint where the error occurred, if applicable.
    """

    __slots__ = ("code", "message", "endpoint")

    def __init__(self, code: int, message: str, endpoint: str | None = None):
        self.code = code
        self.message = message
        self.endpoint = endpoint

    def model_dump(self, **kwargs) -> JSONDict:
        """
        Converts the error message to a JSON-compatible dictionary.

        Returns:
            JSONDict: A dictionary representation of the error message.
        """
        return {"code": self.code, "message": self.message, "endpoint": self.endpoint}

    def dict(self) -> JSONDict:
        """
        Alias for model_dump to maintain compatibility with Pydantic's dict method.

        Returns:
            JSONDict: A dictionary representation of the error message.
        """
        return self.model_dump()
