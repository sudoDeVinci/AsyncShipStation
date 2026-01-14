from asyncio import gather
from asyncio import run as asyncrun
from os import getenv

from dotenv import load_dotenv

from AsyncShipStation import (
    BatchPortal,
    ErrorResponse,
    LabelPortal,
    OrderPortal,
    ShipStationClient,
)

load_dotenv()
V1_API_KEY: str | None = getenv("SHIP_STATION_V1")
V2_API_KEY: str | None = getenv("SHIP_STATION_V2")
V1_SECRET: str | None = getenv("SHIP_STATION_SECRET")


async def main():
    if not V1_API_KEY:
        raise ValueError("SHIP_STATION_V2 environment variable not set")
    if not V2_API_KEY:
        raise ValueError("SHIP_STATION_V1 environment variable not set")
    if not V1_SECRET:
        raise ValueError("SHIP_STATION_SECRET environment variable not set")

    ShipStationClient.configure(
        v2_key=V2_API_KEY, v1_key=V1_API_KEY, v1_secret=V1_SECRET
    )


if __name__ == "__main__":
    asyncrun(main())
