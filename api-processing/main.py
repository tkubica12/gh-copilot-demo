import os
import uuid
import dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.core.settings import settings
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

app = FastAPI(title="AI processing", description="API to process pictures and documents")

# Load environment variables
dotenv.load_dotenv()

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        raise EnvironmentError(f"{var_name} environment variable is not set")
    return value

storage_account_url = get_env_var("STORAGE_ACCOUNT_URL")
storage_container = get_env_var("STORAGE_CONTAINER")
processed_base_url = get_env_var("PROCESSED_BASE_URL")
servicebus_fqdn = get_env_var("SERVICEBUS_FQDN")
servicebus_queue = get_env_var("SERVICEBUS_QUEUE")
appinsights_connection_string = get_env_var("APPLICATIONINSIGHTS_CONNECTION_STRING")

# Configure Azure Monitor
appinsights_connection_string = get_env_var("APPLICATIONINSIGHTS_CONNECTION_STRING")
resource = Resource.create({SERVICE_NAME: "Processing API Service"})
configure_azure_monitor(connection_string=appinsights_connection_string, resource=resource)
settings.tracing_implementation = "opentelemetry"
FastAPIInstrumentor.instrument_app(app)

# CORS
origins = [os.environ.get("CORS_ORIGIN", "*")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get clients to storage and Service Bus
credential = DefaultAzureCredential()
storage_account_client = BlobServiceClient(account_url=storage_account_url, credential=credential)
container_client = storage_account_client.get_container_client(storage_container)
servicebus_client = ServiceBusClient(servicebus_fqdn, credential=credential)
servicebus_queue = servicebus_client.get_queue_sender(servicebus_queue)

@app.get("/", include_in_schema=False)
def get_openapi_spec():
    return app.openapi()

@app.post(
    "/api/process",
    response_class=JSONResponse,
    status_code=202,
    responses={
        202: {
            "description": "Accepted and processing",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "results_url": "https://example.com/processed/123e4567-e89b-12d3-a456-426614174000"
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["string", 0],
                                "msg": "string",
                                "type": "string"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def process_file(file: UploadFile = File(...)):
    # Generate GUID
    guid = str(uuid.uuid4())

    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in [".jpg", ".jpeg", ".png", ".pdf"]:
        return JSONResponse(status_code=400, content={"detail": "Unsupported file type"})

    # Upload file to storage
    blob_name = f"{guid}{extension}"
    container_client.upload_blob(name=blob_name, data=file.file, overwrite=False)

    # Send message to Service Bus
    message = ServiceBusMessage(json.dumps({"blob_name": blob_name, "id": guid}))
    servicebus_queue.send_messages(message)

    return JSONResponse(status_code=202, content={"id": guid, "results_url": f"{processed_base_url}/{guid}"})
