import asyncio
import os

from dotenv import load_dotenv

from AsyncShipStation import (
    BatchPortal,
    ErrorResponse,
    InventoryPortal,
    LabelPortal,
    OrderPortal,
    ProductPortal,
    ShipmentPortal,
    ShipStationClient,
)

load_dotenv()
V1_API_KEY: str | None = os.getenv("SHIP_STATION_V1")
V2_API_KEY: str | None = os.getenv("SHIP_STATION_V2")
V1_SECRET: str | None = os.getenv("SHIP_STATION_SECRET")


async def main() -> None:
    if not V1_API_KEY:
        raise ValueError("SHIP_STATION_V2 environment variable not set")
    if not V2_API_KEY:
        raise ValueError("SHIP_STATION_V1 environment variable not set")
    if not V1_SECRET:
        raise ValueError("SHIP_STATION_SECRET environment variable not set")

    results: list[tuple[int, ErrorResponse | object]] = []

    ShipStationClient.configure(
        v2_key=V2_API_KEY, v1_key=V1_API_KEY, v1_secret=V1_SECRET
    )

    async with ShipStationClient.scoped_client("v2") as _:
        results.extend(
            await asyncio.gather(
                InventoryPortal.list_warehouses(),
                InventoryPortal.list(),
                BatchPortal.list(),
                LabelPortal.list(),
                ProductPortal.list(),
                ShipmentPortal.list(),
            )
        )

    async with ShipStationClient.scoped_client("v1") as _:
        results.extend(
            await asyncio.gather(
                OrderPortal.list(),
            )
        )

    for status, data in results:
        if status in (200, 207, 201):
            print(f"Success :: {status} :: {str(data)[:100]} ...")
        else:
            print(f"Error :: {status} :: {str(data)[:100]} ...")


if __name__ == "__main__":
    asyncio.run(main())
