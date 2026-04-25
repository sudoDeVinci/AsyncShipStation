from ..common import Address, Taggable

class Warehouse(Taggable):
    "A warehouse location for shipment origins."

    warehouse_id: str
    is_default: bool | None
    name: str
    created_at: str
    origin_address: Address
    return_address: Address

class WarehouseListResponse(Taggable):
    "Response from listing warehouses."

    warehouses: list[Warehouse]
