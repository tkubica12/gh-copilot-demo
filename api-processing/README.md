# API Processing

This API accepts both image and PDF uploads, stores them in Azure Blob Storage for long-term retention, and sends messages to Azure Service Bus for AI processing.

You can access it at `/api/process`.

## Supported File Types

### Images
- JPEG (image/jpeg, image/jpg)
- PNG (image/png) 
- GIF (image/gif)
- BMP (image/bmp)

### Documents
- PDF (application/pdf)

## Processing Features

### Images
- AI-powered image description using Azure OpenAI Vision
- Stores original images in blob storage
- Provides detailed descriptions of image content

### PDFs  
- Content extraction using markitdown library
- AI-powered document summarization using Azure OpenAI
- Stores original PDFs in blob storage for forensic purposes
- Extracts and processes text content from PDF documents

## Components Used
- Azure Storage Blob (storing images and PDFs)
- Azure Service Bus (sending processing messages)
- Azure Monitor (monitoring and audit logging)
- Azure OpenAI (AI processing for both images and documents)

## Tests
We distinguish **unit** and **integration** tests:

- Unit tests (under `tests/unit`) run fast, have no external side‑effects and mock all Azure dependencies.
- Integration tests (under `tests/integration`) talk to real Azure resources (blob + Service Bus). They are **skipped by default**.

### Install dependencies (uv)
Sync base dependencies (runtime only):
```
uv sync
```
Include test dependencies (choose one):
```
uv sync --extra test          # use optional dependency group
# OR install dev deps (duplicates for convenience)
uv sync --dev
```

### Run unit tests only
```
uv run pytest -m "not integration" -q
```

### Run integration tests
Ensure required environment variables point to test resources, then:
```
uv run pytest -m integration -q
```

Required variables: `STORAGE_ACCOUNT_URL`, `STORAGE_CONTAINER`, `SERVICEBUS_FQDN`, `SERVICEBUS_QUEUE`, `PROCESSED_BASE_URL`, `APPLICATIONINSIGHTS_CONNECTION_STRING`.

### Run all tests
```
uv run pytest -q
```

### Markers
`integration` – real Azure calls (run explicitly with `-m integration`).

---
Tests use `pytest` fixtures in `tests/conftest.py` to inject fakes for Azure SDK clients during unit testing.

