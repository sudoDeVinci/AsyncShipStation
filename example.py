import asyncio
import os

from dotenv import load_dotenv

from AsyncShipStation import (
    BatchPortal,
    InventoryPortal,
    LabelPortal,
    ProductPortal,
    ShipmentPortal,
    ShipStationClient,
)

load_dotenv()
API_KEY: str | None = os.getenv("API_KEY")


async def main() -> None:
    if API_KEY is None:
        raise ValueError("API_KEY environment variable not set")

    ShipStationClient.configure(api_key=API_KEY)
    async with ShipStationClient.scoped_client() as _:
        results = await asyncio.gather(
            InventoryPortal.list_warehouses(),
            InventoryPortal.list(),
            BatchPortal.list(),
            LabelPortal.list(),
            ProductPortal.list(),
            ShipmentPortal.list(),
        )

    for status, data in results:
        if status in (200, 207, 201):
            print(f"Success :: {data}")
        else:
            print(f"Error :: {data}")


if __name__ == "__main__":
    asyncio.run(main())
