# AI Image Processing Demo - Architecture Guidelines

## Overview

This document outlines the architectural patterns, design principles, and coding guidelines for the AI Image Processing Demo application. The system demonstrates modern cloud-native microservices architecture on Azure, implementing asynchronous processing, event-driven communication, and scalable containerized services.

## Architecture Patterns

### 1. Microservices Architecture

The application follows a microservices pattern with clear separation of concerns:

- **API Processing Service**: Handles image uploads and initiates processing workflows
- **Worker Service**: Performs AI-powered image analysis using Azure OpenAI
- **API Status Service**: Provides processing status and results retrieval
- **Frontend Service**: User interface for image upload and result viewing

#### Key Principles:
- Each service has a single responsibility
- Services communicate through well-defined APIs and message queues
- Independent deployment and scaling capabilities
- Fault isolation between services

### 2. Event-Driven Architecture

The system implements asynchronous, event-driven communication patterns:

```
Frontend → API Processing → Service Bus → Worker → Cosmos DB ← API Status
```

#### Benefits:
- Loose coupling between services
- Improved resilience and fault tolerance
- Natural load distribution
- Scalability through queue-based processing

### 3. Serverless and Container-First Approach

All services are containerized and deployed using Azure Container Apps:

- **Serverless scaling**: Automatic scale-to-zero and scale-out based on demand
- **Event-driven scaling**: Worker service scales based on Service Bus queue depth
- **Resource efficiency**: Pay only for actual usage
- **Simplified operations**: Managed infrastructure with built-in monitoring

## Technology Stack

### Backend Services (Python + FastAPI)
- **Framework**: FastAPI for high-performance async APIs
- **Authentication**: Azure Active Directory with Managed Identity
- **Environment Management**: python-dotenv for configuration
- **Validation**: Pydantic models for request/response validation

### Frontend (React)
- **Framework**: React with functional components and hooks
- **HTTP Client**: Axios for API communication
- **UI Components**: Custom CSS with modern styling
- **State Management**: React useState for local state

### Infrastructure (Terraform)
- **Infrastructure as Code**: Terraform for all Azure resources
- **Modular Design**: Resource-specific files (storage.tf, service_bus.tf, etc.)
- **Environment Separation**: Variable-driven configuration
- **Security-First**: RBAC, managed identities, and principle of least privilege

## Core Design Principles

### 1. Security by Design

#### Authentication & Authorization
- **Managed Identity**: All services use Azure Managed Identity for authentication
- **RBAC**: Fine-grained role-based access control for each service
- **No Secrets in Code**: All sensitive data stored in environment variables
- **OAuth Authentication**: Storage accounts use OAuth instead of access keys

#### Network Security
- **HTTPS Only**: All communication encrypted in transit
- **CORS Configuration**: Properly configured cross-origin resource sharing
- **Private Networking**: Services communicate within Azure virtual networks

### 2. Observability & Monitoring

#### Distributed Tracing
```python
# Configure Azure Monitor with OpenTelemetry
resource = Resource.create({SERVICE_NAME: "Service Name"})
configure_azure_monitor(connection_string=appinsights_connection_string, resource=resource)
settings.tracing_implementation = "opentelemetry"
```

#### Monitoring Stack
- **Application Insights**: Centralized logging and application performance monitoring
- **OpenTelemetry**: Distributed tracing across all services
- **Service-Specific Instrumentation**: Custom instrumentation for FastAPI and OpenAI calls

### 3. Resilience & Error Handling

#### Retry Patterns
- **Service Bus**: Built-in retry logic with dead letter queues
- **Message Processing**: Graceful error handling with message abandonment
- **API Resilience**: Proper HTTP status codes and error responses

#### Graceful Degradation
- **Status Polling**: Clients retry with exponential backoff
- **Circuit Breaker Pattern**: Failed requests don't cascade
- **Resource Limits**: Configurable timeouts and batch sizes

## Service Implementation Guidelines

### 1. Environment Configuration

All services follow a consistent pattern for environment variable handling:

```python
def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        raise EnvironmentError(f"{var_name} environment variable is not set")
    return value
```

#### Configuration Principles:
- **Fail Fast**: Services fail startup if required configuration is missing
- **Type Safety**: Convert environment variables to appropriate types (int, float, bool)
- **Documentation**: Clear variable descriptions in Terraform variables
- **Defaults**: Sensible defaults for non-sensitive configuration

### 2. API Design Standards

#### FastAPI Implementation
```python
app = FastAPI(title="Service Name", description="Service Description")

# CORS Configuration
origins = [os.environ.get("CORS_ORIGIN", "*")]
app.add_middleware(CORSMiddleware, ...)

# OpenAPI Documentation
@app.get("/", include_in_schema=False)
def get_openapi_spec():
    return app.openapi()
```

#### API Design Principles:
- **OpenAPI Documentation**: Comprehensive API documentation with examples
- **HTTP Status Codes**: Proper use of status codes (202 for async processing, 200 for completion)
- **Response Headers**: Include retry-after headers for polling endpoints
- **Error Handling**: Consistent error response format across all APIs

### 3. Azure Client Management

#### Consistent Client Initialization
```python
# Use DefaultAzureCredential for authentication
credential = DefaultAzureCredential()

# Initialize Azure service clients
storage_client = BlobServiceClient(account_url=storage_url, credential=credential)
servicebus_client = ServiceBusClient(servicebus_fqdn, credential=credential)
cosmos_client = CosmosClient(cosmos_url, credential=credential)
```

#### Client Management Principles:
- **Managed Identity**: All Azure clients use DefaultAzureCredential
- **Resource Efficiency**: Reuse clients across requests
- **Async Operations**: Use async clients where available (aio variants)
- **Connection Pooling**: Leverage built-in connection pooling

### 4. Message Processing Patterns

#### Service Bus Message Handling
```python
async def process_message(msg, receiver):
    try:
        # Process message
        await process_business_logic(msg)
        await receiver.complete_message(msg)
    except Exception as e:
        print(f"Error: {e}")
        await receiver.abandon_message(msg)
```

#### Message Processing Principles:
- **Idempotency**: Messages can be processed multiple times safely
- **Error Isolation**: Failed messages don't block others
- **Batch Processing**: Process multiple messages concurrently
- **Dead Letter Handling**: Failed messages move to dead letter queue

## Infrastructure Patterns

### 1. Terraform Organization

#### File Structure
```
terraform/
├── main.tf                    # Resource groups and base resources
├── variables.tf               # Input variables with descriptions
├── locals.tf                  # Computed values and naming conventions
├── providers.tf               # Provider configuration
├── storage.tf                 # Storage account and containers
├── service_bus.tf             # Service Bus namespace and queues
├── cosmos.tf                  # Cosmos DB account and containers
├── rbac.tf                    # Role assignments and permissions
├── monitoring.tf              # Application Insights and Log Analytics
├── container_app.*.tf         # Container Apps (one per service)
└── container_app_env.tf       # Container App Environment
```

#### Terraform Principles:
- **Resource Separation**: Group related resources in dedicated files
- **Local Values**: Use locals for computed values and naming conventions
- **Variable Stability**: Variables define stable interfaces for modules
- **RBAC Separation**: Dedicated file for all role assignments

### 2. Naming Conventions

#### Resource Naming Pattern
```hcl
locals {
  base_name = "${var.prefix}-${random_string.main.result}"
  base_name_nodash = "${var.prefix}${random_string.main.result}"
}

# Examples:
# "sb-ghdemo-abc1"     (Service Bus)
# "cosmos-ghdemo-abc1" (Cosmos DB)
# "stghdemoadbc1"      (Storage Account - no dashes)
```

#### Naming Principles:
- **Consistent Prefixes**: Use standard Azure resource type prefixes
- **Environment Suffix**: Include environment/randomization for uniqueness
- **Length Constraints**: Handle Azure resource name length limitations
- **DNS Compatibility**: Use lowercase and avoid special characters

### 3. Security and RBAC

#### Managed Identity Pattern
```hcl
resource "azurerm_user_assigned_identity" "main" {
  name                = "${local.base_name}-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

# Assign minimal required permissions
resource "azurerm_role_assignment" "app_storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}
```

#### Security Principles:
- **Principle of Least Privilege**: Grant minimal required permissions
- **Managed Identities**: Avoid service principals and access keys
- **Separate Identities**: Use different identities for different access patterns
- **Custom Roles**: Create custom Cosmos DB roles for fine-grained access

## Container and Deployment Patterns

### 1. Container Design

#### Dockerfile Standards
```dockerfile
# Multi-stage builds for frontend
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
```

#### Container Principles:
- **Multi-stage Builds**: Reduce final image size
- **Official Base Images**: Use official, maintained base images
- **Minimal Images**: Use Alpine or slim variants where possible
- **Non-root Users**: Run containers as non-root users when possible

### 2. Container App Configuration

#### Scaling and Resource Management
```hcl
scale = {
  minReplicas     = 1
  maxReplicas     = 5
  pollingInterval = 5
  cooldownPeriod  = 60
  rules = [
    {
      name = "queue-scaling"
      custom = {
        type = "azure-servicebus"
        metadata = {
          queueName    = azurerm_servicebus_queue.main.name
          namespace    = azurerm_servicebus_namespace.main.name
          messageCount = "5"
        }
      }
    }
  ]
}
```

#### Deployment Principles:
- **Autoscaling**: Configure appropriate scaling rules for each service
- **Resource Limits**: Set CPU and memory limits based on service requirements
- **Health Checks**: Implement readiness and liveness probes
- **Environment Injection**: Use Terraform to inject environment variables

## Data Management Patterns

### 1. Cosmos DB Design

#### Document Structure
```json
{
  "id": "uuid-generated-id",
  "ai_response": "processed result text",
  "_ts": "system-generated-timestamp"
}
```

#### Data Principles:
- **Partition Strategy**: Use document ID as partition key for even distribution
- **Serverless Billing**: Use serverless mode for variable workloads
- **Session Consistency**: Use session consistency for most scenarios
- **Upsert Operations**: Use upsert for idempotent operations

### 2. Blob Storage Organization

#### Blob Naming Convention
```
{guid}.jpg
```

#### Storage Principles:
- **Unique Naming**: Use GUIDs to prevent naming conflicts
- **Container Organization**: Separate containers for different data types
- **Lifecycle Management**: Implement blob lifecycle policies for cost optimization
- **Access Patterns**: Use appropriate access tiers (hot, cool, archive)

## Frontend Development Guidelines

### 1. React Component Design

#### State Management Pattern
```javascript
function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle');
  const [result, setResult] = useState('');
  
  // Component implementation
}
```

#### Frontend Principles:
- **Functional Components**: Use functional components with hooks
- **Local State**: Use local state for UI-specific data
- **Error Handling**: Gracefully handle API errors and network issues
- **User Feedback**: Provide clear feedback during async operations

### 2. API Integration

#### Polling Pattern
```javascript
const pollStatus = async (url) => {
  const response = await axios.get(url);
  if (response.status === 200) {
    // Processing complete
    setResult(response.data.data.result);
  } else if (response.status === 202) {
    // Continue polling
    setTimeout(() => pollStatus(url), 5000);
  }
};
```

#### Integration Principles:
- **Exponential Backoff**: Implement proper retry logic
- **Loading States**: Show appropriate loading indicators
- **Responsive Design**: Ensure mobile-friendly UI
- **Accessibility**: Follow web accessibility guidelines

## Development and Operations

### 1. Development Workflow

#### Local Development
- Use Docker Compose for local development environments
- Environment variable templates for easy setup
- Mock services for external dependencies during development

#### Testing Strategy
- Unit tests for business logic
- Integration tests for API endpoints
- End-to-end tests for critical user workflows
- Performance testing with load generation tools

### 2. CI/CD Pipeline

#### Build Process
- Automated container image building
- Security scanning of container images
- Dependency vulnerability scanning
- Terraform plan validation

#### Deployment Process
- Infrastructure deployment with Terraform
- Blue-green deployments for zero-downtime updates
- Automated rollback on deployment failures
- Environment-specific configuration management

## Monitoring and Alerting

### 1. Key Metrics

#### Application Metrics
- Request latency and throughput
- Error rates and types
- Queue depth and processing time
- AI service response times

#### Infrastructure Metrics
- Container resource utilization
- Database performance metrics
- Storage account performance
- Network latency and bandwidth

### 2. Alerting Strategy

#### Critical Alerts
- Service availability issues
- High error rates
- Queue depth thresholds
- Resource exhaustion

#### Notification Channels
- Email notifications for critical issues
- Slack integration for team notifications
- Dashboard monitoring for real-time visibility

## Conclusion

This architecture demonstrates modern cloud-native development practices with a focus on:

- **Scalability**: Event-driven architecture with auto-scaling capabilities
- **Reliability**: Fault tolerance and graceful error handling
- **Security**: Zero-trust security model with managed identities
- **Observability**: Comprehensive monitoring and distributed tracing
- **Maintainability**: Clean code structure and infrastructure as code

The patterns and guidelines outlined in this document should be followed for all services in the system to ensure consistency, maintainability, and operational excellence.