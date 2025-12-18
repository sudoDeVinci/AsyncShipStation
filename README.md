# ShipStation Interaction / Automation
[![Type-Check](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/mypy.yml)
[![Linting](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/AsyncShipStation/actions/workflows/linting.yml)
[![Python 3.11.7](https://img.shields.io/badge/python-3.11.7-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Validation: Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

It looks like there's no recently updated shipstation APIs for python, at least that are easily found. We therefore will roll our own simple API for ShipStation.

## Auth
ShipStation doesn't force auth before usage, but requires the API-Key header on each request.

## Rate Limiting
Accounts that send too many requests in quick succession will receive a 429 Too Many Requests error response and include a Retry-After header with the number of seconds to wait for. By default we get 200 requests per minute.
ShipStation has bulk op endpoints. These only count as a single request.

## Batches
[/batches](/batches/_types.py)
Process labels in bulk and receive a large number of labels and customs forms in bulk responses. Batching is ideal for workflows that need to process hundreds or thousands of labels quickly.
200
