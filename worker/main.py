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
import io
from openai import AsyncAzureOpenAI
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.core.settings import settings
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
import PyPDF2

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

async def extract_text_from_pdf(pdf_data):
    """
    Extract text content from a PDF file.
    """
    try:
        # Use a thread pool to run PyPDF2 operations which are CPU-bound and blocking
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(executor, _extract_pdf_text, pdf_data)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return "Error extracting text from PDF"

def _extract_pdf_text(pdf_data):
    """
    Helper function to extract text from PDF data.
    This runs in a separate thread to avoid blocking the event loop.
    """
    pdf_text = ""
    try:
        with io.BytesIO(pdf_data) as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()
    except Exception as e:
        print(f"Error in _extract_pdf_text: {e}")
        return f"Error processing PDF: {str(e)}"
    
    return pdf_text

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
        message_body = json.loads(str(msg))
        blob_name = message_body.get("blob_name", "")
        id = message_body.get("id", "")
        file_type = message_body.get("file_type", "image")  # Default to image if not specified
        blob_client = storage_account_client.get_blob_client(storage_container, blob_name)
        print(f"Downloading data from {blob_name}")
        download_stream = await blob_client.download_blob()
        file_data = await download_stream.readall()
        
        if file_type == "pdf":
            # Process PDF file
            print(f"Processing PDF file {blob_name}")
            pdf_content = await extract_text_from_pdf(file_data)
            
            response = await client.chat.completions.create(
                model=azure_openai_deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Provide a concise summary of the PDF content."},
                    {"role": "user", "content": f"Summarize this PDF content: {pdf_content[:5000]}"}  # Limit text to avoid token limits
                ]
            )
        else:
            # Process image file
            print(f"Processing image file {blob_name}")
            encoded_image = base64.b64encode(file_data).decode("utf-8")
            
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
        
        print("OpenAI response:", f"{response.choices[0].message.content[:50]}...")
        print(f"Saving response to Cosmos DB to document with id {id}")
        doc = {
            "id": id,
            "ai_response": response.choices[0].message.content
        }
        await cosmos_container.upsert_item(doc)
        await receiver.complete_message(msg)
    except Exception as e:
        print(f"Error encountered: {e}. Abandoning message for retry.")
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