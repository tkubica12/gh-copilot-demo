import os
import dotenv
import asyncio
import logging
from azure.servicebus.aio import ServiceBusClient
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from azure.cosmos.aio import CosmosClient
from concurrent.futures import ThreadPoolExecutor
import json
import io
from markitdown import MarkItDown
from openai import AsyncAzureOpenAI
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.core.settings import settings
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
from models.pdf_models import PdfProcessingResult, ServiceBusMessage
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
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

dotenv.load_dotenv()

# Configure Azure Monitor
appinsights_connection_string = get_env_var("APPLICATIONINSIGHTS_CONNECTION_STRING")
resource = Resource.create({SERVICE_NAME: "PDF Processing Worker Service"})
configure_azure_monitor(connection_string=appinsights_connection_string, resource=resource)
settings.tracing_implementation = "opentelemetry"
OpenAIInstrumentor().instrument()

azure_openai_api_key = get_env_var("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = get_env_var("AZURE_OPENAI_ENDPOINT")
azure_openai_api_version = "2024-10-21"
azure_openai_deployment_name = get_env_var("AZURE_OPENAI_DEPLOYMENT_NAME")
servicebus_fqdn = get_env_var("SERVICEBUS_FQDN")
servicebus_queue = get_env_var("SERVICEBUS_QUEUE")
storage_account_url = get_env_var("STORAGE_ACCOUNT_URL")
storage_container = get_env_var("STORAGE_CONTAINER")
batch_size = int(get_env_var("BATCH_SIZE"))
max_wait_time = float(get_env_var("BATCH_MAX_WAIT_TIME"))
cosmos_account_url = get_env_var("COSMOS_ACCOUNT_URL")
cosmos_db_name = get_env_var("COSMOS_DB_NAME")
cosmos_container_name = get_env_var("COSMOS_CONTAINER_NAME")

# Create clients
credential = DefaultAzureCredential()
servicebus_client = ServiceBusClient(servicebus_fqdn, credential=credential)
storage_account_client = BlobServiceClient(account_url=storage_account_url, credential=credential)
cosmos_client = CosmosClient(cosmos_account_url, credential=credential)
cosmos_database = cosmos_client.get_database_client(cosmos_db_name)
cosmos_container = cosmos_database.get_container_client(cosmos_container_name)

# Initialize markitdown for PDF processing
md_converter = MarkItDown()

client = AsyncAzureOpenAI(
    api_key=azure_openai_api_key,  
    api_version=azure_openai_api_version,
    base_url=f"{azure_openai_endpoint}/openai/deployments/{azure_openai_deployment_name}"
)

async def extract_pdf_content(pdf_data: bytes, filename: str) -> tuple[str, int]:
    """
    Extract text content from PDF using markitdown.
    
    Args:
        pdf_data: Raw PDF file data
        filename: Original filename for context
        
    Returns:
        tuple: (extracted_text, page_count)
        
    Raises:
        Exception: If PDF extraction fails
    """
    try:
        # Use markitdown to extract content from PDF
        with io.BytesIO(pdf_data) as pdf_stream:
            # Create a temporary file-like object for markitdown
            pdf_stream.seek(0)
            result = md_converter.convert_stream(pdf_stream, file_extension=".pdf")
            
            extracted_text = result.text_content
            
            # Try to estimate page count from content structure
            # This is approximate as markitdown doesn't provide direct page count
            page_count = max(1, extracted_text.count('\n\n') // 10)  # Rough estimation
            
            return extracted_text, page_count
            
    except Exception as e:
        logger.error(f"Failed to extract PDF content from {filename}: {e}")
        raise


async def generate_ai_summary(content_text: str, filename: str) -> str:
    """
    Generate AI summary of PDF content using Azure OpenAI.
    
    Args:
        content_text: Extracted text content from PDF
        filename: Original filename for context
        
    Returns:
        str: AI-generated summary
        
    Raises:
        Exception: If AI summarization fails
    """
    try:
        logger.info(f"Generating AI summary for {filename}")
        
        response = await client.chat.completions.create(
            model=azure_openai_deployment_name,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that creates concise and informative summaries of documents. Focus on the main topics, key points, and important information. Keep the summary comprehensive but readable."
                },
                {
                    "role": "user", 
                    "content": f"Please provide a summary of the following document content:\n\n{content_text}"
                }
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        summary = response.choices[0].message.content
        logger.info(f"AI summary generated for {filename}: {len(summary)} characters")
        
        return summary
        
    except Exception as e:
        logger.error(f"Failed to generate AI summary for {filename}: {e}")
        raise


async def process_message(msg, receiver):
    """
    Process a single PDF processing message.
    
    Args:
        msg: Service Bus message
        receiver: Service Bus receiver
    """
    try:
        logger.info(f"Processing message: {msg}")
        message_body = json.loads(str(msg))
        
        # Parse message data
        try:
            message_data = ServiceBusMessage(**message_body)
        except Exception as e:
            logger.error(f"Invalid message format: {e}")
            await receiver.abandon_message(msg)
            return
        
        blob_name = message_data.blob_name
        processing_id = message_data.id
        original_filename = message_data.original_filename
        file_size_bytes = message_data.file_size_bytes
        
        # Download PDF from blob storage
        blob_client = storage_account_client.get_blob_client(storage_container, blob_name)
        logger.info(f"Downloading PDF data from {blob_name}")
        download_stream = await blob_client.download_blob()
        pdf_data = await download_stream.readall()
        
        # Extract content from PDF
        logger.info(f"Extracting content from PDF {original_filename}")
        content_text, page_count = await extract_pdf_content(pdf_data, original_filename)
        
        # Generate AI summary
        ai_summary = await generate_ai_summary(content_text, original_filename)
        
        # Create processing result
        processing_result = PdfProcessingResult(
            id=processing_id,
            original_filename=original_filename,
            content_text=content_text,
            ai_summary=ai_summary,
            processing_timestamp=datetime.utcnow(),
            file_size_bytes=file_size_bytes,
            page_count=page_count
        )
        
        # Save result to Cosmos DB
        logger.info(f"Saving processing result to Cosmos DB for document {processing_id}")
        doc = processing_result.model_dump()
        # Convert datetime to string for Cosmos DB
        doc["processing_timestamp"] = doc["processing_timestamp"].isoformat()
        await cosmos_container.upsert_item(doc)
        
        # Complete the message
        await receiver.complete_message(msg)
        logger.info(f"Successfully processed PDF {original_filename} with ID {processing_id}")
        
    except Exception as e:
        logger.error(f"Error processing PDF message: {e}")
        await receiver.abandon_message(msg)

async def main():
    """
    Main worker loop to process PDF processing messages from Service Bus.
    """
    logger.info("Starting PDF processing worker")
    
    async with ServiceBusClient(servicebus_fqdn, credential=credential) as sb_client:
        receiver = sb_client.get_queue_receiver(
            queue_name=servicebus_queue,
            max_lock_renewal_duration=120
        )
        async with receiver:
            while True:
                try:
                    messages = await receiver.receive_messages(
                        max_message_count=batch_size, 
                        max_wait_time=max_wait_time
                    )
                    
                    if not messages:
                        await asyncio.sleep(1)
                        continue
                        
                    tasks = []
                    for message in messages:
                        tasks.append(asyncio.create_task(process_message(message, receiver)))
                        
                    if tasks:
                        await asyncio.gather(*tasks)
                        
                except Exception as e:
                    logger.error(f"Error in main processing loop: {e}")
                    await asyncio.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    asyncio.run(main())