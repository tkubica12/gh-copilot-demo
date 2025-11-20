# Azure Emulators

This directory contains a Docker Compose file to run local emulators for Azure services.

## Services

- **Azure Cosmos DB Emulator (NoSQL API)**: Runs on port `8081`.
- **Azurite (Blob Storage)**: Runs on port `10000`.

## Prerequisites

- Docker Desktop installed and running.

## Usage

To start the emulators, run:

```bash
docker-compose up -d
```

To stop the emulators:

```bash
docker-compose down
```

## Connection Strings

### Cosmos DB
- **URI**: `https://localhost:8081`
- **Key**: `C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==`

### Azurite (Blob Storage)
- **Connection String**: `DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;`
