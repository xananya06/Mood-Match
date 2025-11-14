import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://localhost:8000';

function MoodEntry() {
  const [moodText, setMoodText] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/mood/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: `user_${Date.now()}`,
          mood_description: moodText,
          context: 'general'
        })
      });

      const result = await response.json();
      
      // Check for crisis
      if (result.mood_analysis?.crisis_detected) {
        navigate('/crisis', { state: { result } });
      } else {
        navigate('/processing', { state: { result } });
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-2">
            Mood Match 🧘‍♀️
          </h1>
          <p className="text-xl text-gray-600">
            Find a BU peer when you need one most
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            How are you feeling today?
          </h2>
          
          <form onSubmit={handleSubmit}>
            <textarea
              value={moodText}
              onChange={(e) => setMoodText(e.target.value)}
              placeholder="I'm feeling stressed about finals coming up..."
              className="w-full h-40 p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none resize-none text-lg"
              required
            />

            <div className="mt-6 flex flex-col gap-3">
              <button
                type="submit"
                disabled={loading || !moodText.trim()}
                className="w-full bg-purple-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Processing with AI agents...
                  </span>
                ) : (
                  'Find me a peer support buddy'
                )}
              </button>

              {loading && (
                <div className="text-center text-sm text-gray-500 animate-pulse">
                  🤖 Multi-agent system analyzing your mood...
                </div>
              )}
            </div>
          </form>

          {/* Info Section */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h3 className="font-semibold text-gray-700 mb-2">How it works:</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2">
                <span className="text-purple-600">•</span>
                <span>AI agents analyze your emotional state and needs</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-600">•</span>
                <span>We match you with a compatible BU student</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-600">•</span>
                <span>Start a supportive conversation with your peer</span>
              </li>
            </ul>
          </div>

          {/* Safety Note */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>🛡️ Safety first:</strong> If you're experiencing a crisis, 
              our system will automatically connect you with professional resources.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-6 text-gray-500 text-sm">
          Made with 💜 for BU students
        </div>
      </div>
    </div>
  );
}

export default MoodEntry;