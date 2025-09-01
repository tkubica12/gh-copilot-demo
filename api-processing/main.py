import os
import uuid
import dotenv
import logging
from datetime import datetime, timezone
from fastapi import FastAPI, File, UploadFile, HTTPException
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

app = FastAPI(title="AI processing", description="API to process images and PDFs")

# Load environment variables
dotenv.load_dotenv()

# Setup logging for auditing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Supported file types
SUPPORTED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/gif", "image/bmp"}
SUPPORTED_PDF_TYPES = {"application/pdf"}
SUPPORTED_FILE_TYPES = SUPPORTED_IMAGE_TYPES | SUPPORTED_PDF_TYPES

def validate_file_type(file: UploadFile) -> tuple[bool, str]:
    """
    Validate if the uploaded file is supported.
    Returns (is_valid, file_type_category)
    """
    content_type = file.content_type
    
    if content_type in SUPPORTED_IMAGE_TYPES:
        return True, "image"
    elif content_type in SUPPORTED_PDF_TYPES:
        return True, "pdf"
    else:
        return False, "unsupported"

def get_blob_extension(file_type_category: str, original_filename: str = "") -> str:
    """Get appropriate file extension for blob storage."""
    if file_type_category == "image":
        return ".jpg"  # Default to jpg for images
    elif file_type_category == "pdf":
        return ".pdf"
    else:
        # Try to extract from original filename
        if "." in original_filename:
            return "." + original_filename.split(".")[-1].lower()
        return ".bin"  # fallback

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
        400: {
            "description": "Bad Request - Unsupported file type",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Unsupported file type. Supported types: images (JPEG, PNG, GIF, BMP) and PDFs"
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
    """
    Process uploaded images or PDFs.
    
    For images: Generates AI description
    For PDFs: Extracts content and generates summary
    """
    # Audit log: Request received
    logger.info(f"Processing request for file: {file.filename}, content-type: {file.content_type}")
    
    # Validate file type
    is_valid, file_type_category = validate_file_type(file)
    if not is_valid:
        logger.warning(f"Unsupported file type: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Supported types: images (JPEG, PNG, GIF, BMP) and PDFs"
        )
    
    # Generate GUID
    guid = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Determine file extension and blob name
    file_extension = get_blob_extension(file_type_category, file.filename or "")
    blob_name = f"{guid}{file_extension}"
    
    try:
        # Upload file to storage for long-term retention
        logger.info(f"Uploading {file_type_category} file to blob storage: {blob_name}")
        container_client.upload_blob(name=blob_name, data=file.file, overwrite=False)
        
        # Audit log: File uploaded successfully
        logger.info(f"Successfully uploaded file {blob_name} to blob storage")
        
        # Send message to Service Bus for processing
        message_data = {
            "blob_name": blob_name,
            "id": guid,
            "file_type": file_type_category,
            "original_filename": file.filename,
            "timestamp": timestamp
        }
        
        message = ServiceBusMessage(json.dumps(message_data))
        servicebus_queue.send_messages(message)
        
        # Audit log: Message sent successfully
        logger.info(f"Successfully sent processing message for {blob_name} to Service Bus")
        
        return JSONResponse(
            status_code=202,
            content={
                "id": guid,
                "results_url": f"{processed_base_url}/{guid}",
                "file_type": file_type_category
            }
        )
        
    except Exception as e:
        # Audit log: Processing failed
        logger.error(f"Error processing file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
