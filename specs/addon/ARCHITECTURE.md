# Service Architecture Snapshot

## Context
The Addon Service manages orders for accessories and experiences.

## Component Diagram
```mermaid
graph TD
    Client -->|HTTP| API[FastAPI App]
    API -->|Read/Write| DB[(Cosmos DB 'addons')]
    API -->|Publish| SB[Service Bus 'addon.ordered']
```

## Data Flow
1.  **Order Addon**: Client POSTs order -> API saves to Cosmos -> Publishes event to Service Bus.
