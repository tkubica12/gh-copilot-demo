# Shared Testing Strategy

Define the organization-wide testing expectations that every service must follow before shipping.

## Test Pyramid Targets
| Layer | Goal | Tooling Baseline |
| --- | --- | --- |
| **Unit** | Logic verification | `pytest` |
| **Integration** | Service + DB/Blob verification | `pytest` with running services (Local/Dev) |
| **E2E** | Full flow verification | `pytest` calling public APIs |

## Quality Gates
- **CI**: All tests must pass before merge.
- **Linting**: `ruff` or `flake8` must pass.

## Tooling
- **Test Runner**: `pytest`
- **HTTP Client**: `httpx` (async)

## Specification by Example
- **Given** a running Toy Service, **When** `POST /toy` is called, **Then** the toy is persisted in Cosmos DB and retrievable via `GET /toy/{id}`.

## No Auth Testing
- Since authentication is removed, tests do not need to generate tokens. They can directly call APIs.
