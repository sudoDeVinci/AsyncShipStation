from ..common import Taggable

class V1Store(Taggable):
    storeId: str
    storeName: str
    marketplaceId: int
    marketplaceName: str
    accountName: str | None
    email: str | None
    integrationUrl: str | None
    active: bool
    companyName: str
    phone: str
    publicEmail: str
    website: str
    refreshDate: str
    lastRefreshAttempt: str
    createDate: str
    modifyDate: str
    autoRefresh: bool

class V1MarketPlace(Taggable):
    name: str
    marketplaceId: int
    canRefresh: bool
    supportsCustomMappings: bool
    supportsCustomStatuses: bool
    canConfirmShipments: bool
