# K6 Performance Test

This directory contains a k6 performance test for the AI image processing API. The test simulates a complete image processing workflow by uploading an image file and polling for processing results.

## What the Test Does

The performance test:
1. **Uploads an image** - Posts `example.jpg` to `/api/process` endpoint (expects 202 response)
2. **Gets processing URL** - Extracts the `results_url` from the upload response
3. **Polls for completion** - Repeatedly calls the results URL until processing is complete (expects 200 response)
4. **Validates responses** - Checks that all HTTP responses have expected status codes

## Test Configuration

- **Virtual Users**: 100 concurrent users
- **Duration**: 10 seconds
- **Graceful Stop**: 3 minutes (allows in-flight requests to complete)
- **Executor**: `constant-vus` (maintains constant number of virtual users)

## Prerequisites

Choose one of the following:

### Option 1: Docker (Recommended)
- Docker installed and running
- No additional dependencies required

### Option 2: Local k6
- k6 binary installed ([installation guide](https://k6.io/docs/get-started/installation/))

## Running the Test

### With Docker (Recommended)

1. **Build the container:**
   ```bash
   cd perftest
   docker build -t k6-perftest .
   ```

2. **Run against default URL:**
   ```bash
   docker run --rm k6-perftest
   ```

3. **Run against custom URL:**
   ```bash
   docker run --rm -e TEST_URL=https://your-api-endpoint.com k6-perftest
   ```

### With Local k6

1. **Navigate to perftest directory:**
   ```bash
   cd perftest
   ```

2. **Run against default URL:**
   ```bash
   k6 run script.js
   ```

3. **Run against custom URL:**
   ```bash
   TEST_URL=https://your-api-endpoint.com k6 run script.js
   ```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TEST_URL` | Target API base URL | `https://ca-api-processing-aiasync-gchk.yellowmoss-adbbb4fb.germanywestcentral.azurecontainerapps.io` |

### Test Parameters

To modify test parameters, edit `script.js` and adjust the `options` object:

```javascript
export const options = {
  scenarios: {
    default: {
      executor: 'constant-vus',
      vus: 100,           // Number of virtual users
      duration: '10s',    // Test duration
      gracefulStop: '3m', // Time to wait for requests to complete
    },
  },
};
```

## Understanding Results

### Key Metrics

- **http_req_duration**: Response time for HTTP requests
- **http_req_failed**: Percentage of failed HTTP requests
- **iterations**: Number of complete test iterations (upload + poll cycles)
- **vus**: Number of active virtual users

### Success Criteria

- `post status is 202`: Image upload requests should return HTTP 202
- `get status is 200`: Final status check should return HTTP 200
- Low error rate: Failed requests should be minimal

### Sample Output

```
     ✓ post status is 202
     ✓ get status is 200

     checks.........................: 100.00% ✓ 200       ✗ 0  
     data_received..................: 50 kB   5.0 kB/s
     data_sent......................: 25 kB   2.5 kB/s
     http_req_duration..............: avg=1.2s    min=200ms med=1.1s max=3.2s p(95)=2.8s
     http_req_failed................: 0.00%   ✓ 0        ✗ 150
     iterations.....................: 100     10/s
     vus............................: 100     min=100     max=100
```

## Files

- `script.js` - Main k6 test script
- `example.jpg` - Sample image file for testing
- `Dockerfile` - Container image definition for running tests
- `README.md` - This documentation

## Azure Deployment

This performance test can also be executed as an Azure Container App Job. See `terraform/container_app_job.perftest.tf` for the infrastructure configuration. The job is configured to:

- Run on-demand (manual trigger)
- Use 1 CPU and 2Gi memory
- Automatically inject the correct `TEST_URL` environment variable
- Timeout after 1 hour with up to 3 retry attempts

## Troubleshooting

### Common Issues

**Docker build fails:**
- Ensure Docker is running and you have internet connectivity
- Check that you're in the `perftest` directory

**Test fails with connection errors:**
- Verify the target API is running and accessible
- Check if the `TEST_URL` is correct
- Ensure network connectivity to the target endpoint

**High error rates:**
- The target API might be overwhelmed - consider reducing `vus` (virtual users)
- Check API logs for error details
- Verify the API can handle the expected load

**Image upload fails:**
- Ensure `example.jpg` exists in the same directory as `script.js`
- Check file permissions
- Verify the API accepts JPEG images