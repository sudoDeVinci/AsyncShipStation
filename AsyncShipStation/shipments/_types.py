from typing import Literal

from ..common import PaginatinatedResponse
from ..labels import LabelShipment

ShipmentStatuses = Literal["pending", "processing", "label_purchased", "cancelled"]


class Shipment(LabelShipment):
    shipment_id: str


class ShipmentListResponse(PaginatinatedResponse):
    shipments: list[Shipment]
