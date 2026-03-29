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
    DownloadPortal,
    ErrorResponse,
    LabelListResponse,
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

    ShipStationClient.configure(
        v2_key=V2_API_KEY, v1_key=V1_API_KEY, v1_secret=V1_SECRET
    )

    async with ShipStationClient.scoped_client("both") as _:
        bstat, batches = await BatchPortal.list(batch_number="100116", page_size=1)
        if bstat not in (200, 201):
            print(f"Error: {bstat} :: {batches}")
            return
        if not batches:
            print("No batches found")
            return
        with open(BATCHES_JSON, "w") as f:
            dump(batches, f, indent=4)

        batch = cast(BatchListResponse, batches)["batches"][0]
        batch_id = batch["batch_id"]

        lstat, labels = await LabelPortal.list(batch_id=batch_id)
        if lstat not in (200, 201):
            print(f"Error: {lstat} :: {labels}")
            return
        if not labels:
            print("No labels found")
            return
        with open(LABELS_JSON, "w") as f:
            dump(labels, f, indent=4)

        label = cast(LabelListResponse, labels)["labels"]

        dlstat, dl = await DownloadPortal.download_packing_slips(
            label,
        )
        if dlstat not in (200, 201):
            print(f"Error: {dlstat} :: {dl}")
            return
        if not dl:
            print("No label found")
            return
        with open(LABEL_PDF, "wb") as f:
            f.write(cast(bytes, dl))


if __name__ == "__main__":
    asyncrun(main())
