import os
import dotenv
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from azure.cosmos.aio import CosmosClient
from concurrent.futures import ThreadPoolExecutor
import json
import requests
import base64
from openai import AsyncAzureOpenAI
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.core.settings import settings
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
from markitdown import MarkItDown
import io
import logging

# Load environment variables
def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        raise EnvironmentError(f"{var_name} environment variable is not set")
    return value

dotenv.load_dotenv()

# Configure Azure Monitor
appinsights_connection_string = get_env_var("APPLICATIONINSIGHTS_CONNECTION_STRING")
resource = Resource.create({SERVICE_NAME: "AI Worker Service"})
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

client = AsyncAzureOpenAI(
    api_key=azure_openai_api_key,  
    api_version=azure_openai_api_version,
    base_url=f"{azure_openai_endpoint}/openai/deployments/{azure_openai_deployment_name}"
)

# Initialize MarkItDown for PDF processing
markdown_converter = MarkItDown()

# Setup logging for auditing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_pdf_file(blob_name: str) -> bool:
    """Check if the file is a PDF based on extension."""
    return blob_name.lower().endswith('.pdf')

def extract_pdf_content(pdf_data: bytes) -> str:
    """Extract text content from PDF using markitdown."""
    try:
        # Create a BytesIO stream from PDF data
        pdf_stream = io.BytesIO(pdf_data)
        
        # Convert PDF to markdown/text
        result = markdown_converter.convert(pdf_stream)
        
        # Return the text content
        return result.text_content or result.markdown
    except Exception as e:
        logger.error(f"Error extracting PDF content: {e}")
        raise Exception(f"Failed to extract PDF content: {e}")

async def process_pdf_content(pdf_content: str) -> str:
    """Process PDF content and generate a summary using OpenAI."""
    try:
        logger.info("Sending PDF content to OpenAI for summarization...")
        
        response = await client.chat.completions.create(
            model=azure_openai_deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes document content. Provide a clear, concise summary of the main points from the document."},
                {"role": "user", "content": f"Please summarize the following document content:\n\n{pdf_content}"}
            ]
        )
        
        summary = response.choices[0].message.content
        logger.info(f"Generated summary: {summary[:100]}...")
        return summary
        
    except Exception as e:
        logger.error(f"Error generating PDF summary: {e}")
        raise Exception(f"Failed to generate PDF summary: {e}")

async def process_image_content(encoded_image: str) -> str:
    """Process image content using OpenAI vision."""
    try:
        logger.info("Sending image to OpenAI for description...")
        
        response = await client.chat.completions.create(
            model=azure_openai_deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Describe this picture:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]}
            ]
        )
        
        description = response.choices[0].message.content
        logger.info(f"Generated description: {description[:100]}...")
        return description
        
    except Exception as e:
        logger.error(f"Error generating image description: {e}")
        raise Exception(f"Failed to generate image description: {e}")

async def process_message(msg, receiver):
    """
    Process a single message and then complete it.
    Handles both images and PDFs.
    """
    try:
        print(f"Processing message: {msg}")
        message_body = json.loads(str(msg))
        blob_name = message_body.get("blob_name", "")
        id = message_body.get("id", "")
        
        # Audit log: Start processing
        logger.info(f"Starting processing for file: {blob_name}, ID: {id}")
        
        blob_client = storage_account_client.get_blob_client(storage_container, blob_name)
        print(f"Downloading file data from {blob_name}")
        download_stream = await blob_client.download_blob()
        file_data = await download_stream.readall()
        
        # Audit log: File downloaded
        logger.info(f"Downloaded file {blob_name}, size: {len(file_data)} bytes")
        
        ai_response = ""
        
        if is_pdf_file(blob_name):
            # Process PDF file
            logger.info(f"Processing PDF file: {blob_name}")
            
            try:
                # Extract content from PDF
                pdf_content = extract_pdf_content(file_data)
                logger.info(f"Extracted PDF content, length: {len(pdf_content)} characters")
                
                # Generate summary
                ai_response = await process_pdf_content(pdf_content)
                
                # Audit log: PDF processed successfully
                logger.info(f"Successfully processed PDF {blob_name}, generated summary")
                
            except Exception as e:
                logger.error(f"Error processing PDF {blob_name}: {e}")
                raise e
                
        else:
            # Process as image file (existing logic)
            logger.info(f"Processing image file: {blob_name}")
            
            try:
                encoded_image = base64.b64encode(file_data).decode("utf-8")
                ai_response = await process_image_content(encoded_image)
                
                # Audit log: Image processed successfully
                logger.info(f"Successfully processed image {blob_name}")
                
            except Exception as e:
                logger.error(f"Error processing image {blob_name}: {e}")
                raise e
        
        print("AI response:", f"{ai_response[:50]}...")
        print(f"Saving response to Cosmos DB to document with id {id}")
        
        doc = {
            "id": id,
            "ai_response": ai_response,
            "file_name": blob_name,
            "file_type": "pdf" if is_pdf_file(blob_name) else "image",
            "processed_at": message_body.get("timestamp", "")
        }
        
        await cosmos_container.upsert_item(doc)
        
        # Audit log: Successfully saved to database
        logger.info(f"Successfully saved processing result for {blob_name} to Cosmos DB")
        
        await receiver.complete_message(msg)
        
    except Exception as e:
        print(f"Error encountered: {e}. Abandoning message for retry.")
        
        # Audit log: Processing failed
        logger.error(f"Processing failed for message {msg}: {e}")
        
        await receiver.abandon_message(msg)
        return

async def main():
    async with ServiceBusClient(servicebus_fqdn, credential=credential) as sb_client:
        receiver = sb_client.get_queue_receiver(
            queue_name=servicebus_queue,
            max_lock_renewal_duration=120
        )
        async with receiver:
            while True:
                messages = await receiver.receive_messages(max_message_count=batch_size, max_wait_time=max_wait_time)
                if not messages:
                    await asyncio.sleep(1)
                    continue
                tasks = []
                for message in messages:
                    tasks.append(asyncio.create_task(process_message(message, receiver)))
                if tasks:
                    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())