from typing import List, Literal, cast

from ..common import (
    DeliveryConfirmationMethods,
    Dimensions,
    Endpoints,
    ErrorResponse,
    ShipStationClient,
    ShipStationConnection,
    Weight,
)
from ..shipments import Shipment
from ._types import (
    CalculateRatesRequest,
    CalculateRatesResponse,
    Rate,
    RateEstimate,
    RateEstimateOptions,
    RateRequestOptions,
)


class RatesPortal(ShipStationClient):
    """Portal for interacting with the ShipStation Rates API (V2)."""

    @classmethod
    async def calculate_rates(
        cls: type["RatesPortal"],
        connection: ShipStationConnection,
        carrier_ids: List[str],
        shipment_id: str | None = None,
        shipment: Shipment | None = None,
        package_types: List[str] | None = None,
        service_codes: List[str] | None = None,
        calculate_tax_amount: bool = False,
        preferred_currency: str | None = None,
        is_return: bool = False,
    ) -> tuple[int, CalculateRatesResponse | ErrorResponse]:
        """
        Get shipping rates for a shipment.
        https://docs.shipstation.com/openapi/rates/calculate_rates

        You must provide either a shipment_id or a shipment object.

        Args:
            carrier_ids: List of carrier IDs to get rates from
            shipment_id: ID of an existing shipment to get rates for
            shipment: Full shipment object (alternative to shipment_id)
            package_types: Optional list of package types to filter rates
            service_codes: Optional list of service codes to filter rates
            calculate_tax_amount: Whether to calculate tax amounts
            preferred_currency: Preferred currency for rates
            is_return: Whether this is a return shipment

        Returns:
            Tuple of status code and CalculateRatesResponse or ErrorResponse
        """
        options = {
            "carrier_ids": carrier_ids,
            "package_types": package_types,
            "service_codes": service_codes,
            "calculate_tax_amount": calculate_tax_amount,
            "preferred_currency": preferred_currency,
            "is_return": is_return,
        }

        rate_options = cast(
            RateRequestOptions, {k: v for k, v in options.items() if v is not None}
        )

        payload_options = {
            "rate_options": rate_options,
            "shipment": shipment,
            "shipment_id": shipment_id,
        }

        payload = cast(
            CalculateRatesRequest,
            {k: v for k, v in payload_options.items() if v is not None},
        )

        if payload.get("shipment", payload.get("shipment_id", None)) is None:
            # Return an error - one of the two is required
            error_response: ErrorResponse = {
                "request_id": None,
                "errors": [
                    {
                        "error_source": "ShipStation",
                        "error_type": "validation",
                        "error_code": "field_value_required",
                        "message": "Either shipment_id or shipment must be provided.",
                    }
                ],
            }
            return (400, error_response)

        endpoint = f"{connection.v2_endpoint}/{Endpoints.RATES.value}"

        try:
            res = await connection.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                CalculateRatesResponse,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def estimate_rates(
        cls: type["RatesPortal"],
        connection: ShipStationConnection,
        from_country_code: str,
        from_postal_code: str,
        to_country_code: str,
        to_postal_code: str,
        weight: Weight,
        carrier_id: str | None = None,
        carrier_ids: List[str] | None = None,
        from_city_locality: str | None = None,
        from_state_province: str | None = None,
        to_city_locality: str | None = None,
        to_state_province: str | None = None,
        dimensions: Dimensions | None = None,
        confirmation: DeliveryConfirmationMethods | None = None,
        address_residential_indicator: Literal["unknown", "yes", "no"] = "unknown",
        ship_date: str | None = None,
    ) -> tuple[int, List[RateEstimate] | ErrorResponse]:
        """
        Get rate estimates without creating a full shipment.
        https://docs.shipstation.com/openapi/rates/estimate_rates

        This is useful for quick rate comparisons before creating shipments.

        Args:
            from_country_code: Origin country code (e.g., "US")
            from_postal_code: Origin postal code
            to_country_code: Destination country code
            to_postal_code: Destination postal code
            weight: Package weight
            carrier_id: Optional carrier ID to get estimates from
            carrier_ids: Optional list of carrier IDs to get estimates from
            from_city_locality: Optional origin city
            from_state_province: Optional origin state/province
            to_city_locality: Optional destination city
            to_state_province: Optional destination state/province
            dimensions: Optional package dimensions
            confirmation: Optional delivery confirmation type
            address_residential_indicator: Whether destination is residential
            ship_date: Optional ship date (ISO 8601)

        Returns:
            Tuple of status code and list of RateEstimate or ErrorResponse
        """
        payload_options = {
            "carrier_ids": carrier_ids,
            "from_country_code": from_country_code,
            "from_postal_code": from_postal_code,
            "to_country_code": to_country_code,
            "to_postal_code": to_postal_code,
            "weight": weight,
            "address_residential_indicator": address_residential_indicator,
            "from_city_locality": from_city_locality,
            "from_state_province": from_state_province,
            "to_city_locality": to_city_locality,
            "to_state_province": to_state_province,
            "dimensions": dimensions,
            "confirmation": confirmation,
            "ship_date": ship_date,
        }

        payload: RateEstimateOptions = cast(
            RateEstimateOptions,
            {k: v for k, v in payload_options.items() if v is not None},
        )

        endpoint = f"{connection.v2_endpoint}/{Endpoints.RATES.value}/estimate"

        try:
            res = await connection.request("POST", endpoint, json=payload)  # type: ignore[arg-type]

            return cls.validate_response(
                res,
                (200,),
                list,  # Returns an array of RateEstimate
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)

    @classmethod
    async def get_by_id(
        cls: type["RatesPortal"],
        connection: ShipStationConnection,
        rate_id: str,
    ) -> tuple[int, Rate | ErrorResponse]:
        """
        Retrieve a previously queried rate by its ID.
        https://docs.shipstation.com/openapi/rates/get_rate_by_id

        Args:
            rate_id: The rate ID to retrieve

        Returns:
            Tuple of status code and Rate or ErrorResponse
        """
        endpoint = f"{connection.v2_endpoint}/{Endpoints.RATES.value}/{rate_id}"

        try:
            res = await connection.request("GET", endpoint)

            return cls.validate_response(
                res,
                (200,),
                Rate,
            )

        except Exception as e:
            return cls.parse_unknown_exception(e)


__all__ = ["RatesPortal"]
