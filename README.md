# ShipStation Interaction / Automation
[![Type-Check](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/mypy.yml)
[![Linting](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/linting.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Validation: Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

Async Python client for ShipStation V1 and V2 APIs with full type hints.

## Features

- **Full V1 & V2 API Support**: Works with both ShipStation API versions
- **Async/Await**: Built on `httpx` for efficient async HTTP requests
- **Type Safety**: Complete TypedDict definitions for all request/response types
- **Connection Pooling**: Efficient connection reuse for concurrent requests
- **Portal Pattern**: Clean, organized API with dedicated portals for each resource

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
Create a `.env` file to store your keys. The library supports both V1 and V2 APIs:

```bash
# V2 API Key (recommended for most operations)
SHIP_STATION_V2=your_v2_api_key

# V1 API Key and Secret (required for orders endpoint)
SHIP_STATION_V1=your_v1_api_key
SHIP_STATION_SECRET=your_v1_secret
```

### Configuring the Client

```python
from AsyncShipStation import ShipStationClient

# Configure with both V1 and V2 credentials
ShipStationClient.configure(
    v2_key="your_v2_api_key",
    v1_key="your_v1_api_key",
    v1_secret="your_v1_secret",
)
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

[/rates](/rates/_types.py) *(V2)*
Calculate and estimate shipping rates across multiple carriers. Supports both full rate calculation with shipment details and quick rate estimates.

[/shipments](/shipments/_types.py) *(V2)*
Create, retrieve, and manage shipments. Includes support for getting rates, adding/removing tags, and cancellation.

[/tags](/tags/_types.py) *(V2)*
Manage tags for organizing shipments and orders. Create, list, and delete tags.

[/warehouses](/warehouses/_types.py) *(V2)*
Retrieve warehouse information including origin addresses for shipments.

## Workflow Automation Demo

The library includes a workflow demonstration script (`workflow_demo.py`) that shows how to automate the order-to-label process:

1. **Fetch orders** from the V1 API
2. **Group orders by carrier** for efficient batch processing
3. **Create shipments** in the V2 API
4. **Estimate rates** across carriers
5. **Create batches** for bulk label processing

### Running the Demo

```bash
# Ensure your .env file is configured with API keys
python workflow_demo.py
```

### Safety Features

The workflow script includes multiple safety features:

- **DRY-RUN mode** (default): Only simulates operations, no actual API modifications
- **SIMULATE mode**: Prints what would happen without making any API calls
- **LIVE mode**: Actually executes operations (requires explicit confirmation)
- **test_label flag**: Use test labels to avoid charges during development
- **Rate confirmation**: Pause before purchasing labels for human review

```python
from workflow_demo import WorkflowConfig, ExecuteMode

config = WorkflowConfig(
    execute_mode=ExecuteMode.DRY_RUN,  # Safe default
    use_test_labels=True,               # Use test labels when purchasing
    require_rate_confirmation=True,     # Pause for confirmation
    max_orders_to_process=10,           # Limit orders for safety
)
```

### Production Checklist

Before running in LIVE mode against production:

- [ ] Test with a ShipStation sandbox/test account first
- [ ] Always use `test_label=True` for initial label purchases
- [ ] Set `max_orders_to_process` to a small number initially
- [ ] Review rate estimates before confirming purchases
- [ ] Implement proper error handling and logging
- [ ] Set up monitoring for API rate limits (200 requests/minute)

## V2 API Portals

### RatesPortal

```python
from AsyncShipStation import RatesPortal, ShipStationClient

async with ShipStationClient.scoped_client("v2"):
    # Calculate rates for an existing shipment
    status, rates = await RatesPortal.calculate_rates(
        carrier_ids=["se-123456"],
        shipment_id="se-shipment-id",
    )
    
    # Quick rate estimate without creating a shipment
    status, estimates = await RatesPortal.estimate_rates(
        carrier_ids=["se-123456", "se-789012"],
        from_country_code="US",
        from_postal_code="78701",
        to_country_code="US",
        to_postal_code="90210",
        weight={"value": 1.5, "unit": "pound"},
    )
```

### TagsPortal

```python
from AsyncShipStation import TagsPortal

async with ShipStationClient.scoped_client("v2"):
    # List all tags
    status, tags = await TagsPortal.list()
    
    # Create a new tag
    status, tag = await TagsPortal.create("Priority", color="red")
    
    # Delete a tag
    status, _ = await TagsPortal.delete("Priority")
```

### WarehousePortal

```python
from AsyncShipStation import WarehousePortal

async with ShipStationClient.scoped_client("v2"):
    # List warehouses
    status, warehouses = await WarehousePortal.list()
    
    # Get specific warehouse
    status, warehouse = await WarehousePortal.get_by_id("wh-123456")
```

### ShipmentPortal (Extended)

```python
from AsyncShipStation import ShipmentPortal

async with ShipStationClient.scoped_client("v2"):
    # Create shipments
    status, result = await ShipmentPortal.create([
        {
            "carrier_id": "se-123456",
            "service_code": "usps_priority_mail",
            "ship_to": {...},
            "ship_from": {...},
            "packages": [...],
        }
    ])
    
    # Get rates for a shipment
    status, rates = await ShipmentPortal.get_rates("se-shipment-id")
    
    # Add/remove tags
    await ShipmentPortal.add_tag("se-shipment-id", "Priority")
    await ShipmentPortal.remove_tag("se-shipment-id", "Priority")
    
    # Cancel a shipment (before label purchase)
    await ShipmentPortal.cancel_by_id("se-shipment-id")
```
