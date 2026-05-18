from ..common import V1Address
from ..common._types import Taggable


class V1Warehouse(Taggable):
    warehouseId: int
    warehouseName: str
    originAddress: V1Address
    returnAddress: V1Address | None
    isDefault: bool
    createDate: str  # in the form "2014-10-21T08:11:43.8800000"
    sellerIntegrationId: str | None
    extInventoryIdentity: str | None
    registerFedexMeter: bool | None
