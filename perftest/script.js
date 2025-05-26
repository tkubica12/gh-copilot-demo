import http from 'k6/http';
import { sleep, check } from 'k6';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

// Get the URL from an environment variable or use a default value
const processBaseUrl = __ENV.TEST_URL || 'https://ca-api-processing-aiasync-gchk.yellowmoss-adbbb4fb.germanywestcentral.azurecontainerapps.io';
console.log(`Using processBaseUrl: ${processBaseUrl}`);

// Read the file contents in the init stage
const imageContent = open('./example.jpg', 'b');
const pdfContent = __ENV.TEST_PDF === 'true' ? open('./example.pdf', 'b') : null;

// Use PDF or image based on environment variable
const useTestPdf = __ENV.TEST_PDF === 'true';
console.log(`Testing with ${useTestPdf ? 'PDF' : 'image'} files`);

export const options = {
  scenarios: {
    default: {
      executor: 'constant-vus',
      vus: 100,
      duration: '10s',
      gracefulStop: '3m',
    },
  },
};

export default function() {
  // Create a new FormData instance
  const form = new FormData();
  
  // Append the file to the form based on the test type
  if (useTestPdf && pdfContent) {
    form.append('file', http.file(pdfContent, 'example.pdf', 'application/pdf'));
  } else {
    form.append('file', http.file(imageContent, 'example.jpg', 'image/jpeg'));
  }

  // Define headers
  const headers = {
    'Content-Type': 'multipart/form-data; boundary=' + form.boundary,
  };

  // POST request to upload the file
  const postResponse = http.post(`${processBaseUrl}/api/process`, form.body(), { headers });

  check(postResponse, {
    'post status is 202': (r) => r.status === 202,
  });

  if (postResponse.status !== 202) {
    console.error(`Failed to upload file. Status: ${postResponse.status}, Response: ${postResponse.body}`);
    return;
  }

  let resultsUrl;
  try {
    resultsUrl = JSON.parse(postResponse.body).results_url;
  } catch (e) {
    console.error('Failed to parse response body:', postResponse.body);
    return;
  }

  // Poll the status until a 200 response is received
  let statusResponse;
  do {
    statusResponse = http.get(resultsUrl);
    if (statusResponse.status === 202) {
      sleep(1); // Wait for 1 second before retrying
    }
  } while (statusResponse.status === 202);

  check(statusResponse, {
    'get status is 200': (r) => r.status === 200,
  });
}