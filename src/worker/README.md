# Image processing worker

This worker listens to messages from an Azure Service Bus queue, processes images using Azure OpenAI, and stores the results in Azure Cosmos DB.

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading images)
- Azure OpenAI (processing images)
- Azure Cosmos DB (storing results)

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for Python package management.

### Install dependencies

```bash
uv sync
```

### Run locally

```bash
uv run main.py
```
