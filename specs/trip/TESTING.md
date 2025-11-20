# Service Testing Strategy

Summarize how this service validates behavior, referencing shared standards in `../../platform/TESTING.md`.

## Test Matrix
| Layer | Tools | Scope | Owner |
| --- | --- | --- | --- |
| **Integration** | `pytest` | API -> DB/Blob | Backend Team |

## Scenarios
-   **Given** a toy ID, **When** creating a trip, **Then** the trip is created and linked to the toy.
-   **Given** a trip, **When** uploading an image, **Then** it appears in the gallery.
