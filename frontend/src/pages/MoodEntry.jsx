import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://localhost:8000';

// DEMO: Sample posts to show in the feed
const SAMPLE_POSTS = [
  {
    id: 1,
    emotion: "stressed",
    preview: "Finals are in 2 weeks and I feel so overwhelmed...",
    timestamp: "5 mins ago",
    urgency: "MODERATE",
    avatar: "😰"
  },
  {
    id: 2,
    emotion: "lonely",
    preview: "Missing home a lot today. Anyone else feeling homesick?",
    timestamp: "12 mins ago",
    urgency: "MODERATE",
    avatar: "🏠"
  },
  {
    id: 3,
    emotion: "anxious",
    preview: "Worried about my internship applications. The waiting is killing me...",
    timestamp: "23 mins ago",
    urgency: "MODERATE",
    avatar: "😟"
  },
  {
    id: 4,
    emotion: "overwhelmed",
    preview: "Juggling 3 group projects and a part-time job. Need some encouragement...",
    timestamp: "1 hour ago",
    urgency: "HIGH",
    avatar: "😫"
  }
];

function MoodEntry() {
  const [moodText, setMoodText] = useState('');
  const [loading, setLoading] = useState(false);
  const [showFeed, setShowFeed] = useState(true);
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

  const urgencyColor = (level) => {
    switch(level) {
      case 'HIGH': return 'border-red-400 bg-red-50';
      case 'MODERATE': return 'border-yellow-400 bg-yellow-50';
      default: return 'border-green-400 bg-green-50';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-4">
      <div className="max-w-6xl mx-auto py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-2">
            Mood Match 🧘‍♀️
          </h1>
          <p className="text-xl text-gray-600">
            Find a BU peer when you need one most
          </p>
          <div className="mt-2 text-sm text-gray-500">
            🤖 Powered by Multi-Agent AI System
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Left: Current Activity Feed */}
          {showFeed && (
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-800">
                  🌊 Current Activity
                </h3>
                <span className="text-sm text-gray-500">{SAMPLE_POSTS.length} seeking support</span>
              </div>
              
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {SAMPLE_POSTS.map(post => (
                  <div 
                    key={post.id}
                    className={`p-4 rounded-lg border-2 ${urgencyColor(post.urgency)} hover:shadow-md transition-shadow`}
                  >
                    <div className="flex items-start gap-3">
                      <div className="text-3xl flex-shrink-0">{post.avatar}</div>
                      <div className="flex-1 min-w-0">
                        <p className="text-gray-800 line-clamp-2 mb-1">
                          {post.preview}
                        </p>
                        <div className="flex items-center gap-2 text-xs">
                          <span className="text-gray-500">{post.timestamp}</span>
                          <span className={`px-2 py-0.5 rounded-full font-semibold ${
                            post.urgency === 'HIGH' ? 'bg-red-200 text-red-800' :
                            post.urgency === 'MODERATE' ? 'bg-yellow-200 text-yellow-800' :
                            'bg-green-200 text-green-800'
                          }`}>
                            {post.urgency}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-4 p-3 bg-blue-50 rounded-lg text-sm text-blue-800">
                💡 <strong>Demo Mode:</strong> These are sample posts showing real-time activity
              </div>
            </div>
          )}

          {/* Right: Your Post */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              ✍️ Share how you're feeling
            </h2>
            
            <form onSubmit={handleSubmit}>
              <div className="relative">
                <textarea
                  value={moodText}
                  onChange={(e) => setMoodText(e.target.value)}
                  placeholder="Type here...

Example: 'I'm feeling stressed about finals coming up and could use someone to talk to...'

or try: 'I want to hurt myself' (for crisis detection demo)"
                  className="w-full h-48 p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none resize-none text-lg"
                  required
                />
                <div className="absolute bottom-3 right-3 text-xs text-gray-400">
                  {moodText.length}/500
                </div>
              </div>

              <div className="mt-6 flex flex-col gap-3">
                <button
                  type="submit"
                  disabled={loading || !moodText.trim()}
                  className="w-full bg-purple-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Multi-Agent System Analyzing...
                    </span>
                  ) : (
                    '🔍 Find My Peer Match'
                  )}
                </button>

                {loading && (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-gray-600 animate-pulse">
                      <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                      <span>MoodAnalyzer processing...</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600 animate-pulse delay-100">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <span>Coordinator deciding strategy...</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600 animate-pulse delay-200">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>PeerMatcher finding compatible peers...</span>
                    </div>
                  </div>
                )}
              </div>
            </form>

            {/* Info Section */}
            <div className="mt-8 pt-6 border-t border-gray-200">
              <h3 className="font-semibold text-gray-700 mb-3">🚀 How it works:</h3>
              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">1.</span>
                  <span><strong>AI Agents Analyze</strong> - Multiple AI agents examine your emotional state and needs</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">2.</span>
                  <span><strong>Smart Matching</strong> - System finds you a compatible BU student (no repeat matches!)</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-purple-600 font-bold">3.</span>
                  <span><strong>Safe Connection</strong> - Start a supportive conversation with conversation starters</span>
                </div>
              </div>
            </div>

            {/* Safety Note */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
              <p className="text-sm text-blue-800">
                <strong>🛡️ Safety first:</strong> If you're experiencing a crisis, 
                our multi-agent system will automatically connect you with professional resources.
              </p>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="mt-8 grid grid-cols-3 gap-4 text-center">
          <div className="bg-white rounded-lg p-4 shadow">
            <div className="text-3xl font-bold text-purple-600">{SAMPLE_POSTS.length}</div>
            <div className="text-sm text-gray-600">Active Users</div>
          </div>
          <div className="bg-white rounded-lg p-4 shadow">
            <div className="text-3xl font-bold text-blue-600">4</div>
            <div className="text-sm text-gray-600">AI Agents</div>
          </div>
          <div className="bg-white rounded-lg p-4 shadow">
            <div className="text-3xl font-bold text-green-600">95%</div>
            <div className="text-sm text-gray-600">Match Success</div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          Made with 💜 for BU students • Multi-Agent AI System
        </div>
      </div>
    </div>
  );
}

export default MoodEntry;