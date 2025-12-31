import asyncio
import os

from dotenv import load_dotenv

from AsyncShipStation.common import ShipStationClient
from AsyncShipStation.inventory import InventoryPortal

load_dotenv()
API_KEY: str | None = os.getenv("API_KEY")


async def main() -> None:
    if API_KEY is None:
        raise ValueError("API_KEY environment variable not set")

    ShipStationClient.configure(api_key=API_KEY)

    async with InventoryPortal.scoped_client() as _:
        status, warehouses = await InventoryPortal.list_warehouses(page_size=10)
        print(f"Status: {status}, Warehouses: {warehouses}")
        # You can add more calls to other methods here for testing


if __name__ == "__main__":
    asyncio.run(main())
