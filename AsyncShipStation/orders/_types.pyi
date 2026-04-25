from typing import Literal

from ..common import (
    DeliveryConfirmationMethods,
    Option,
    PaginatinatedResponse,
    Taggable,
    V1Address,
    V1Dimensions,
    V1Weight,
)

class V1AdvancedOptions(Taggable):
    warehouseId: int
    nonMachinable: bool
    saturdayDelivery: bool
    containsAlcohol: bool
    storeId: int
    customField1: str | None
    customField2: str | None
    customField3: str | None
    source: str
    mergedOrSplit: bool
    mergedIds: list[int]
    parentId: int | None
    billToParty: (
        Literal["my_account", "my_other_account", "recipient", "third_party"] | None
    )
    billToAccount: str | None
    billToPostalCode: str | None
    billToCountryCode: str | None
    billToMyOtherAccount: str | None

class V1InsuranceOptions(Taggable):
    provider: Literal["shipsurance", "carrier", "provider", "xcover", "parcelguard"]
    insureShipment: bool
    insuredValue: float

class V1Customsitem(Taggable):
    customsItemId: str
    description: str
    quantity: int
    value: float
    harmonizedtariffCode: str
    countryofOrigin: str

class V1InternationalOptions(Taggable):
    contents: Literal["merchandise", "documents", "gift", "returned_goods", "sample"]
    customsItems: V1Customsitem
    nonDelivery: Literal["return_to_sender", "treat_as_abandoned"]

class V1OrderItem(Taggable):
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
    fulfillmentSku: object | None
    adjustment: object | None
    upc: object | None
    createdDate: str
    modifyDate: str | None

class V1Order(Taggable):
    orderId: int
    orderNumber: str
    orderKey: str
    orderDate: str
    createDate: str
    modifyDate: str
    paymentDate: str
    shipByDate: str | None
    orderStatus: Literal[
        "awaiting_payment", "awaiting_shipment", "shipped", "on_hold", "cancelled"
    ]
    customerId: int
    customerUsername: str
    customerEmail: str
    billTo: V1Address
    shipTo: V1Address
    items: list[V1OrderItem]
    orderTotal: float
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
    confirmation: DeliveryConfirmationMethods
    shipDate: str
    holdUntilDate: str | None
    weight: V1Weight
    dimensions: V1Dimensions
    insuranceOptions: V1InsuranceOptions
    advancedOptions: V1AdvancedOptions
    tagIds: list[int] | None
    userId: str
    externallyFulfilled: bool
    externallyFulfilledBy: str | None

class V1OrderListResponse(PaginatinatedResponse):
    orders: list[V1Order]

class V1OrderCreationResponseResult(Taggable):
    orderId: int
    orderNumber: str
    orderkey: str
    success: bool
    errorMessage: str | None

class V1BatchOrderCreationResponse(Taggable):
    hasErrors: bool
    results: list[V1OrderCreationResponseResult]

class V1OrderLabel(Taggable):
    shipmentId: int
    shipmentCost: float
    insuranceCost: float
    trackingNumber: str
    labelData: str | bytes | None
    formData: str | None
