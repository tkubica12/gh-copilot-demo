# Image processing worker

This worker listens to messages from an Azure Service Bus queue, processes images using Azure OpenAI, and stores the results in Azure Cosmos DB.

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading images)
- Azure OpenAI (processing images)
- Azure Cosmos DB (storing results)

## Development

### Dependencies
This project uses `pyproject.toml` for dependency management. Install dependencies using:

```bash
uv sync --all-extras  # Installs runtime and test dependencies
```

Or with pip:
```bash
pip install -e .
pip install -e .[test]  # For test dependencies
```

### Running the Service
```bash
uv run python main.py  # Using uv
# or
python main.py  # Using standard Python
```

### Testing

#### Unit Tests
Unit tests are located in `tests/unit/` and test core business logic with mocked Azure dependencies.

Run unit tests:
```bash
uv run pytest tests/unit/ -v
# or
python -m pytest tests/unit/ -v
```

#### Test Coverage
The unit tests cover:
- Environment variable validation (`get_env_var` function)
- Message processing logic with mocked Azure services
- Error handling for invalid messages and exceptions
- Cosmos DB document storage verification

#### Integration Tests
Integration tests require real Azure resources and are located in `tests/integration/` (to be implemented).

### Environment Variables
Required environment variables:
- `APPLICATIONINSIGHTS_CONNECTION_STRING`: Azure Application Insights connection string
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Azure OpenAI deployment name
- `SERVICEBUS_FQDN`: Azure Service Bus namespace FQDN
- `SERVICEBUS_QUEUE`: Service Bus queue name
- `STORAGE_ACCOUNT_URL`: Azure Storage account URL
- `STORAGE_CONTAINER`: Blob storage container name
- `BATCH_SIZE`: Number of messages to process in batch (default: 5)
- `BATCH_MAX_WAIT_TIME`: Maximum wait time for batch in seconds (default: 10.0)
- `COSMOS_ACCOUNT_URL`: Azure Cosmos DB account URL
- `COSMOS_DB_NAME`: Cosmos DB database name
- `COSMOS_CONTAINER_NAME`: Cosmos DB container name
