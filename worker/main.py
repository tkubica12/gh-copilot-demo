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
import logging
import tempfile

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

# Configure logging for auditing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
audit_logger = logging.getLogger('audit')

# Initialize MarkItDown for PDF processing
md = MarkItDown()

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

async def process_message(msg, receiver):
    """
    Process a single message and then complete it.
    """
    try:
        print(f"Processing message: {msg}")
        audit_logger.info(f"Starting processing for message: {msg}")
        
        message_body = json.loads(str(msg))
        blob_name = message_body.get("blob_name", "")
        id = message_body.get("id", "")
        file_type = message_body.get("file_type", "image")  # default to image for backward compatibility
        
        audit_logger.info(f"Processing {file_type} file: {blob_name} with ID: {id}")
        
        blob_client = storage_account_client.get_blob_client(storage_container, blob_name)
        print(f"Downloading {file_type} data from {blob_name}")
        download_stream = await blob_client.download_blob()
        file_data = await download_stream.readall()
        
        ai_response = ""
        
        if file_type == "pdf":
            # Process PDF using markitdown
            print(f"Extracting text from PDF {blob_name}...")
            audit_logger.info(f"Extracting text from PDF: {blob_name}")
            
            # Save PDF to temporary file for markitdown processing
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name
            
            try:
                # Extract text from PDF
                result = md.convert(temp_file_path)
                pdf_text = result.text_content
                print(f"Extracted {len(pdf_text)} characters from PDF")
                audit_logger.info(f"Extracted {len(pdf_text)} characters from PDF {blob_name}")
                
                # Send text to OpenAI for summarization
                print(f"Sending PDF text to OpenAI for summarization...")
                response = await client.chat.completions.create(
                    model=azure_openai_deployment_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that summarizes documents. Provide a clear, concise summary of the main points."},
                        {"role": "user", "content": f"Please summarize the following document:\n\n{pdf_text[:4000]}"}  # Limit text to avoid token limits
                    ]
                )
                ai_response = response.choices[0].message.content
                audit_logger.info(f"Generated summary for PDF {blob_name}")
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        else:
            # Process image (existing logic)
            encoded_image = base64.b64encode(file_data).decode("utf-8")
            print(f"Sending image {blob_name} to OpenAI...")
            audit_logger.info(f"Analyzing image: {blob_name}")
            
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
            audit_logger.info(f"Generated description for image {blob_name}")
        
        print("OpenAI response:", f"{ai_response[:50]}...")
        print(f"Saving response to Cosmos DB to document with id {id}")
        
        # Save to Cosmos DB with additional metadata for auditing
        doc = {
            "id": id,
            "ai_response": ai_response,
            "file_type": file_type,
            "blob_name": blob_name,
            "processed_at": None  # Cosmos DB will add _ts automatically
        }
        await cosmos_container.upsert_item(doc)
        audit_logger.info(f"Saved processing result for {file_type} {blob_name} to Cosmos DB with ID: {id}")
        
        await receiver.complete_message(msg)
        audit_logger.info(f"Successfully completed processing for {file_type} {blob_name}")
        
    except Exception as e:
        print(f"Error encountered: {e}. Abandoning message for retry.")
        audit_logger.error(f"Error processing message for blob {blob_name}: {str(e)}")
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