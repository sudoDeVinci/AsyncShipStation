# ShipStation Interaction / Automation

It looks like there's no recently updated shipstation APIs for python, at least that are easily found. We therefore will roll our own simple API for ShipStation.

## Auth
ShipStation doesn't force auth before usage, but requires the API-Key header on each request.

## Rate Limiting
Accounts that send too many requests in quick succession will receive a 429 Too Many Requests error response and include a Retry-After header with the number of seconds to wait for. By default we get 200 requests per minute.
ShipStation has bulk op endpoints. These only count as a single request.

## Batches
[/batches](/batches/_types.py)
Process labels in bulk and receive a large number of labels and customs forms in bulk responses. Batching is ideal for workflows that need to process hundreds or thousands of labels quickly.
