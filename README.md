# ShipStation Interaction / Automation
[![Type-Check](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/mypy.yml)
[![Linting](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/linting.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Validation: Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![Python 3.11.14](https://img.shields.io/badge/python-3.11.14-blue.svg)](https://www.python.org/downloads/)
![PyPI - Version](https://img.shields.io/pypi/v/AsyncShipStation)
![PyPI - License](https://img.shields.io/pypi/l/AsyncShipStation)

Async Python client for ShipStation v1 and v2 APIs with an emphasis on typing.

## Install

### pip

~~~bash
pip install AsyncShipStation
~~~

### Manual

~~~bash
git clone git@github.com:sudoDeVinci/AsyncShipStation.git
cd AsyncShipStation
pip install -r requirements.txt
~~~

## Quick Start

Create a connection, then pass it to the portal you want to use.

~~~python
import asyncio

from AsyncShipStation import ShipStationClient, ShipmentPortal


async def main() -> None:
    connection = await ShipStationClient.configure(
        v2_key="your_v2_api_key",
        v1_key="your_v1_api_key",
        v1_secret="your_v1_secret",
    )

    async with ShipStationClient.scoped_client(connection=connection, version="v2"):
        status, shipments = await ShipmentPortal.list(
            connection,
            page_size=10,
            page=1,
        )
        print(status, shipments)


if __name__ == "__main__":
    asyncio.run(main())
~~~

## Client Lifecycle

### Use the async context manager

Use `scoped_client()` when you want the connection lifecycle handled for you.

~~~python
import asyncio
import os

from dotenv import load_dotenv

from AsyncShipStation import ShipStationClient, ShipmentPortal

load_dotenv()
V2_API_KEY: str | None = os.getenv("SHIP_STATION_V2")
V1_API_KEY: str | None = os.getenv("SHIP_STATION_V1")
V1_SECRET: str | None = os.getenv("SHIP_STATION_SECRET")


async def main() -> None:
    connection = await ShipStationClient.configure(
        v2_key=V2_API_KEY or "",
        v1_key=V1_API_KEY,
        v1_secret=V1_SECRET,
    )

    async with ShipStationClient.scoped_client(connection=connection, version="v2"):
        status, shipments = await ShipmentPortal.list(connection, page_size=10, page=1)
        print(status, shipments)


if __name__ == "__main__":
    asyncio.run(main())
~~~

### Start and close explicitly

Use `start()` and `close()` if you want to manage the lifecycle yourself.

~~~python
import asyncio
import os

from dotenv import load_dotenv

from AsyncShipStation import ShipStationClient, ShipmentPortal

load_dotenv()
V2_API_KEY: str | None = os.getenv("SHIP_STATION_V2")
V1_API_KEY: str | None = os.getenv("SHIP_STATION_V1")
V1_SECRET: str | None = os.getenv("SHIP_STATION_SECRET")


async def main() -> None:
    connection = await ShipStationClient.configure(
        v2_key=V2_API_KEY or "",
        v1_key=V1_API_KEY,
        v1_secret=V1_SECRET,
    )

    await ShipStationClient.start(connection=connection, version="v2")
    try:
        status, shipments = await ShipmentPortal.list(connection, page_size=10, page=1)
        print(status, shipments)
    finally:
        await ShipStationClient.close(connection=connection, version="v2")


if __name__ == "__main__":
    asyncio.run(main())
~~~

## Concurrent Requests

A single connection can be shared across concurrent requests.

~~~python
import asyncio

from AsyncShipStation import (
    BatchPortal,
    LabelPortal,
    ShipmentPortal,
    ShipStationClient,
)


async def main() -> None:
    connection = await ShipStationClient.configure(
        v2_key="your_v2_api_key",
        v1_key="your_v1_api_key",
        v1_secret="your_v1_secret",
    )

    async with ShipStationClient.scoped_client(connection=connection, version="v2"):
        results = await asyncio.gather(
            ShipmentPortal.list(connection, page_size=10, page=1),
            BatchPortal.list(connection, page_size=10, page=1),
            LabelPortal.list(connection, page_size=10, page=1),
        )

    for status, data in results:
        if status in (200, 201, 207):
            print(f"Success :: {data}")
        else:
            print(f"Error :: {data}")


if __name__ == "__main__":
    asyncio.run(main())
~~~

## Connection Lookup

If you need to retrieve a connection from the pool later, use `connection.pool_key`.

~~~python
import asyncio

from AsyncShipStation import ShipStationClient, ShipmentPortal


async def main() -> None:
    connection = await ShipStationClient.configure(
        v2_key="your_v2_api_key",
        v1_key="your_v1_api_key",
        v1_secret="your_v1_secret",
    )

    async with ShipStationClient.scoped_client(
        connection_hash=connection.pool_key,
        version="v2",
    ) as scoped_connection:
        status, shipments = await ShipmentPortal.list(
            scoped_connection,
            page_size=10,
            page=1,
        )
        print(status, shipments)


if __name__ == "__main__":
    asyncio.run(main())
~~~

## Rate Limiting

Accounts that send too many requests in quick succession will receive a `429 Too Many Requests` response with a `Retry-After` header that tells you how long to wait.

ShipStation bulk operation endpoints count as a single request.

## Endpoints

[/batches](/batches/_types.py)  
Process labels in bulk and receive labels and customs forms in bulk responses.

[/carriers](/carriers/_types.py)  
Retrieve details about the carriers connected to your account, including carrier IDs, service IDs, advanced options, and package types.

[/fulfillments](/fulfillments/_types.py)  
Manage fulfillments that represent completed shipments.

[/inventory](/inventory/_types.py)  
Manage inventory, adjust quantities, and work with warehouses and locations.  
- [/inventory_warehouses](/inventory._types.py)  
- [/inventory_locations](/inventory._types.py)

[/labels](/labels/_types.py)  
Purchase and print shipping labels, create return labels, void labels, and retrieve label details.

[/manifests](/manifests/_types.py)  
Retrieve and work with shipment manifests.

[/rates](/rates/_types.py) *(v2)*  
Calculate and estimate shipping rates across multiple carriers.

[/shipments](/shipments/_types.py) *(v2)*  
Create, retrieve, and manage shipments.

[/tags](/tags/_types.py) *(v2)*  
Manage tags for organizing shipments and orders.

[/warehouses](/warehouses/_types.py) *(v2)*  
Retrieve warehouse information, including shipment origin addresses.
