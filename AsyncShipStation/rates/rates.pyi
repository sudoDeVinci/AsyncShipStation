from typing import List, Literal, cast
from ..common import DeliveryConfirmationMethods, Dimensions, Endpoints, ErrorResponse, ShipStationClient, ShipStationConnection, Tag, Weight
from ..shipments import Shipment
from ._types import CalculateRatesRequest, CalculateRatesResponse, Rate, RateEstimate, RateEstimateOptions, RateRequestOptions

class RatesPortal(ShipStationClient):
    'Portal for interacting with the ShipStation Rates API (V2).'

    @classmethod
    async def calculate_rates(cls: type['RatesPortal'], connection: ShipStationConnection, carrier_ids: List[str], shipment_id: str | None = None, shipment: Shipment | None = None, package_types: List[str] | None = None, service_codes: List[str] | None = None, calculate_tax_amount: bool = False, preferred_currency: str | None = None, is_return: bool = False) -> tuple[int, CalculateRatesResponse | ErrorResponse]: ...

    @classmethod
    async def estimate_rates(cls: type['RatesPortal'], connection: ShipStationConnection, from_country_code: str, from_postal_code: str, to_country_code: str, to_postal_code: str, weight: Weight, carrier_id: str | None = None, carrier_ids: List[str] | None = None, from_city_locality: str | None = None, from_state_province: str | None = None, to_city_locality: str | None = None, to_state_province: str | None = None, dimensions: Dimensions | None = None, confirmation: DeliveryConfirmationMethods | None = None, address_residential_indicator: Literal['unknown', 'yes', 'no'] = 'unknown', ship_date: str | None = None) -> tuple[int, List[RateEstimate] | ErrorResponse]: ...

    @classmethod
    async def get_by_id(cls: type['RatesPortal'], connection: ShipStationConnection, rate_id: str) -> tuple[int, Rate | ErrorResponse]: ...

__all__ = ['RatesPortal']
