# Service Security Notes

Detail the threat model and controls unique to this service.

## Threat Model Snapshot
| Asset | Threat | Mitigation |
| --- | --- | --- |
| **Trip Data** | Malicious modification | None (Public Demo). |
| **Blob Storage** | Public access abuse | Managed Identity. |

## Controls Checklist
-   **Auth**: None (Public).
-   **Secrets**: Managed Identity.
