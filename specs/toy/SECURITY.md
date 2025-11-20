# Service Security Notes

Detail the threat model and controls unique to this service.

## Threat Model Snapshot
| Asset | Threat | Mitigation |
| --- | --- | --- |
| **Toy Data** | Malicious modification | None (Public Demo). Backups available. |
| **Blob Storage** | Public access abuse | Managed Identity for service access. |

## Controls Checklist
-   **Auth**: None (Public).
-   **Secrets**: Managed Identity used for Azure resources.
