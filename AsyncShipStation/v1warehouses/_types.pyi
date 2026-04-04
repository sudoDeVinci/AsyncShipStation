from typing import TypedDict
from ..common import V1Address

class V1Warehouse(TypedDict):
    warehouseId: int
    warehouseName: str
    originAddress: V1Address
    returnAddress: V1Address | None
    isDefault: bool
    createDate: str
    sellerIntegrationId: str | None
    extInventoryIdentity: str | None
    registerFedexMeter: bool | None
