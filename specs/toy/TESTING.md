# Service Testing Strategy

Summarize how this service validates behavior, referencing shared standards in `../../platform/TESTING.md`.

## Test Matrix
| Layer | Tools | Scope | Owner |
| --- | --- | --- | --- |
| **Integration** | `pytest` | API -> DB/Blob | Backend Team |

## Scenarios
-   **Given** a new toy name, **When** registered, **Then** it appears in the list.
-   **Given** a toy, **When** avatar uploaded, **Then** the avatar URL is updated.
