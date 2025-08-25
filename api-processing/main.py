import os
import uuid
import dotenv
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
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
from datetime import datetime
from models.pdf_models import ProcessPdfResponse, AuditLog

app = FastAPI(title="AI PDF processing", description="API to process PDF documents")

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv.load_dotenv()

def get_env_var(var_name):
    """
    Get environment variable value with error handling.
    
    Args:
        var_name: Name of the environment variable
        
    Returns:
        str: Environment variable value
        
    Raises:
        EnvironmentError: If the environment variable is not set
    """
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
resource = Resource.create({SERVICE_NAME: "PDF Processing API Service"})
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
servicebus_queue_sender = servicebus_client.get_queue_sender(servicebus_queue)


async def log_audit_event(operation_id: str, operation_type: str, request: Request, 
                         file_name: str, file_size: int, status: str, error_message: str = None):
    """
    Log audit events for PDF processing operations.
    
    Args:
        operation_id: Unique identifier for the operation
        operation_type: Type of operation (upload, process, retrieve)
        request: FastAPI request object for IP extraction
        file_name: Name of the file being processed
        file_size: Size of the file in bytes
        status: Status of the operation
        error_message: Optional error message if operation failed
    """
    try:
        audit_log = AuditLog(
            operation_id=operation_id,
            operation_type=operation_type,
            user_ip=request.client.host if request.client else None,
            file_name=file_name,
            file_size_bytes=file_size,
            status=status,
            error_message=error_message
        )
        
        logger.info(f"Audit log: {audit_log.model_dump_json()}")
        
    except Exception as e:
        logger.error(f"Failed to log audit event: {e}")


@app.get("/", include_in_schema=False)
def get_openapi_spec():
    """Return OpenAPI specification for the service."""
    return app.openapi()

@app.post(
    "/api/process",
    response_model=ProcessPdfResponse,
    status_code=202,
    responses={
        202: {
            "description": "PDF accepted and processing started",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "results_url": "https://example.com/processed/123e4567-e89b-12d3-a456-426614174000",
                        "status": "processing"
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
async def process_pdf(request: Request, file: UploadFile = File(...)):
    """
    Process a PDF document by extracting content and generating AI summary.
    
    Args:
        request: FastAPI request object
        file: Uploaded PDF file
        
    Returns:
        ProcessPdfResponse: Processing job details
        
    Raises:
        HTTPException: If file validation fails or processing cannot be initiated
    """
    
    # Validate file type
    if not file.content_type or not file.content_type.lower().startswith('application/pdf'):
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=422, detail="Only PDF files are accepted")
    
    # Generate unique identifier
    guid = str(uuid.uuid4())
    
    try:
        # Read file content for size validation
        file_content = await file.read()
        file_size = len(file_content)
        
        # Reset file pointer for upload
        await file.seek(0)
        
        # Log audit event for upload
        await log_audit_event(
            operation_id=guid,
            operation_type="upload",
            request=request,
            file_name=file.filename or "unknown.pdf",
            file_size=file_size,
            status="success"
        )
        
        # Upload PDF to storage with proper extension
        blob_name = f"{guid}.pdf"
        container_client.upload_blob(name=blob_name, data=file_content, overwrite=False)
        
        # Send message to Service Bus for processing
        message_data = {
            "blob_name": blob_name,
            "id": guid,
            "original_filename": file.filename or "unknown.pdf",
            "file_size_bytes": file_size,
            "processing_type": "pdf_summary"
        }
        message = ServiceBusMessage(json.dumps(message_data))
        servicebus_queue_sender.send_messages(message)
        
        # Log audit event for processing initiation
        await log_audit_event(
            operation_id=guid,
            operation_type="process",
            request=request,
            file_name=file.filename or "unknown.pdf",
            file_size=file_size,
            status="processing"
        )
        
        response = ProcessPdfResponse(
            id=guid,
            results_url=f"{processed_base_url}/{guid}",
            status="processing"
        )
        
        logger.info(f"PDF processing initiated for {file.filename} with ID {guid}")
        return response
        
    except Exception as e:
        # Log audit event for error
        await log_audit_event(
            operation_id=guid,
            operation_type="upload",
            request=request,
            file_name=file.filename or "unknown.pdf",
            file_size=len(file_content) if 'file_content' in locals() else 0,
            status="error",
            error_message=str(e)
        )
        
        logger.error(f"Error processing PDF upload: {e}")
        raise HTTPException(status_code=500, detail="Failed to process PDF upload")
