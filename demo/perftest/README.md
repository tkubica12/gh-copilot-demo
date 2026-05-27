# Performance Test (k6)

This directory contains a k6 performance test for the AI image processing API. The test simulates multiple users uploading images concurrently and polling for processing results.

## Test Scenario

The performance test validates the complete asynchronous image processing workflow:

1. **Upload Image** - POST multipart/form-data to `/api/process` endpoint
   - Uploads `example.jpg` to the processing API
   - Expects HTTP 202 (Accepted) response with a `results_url`

2. **Poll for Results** - GET from the `results_url` until processing completes
   - Polls the status endpoint every 1 second
   - Expects HTTP 202 (Processing) while work is in progress
   - Expects HTTP 200 (OK) when processing is complete

## Load Configuration

The test is configured to simulate realistic load:
- **Virtual Users (VUs)**: 100 concurrent users
- **Duration**: 10 seconds of sustained load
- **Graceful Stop**: 3 minutes to allow in-flight requests to complete

This configuration generates approximately 100 concurrent image uploads with subsequent polling, stress-testing both the upload and status APIs.

## Running the Test

### Prerequisites
- k6 installed locally, OR
- Docker for containerized execution

### Option 1: Run Locally with k6

Install k6 from [https://k6.io/docs/get-started/installation/](https://k6.io/docs/get-started/installation/)

```bash
cd demo/perftest

# Run against default URL (configured in script)
k6 run script.js

# Run against custom URL
k6 run -e TEST_URL=https://your-api-url.example.com script.js
```

### Option 2: Run with Docker

```bash
cd demo/perftest

# Build the image
docker build -t perftest .

# Run against default URL
docker run perftest

# Run against custom URL
docker run -e TEST_URL=https://your-api-url.example.com perftest
```

### Option 3: Azure Container Apps Job

The test is deployed as an Azure Container App Job via Terraform (see `deploy/terraform/container_app_job.perftest.tf`):
- Automatically configured with the deployed API URL
- Can be triggered manually or via CI/CD
- Resources: 1 CPU, 2Gi memory
- Timeout: 3600 seconds

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TEST_URL` | Base URL of the API to test | `https://ca-api-processing-aiasync-gchk.yellowmoss-adbbb4fb.germanywestcentral.azurecontainerapps.io` |

## Interpreting Results

k6 provides comprehensive metrics after test execution. Here's how to interpret them:

### Key Metrics

#### HTTP Request Metrics
- **`http_req_duration`** - Total request time (includes DNS, connection, TLS, sending, waiting, receiving)
  - **Target**: < 1s for upload (POST), < 200ms for status check (GET)
  - **p(90)**: 90th percentile - 90% of requests were faster than this
  - **p(95)**: 95th percentile - good indicator of "worst normal case"

- **`http_req_waiting`** - Time waiting for server response (TTFB - Time To First Byte)
  - Indicates server processing time
  - High values suggest backend performance issues

- **`http_reqs`** - Total number of HTTP requests generated
  - Should be > 100 for upload requests (100 VUs)
  - Will be much higher for status polling (depends on processing time)

#### Check Metrics
- **`checks`** - Percentage of successful checks
  - **Target**: 100% for production-ready systems
  - Failed checks indicate:
    - `post status is 202` failures: Upload API issues
    - `get status is 200` failures: Status API or processing issues

#### VU and Iteration Metrics
- **`vus`** - Number of active virtual users
  - Should match configured value (100)

- **`iterations`** - Number of completed test iterations
  - Each VU completes one full workflow (upload + poll until complete)
  - Lower than expected iterations suggests slow processing or failures

### Sample Output Interpretation

```
✓ post status is 202
✓ get status is 200

checks.........................: 100.00% ✓ 500    ✗ 0
data_received..................: 2.5 MB  250 kB/s
data_sent......................: 125 MB  12 MB/s
http_req_blocked...............: avg=1.2ms    min=1µs      med=3µs      max=123ms    p(90)=5µs      p(95)=10µs
http_req_connecting............: avg=1.1ms    min=0s       med=0s       max=120ms    p(90)=0s       p(95)=0s
http_req_duration..............: avg=2.3s     min=150ms    med=2.1s     max=5.2s     p(90)=3.8s     p(95)=4.2s
  { expected_response:true }...: avg=2.3s     min=150ms    med=2.1s     max=5.2s     p(90)=3.8s     p(95)=4.2s
http_req_failed................: 0.00%   ✓ 0      ✗ 500
http_req_receiving.............: avg=45µs     min=20µs     med=40µs     max=2ms      p(90)=70µs     p(95)=90µs
http_req_sending...............: avg=1.2ms    min=10µs     med=30µs     max=150ms    p(90)=5ms      p(95)=10ms
http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
http_req_waiting...............: avg=2.3s     min=149ms    med=2.1s     max=5.2s     p(90)=3.8s     p(95)=4.2s
http_reqs......................: 500     50/s
iteration_duration.............: avg=5.5s     min=2.1s     med=5.2s     max=8.3s     p(90)=7.1s     p(95)=7.8s
iterations.....................: 100     10/s
vus............................: 100     min=100  max=100
vus_max........................: 100     min=100  max=100
```

**Analysis:**
- ✅ **All checks passed** (100%) - Both upload and status checks succeeded
- ✅ **No failed requests** (http_req_failed: 0.00%)
- ⚠️ **Average request duration: 2.3s** - Acceptable for async processing but includes polling time
- ✅ **500 total requests** - 100 uploads + 400 status checks (4 polls per upload on average)
- ⚠️ **95th percentile: 4.2s** - Most requests complete within acceptable time
- ✅ **Throughput: 50 req/s** - System handling load well

### Red Flags to Watch For

🚨 **Failed Checks** (`checks` < 100%)
- Indicates API errors or unexpected responses
- Review error logs in Application Insights

🚨 **High Request Failure Rate** (`http_req_failed` > 0%)
- 5xx errors suggest backend issues
- 4xx errors suggest client/test configuration problems

🚨 **Slow Response Times** (`http_req_duration` p(95) > 10s)
- May indicate resource contention
- Check CPU/memory metrics in Azure Monitor

🚨 **Low Iteration Count** (< expected VUs)
- VUs unable to complete iterations within test duration
- Suggests very slow processing or deadlocks

## Files

- **`script.js`** - k6 test script implementing the load test
- **`example.jpg`** - Sample image used for testing (1.2 MB)
- **`Dockerfile`** - Container image for running the test in Azure or CI/CD

## Customizing the Test

To modify load parameters, edit `script.js`:

```javascript
export const options = {
  scenarios: {
    default: {
      executor: 'constant-vus',  // Constant number of VUs
      vus: 100,                   // Number of concurrent users
      duration: '10s',            // How long to run the test
      gracefulStop: '3m',         // Time to wait for in-flight requests
    },
  },
};
```

### Alternative Executors

k6 supports various executors for different test scenarios:
- **`constant-vus`** - Constant number of VUs (current configuration)
- **`ramping-vus`** - Gradually increase/decrease VUs (ramp-up/ramp-down)
- **`constant-arrival-rate`** - Constant request rate regardless of response time
- **`ramping-arrival-rate`** - Gradually change request rate

Example ramping configuration:
```javascript
ramping-vus: {
  executor: 'ramping-vus',
  startVUs: 0,
  stages: [
    { duration: '30s', target: 50 },   // Ramp up to 50 VUs
    { duration: '1m', target: 100 },   // Ramp up to 100 VUs
    { duration: '2m', target: 100 },   // Stay at 100 VUs
    { duration: '30s', target: 0 },    // Ramp down
  ],
  gracefulRampDown: '30s',
}
```

## Related Components

This test validates the following services:
- **api-processing** (`src/api-processing`) - Receives image uploads and queues them
- **worker** (`src/worker`) - Processes images using Azure OpenAI
- **api-status** (`src/api-status`) - Provides status and results retrieval

See the main [README.md](../../README.md) for the full system architecture.
