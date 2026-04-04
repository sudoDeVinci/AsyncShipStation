from typing import cast
from ..carriers import PackageGist, PackageList
from ..common import Dimensions, Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection

class CustomPackagePortal(ShipStationClient):
    @classmethod
    async def create(cls: type['CustomPackagePortal'], connection: ShipStationConnection, name: str, package_code: str, dimensions: Dimensions, package_id: str | None = None, description: str | None = None) -> tuple[int, PackageGist | ErrorResponse]: ...

    @classmethod
    async def list(cls: type['CustomPackagePortal'], connection: ShipStationConnection) -> tuple[int, PackageList | ErrorResponse]: ...

    @classmethod
    async def get_by_id(cls: type['CustomPackagePortal'], connection: ShipStationConnection, package_id: str) -> tuple[int, PackageGist | ErrorResponse]: ...

    @classmethod
    async def update(cls: type['CustomPackagePortal'], connection: ShipStationConnection, package_id: str, new_values: PackageGist) -> tuple[int, None | ErrorResponse]: ...

    @classmethod
    async def delete(cls: type['CustomPackagePortal'], connection: ShipStationConnection, package_id: str) -> tuple[int, None | ErrorResponse]: ...

__all__ = ['CustomPackagePortal']
