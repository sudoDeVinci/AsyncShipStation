from ..common import Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection
from ._types import AdvancedCarrierOptionList, Carrier, CarrierListResponse, PackageList, ServiceList

class CarrierPortal(ShipStationClient):
    @classmethod
    async def list_carriers(cls: type['CarrierPortal'], connection: ShipStationConnection) -> tuple[int, CarrierListResponse | ErrorResponse]: ...

    @classmethod
    async def get_by_id(cls: type['CarrierPortal'], connection: ShipStationConnection, carrier_id: str) -> tuple[int, Carrier | ErrorResponse]: ...

    @classmethod
    async def get_options(cls: type['CarrierPortal'], connection: ShipStationConnection, carrier_id: str) -> tuple[int, ErrorResponse | AdvancedCarrierOptionList]: ...

    @classmethod
    async def get_packages(cls: type['CarrierPortal'], connection: ShipStationConnection, carrier_id: str) -> tuple[int, ErrorResponse | PackageList]: ...

    @classmethod
    async def get_services(cls: type['CarrierPortal'], connection: ShipStationConnection, carrier_id: str) -> tuple[int, ErrorResponse | ServiceList]: ...
