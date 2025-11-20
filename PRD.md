# Product Requirements Document (PRD)

## 1. Metadata
- **Product / Feature Name**: Stuffed Toy World Tour (Public Catalog)
- **Author(s)**: Architecture Team
- **Date**: 2025-11-20
- **Revision**: 1.0
- **Status**: Draft
- **Related Docs**: `specs/platform/ARCHITECTURE.md`

## 2. Summary
The Stuffed Toy World Tour application is a public catalog that allows users to create whimsical international trips for plush toys, view gallery images from destinations, and order accessories or experiences (add‑ons). The system demonstrates enterprise microservice patterns (Azure Container Apps, Cosmos DB, Service Bus, OpenTelemetry) in a simplified, public-access environment without user authentication or ownership restrictions.

## 3. Goals & Non-Goals
| Goals | Non-Goals |
| --- | --- |
| Create a public, interactive catalog of toy trips. | User authentication or identity management. |
| Demonstrate microservice architecture on Azure Container Apps. | Private data or ownership enforcement. |
| Implement event-driven workflows (add-ons). | Billing or payment processing. |
| Provide real-time observability via OpenTelemetry. | Complex social interactions between users. |

## 4. Success Metrics
- **System Uptime**: 99.9% availability for public APIs.
- **Observability Coverage**: 100% of services emitting traces and metrics to OTEL collector.
- **Deployment Speed**: Local environment startup < 5 minutes.

## 5. Users & Personas
| Persona | Needs | Success Criteria |
| --- | --- | --- |
| **Public User** | Wants to register toys, create trips, and interact with the system without barriers. | Can perform all actions (create, view, update) anonymously. |
| **Developer** | Wants to understand the microservice architecture and run it locally. | Can spin up the full stack locally with minimal configuration. |

## 6. Assumptions & Constraints
- **Public Access**: All data is public. Anyone can modify any toy or trip (for demo simplicity).
- **Azure PaaS**: The system relies on Azure Cosmos DB, Blob Storage, and Service Bus (or their emulators).

## 7. Specification by Example
| Scenario | Given | When | Then | Automated Test? |
| --- | --- | --- | --- | --- |
| **Register Toy** | The system is running | A user submits a new toy with name "Fluffy" | The toy is created and visible in the public list | Yes |
| **Create Trip** | A toy "Fluffy" exists | A user creates a trip to "Paris" for "Fluffy" | The trip is linked to the toy and visible | Yes |
| **Order Add-on** | A trip exists | A user orders a "Hat" add-on | The add-on is processed and a fulfillment image appears in the gallery | Yes |

## 8. Requirements

### Functional
1.  **Register Toy**: Users can register a toy (name, avatar image, personality tags).
2.  **Create Trip**: Users can create a trip to a single destination for any toy.
3.  **Trip Gallery**: Users can view and upload gallery images for any trip.
4.  **Order Add‑on**: Users can order accessories or experiences for any trip.
5.  **Public Access**: All APIs are open; no authentication tokens required.

### Non-Functional
-   **Performance**: API response time < 500ms for read operations.
-   **Observability**: Full distributed tracing across all services.
-   **Scalability**: Services can scale to zero when not in use (ACA).

## 9. UX & Flows
-   **Web Interface**: A simple Single Page Application (SPA) to browse toys and view trips.

## 10. Dependencies
-   **Azure Cosmos DB**: For data persistence.
-   **Azure Blob Storage**: For image storage.
-   **Azure Service Bus**: For asynchronous messaging (add-ons).

## 11. Rollout Plan
-   **Phase 1**: Local development environment with emulators.
-   **Phase 2**: Deployment to Azure Container Apps (Dev environment).
-   **Phase 3**: Public demo release.

## 12. Risks & Mitigations
| Risk | Impact | Likelihood | Mitigation |
| --- | --- | --- | --- |
| **Data Vandalism** | Public access allows anyone to delete/modify data. | High | Acceptable for demo; periodic data reset. |

## 13. Open Questions
-   Should we implement a simple "admin" key for data cleanup?
-   How to handle concurrent modifications to the same toy/trip? (Last write wins).

## 14. Change Log
| Date | Author | Change |
| --- | --- | --- |
| 2025-11-20 | Architecture Team | Initial Draft (Removed Auth/Ownership) |
