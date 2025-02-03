# Using async architecture in AI applications
In order to provide scalable and highly reliable solution that incorporates AI in user experience workflow let's demonstrate asynchronous microservices solution:

1. User submits image processing request from frontend to processing API
2. Processing API stores image in storage and sends message to processing queue and right after that responds to user with request id and url used to check processing status and get results.
3. Worker service listens to processing queue and processes image. After processing is done it stores results in CosmosDB.
4. Status service takes ID from frontend and either returns 202 if processing is not done yet or 200 with results if processing is done.

### Components
- Azure Container Apps for hosting microservices and providing ingress and autoscaling
- Azure Storage for storing images
- Azure Service Bus for processing queue
- Azure CosmosDB for storing results
- k6 perftest running as Azure Container Apps Job

### Benefits
- Azure Container Apps provides autoscaling and load balancing based on user requests and length of processing queue
- Each microservice can be scaled independently
- No long synchronous calls that can timeout, fail, limit scalability and reliability
- Built-in retry mechanism for processing queue and for frontend to check processing status
- Improved fault isolation, as issues in one microservice do not affect the entire system
- Easier to update and deploy individual microservices without downtime
- Enhanced flexibility in technology stack, allowing different microservices to use the most suitable tools and languages

### TODO
- Add authentication and authorization
- Better OTEL correlations (processing id, chat requests correlations)