import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const handleScan = async () => {
    if (files.length === 0) {
      alert('Please select files to scan.');
      return;
    }

    setLoading(true);
    setResults([]);

    for (const file of files) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://localhost:8000/scan', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        setResults(prev => [...prev, response.data]);
      } catch (error) {
        setResults(prev => [...prev, { filename: file.name, error: error.message }]);
      }
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🛡️ Harmful File Detector</h1>
        <p>Upload files to scan for malware</p>
      </header>
      <main>
        <div className="upload-section">
          <input type="file" multiple onChange={handleFileChange} />
          <button onClick={handleScan} disabled={loading}>
            {loading ? 'Scanning...' : 'Scan Files'}
          </button>
        </div>
        <div className="results-section">
          {results.map((result, index) => (
            <div key={index} className={`result ${result.prediction === 'Harmful' ? 'harmful' : 'safe'}`}>
              <h3>{result.filename}</h3>
              {result.error ? (
                <p>Error: {result.error}</p>
              ) : (
                <>
                  <p>Prediction: {result.prediction}</p>
                  <p>Probability: {result.probability.toFixed(2)}</p>
                  <p>Status: {result.status}</p>
                </>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;