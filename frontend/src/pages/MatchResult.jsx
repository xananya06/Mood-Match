import { useLocation, useNavigate } from 'react-router-dom';

function MatchResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  // Map emotions to avatars and descriptions
  const emotionMap = {
    "stressed": { avatar: "😰", color: "yellow" },
    "lonely": { avatar: "🏠", color: "blue" },
    "anxious": { avatar: "😟", color: "purple" },
    "overwhelmed": { avatar: "😫", color: "red" },
    "sad": { avatar: "😢", color: "blue" },
    "homesick": { avatar: "🏠", color: "blue" },
    "worried": { avatar: "😟", color: "purple" },
    "uncertain": { avatar: "🤔", color: "gray" }
  };

  const conversationStarters = result?.conversation_strategy?.conversation_starters || [
    "Hey! How's your day going?",
    "I'm also dealing with stress lately. How are you managing?",
    "Thanks for connecting. What's on your mind?"
  ];

  const matchScore = Math.floor(Math.random() * 20) + 80; // 80-100 for demo

  // Get matched peer info from mood analysis
  const primaryEmotion = result?.mood_analysis?.primary_emotion || "stressed";
  const emotionInfo = emotionMap[primaryEmotion.toLowerCase()] || emotionMap["stressed"];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-3xl w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Success Header */}
          <div className="text-center mb-8">
            <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-5xl">🎉</span>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Match Found!
            </h1>
            <p className="text-xl text-gray-600">
              We found you a compatible BU peer
            </p>
          </div>

          {/* Matched Peer Card */}
          <div className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-xl p-6 mb-6 border-2 border-purple-200">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">
              You matched with:
            </h3>
            <div className="flex items-center gap-4 bg-white rounded-lg p-4 shadow-md">
              <div className="text-5xl">{emotionInfo.avatar}</div>
              <div className="flex-1">
                <h4 className="font-bold text-gray-900 text-lg">BU Student</h4>
                <p className="text-gray-600 capitalize">Feeling {primaryEmotion}</p>
                {result?.mood_analysis?.matching_criteria?.similar_experience && (
                  <p className="text-sm text-gray-500 mt-1">
                    Also experiencing: {result.mood_analysis.matching_criteria.similar_experience.replace(/_/g, ' ')}
                  </p>
                )}
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-purple-600">{matchScore}%</div>
                <div className="text-xs text-gray-500">Compatible</div>
              </div>
            </div>
          </div>

          {/* Why This Match */}
          {result?.mood_analysis && (
            <div className="bg-blue-50 rounded-lg p-6 mb-6">
              <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                <span>🤝</span>
                Why this match works:
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-blue-600">•</span>
                  <span>Both experiencing <strong>{result.mood_analysis.primary_emotion}</strong> feelings</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600">•</span>
                  <span>Similar support needs: <strong>{result.mood_analysis.needs?.[0]}</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-600">•</span>
                  <span>Compatible communication styles</span>
                </li>
                {result.mood_analysis.matching_criteria?.context && (
                  <li className="flex items-start gap-2">
                    <span className="text-blue-600">•</span>
                    <span>Shared context: <strong>{result.mood_analysis.matching_criteria.context.replace(/_/g, ' ')}</strong></span>
                  </li>
                )}
              </ul>
            </div>
          )}

          {/* Conversation Starters */}
          <div className="mb-6">
            <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
              <span>💬</span>
              Conversation Starters:
            </h3>
            <div className="space-y-3">
              {conversationStarters.slice(0, 3).map((starter, index) => (
                <div 
                  key={index}
                  className="bg-purple-50 border-2 border-purple-200 rounded-lg p-4 hover:bg-purple-100 transition-colors cursor-pointer"
                  onClick={() => {
                    navigator.clipboard.writeText(starter);
                    alert('Copied to clipboard!');
                  }}
                >
                  <p className="text-gray-800">{starter}</p>
                  <p className="text-xs text-gray-500 mt-1">Click to copy</p>
                </div>
              ))}
            </div>
          </div>

          {/* Multi-Agent System Info */}
          {result?.agent_communications && (
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h4 className="font-semibold text-gray-700 mb-2 text-sm">
                🤖 Multi-Agent System Stats:
              </h4>
              <div className="grid grid-cols-3 gap-4 text-center text-sm">
                <div>
                  <p className="text-2xl font-bold text-purple-600">
                    {result.agents_activated?.length || 3}
                  </p>
                  <p className="text-gray-600 text-xs">Agents Used</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-blue-600">
                    {result.agent_communications?.length || 0}
                  </p>
                  <p className="text-gray-600 text-xs">Communications</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-green-600">
                    {result.coordination_strategy || 'Sequential'}
                  </p>
                  <p className="text-gray-600 text-xs">Strategy</p>
                </div>
              </div>
            </div>
          )}

          {/* Safety Guidelines */}
          <div className="bg-yellow-50 border-2 border-yellow-200 rounded-lg p-4 mb-6">
            <h4 className="font-semibold text-yellow-900 mb-2 flex items-center gap-2">
              <span>⚠️</span>
              Safety Guidelines:
            </h4>
            <ul className="text-sm text-yellow-800 space-y-1">
              <li>• Keep conversations supportive and respectful</li>
              <li>• Don't share personal identifying information</li>
              <li>• If you feel uncomfortable, you can end the chat anytime</li>
              <li>• This is peer support, not professional therapy</li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={() => alert('Chat feature coming soon! For MVP, we\'re focusing on the matching system.')}
              className="flex-1 bg-purple-600 text-white py-4 rounded-lg font-bold text-lg hover:bg-purple-700 transition-colors"
            >
              Start Conversation
            </button>
            <button
              onClick={() => navigate('/')}
              className="flex-1 bg-gray-200 text-gray-800 py-4 rounded-lg font-semibold text-lg hover:bg-gray-300 transition-colors"
            >
              Find Another Match
            </button>
          </div>

          {/* BU Resources */}
          {result?.mood_analysis?.recommended_resources && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2 text-sm">
                📚 Recommended BU Resources:
              </h4>
              <div className="flex flex-wrap gap-2">
                {result.mood_analysis.recommended_resources.map((resource, index) => (
                  <span 
                    key={index}
                    className="text-xs bg-blue-100 text-blue-800 px-3 py-1 rounded-full"
                  >
                    {resource}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-6 text-gray-500 text-sm">
          <p>Matched by AI • Powered by Multi-Agent System</p>
        </div>
      </div>
    </div>
  );
}

export default MatchResult;