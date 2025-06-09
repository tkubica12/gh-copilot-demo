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
import tempfile
import datetime

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
markitdown = MarkItDown()

async def process_message(msg, receiver):
    """
    Process a single message and then complete it.
    """
    try:
        print(f"Processing message: {msg}")
        message_body = json.loads(str(msg))
        blob_name = message_body.get("blob_name", "")
        id = message_body.get("id", "")
        file_type = message_body.get("file_type", "image")  # Default to image for backward compatibility
        original_filename = message_body.get("original_filename", "")
        content_type = message_body.get("content_type", "")
        
        # Audit logging for forensics
        processing_start = datetime.datetime.utcnow().isoformat()
        print(f"[AUDIT] Started processing file {blob_name} (original: {original_filename}) of type {file_type} at {processing_start}")
        
        blob_client = storage_account_client.get_blob_client(storage_container, blob_name)
        print(f"Downloading file data from {blob_name}")
        download_stream = await blob_client.download_blob()
        file_data = await download_stream.readall()
        
        if file_type == "pdf":
            # Process PDF file
            ai_response = await process_pdf(file_data, blob_name)
        else:
            # Process image file (existing logic)
            ai_response = await process_image(file_data, blob_name)
        
        processing_end = datetime.datetime.utcnow().isoformat()
        print(f"[AUDIT] Completed processing file {blob_name} at {processing_end}")
        print(f"Saving response to Cosmos DB to document with id {id}")
        
        # Enhanced document structure with auditing information
        doc = {
            "id": id,
            "ai_response": ai_response,
            "file_type": file_type,
            "original_filename": original_filename,
            "blob_name": blob_name,
            "content_type": content_type,
            "processing_start": processing_start,
            "processing_end": processing_end,
            "audit_trail": {
                "processed_by": "AI Worker Service",
                "processing_duration_iso": processing_end,
                "file_size_bytes": len(file_data)
            }
        }
        await cosmos_container.upsert_item(doc)
        await receiver.complete_message(msg)
        print(f"[AUDIT] Successfully stored processing results for {blob_name}")
        
    except Exception as e:
        print(f"[AUDIT] Error processing message for blob {blob_name}: {e}")
        print(f"Error encountered: {e}. Abandoning message for retry.")
        await receiver.abandon_message(msg)
        return

async def process_pdf(file_data, blob_name):
    """
    Process PDF file using markitdown and get summarization from OpenAI
    """
    try:
        print(f"Extracting text from PDF {blob_name} using markitdown...")
        
        # Write PDF data to temporary file for markitdown processing
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(file_data)
            temp_file_path = temp_file.name
        
        try:
            # Extract text using markitdown
            result = markitdown.convert(temp_file_path)
            extracted_text = result.text_content
            
            print(f"Extracted {len(extracted_text)} characters from PDF")
            
            # Send extracted text to OpenAI for summarization
            print(f"Sending PDF text from {blob_name} to OpenAI for summarization...")
            
            response = await client.chat.completions.create(
                model=azure_openai_deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides concise and accurate summaries of documents. Focus on key points, main topics, and important details."},
                    {"role": "user", "content": f"Please provide a comprehensive summary of the following document content:\n\n{extracted_text}"}
                ]
            )
            
            ai_summary = response.choices[0].message.content
            print("OpenAI summary response:", f"{ai_summary[:100]}...")
            return ai_summary
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
                
    except Exception as e:
        print(f"Error processing PDF {blob_name}: {e}")
        raise

async def process_image(file_data, blob_name):
    """
    Process image file using OpenAI vision (existing logic)
    """
    try:
        encoded_image = base64.b64encode(file_data).decode("utf-8")
        print(f"Sending image {blob_name} to OpenAI...")
        
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
        
        ai_response = response.choices[0].message.content
        print("OpenAI response:", f"{ai_response[:50]}...")
        return ai_response
        
    except Exception as e:
        print(f"Error processing image {blob_name}: {e}")
        raise

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