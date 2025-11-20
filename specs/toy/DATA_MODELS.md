# Service Data Models

Capture schemas owned by this service. Link to shared definitions from `../../platform/DATA_MODELS.md`.

## Schema Inventory
| Name | Type | Owner | Source of Truth | Version |
| --- | --- | --- | --- | --- |
| **Toy** | Pydantic | Toy Service | Code | 1.0 |

## Detailed Schemas

### `Toy`
-   **Purpose**: Represents a registered stuffed toy.
-   **Storage**: Cosmos DB `toys` container. Partition Key: `/id`.
-   **Validation**: `name` max 100 chars.

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Fluffy",
  "description": "A brave explorer.",
  "avatar_url": "https://...",
  "personality_tags": ["brave", "curious"]
}
```
