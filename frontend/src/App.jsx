import { useState, useEffect } from 'react';
import { healthCheck } from './services/api';

function App() {
  const [apiStatus, setApiStatus] = useState('checking...');
  const [error, setError] = useState(null);

  useEffect(() => {
    testConnection();
  }, []);

  const testConnection = async () => {
    try {
      const data = await healthCheck();
      setApiStatus(data.status);
    } catch (err) {
      setError(err.message);
      setApiStatus('error');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center p-8 bg-white rounded-lg shadow-lg">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Mood Match
        </h1>
        
        <div className="mb-4">
          <p className="text-lg text-gray-600">
            API Status: 
            <span className={`font-semibold ml-2 ${
              apiStatus === 'healthy' ? 'text-green-600' : 'text-red-600'
            }`}>
              {apiStatus}
            </span>
          </p>
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-700 rounded">
            Error: {error}
          </div>
        )}

        {apiStatus === 'healthy' && (
          <div className="mt-6 p-4 bg-green-50 text-green-700 rounded">
            ✅ Frontend and Backend are connected!
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
