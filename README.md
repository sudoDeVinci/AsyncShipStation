# ShipStation Interaction / Automation
[![Type-Check](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/mypy.yml)
[![Linting](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/linting.yml)
[![Python 3.13.7](https://img.shields.io/badge/python-3.13.7-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Validation: Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

Simple API for ShipStation.

## Install

### pip

```bash
pip install AsyncShipStation
```

### Manual

```bash
git clone git@github.com:sudoDeVinci/AsyncShipStation.git
cd AsyncShipStation
pip install -r requirements.txt
```

## Setup 
Create a `.env` file to store your key.
```bash
API_KEY=your_api_key
```

## Client Lifecycle

The library uses a shared `httpx.AsyncClient` under the hood. You have two options for managing it:

### Option 1: Let it auto-start (simple)

The client starts automatically on first request. Just remember to close it when done:

```python
import asyncio
import os
from dotenv import load_dotenv
from AsyncShipStation import ShipStationClient, InventoryPortal

load_dotenv()
API_KEY: str | None = os.getenv("API_KEY")

async def main() -> None:
    ShipStationClient.configure(api_key=API_KEY)

    # Connection pool starts on first request
    status, warehouses = await InventoryPortal.list_warehouses(page_size=10)
    print(f"Status: {status}, Warehouses: {warehouses}")
    
    ...

    # Clean up when done
    await ShipStationClient.close()


if __name__ == "__main__":
    asyncio.run(main())
```

### Option 2: Use the async context manager (recommended)
Scoped usage where you want automatic cleanup:

```python
import asyncio
import os
from dotenv import load_dotenv
from AsyncShipStation import ShipStationClient, InventoryPortal

load_dotenv()
API_KEY: str | None = os.getenv("API_KEY")

async def main() -> None:
    ShipStationClient.configure(api_key=API_KEY)

    async with InventoryPortal.scoped_client() as _:
        status, warehouses = await InventoryPortal.list_warehouses(page_size=10)
        print(f"Status: {status}, Warehouses: {warehouses}")
        
        ...
     
        # Client closes automatically when exiting the context

if __name__ == "__main__":
    asyncio.run(main())

```

## Concurrent Requests

The client uses connection pooling, so concurrent requests share connections efficiently:

```python
import asyncio
from AsyncShipStation import (
    BatchPortal,
    InventoryPortal,
    LabelPortal,
    ShipStationClient,
)

        ...

ShipStationClient.configure(api_key=API_KEY)
async with ShipStationClient.scoped_client() as _:
    results = await asyncio.gather(
        InventoryPortal.list_warehouses(),
        InventoryPortal.list(),
        BatchPortal.list(),
        LabelPortal.list(),
    )

for status, data in results:
    if status in (200, 207, 201):
        print(f"Success :: {data}")
    else:
        print(f"Error :: {data}")
    
        ...

```


## Rate Limiting
Accounts that send too many requests in quick succession will receive a 429 Too Many Requests error response and include a Retry-After header with the number of seconds to wait for. By default we get 200 requests per minute.
ShipStation has bulk op endpoints. These only count as a single request.

## Endpoints
[/batches](/batches/_types.py)
Process labels in bulk and receive a large number of labels and customs forms in bulk responses. Batching is ideal for workflows that need to process hundreds or thousands of labels quickly.
200

[/carriers](/carriers/_types.py)
Retreive useful details about the carriers connected to your accounts, including carrier IDs, service IDs, advanced options, and available carrier package types.

[/fulfillments](/fulfillments/_types.py)
Manage fulfillments which represent completed shipments. Create fulfillments to mark orders as shipped with tracking information and notify customers and marketplaces.

[/inventory](/inventory/_types.py)
Manage inventory, adjust quantities, and handle warehouses and locations.
  - [/inventory_warehouses](/inventory._types.py)
  - [/inventory_locations](/inventory._types.py)

[/labels](/labels/_types.py)
Purchase and print shipping labels for any carrier active on your account. The labels endpoint also supports creating return labels, voiding labels, and getting label details like tracking.

[/manifests](/manifests/_types.py)
A manifest is a document that provides a list of the day's shipments. It typically contains a barcode that allows the pickup driver to scan a single document to register all shipments, rather than scanning each shipment individually.
