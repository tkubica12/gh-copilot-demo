# K6 Performance Test for Image Processing API

This directory contains a k6 load testing script designed to test the performance and reliability of the image processing API under various load conditions.

## Overview

The performance test simulates concurrent users uploading images to the processing API and polling for results. It validates the entire asynchronous workflow:

1. **Upload**: POST an image file to `/api/process`
2. **Polling**: GET the status from the returned results URL until processing completes
3. **Validation**: Verify both the upload (202 status) and final result (200 status)

## Prerequisites

### Local Installation

To run the test locally, you need to install k6:

**macOS (Homebrew):**
```bash
brew install k6
```

**Windows (Chocolatey):**
```bash
choco install k6
```

**Linux (Debian/Ubuntu):**
```bash
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

For other platforms, see [k6 installation docs](https://k6.io/docs/getting-started/installation/).

### Docker Installation (Alternative)

If you prefer to use Docker, you don't need to install k6 locally. Just ensure Docker is installed and running.

## Test Scenarios

The test currently implements one scenario:

### Default Scenario: Constant Load
- **Executor**: `constant-vus` (constant virtual users)
- **Virtual Users**: 100 concurrent users
- **Duration**: 10 seconds
- **Graceful Stop**: 3 minutes (allows in-flight requests to complete)

Each virtual user performs the following actions in a loop:
1. Upload an image file (`example.jpg`) via POST to `/api/process`
2. Receive a 202 Accepted response with a `results_url`
3. Poll the `results_url` every 1 second until receiving a 200 OK response
4. Validate both the upload and result retrieval were successful

## Running the Test

### Option 1: Run Locally with k6

From the `demo/perftest` directory:

```bash
# Test against default URL (configured in script)
k6 run script.js

# Test against custom URL
k6 run -e TEST_URL=https://your-api-endpoint.com script.js
```

### Option 2: Run with Docker

Build the Docker image:
```bash
docker build -t perftest .
```

Run the test:
```bash
# Test against default URL
docker run perftest

# Test against custom URL
docker run -e TEST_URL=https://your-api-endpoint.com perftest
```

## Configuration Options

### Environment Variables

- **TEST_URL**: The base URL of the API to test (default: configured Azure Container Apps URL)
  ```bash
  k6 run -e TEST_URL=https://your-api.com script.js
  ```

### Modifying Test Scenarios

Edit `script.js` and modify the `options.scenarios` object:

**Increase concurrent users:**
```javascript
scenarios: {
  default: {
    executor: 'constant-vus',
    vus: 200,  // Change from 100 to 200
    duration: '10s',
    gracefulStop: '3m',
  },
}
```

**Extend test duration:**
```javascript
scenarios: {
  default: {
    executor: 'constant-vus',
    vus: 100,
    duration: '5m',  // Change from 10s to 5 minutes
    gracefulStop: '3m',
  },
}
```

**Ramp up load gradually:**
```javascript
scenarios: {
  rampup: {
    executor: 'ramping-vus',
    startVUs: 0,
    stages: [
      { duration: '1m', target: 50 },   // Ramp up to 50 users over 1 minute
      { duration: '3m', target: 50 },   // Stay at 50 for 3 minutes
      { duration: '1m', target: 100 },  // Ramp up to 100 users
      { duration: '3m', target: 100 },  // Stay at 100 for 3 minutes
      { duration: '1m', target: 0 },    // Ramp down to 0
    ],
    gracefulStop: '3m',
  },
}
```

For more scenario options, see [k6 executors documentation](https://k6.io/docs/using-k6/scenarios/executors/).

## Interpreting Results

### Key Metrics

When the test completes, k6 displays a summary with important metrics:

#### HTTP Metrics
- **http_reqs**: Total number of HTTP requests made
  - Higher is better (indicates throughput)
- **http_req_duration**: Time spent on HTTP requests
  - **avg**: Average request duration
  - **min/max**: Fastest and slowest requests
  - **med (p50)**: 50% of requests completed within this time
  - **p90/p95/p99**: 90th, 95th, and 99th percentile response times
  - Lower is better (faster responses)

#### Checks
- **checks**: Percentage of successful validations
  - Shows "post status is 202" success rate
  - Shows "get status is 200" success rate
  - Should be close to 100%

#### Iterations
- **iterations**: Number of complete test cycles (upload + polling)
  - Each iteration is one complete user workflow
  - **iteration_duration**: Time to complete one full cycle

#### Virtual Users
- **vus**: Number of virtual users active during the test
- **vus_max**: Maximum number of VUs configured

### Example Output

```
     ✓ post status is 202
     ✓ get status is 200

     checks.........................: 100.00% ✓ 2000      ✗ 0
     data_received..................: 5.2 MB  520 kB/s
     data_sent......................: 127 MB  12.7 MB/s
     http_req_blocked...............: avg=1.2ms    min=1µs     med=4µs     max=234ms   p(90)=6µs     p(95)=8µs
     http_req_connecting............: avg=459µs    min=0s      med=0s      max=89ms    p(90)=0s      p(95)=0s
     http_req_duration..............: avg=2.1s     min=234ms   med=1.8s    max=12s     p(90)=4.2s    p(95)=5.8s
     http_req_failed................: 0.00%   ✓ 0         ✗ 3000
     http_req_receiving.............: avg=142µs    min=23µs    med=98µs    max=15ms    p(90)=234µs   p(95)=389µs
     http_req_sending...............: avg=1.8ms    min=9µs     med=45µs    max=234ms   p(90)=2.1ms   p(95)=8.9ms
     http_req_tls_handshaking.......: avg=678µs    min=0s      med=0s      max=156ms   p(90)=0s      p(95)=0s
     http_req_waiting...............: avg=2.1s     min=233ms   med=1.8s    max=12s     p(90)=4.2s    p(95)=5.8s
     http_reqs......................: 3000    300/s
     iteration_duration.............: avg=3.5s     min=1.2s    med=3.1s    max=25s     p(90)=6.2s    p(95)=8.4s
     iterations.....................: 1000    100/s
     vus............................: 100     min=100     max=100
     vus_max........................: 100     min=100     max=100
```

### What to Look For

**Good Performance Indicators:**
- ✅ Checks at or near 100%
- ✅ http_req_failed at 0%
- ✅ p95 response times within acceptable limits (e.g., < 5 seconds)
- ✅ Consistent response times (small difference between p50 and p95)

**Performance Issues:**
- ❌ Failed checks (< 100%)
- ❌ High http_req_failed percentage
- ❌ High p95 or p99 response times
- ❌ Large gap between p50 and p99 (indicates inconsistent performance)
- ❌ Errors in console output

### Performance Tuning Insights

- **High iteration_duration**: The polling loop is taking a long time, possibly due to slow backend processing
- **High http_req_duration on POST**: Image upload or initial processing is slow
- **High http_req_duration on GET**: Status endpoint is slow or polling is inefficient
- **Failed checks**: Backend errors, timeouts, or resource exhaustion

## Troubleshooting

### Error: "Failed to upload image"
- **Cause**: The API returned a non-202 status code
- **Solution**: Check that the TEST_URL is correct and the API is running
- **Debug**: Review the console output for the actual status code and response body

### Error: "Failed to parse response body"
- **Cause**: The API response is not valid JSON
- **Solution**: Verify the API is returning the expected response format with a `results_url` field

### Error: "ERRO[0000] open ./example.jpg: no such file or directory"
- **Cause**: The script can't find the example.jpg file
- **Solution**: Run k6 from the `demo/perftest` directory or update the file path in the script

### High Failure Rate
- **Cause**: Backend can't handle the load, network issues, or resource limits
- **Solution**: 
  - Reduce the number of virtual users
  - Increase backend resources
  - Check backend logs for errors
  - Verify network connectivity

### Timeouts During Polling
- **Cause**: Backend processing is taking longer than expected
- **Solution**: 
  - Increase `gracefulStop` duration in the scenario
  - Optimize backend processing time
  - Consider adjusting the polling interval

## File Structure

```
demo/perftest/
├── Dockerfile       # Docker image for running the test
├── example.jpg      # Sample image used in tests
├── script.js        # Main k6 test script
└── README.md        # This file
```

## Next Steps

1. **Baseline Testing**: Run the test against a known-good environment to establish baseline metrics
2. **Load Testing**: Gradually increase VUs to find the breaking point
3. **Stress Testing**: Push the system beyond normal capacity to see how it fails
4. **Soak Testing**: Run at moderate load for extended periods (hours) to find memory leaks
5. **Spike Testing**: Suddenly increase/decrease load to test auto-scaling

## Additional Resources

- [k6 Documentation](https://k6.io/docs/)
- [k6 Test Types](https://k6.io/docs/test-types/introduction/)
- [k6 Metrics Reference](https://k6.io/docs/using-k6/metrics/)
- [k6 Thresholds](https://k6.io/docs/using-k6/thresholds/) - Set pass/fail criteria for tests
