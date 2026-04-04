from typing import TypedDict

class V1Store(TypedDict):
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

class V1MarketPlace(TypedDict):
    name: str
    marketplaceId: int
    canRefresh: bool
    supportsCustomMappings: bool
    supportsCustomStatuses: bool
    canConfirmShipments: bool
