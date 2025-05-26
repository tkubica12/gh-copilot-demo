import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { ClipLoader, DotLoader } from 'react-spinners'; 
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [result, setResult] = useState('');
  const [retryAfter, setRetryAfter] = useState(0);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    setStatus('uploading'); // Set status to 'uploading' on button click
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(window.env.REACT_APP_PROCESS_API_URL, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStatus('processing'); // Change status to 'processing' after upload
      pollStatus(response.data.results_url);
    } catch (error) {
      console.error(error);
      setStatus('idle'); // Reset status on error
    }
  };

  const pollStatus = async (url) => {
    try {
      const response = await axios.get(url);
      if (response.status === 200 && response.data.status === 'completed') {
        setStatus('completed');
        setResult(response.data.data.result);
      } else if (response.status === 202) {
        setRetryAfter(response.headers['retry-after'] || 5);
        setTimeout(() => pollStatus(url), (response.headers['retry-after'] || 5) * 1000);
      }
    } catch (error) {
      console.error(error);
      setStatus('idle'); // Reset status on error
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Document Processor</h1>
      </header>
      
      <div className="upload-card">
        <p>Upload an image or PDF document for AI processing</p>
        <input type="file" onChange={handleFileChange} accept="image/jpeg,image/png,image/gif,application/pdf" />
        <button onClick={handleUpload} disabled={!file}>Upload</button>
      </div>

      {status === 'uploading' && (
        <div className="status-indicator">
          <DotLoader color="#3498db" size={50} />
          <p>Uploading...</p>
        </div>
      )}

      {status === 'processing' && (
        <div className="status-indicator">
          <ClipLoader color="#3498db" size={50} />
          <p>Processing...</p>
        </div>
      )}

      {status === 'completed' && (
        <div className="result">
          <ReactMarkdown>{result}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;