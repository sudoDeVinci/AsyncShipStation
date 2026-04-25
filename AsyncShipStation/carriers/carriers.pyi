from ..common import ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import (
    AdvancedCarrierOptionList,
    Carrier,
    CarrierListResponse,
    PackageList,
    ServiceList,
)

class CarrierPortal(ShipStationClient):
    @classmethod
    async def all(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        identity: bool = False,
    ) -> tuple[int, CarrierListResponse | ErrorResponse]: ...
    @classmethod
    async def get_by_id(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        carrier_id: str,
        identity: bool = False,
    ) -> tuple[int, Carrier | ErrorResponse]: ...
    @classmethod
    async def get_options(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        carrier_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | AdvancedCarrierOptionList]: ...
    @classmethod
    async def get_packages(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        carrier_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | PackageList]: ...
    @classmethod
    async def get_services(
        cls: type["CarrierPortal"],
        connection: ShipStationConnection,
        carrier_id: str,
        identity: bool = False,
    ) -> tuple[int, ErrorResponse | ServiceList]: ...
