from ..carriers import PackageGist, PackageList
from ..common import (
    Dimensions,
    ErrorResponse,
    ShipStationClient,
    ShipStationConnection,
)

class CustomPackagePortal(ShipStationClient):
    @classmethod
    async def create(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
        name: str,
        package_code: str,
        dimensions: Dimensions,
        package_id: str | None = None,
        description: str | None = None,
        identity: bool = False,
    ) -> tuple[int, PackageGist | ErrorResponse]: ...
    @classmethod
    async def all(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
        identity: bool = False,
    ) -> tuple[int, PackageList | ErrorResponse]: ...
    @classmethod
    async def get_by_id(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
        package_id: str,
        identity: bool = False,
    ) -> tuple[int, PackageGist | ErrorResponse]: ...
    @classmethod
    async def update(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
        package_id: str,
        new_values: PackageGist,
        identity: bool = False,
    ) -> tuple[int, None | ErrorResponse]: ...
    @classmethod
    async def delete(
        cls: type["CustomPackagePortal"],
        connection: ShipStationConnection,
        package_id: str,
        identity: bool = False,
    ) -> tuple[int, None | ErrorResponse]: ...

__all__ = ["CustomPackagePortal"]
