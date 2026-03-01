from asyncio import gather
from asyncio import run as asyncrun
from json import dump
from os import getenv
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from AsyncShipStation import (
    BatchListResponse,
    BatchPortal,
    CarrierPortal,
    ErrorResponse,
    LabelPortal,
    OrderPortal,
    ShipStationClient,
    V1OrderListResponse,
    V1Warehouse,
    V1WarehousePortal,
    WarehousePortal,
)

load_dotenv()
V1_API_KEY: str | None = getenv("SHIP_STATION_V1")
V2_API_KEY: str | None = getenv("SHIP_STATION_V2")
V1_SECRET: str | None = getenv("SHIP_STATION_SECRET")

CWD: Path = Path(__file__).parent.resolve()
TEST: Path = CWD / "__cache__"
TEST.mkdir(exist_ok=True)
SS_ORDER_JSON: Path = TEST / "ss_order.json"
HYGP_ORDER_JSON: Path = TEST / "hygp_order.json"
FONT_GROUPINGS: Path = TEST / "font_groupings.json"
CARRIER_JSON: Path = TEST / "carriers.json"
RECIPIENTS_JSON: Path = TEST / "recipients.json"
WAREHOUSES_JSON: Path = TEST / "warehouses.json"
V1_WAREHOUSES_JSON: Path = TEST / "v1_warehouses.json"


async def main() -> None:
    if not V1_API_KEY:
        raise ValueError("SHIP_STATION_V2 environment variable not set")
    if not V2_API_KEY:
        raise ValueError("SHIP_STATION_V1 environment variable not set")
    if not V1_SECRET:
        raise ValueError("SHIP_STATION_SECRET environment variable not set")

    ShipStationClient.configure(
        v2_key=V2_API_KEY, v1_key=V1_API_KEY, v1_secret=V1_SECRET
    )

    async with ShipStationClient.scoped_client("both") as _:
        bstatus, batches = await BatchPortal.list(sort_by="processed_at")
        cstatus, carriers = await CarrierPortal.get_by_id("se-564137")
        wstatus, warehouses = await WarehousePortal.get_by_name(
            "HYGP World Headquarters"
        )

        ostatus, orderres = await OrderPortal.list(orderStatus="awaiting_shipment")
        wstatus, v1_warehouses = await V1WarehousePortal.get_by_name(
            "HYGP World Headquarters"
        )

    if bstatus not in (200, 201):
        print(f"Error: {bstatus} :: {batches}")
        return

    if ostatus not in (200, 201):
        print(f"Error: {ostatus} :: {orderres}")
        return

    if not batches:
        print("No batches found")
        return

    if not orderres:
        print("No orders found")
        return

    with open(CARRIER_JSON, "w") as f:
        dump(carriers, f, indent=4)

    with open(WAREHOUSES_JSON, "w") as f:
        dump(warehouses, f, indent=4)

    with open(V1_WAREHOUSES_JSON, "w") as f:
        dump(v1_warehouses, f, indent=4)


if __name__ == "__main__":
    asyncrun(main())
