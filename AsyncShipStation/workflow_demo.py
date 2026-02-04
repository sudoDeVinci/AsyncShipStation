"""
Workflow Demonstration Script for ShipStation V2 API

This script demonstrates the order-to-label automation workflow:
1. Fetch orders (from V1 API)
2. Group orders by carrier
3. Create shipments and estimate rates
4. Create batches for each carrier
5. (Optionally) Process labels

SAFETY: By default, this script runs in DRY-RUN mode and will NOT:
- Create actual shipments
- Purchase labels
- Modify any data in your ShipStation account

To enable live operations, set EXECUTE_MODE to "live" and provide explicit confirmation.
"""

import asyncio
import os
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, no_type_check

from dotenv import load_dotenv

from AsyncShipStation import (
    BatchPortal,
    CarrierPortal,
    OrderPortal,
    RatesPortal,
    ShipmentPortal,
    ShipStationClient,
    TagsPortal,
    V1Order,
    WarehousePortal,
)


class ExecuteMode(Enum):
    """Execution mode for the workflow."""

    SIMULATE = "simulate"  # Only print what would happen, no API calls
    DRY_RUN = "dry_run"  # Make read-only API calls, but no modifications
    LIVE = "live"  # Actually execute all operations (DANGEROUS)


@dataclass
class WorkflowConfig:
    """Configuration for the workflow."""

    execute_mode: ExecuteMode = ExecuteMode.DRY_RUN
    use_test_labels: bool = True  # Use test_label flag when purchasing
    require_rate_confirmation: bool = True  # Pause for confirmation before purchasing
    max_orders_to_process: int = 10  # Limit orders for safety
    default_carrier_id: str | None = None  # Optional default carrier
    verbose: bool = True


@dataclass
class ShipmentPayload:
    """Represents a shipment to be created."""

    order_id: str
    order_number: str
    carrier_id: str | None
    service_code: str | None
    ship_to: dict[str, Any]
    ship_from: dict[str, Any]
    packages: list[dict[str, Any]]
    weight: dict[str, Any]
    order_data: V1Order


@dataclass
class WorkflowResult:
    """Results from running the workflow."""

    orders_fetched: int = 0
    orders_by_carrier: dict[str, list[str]] = field(default_factory=dict)
    shipments_created: list[str] = field(default_factory=list)
    batches_created: list[str] = field(default_factory=list)
    labels_purchased: int = 0
    errors: list[str] = field(default_factory=list)
    dry_run: bool = True


@no_type_check
def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


@no_type_check
def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"  WARNING: {message}")


@no_type_check
def print_success(message: str) -> None:
    """Print a success message."""
    print(f" {message}")


@no_type_check
def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ️  {message}")


@no_type_check
def print_error(message: str) -> None:
    """Print an error message."""
    print(f"❌ {message}")


@no_type_check
async def fetch_carriers(config: WorkflowConfig) -> dict[str, str]:
    """Fetch available carriers and return a mapping of carrier_id -> carrier_name."""
    carriers: dict[str, str] = {}

    if config.execute_mode == ExecuteMode.SIMULATE:
        print_info("SIMULATE: Would fetch carriers from API")
        return {"se-123456": "UPS", "se-789012": "FedEx", "se-345678": "USPS"}

    status, response = await CarrierPortal.list_carriers()

    if status != 200:
        print_error(f"Failed to fetch carriers: {response}")
        return carriers

    for carrier in response.get("carriers", []):
        carrier_id = carrier.get("carrier_id", "")
        carrier_name = carrier.get("friendly_name", carrier.get("name", "Unknown"))
        carriers[carrier_id] = carrier_name

    print_success(f"Fetched {len(carriers)} carriers")
    return carriers


@no_type_check
async def fetch_warehouses(config: WorkflowConfig) -> list[dict[str, Any]]:
    """Fetch available warehouses."""
    if config.execute_mode == ExecuteMode.SIMULATE:
        print_info("SIMULATE: Would fetch warehouses from API")
        return [
            {
                "warehouse_id": "wh-123",
                "name": "Main Warehouse",
                "origin_address": {"city_locality": "Austin", "state_province": "TX"},
            }
        ]

    status, response = await WarehousePortal.list()

    if status != 200:
        print_error(f"Failed to fetch warehouses: {response}")
        return []

    warehouses = response.get("warehouses", [])
    print_success(f"Fetched {len(warehouses)} warehouses")
    return warehouses


@no_type_check
async def fetch_tags(config: WorkflowConfig) -> list[dict[str, Any]]:
    """Fetch available tags."""
    if config.execute_mode == ExecuteMode.SIMULATE:
        print_info("SIMULATE: Would fetch tags from API")
        return [{"tag_id": 1, "name": "Priority", "color": "red"}]

    status, response = await TagsPortal.list()

    if status != 200:
        print_error(f"Failed to fetch tags: {response}")
        return []

    tags = response.get("tags", [])
    print_success(f"Fetched {len(tags)} tags")
    return tags


@no_type_check
async def fetch_orders(
    config: WorkflowConfig,
    order_status: str = "awaiting_shipment",
) -> list[V1Order]:
    """Fetch orders that need to be shipped."""
    if config.execute_mode == ExecuteMode.SIMULATE:
        print_info(f"SIMULATE: Would fetch orders with status '{order_status}'")
        # Return mock orders for simulation
        return [
            {
                "orderId": 12345,
                "orderNumber": "ORDER-001",
                "orderStatus": "awaiting_shipment",
                "carrierCode": "ups",
                "serviceCode": "ups_ground",
                "shipTo": {
                    "name": "John Doe",
                    "street1": "123 Main St",
                    "city": "Austin",
                    "state": "TX",
                    "postalCode": "78701",
                    "country": "US",
                },
                "weight": {"value": 1.5, "units": "pounds"},
                "items": [],
            },
            {
                "orderId": 12346,
                "orderNumber": "ORDER-002",
                "orderStatus": "awaiting_shipment",
                "carrierCode": "fedex",
                "serviceCode": "fedex_ground",
                "shipTo": {
                    "name": "Jane Smith",
                    "street1": "456 Oak Ave",
                    "city": "Dallas",
                    "state": "TX",
                    "postalCode": "75201",
                    "country": "US",
                },
                "weight": {"value": 2.0, "units": "pounds"},
                "items": [],
            },
        ]

    status, response = await OrderPortal.list(
        orderStatus=order_status,
        pageSize=config.max_orders_to_process,
    )

    if status != 200:
        print_error(f"Failed to fetch orders: {response}")
        return []

    orders = response.get("orders", [])
    print_success(f"Fetched {len(orders)} orders with status '{order_status}'")
    return orders


@no_type_check
def group_orders_by_carrier(
    orders: list[V1Order],
    carriers: dict[str, str],
    config: WorkflowConfig,
) -> dict[str, list[V1Order]]:
    """Group orders by their carrier code."""
    grouped: dict[str, list[V1Order]] = defaultdict(list)

    for order in orders:
        carrier_code = order.get("carrierCode") or "unknown"
        grouped[carrier_code].append(order)

    if config.verbose:
        print_section("Orders Grouped by Carrier")
        for carrier_code, carrier_orders in grouped.items():
            order_numbers = [o.get("orderNumber", "?") for o in carrier_orders]
            print(f"  {carrier_code}: {len(carrier_orders)} orders - {order_numbers}")

    return grouped


@no_type_check
def build_shipment_payload(
    order: V1Order,
    warehouse: dict[str, Any] | None = None,
) -> ShipmentPayload:
    """Build a shipment payload from an order."""
    ship_to_raw = order.get("shipTo", {})

    # Convert V1 address format to V2 format
    ship_to = {
        "name": ship_to_raw.get("name", ""),
        "address_line1": ship_to_raw.get("street1", ""),
        "address_line2": ship_to_raw.get("street2"),
        "city_locality": ship_to_raw.get("city", ""),
        "state_province": ship_to_raw.get("state", ""),
        "postal_code": ship_to_raw.get("postalCode", ""),
        "country_code": ship_to_raw.get("country", "US"),
        "phone": ship_to_raw.get("phone"),
    }

    # Use warehouse address as ship_from if available
    if warehouse:
        origin = warehouse.get("origin_address", {})
        ship_from = {
            "name": warehouse.get("name", ""),
            "address_line1": origin.get("address_line1", ""),
            "city_locality": origin.get("city_locality", ""),
            "state_province": origin.get("state_province", ""),
            "postal_code": origin.get("postal_code", ""),
            "country_code": origin.get("country_code", "US"),
        }
    else:
        ship_from = {}

    weight_raw = order.get("weight", {})
    weight = {
        "value": weight_raw.get("value", 1.0),
        "unit": "pound" if weight_raw.get("units") == "pounds" else "ounce",
    }

    packages = [
        {
            "weight": weight,
            "dimensions": order.get("dimensions"),
        }
    ]

    return ShipmentPayload(
        order_id=str(order.get("orderId", "")),
        order_number=str(order.get("orderNumber", "")),
        carrier_id=order.get("carrierCode"),
        service_code=order.get("serviceCode"),
        ship_to=ship_to,
        ship_from=ship_from,
        packages=packages,
        weight=weight,
        order_data=order,
    )


@no_type_check
async def estimate_rates_for_shipment(
    payload: ShipmentPayload,
    carrier_ids: list[str],
    config: WorkflowConfig,
) -> list[dict[str, Any]]:
    """Get rate estimates for a shipment payload."""
    if config.execute_mode == ExecuteMode.SIMULATE:
        print_info(f"SIMULATE: Would estimate rates for order {payload.order_number}")
        return [
            {
                "carrier_id": "se-123456",
                "service_code": "ups_ground",
                "shipping_amount": {"amount": "8.50", "currency": "usd"},
                "delivery_days": 5,
            }
        ]

    # Use the rates estimate endpoint
    status, response = await RatesPortal.estimate_rates(
        carrier_ids=carrier_ids,
        from_country_code=payload.ship_from.get("country_code", "US"),
        from_postal_code=payload.ship_from.get("postal_code", ""),
        to_country_code=payload.ship_to.get("country_code", "US"),
        to_postal_code=payload.ship_to.get("postal_code", ""),
        weight=payload.weight,
    )

    if status != 200:
        print_error(f"Failed to estimate rates for {payload.order_number}: {response}")
        return []

    return response


@no_type_check
async def create_shipment(
    payload: ShipmentPayload,
    config: WorkflowConfig,
) -> str | None:
    """Create a shipment from a payload. Returns shipment_id if successful."""
    if config.execute_mode != ExecuteMode.LIVE:
        print_info(f"DRY-RUN: Would create shipment for order {payload.order_number}")
        if config.verbose:
            print(
                f"    Ship to: {payload.ship_to.get('name')} - "
                f"{payload.ship_to.get('city_locality')}, "
                f"{payload.ship_to.get('state_province')}"
            )
            print(f"    Carrier: {payload.carrier_id}, Service: {payload.service_code}")
            print(f"    Weight: {payload.weight}")
        return f"simulated-shipment-{payload.order_number}"

    # Build the shipment creation request
    shipment_request = {
        "external_shipment_id": payload.order_number,
        "carrier_id": payload.carrier_id,
        "service_code": payload.service_code,
        "ship_to": payload.ship_to,
        "ship_from": payload.ship_from,
        "packages": payload.packages,
    }

    status, response = await ShipmentPortal.create([shipment_request])

    if status not in (200, 201, 207):
        print_error(f"Failed to create shipment for {payload.order_number}: {response}")
        return None

    # Extract shipment ID from response
    shipments = response.get("shipments", [])
    if shipments:
        shipment_id = shipments[0].get("shipment_id")
        print_success(
            f"Created shipment {shipment_id} for order {payload.order_number}"
        )
        return shipment_id

    return None


@no_type_check
async def create_batch_for_carrier(
    carrier_code: str,
    shipment_ids: list[str],
    config: WorkflowConfig,
) -> str | None:
    """Create a batch for a set of shipments. Returns batch_id if successful."""
    if config.execute_mode != ExecuteMode.LIVE:
        print_info(
            f"DRY-RUN: Would create batch for carrier '{carrier_code}' "
            f"with {len(shipment_ids)} shipments"
        )
        return f"simulated-batch-{carrier_code}"

    external_batch_id = f"batch-{carrier_code}-auto"

    status, response = await BatchPortal.create(
        external_batch_id=external_batch_id,
        shipment_ids=shipment_ids,
        rate_ids=None,
        batch_notes=f"Auto-created batch for carrier {carrier_code}",
        process_labels=None,  # Don't auto-process - require explicit confirmation
    )

    if status not in (200, 201):
        print_error(f"Failed to create batch for {carrier_code}: {response}")
        return None

    batch_id = response.get("batch_id")
    print_success(f"Created batch {batch_id} for carrier {carrier_code}")
    return batch_id


@no_type_check
async def run_workflow(config: WorkflowConfig) -> WorkflowResult:
    """
    Run the order-to-label workflow.

    Steps:
    1. Fetch carriers, warehouses, and orders
    2. Group orders by carrier
    3. Build shipment payloads
    4. Estimate rates for each shipment
    5. Create shipments (if in live mode)
    6. Create batches per carrier (if in live mode)
    7. (Optional) Process labels
    """
    result = WorkflowResult(dry_run=config.execute_mode != ExecuteMode.LIVE)

    print_section("ShipStation Workflow Demo")
    print(f"Execution Mode: {config.execute_mode.value.upper()}")

    if config.execute_mode == ExecuteMode.LIVE:
        print_warning("LIVE MODE ENABLED - Real operations will be performed!")
        print_warning("This may create shipments and potentially purchase labels.")
        confirm = input("Type 'YES' to continue: ")
        if confirm != "YES":
            print("Aborted.")
            return result

    # Step 1: Fetch reference data
    print_section("Step 1: Fetching Reference Data")

    carriers = await fetch_carriers(config)
    warehouses = await fetch_warehouses(config)
    await fetch_tags(config)  # Just to show it works

    default_warehouse = warehouses[0] if warehouses else None

    # Step 2: Fetch orders
    print_section("Step 2: Fetching Orders")

    orders = await fetch_orders(config)
    result.orders_fetched = len(orders)

    if not orders:
        print_warning("No orders found to process")
        return result

    # Step 3: Group by carrier
    print_section("Step 3: Grouping Orders by Carrier")

    grouped_orders = group_orders_by_carrier(orders, carriers, config)
    result.orders_by_carrier = {
        carrier: [str(o.get("orderNumber")) for o in orders_list]
        for carrier, orders_list in grouped_orders.items()
    }

    # Step 4: Build shipment payloads and estimate rates
    print_section("Step 4: Building Shipment Payloads & Estimating Rates")

    carrier_ids = list(carriers.keys())
    shipments_by_carrier: dict[str, list[ShipmentPayload]] = defaultdict(list)

    for carrier_code, carrier_orders in grouped_orders.items():
        for order in carrier_orders:
            payload = build_shipment_payload(order, default_warehouse)
            shipments_by_carrier[carrier_code].append(payload)

            # Estimate rates (optional, for demonstration)
            if carrier_ids and config.verbose:
                rates = await estimate_rates_for_shipment(payload, carrier_ids, config)
                if rates:
                    cheapest = min(
                        rates,
                        key=lambda r: float(
                            r.get("shipping_amount", {}).get("amount", "999")
                        ),
                    )
                    print(
                        f"  Best rate for {payload.order_number}: "
                        f"${cheapest.get('shipping_amount', {}).get('amount')} "
                        f"({cheapest.get('service_code')})"
                    )

    # Step 5: Create shipments
    print_section("Step 5: Creating Shipments")

    created_shipments_by_carrier: dict[str, list[str]] = defaultdict(list)

    for carrier_code, payloads in shipments_by_carrier.items():
        for payload in payloads:
            shipment_id = await create_shipment(payload, config)
            if shipment_id:
                created_shipments_by_carrier[carrier_code].append(shipment_id)
                result.shipments_created.append(shipment_id)

    # Step 6: Create batches
    print_section("Step 6: Creating Batches by Carrier")

    for carrier_code, shipment_ids in created_shipments_by_carrier.items():
        if shipment_ids:
            batch_id = await create_batch_for_carrier(
                carrier_code, shipment_ids, config
            )
            if batch_id:
                result.batches_created.append(batch_id)

    # Step 7: Summary
    print_section("Workflow Complete - Summary")

    print(f"  Orders fetched: {result.orders_fetched}")
    print(f"  Shipments created: {len(result.shipments_created)}")
    print(f"  Batches created: {len(result.batches_created)}")
    print(f"  Dry run: {result.dry_run}")

    if result.dry_run:
        print_info(
            "This was a DRY RUN. No actual changes were made to your ShipStation account."
        )
        print_info("To execute for real, set execute_mode to ExecuteMode.LIVE")

    return result


@no_type_check
async def main() -> None:
    """Main entry point."""
    load_dotenv()

    V1_API_KEY = os.getenv("SHIP_STATION_V1")
    V2_API_KEY = os.getenv("SHIP_STATION_V2")
    V1_SECRET = os.getenv("SHIP_STATION_SECRET")

    if not V1_API_KEY or not V2_API_KEY or not V1_SECRET:
        print_error(
            "Missing environment variables. "
            "Please set SHIP_STATION_V1, SHIP_STATION_V2, and SHIP_STATION_SECRET"
        )
        return

    # Configure the client
    ShipStationClient.configure(
        v2_key=V2_API_KEY,
        v1_key=V1_API_KEY,
        v1_secret=V1_SECRET,
    )

    # Configure the workflow
    config = WorkflowConfig(
        execute_mode=ExecuteMode.DRY_RUN,  # SAFE default
        use_test_labels=True,
        require_rate_confirmation=True,
        max_orders_to_process=10,
        verbose=True,
    )

    # Run with V2 client for most operations
    async with ShipStationClient.scoped_client("v2"):
        # Temporarily switch to V1 for orders
        async with ShipStationClient.scoped_client("v1"):
            orders = await fetch_orders(config)

        # Back to V2 for the rest of the workflow
        if orders:
            await run_workflow(config)


if __name__ == "__main__":
    print(
        """
╔══════════════════════════════════════════════════════════════╗
║  ShipStation Order-to-Label Workflow Demo                    ║
║                                                              ║
║  This script demonstrates the automation workflow for:       ║
║  - Fetching orders                                           ║
║  - Grouping by carrier                                       ║
║  - Creating shipments                                        ║
║  - Estimating rates                                          ║
║  - Creating batches                                          ║
║                                                              ║
║  DEFAULT: DRY-RUN MODE (no changes made)                     ║
╚══════════════════════════════════════════════════════════════╝
"""
    )
    asyncio.run(main())
