from typing import Literal

from AsyncShipStation.orders._types import (
    V1AdvancedOptions,
    V1Dimensions,
    V1InsuranceOptions,
    V1InternationalOptions,
    V1OrderLabel,
    V1OrderListResponse,
    V1Weight,
)

from ..common import ErrorResponse, ShipStationClient


class OrderPortal(ShipStationClient):
    @classmethod
    async def list(
        cls: type[ShipStationClient],
        customerName: str | None = None,
        itemKeyword: str | None = None,
        createDateStart: str | None = None,
        createDateEnd: str | None = None,
        customsCountryCode: str | None = None,
        modifyDateStart: str | None = None,
        modifyDateEnd: str | None = None,
        orderDateStart: str | None = None,
        orderDateEnd: str | None = None,
        orderNumber: str | None = None,
        orderStatus: (
            Literal[
                "awaiting_payment",
                "awaiting_shipment",
                "pending_fulfillment",
                "shipped",
                "on_hold",
                "cancelled",
                "rejected_fulfillment",
            ]
            | None
        ) = None,
        paymentDateStart: str | None = None,
        paymentDateEnd: str | None = None,
        storeId: int | None = None,
        sortBy: Literal["OrderDate", "ModifyDate", "CreateDate"] | None = None,
        sortDir: Literal["DESC", "ASC"] | None = None,
        page: int | None = None,
        pageSize: int | None = None,
    ) -> tuple[int, ErrorResponse | V1OrderListResponse]:
        params = {
            "customerName": customerName,
            "itemKeyword": itemKeyword,
            "createDateStart": createDateStart,
            "createDateEnd": createDateEnd,
            "customsCountryCode": customsCountryCode,
            "modifyDateStart": modifyDateStart,
            "modifyDateEnd": modifyDateEnd,
            "orderDateStart": orderDateStart,
            "orderDateEnd": orderDateEnd,
            "orderNumber": orderNumber,
            "orderStatus": orderStatus,
            "paymentDateStart": paymentDateStart,
            "paymentDateEnd": paymentDateEnd,
            "storeId": storeId,
            "sortBy": sortBy,
            "sortDir": sortDir,
            "page": page,
            "pageSize": pageSize,
        }

        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f"{cls._v1_endpoint}/orders"

        try:
            res = await cls.request("GET", endpoint, "v1", params=params)  # type: ignore[arg-type]
            return cls.validate_response(
                res,
                (200, 201),
                V1OrderListResponse,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def create_label(
        cls: type[ShipStationClient],
        orderId: int,
        carrierCode: str,
        serviceCode: str,
        confirmation: Literal[
            "none", "delivery", "signature", "adult_signature", "direct_signature"
        ],
        shipDate: str,
        weight: V1Weight | None = None,
        dimensions: V1Dimensions | None = None,
        insuranceoptions: V1InsuranceOptions | None = None,
        internationalOptions: V1InternationalOptions | None = None,
        advancedOptions: V1AdvancedOptions | None = None,
        testLabel: bool = False,
    ) -> tuple[int, V1OrderLabel | ErrorResponse]:
        payload = {
            "orderId": orderId,
            "carrierCode": carrierCode,
            "serviceCode": serviceCode,
            "confirmation": confirmation,
            "shipDate": shipDate,
            "weight": weight,
            "dimensions": dimensions,
            "insuranceOptions": insuranceoptions,
            "internationalOptions": internationalOptions,
            "advancedOptions": advancedOptions,
            "testLabel": testLabel,
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        endpoint = f"{cls._v1_endpoint}/orders/createlabelfororder"

        try:
            res = await cls.request("POST", endpoint, "v1", json=payload)  # type: ignore[arg-type]
            return cls.validate_response(
                res,
                (200, 201),
                V1OrderLabel,
            )
        except Exception as e:
            return cls.parse_unknown_exception(e)
