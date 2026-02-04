from asyncio import gather
from asyncio import run as asyncrun
from os import getenv
from typing import cast

from dotenv import load_dotenv

from AsyncShipStation import (
    BatchListResponse,
    BatchPortal,
    ErrorResponse,
    LabelPortal,
    OrderPortal,
    ShipStationClient,
    V1OrderListResponse,
)

load_dotenv()
V1_API_KEY: str | None = getenv("SHIP_STATION_V1")
V2_API_KEY: str | None = getenv("SHIP_STATION_V2")
V1_SECRET: str | None = getenv("SHIP_STATION_SECRET")


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

    async with ShipStationClient.scoped_client("v2") as _:
        bstatus, batches = await BatchPortal.list(sort_by="processed_at")

    async with ShipStationClient.scoped_client("v1") as _:
        ostatus, orderres = await OrderPortal.list(orderStatus="awaiting_shipment")

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

    orderlistres = cast(V1OrderListResponse, orderres)
    print(f"ORDERS\nTotal: {orderlistres['total']}\nPages: {orderlistres['pages']}")
    print(f"-------------\n{orderlistres['orders'][0]}")

    batchlistres = cast(BatchListResponse, batches)
    print(f"\nBATCHES\nTotal: {batchlistres['total']}\nPages: {batchlistres['pages']}")
    print(f"-------------\n{batchlistres['batches'][0]}")


if __name__ == "__main__":
    asyncrun(main())
