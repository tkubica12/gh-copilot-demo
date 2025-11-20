# Service Data Models

Capture schemas owned by this service. Link to shared definitions from `../../platform/DATA_MODELS.md`.

## Schema Inventory
| Name | Type | Owner | Source of Truth | Version |
| --- | --- | --- | --- | --- |
| **Trip** | Pydantic | Trip Service | Code | 1.0 |

## Detailed Schemas

### `Trip`
-   **Purpose**: Represents a trip.
-   **Storage**: Cosmos DB `trips` container. Partition Key: `/id`.

```json
{
  "id": "uuid",
  "toy_id": "uuid",
  "destination": "Tokyo",
  "start_date": "2025-01-01",
  "gallery": [
      { "url": "...", "caption": "At the tower" }
  ]
}
```
