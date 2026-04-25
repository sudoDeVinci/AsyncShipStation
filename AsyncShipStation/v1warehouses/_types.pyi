from ..common import Taggable, V1Address

class V1Warehouse(Taggable):
    warehouseId: int
    warehouseName: str
    originAddress: V1Address
    returnAddress: V1Address | None
    isDefault: bool
    createDate: str
    sellerIntegrationId: str | None
    extInventoryIdentity: str | None
    registerFedexMeter: bool | None
