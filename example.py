from asyncio import gather
from asyncio import run as asyncrun
from json import dumps
from os import getenv
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from AsyncShipStation import (
    BatchListResponse,
    BatchPortal,
    DownloadPortal,
    LabelListResponse,
    LabelPortal,
    ShipmentListResponse,
    ShipmentPortal,
    ShipStationClient,
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
BATCHES_JSON: Path = TEST / "batches.json"
LABELS_JSON: Path = TEST / "labels.json"
LABEL_PDF: Path = TEST / "label.pdf"


async def main() -> None:
    if not V1_API_KEY:
        raise ValueError("SHIP_STATION_V2 environment variable not set")
    if not V2_API_KEY:
        raise ValueError("SHIP_STATION_V1 environment variable not set")
    if not V1_SECRET:
        raise ValueError("SHIP_STATION_SECRET environment variable not set")

    connection = await ShipStationClient.configure(
        v2_key=V2_API_KEY, v1_key=V1_API_KEY, v1_secret=V1_SECRET
    )

    async with ShipStationClient.scoped_client(
        connection_hash=hash(connection), version="v2"
    ) as _:
        stat, shipments = await ShipmentPortal.list(connection, page_size=10, page=1)

    with open(SS_ORDER_JSON, "w") as f:
        f.write(dumps(shipments, indent=4))


if __name__ == "__main__":
    asyncrun(main())
