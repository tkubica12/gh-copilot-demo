# Data Models

Document every persistent or transient data contract here. Treat this as the definitive schema catalog referenced by APIs, storage engines, and analytics jobs.

## Authoritative Principles
- **Single source of truth**: Schemas here must match Pydantic models in code.
- **Simplicity**: Models should be kept simple for the public catalog use case.
- **No Auth**: No user IDs or owner fields.

## Schema Inventory
| Name | Type | Partition Key | Description | Version |
| --- | --- | --- | --- | --- |
| **Toy** | Pydantic/Cosmos | `id` | Represents a stuffed toy. | 1.0 |
| **Trip** | Pydantic/Cosmos | `id` | Represents a trip taken by a toy. | 1.0 |
| **Addon** | Pydantic/Cosmos | `id` | Represents an accessory or experience order. | 1.0 |

## Detailed Schemas

### `Toy`
- **Storage Location**: Cosmos DB `toys` container.
- **Constraints**: `name` is required.

```json
{
  "id": "uuid-string",
  "name": "Fluffy",
  "description": "A brave teddy bear.",
  "avatar_url": "https://...",
  "personality_tags": ["brave", "cuddly"]
}
```

### `Trip`
- **Storage Location**: Cosmos DB `trips` container.
- **Constraints**: `toy_id` is required.

```json
{
  "id": "uuid-string",
  "toy_id": "uuid-string",
  "destination": "Paris",
  "start_date": "2025-11-20",
  "status": "active"
}
```

### `Addon`
- **Storage Location**: Cosmos DB `addons` container.

```json
{
  "id": "uuid-string",
  "trip_id": "uuid-string",
  "type": "accessory",
  "name": "Beret",
  "status": "fulfilled"
}
```
