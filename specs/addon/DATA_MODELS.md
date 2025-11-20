# Service Data Models

## Schema Inventory
| Name | Type | Owner | Source of Truth | Version |
| --- | --- | --- | --- | --- |
| **Addon** | Pydantic | Addon Service | Code | 1.0 |

## Detailed Schemas

### `Addon`
-   **Purpose**: Represents an order.
-   **Storage**: Cosmos DB `addons` container.

```json
{
  "id": "uuid",
  "trip_id": "uuid",
  "item_name": "Hat",
  "status": "pending"
}
```
