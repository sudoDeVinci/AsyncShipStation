from typing import Literal, TypedDict

from ..common import Option, PaginatinatedResponse, V1Address, V1Dimensions, V1Weight


class V1AdvancedOptions(TypedDict):
    warehouseId: int
    nonMachinable: bool
    saturdayDelivery: bool
    containsAlcohol: bool
    storeId: int
    customField1: str | None
    customField2: str | None
    customField3: str | None
    source: str
    mergedOrSplit: bool  # read-only
    mergedIds: list[int]  # read-only
    parentId: int | None  # read-only
    billToParty: (
        Literal["my_account", "my_other_account", "recipient", "third_party"] | None
    )
    billToAccount: str | None
    billToPostalCode: str | None
    billToCountryCode: str | None
    billToMyOtherAccount: str | None


class V1InsuranceOptions(TypedDict):
    provider: Literal["shipsurance", "carrier", "provider", "xcover", "parcelguard"]
    insureShipment: bool
    insuredValue: float


class V1Customsitem(TypedDict):
    customsItemId: str
    description: str
    quantity: int
    value: float
    harmonizedtariffCode: str
    countryofOrigin: str


class V1InternationalOptions(TypedDict):
    contents: Literal["merchandise", "documents", "gift", "returned_goods", "sample"]
    customsItems: V1Customsitem
    nonDelivery: Literal["return_to_sender", "treat_as_abandoned"]


class V1OrderItem(TypedDict):
    orderItemId: int
    lineItemKey: int
    sku: str
    name: str
    imageUrl: str
    weight: V1Weight
    quantity: int
    unitPrice: float
    taxAmount: float
    shippingAmount: float
    warehouseLocation: V1Address | None
    options: list[Option]
    productId: int
    fulfillmentSku: object | None  # no clue
    adjustment: object | None  # no clue
    upc: object | None  # no clue
    createdDate: str
    modifyDate: str | None


class V1Order(TypedDict):
    orderId: int
    orderNumber: str
    orderKey: str
    orderDate: str
    createDate: str  # read-only
    modifyDate: str  # read-only
    paymentDate: str
    shipByDate: str | None
    orderStatus: Literal[
        "awaiting_payment", "awaiting_shipment", "shipped", "on_hold", "cancelled"
    ]
    customerId: int  # read-only
    customerUsername: str
    customerEmail: str
    billTo: V1Address
    shipTo: V1Address
    items: list[V1OrderItem]
    orderTotal: float  # read-only
    amountPaid: float
    taxAmount: float
    shippingAmount: float
    customerNotes: str
    internalNotes: str
    gift: bool
    giftMessage: str
    paymentMethod: str
    requestedShippingService: str | None
    carrierCode: str
    serviceCode: str
    packageCode: str
    confirmation: str
    shipDate: str
    holdUntilDate: str | None
    weight: V1Weight
    dimensions: V1Dimensions
    insuranceOptions: V1InsuranceOptions
    advancedOptions: V1AdvancedOptions
    tagIds: list[int] | None
    userId: str  # read-only
    externallyFulfilled: bool  # read-only
    externallyFulfilledBy: str | None  # read-only


class V1OrderListResponse(PaginatinatedResponse):
    orders: list[V1Order]


class V1OrderLabel(TypedDict):
    shipmentId: int
    shipmentCost: float
    insuranceCost: float
    trackingNumber: str
    labelData: str | bytes | None  # base64 encoded PDF value
    formData: str | None
