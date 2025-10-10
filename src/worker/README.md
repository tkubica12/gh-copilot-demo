# Image processing worker

This worker listens to messages from an Azure Service Bus queue, processes images using Azure OpenAI, and stores the results in Azure Cosmos DB.

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading images)
- Azure OpenAI (processing images)
- Azure Cosmos DB (storing results)

## Dependency Management

This service uses **uv** as the package manager. Dependencies are defined in `pyproject.toml`.

### Install dependencies
Sync dependencies:
```
uv sync
```

### Update dependencies
After modifying `pyproject.toml`:
```
uv sync
```

### Docker builds
The Dockerfile uses a `requirements.txt` file generated from `pyproject.toml` for faster and more reliable container builds:
```
uv pip compile pyproject.toml -o requirements.txt
```
This file is committed to the repository and should be regenerated when dependencies change.

