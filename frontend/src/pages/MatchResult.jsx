import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function MatchResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const { result, moodText } = location.state || {};
  const [showEmailPreview, setShowEmailPreview] = useState(false);

  if (!result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-white flex items-center justify-center p-4">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No match result found</p>
          <button
            onClick={() => navigate('/')}
            className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700"
          >
            Start Over
          </button>
        </div>
      </div>
    );
  }

  if (!result.match_found) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-white flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md border-2 border-yellow-300">
          <div className="text-6xl mb-4 text-center">⏳</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4 text-center">
            No Matches Right Now
          </h2>
          <p className="text-gray-600 mb-6 text-center">
            We couldn't find a compatible peer at the moment. Try again later or adjust your preferences.
          </p>
          <button
            onClick={() => navigate('/')}
            className="w-full bg-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-purple-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const peer = result.matched_peer;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Success Header */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4 animate-bounce">🎉</div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Match Found!
          </h1>
          <p className="text-xl text-gray-600">
            We found someone who understands what you're going through
          </p>
        </div>

        {/* Match Score Card */}
        <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl p-6 mb-6 border-2 border-green-300 shadow-lg">
          <div className="text-center">
            <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-blue-600 mb-2">
              {result.match_score}% Compatible
            </div>
            <div className="flex items-center justify-center gap-6 text-sm text-gray-700">
              <div>
                <span className="font-semibold">Mood Similarity:</span> {result.mood_similarity_score}%
              </div>
              <div className="w-px h-4 bg-gray-300"></div>
              <div>
                <span className="font-semibold">Profile Compatibility:</span> {result.profile_compatibility_score}%
              </div>
            </div>
          </div>
        </div>

        {/* Matched Peer Card */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 border-2 border-purple-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <span>👤</span>
            Your Match
          </h2>
          
          <div className="flex items-start gap-4 mb-4">
            <div className="text-5xl">{peer.avatar}</div>
            <div className="flex-1">
              <h3 className="text-2xl font-bold text-gray-900">{peer.name}</h3>
              <p className="text-gray-600 mb-2">{peer.year}</p>
              <p className="text-gray-700 mb-3">{peer.bio}</p>
              
              {/* Interests */}
              {peer.interests && peer.interests.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {peer.interests.map((interest, idx) => (
                    <span key={idx} className="text-sm bg-purple-100 text-purple-700 px-3 py-1 rounded-full">
                      {interest}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Why This Match Works */}
        <div className="bg-blue-50 rounded-lg p-6 mb-6 border-2 border-blue-200">
          <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
            <span>🎯</span>
            Why This Match Works:
          </h3>
          <div className="space-y-3">
            {/* Shared Emotional Themes */}
            {result.shared_emotional_themes && result.shared_emotional_themes.length > 0 && (
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">
                  Shared Emotional Themes:
                </p>
                <ul className="list-disc list-inside space-y-1 text-gray-700">
                  {result.shared_emotional_themes.map((theme, idx) => (
                    <li key={idx} className="text-sm">{theme}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Shared Interests */}
            {result.shared_interests && result.shared_interests.length > 0 && (
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-1">
                  Shared Interests:
                </p>
                <div className="flex flex-wrap gap-2">
                  {result.shared_interests.map((interest, idx) => (
                    <span key={idx} className="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded-full">
                      {interest}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Match Rationale */}
            <div className="pt-2 border-t border-blue-300">
              <p className="text-sm text-gray-700 italic">
                {result.match_rationale}
              </p>
            </div>
          </div>
        </div>

        {/* Suggested Meetup Locations - NEW! */}
        {result?.location_recommendations?.locations && result.location_recommendations.locations.length > 0 && (
          <div className="bg-green-50 rounded-lg p-6 mb-6 border-2 border-green-200">
            <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2 text-lg">
              <span>📍</span>
              Where to Meet:
            </h3>
            <div className="space-y-3">
              {result.location_recommendations.locations.map((loc, index) => (
                <div 
                  key={index}
                  className="bg-white rounded-lg p-4 border-2 border-green-300 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start gap-3">
                    <span className="text-3xl">{loc.emoji || '📍'}</span>
                    <div className="flex-1">
                      <h4 className="font-bold text-gray-900 text-lg">{loc.location_name}</h4>
                      <p className="text-sm text-gray-600 mb-2">{loc.address}</p>
                      <div className="space-y-1 text-sm">
                        <p className="text-gray-700">
                          <strong className="text-green-700">Why:</strong> {loc.reasoning}
                        </p>
                        <p className="text-gray-600">
                          <strong>Vibe:</strong> {loc.vibe}
                        </p>
                        <p className="text-gray-500 text-xs">
                          <strong>Best time:</strong> {loc.best_time}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {result.location_recommendations.timing_suggestion && (
              <div className="mt-4 p-3 bg-white rounded-lg border border-green-300">
                <p className="text-sm text-gray-700">
                  💡 <strong>Timing tip:</strong> {result.location_recommendations.timing_suggestion}
                </p>
              </div>
            )}
            
            {result.location_recommendations.overall_strategy && (
              <p className="text-xs text-gray-600 mt-2 italic">
                Strategy: {result.location_recommendations.overall_strategy}
              </p>
            )}
          </div>
        )}

        {/* Conversation Starters */}
        {result.conversation_starters && result.conversation_starters.length > 0 && (
          <div className="bg-purple-50 rounded-lg p-6 mb-6 border-2 border-purple-200">
            <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
              <span>💬</span>
              Conversation Starters:
            </h3>
            <ul className="space-y-2">
              {result.conversation_starters.map((starter, idx) => (
                <li key={idx} className="flex items-start gap-2 text-gray-700">
                  <span className="text-purple-600 font-bold">•</span>
                  <span>{starter}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Email Preview */}
        {result.email_preview && (
          <div className="bg-white rounded-lg p-6 mb-6 border-2 border-gray-300">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-gray-900 flex items-center gap-2">
                <span>📧</span>
                Email Notification Preview
              </h3>
              <button
                onClick={() => setShowEmailPreview(!showEmailPreview)}
                className="text-sm text-purple-600 hover:text-purple-700 font-medium"
              >
                {showEmailPreview ? 'Hide' : 'Show'} Email
              </button>
            </div>
            
            {showEmailPreview && (
              <div className="border-l-4 border-purple-400 pl-4">
                <p className="text-sm font-semibold text-gray-700 mb-1">
                  Subject: {result.email_preview.subject}
                </p>
                <div 
                  className="text-sm text-gray-600 mt-2"
                  dangerouslySetInnerHTML={{ __html: result.email_preview.body }}
                />
              </div>
            )}
          </div>
        )}

        {/* Safety Reminder */}
        <div className="bg-yellow-50 rounded-lg p-6 mb-6 border-2 border-yellow-300">
          <h3 className="font-bold text-gray-900 mb-2 flex items-center gap-2">
            <span>⚠️</span>
            Safety Reminder
          </h3>
          <p className="text-sm text-gray-700 mb-2">
            This is peer support, not professional therapy. If you feel uncomfortable at any point, you can end the conversation.
          </p>
          <p className="text-sm text-gray-700">
            <strong>In crisis?</strong> Contact BU Police (617-353-2121), Crisis Text Line (741741), or National Suicide Prevention Lifeline (988).
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-4">
          <button
            onClick={() => navigate('/')}
            className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-purple-700 hover:to-blue-700 shadow-lg hover:shadow-xl transition-all"
          >
            🏠 Back to Home
          </button>
          <button
            onClick={() => window.print()}
            className="bg-gray-200 text-gray-700 font-semibold py-3 px-6 rounded-lg hover:bg-gray-300"
          >
            🖨️ Print
          </button>
        </div>
      </div>
    </div>
  );
}