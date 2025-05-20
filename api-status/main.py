import os
import dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.identity.aio import DefaultAzureCredential
from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.core.settings import settings
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator, metrics

app = FastAPI(title="AI Results", description="API to get processed results")

# Load environment variables
dotenv.load_dotenv()

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        raise EnvironmentError(f"{var_name} environment variable is not set")
    return value

cosmos_account_url = get_env_var("COSMOS_ACCOUNT_URL")
cosmos_db_name = get_env_var("COSMOS_DB_NAME")
cosmos_container_name = get_env_var("COSMOS_CONTAINER_NAME")
appinsights_connection_string = get_env_var("APPLICATIONINSIGHTS_CONNECTION_STRING")
retry_after = get_env_var("RETRY_AFTER")

# Configure Azure Monitor
appinsights_connection_string = get_env_var("APPLICATIONINSIGHTS_CONNECTION_STRING")
resource = Resource.create({SERVICE_NAME: "Status API Service"})
configure_azure_monitor(connection_string=appinsights_connection_string, resource=resource)
settings.tracing_implementation = "opentelemetry"
FastAPIInstrumentor.instrument_app(app)

# Configure Prometheus metrics
RESULTS_FOUND_COUNTER = Counter(
    "api_status_results_found_total",
    "Total number of results found",
)
RESULTS_PENDING_COUNTER = Counter(
    "api_status_results_pending_total",
    "Total number of results that are still pending",
)
STATUS_REQUEST_PROCESSING_TIME = Histogram(
    "api_status_request_processing_seconds",
    "Time spent processing status requests",
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
)
ERROR_COUNTER = Counter(
    "api_status_errors_total",
    "Total number of errors encountered",
)

# Prometheus metrics endpoint
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_app_router_include=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    inprogress_name="api_status_inprogress",
    inprogress_help="Inprogress requests in Status API",
)
instrumentator.add(metrics.latency(metric_name="api_status_request_latency_seconds"))
instrumentator.instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")

# CORS
origins = [os.environ.get("CORS_ORIGIN", "*")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get CosmosDB client
credential = DefaultAzureCredential()
cosmos_client = CosmosClient(cosmos_account_url, credential=credential)
database = cosmos_client.get_database_client(cosmos_db_name)
container = database.get_container_client(cosmos_container_name)

@app.get("/", include_in_schema=False)
def get_openapi_spec():
    return app.openapi()

@app.get(
    "/api/status/{guid}",
    response_class=JSONResponse,
    responses={
        200: {
            "description": "Result found",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "status": "completed",
                        "data": {
                            "result": "some result data"
                        }
                    }
                }
            }
        },
        202: {
            "description": "Processing, please retry after some time",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Processing, please retry after some time."
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error message"
                    }
                }
            }
        }
    }
)
async def get_results(guid: str):
    # Use Prometheus histogram to track processing time
    with STATUS_REQUEST_PROCESSING_TIME.time():
        try:
            query = "SELECT * FROM c WHERE c.id = @id"
            parameters = [{"name": "@id", "value": guid}]
            items = [item async for item in container.query_items(query=query, parameters=parameters, partition_key=guid)]
            if items:
                item = items[0]
                response = {
                    "id": item["id"],
                    "status": "completed",
                    "data": {
                        "result": item["ai_response"]
                    }
                }
                # Increment results found counter
                RESULTS_FOUND_COUNTER.inc()
                return JSONResponse(status_code=200, content=response)
            else:
                # Increment results pending counter
                RESULTS_PENDING_COUNTER.inc()
                return JSONResponse(status_code=202, headers={"Retry-After": retry_after}, content={"message": "Processing, please retry after some time."})
        except Exception as e:
            # Increment error counter on exception
            ERROR_COUNTER.inc()
            raise HTTPException(status_code=500, detail=str(e))
