import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Demo student posts with profiles
const SAMPLE_POSTS = [
  {
    id: 1,
    name: "Marcus",
    avatar: "👨‍💻",
    year: "Junior, CS Major",
    emotion: "anxious",
    preview: "Internship rejections are hitting different this year. Applied to 50+ places and only got 2 interviews. Starting to doubt myself...",
    interests: ["Gaming", "Basketball", "Hackathons"],
    timestamp: "5 mins ago",
    urgency: "MODERATE"
  },
  {
    id: 2,
    name: "Priya",
    avatar: "👩‍💼",
    year: "Senior, Business Analytics",
    emotion: "homesick",
    preview: "Missing home a lot lately. Everything here still feels temporary even after 3 years. My family doesn't really understand...",
    interests: ["Data viz", "Yoga", "K-pop"],
    timestamp: "12 mins ago",
    urgency: "MODERATE"
  },
  {
    id: 3,
    name: "Jake",
    avatar: "🧑‍🔧",
    year: "Sophomore, Engineering",
    emotion: "overwhelmed",
    preview: "Thermodynamics is destroying me. I study for hours but still bomb the exams. Feel like everyone else just 'gets it'...",
    interests: ["Rock climbing", "EDM", "3D printing"],
    timestamp: "23 mins ago",
    urgency: "HIGH"
  },
  {
    id: 4,
    name: "Sara",
    avatar: "👩‍🎓",
    year: "First-year, Undecided",
    emotion: "lonely",
    preview: "Honestly feeling really lonely. Everyone seems to have found their friend groups already and I'm still eating lunch alone...",
    interests: ["Poetry", "Mental health", "Indie folk"],
    timestamp: "45 mins ago",
    urgency: "MODERATE"
  }
];

const urgencyColor = (urgency) => {
  const colors = {
    LOW: 'border-green-300 bg-green-50',
    MODERATE: 'border-yellow-300 bg-yellow-50',
    HIGH: 'border-orange-300 bg-orange-50',
    CRISIS: 'border-red-300 bg-red-50'
  };
  return colors[urgency] || colors.MODERATE;
};

export default function MoodEntry() {
  const navigate = useNavigate();
  const [moodText, setMoodText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!moodText.trim()) {
      alert('Please share how you\'re feeling');
      return;
    }

    setIsSubmitting(true);
    
    try {
      // Navigate to processing page with mood text
      navigate('/processing', { 
        state: { 
          moodText,
          userId: 'student_ananya'  // Demo user
        } 
      });
    } catch (error) {
      console.error('Error:', error);
      alert('Something went wrong. Please try again.');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Mood Match
          </h1>
          <p className="text-gray-600">
            Connect with BU peers who understand what you're going through
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Left: Your Mood Entry */}
          <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-purple-200">
            <div className="flex items-center gap-3 mb-4">
              <div className="text-3xl">👩‍💻</div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Ananya</h2>
                <p className="text-sm text-gray-600">MS AI (Graduating Dec 2025)</p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  How are you feeling today?
                </label>
                <textarea
                  value={moodText}
                  onChange={(e) => setMoodText(e.target.value)}
                  className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 outline-none resize-none"
                  rows="8"
                  placeholder="Share what's on your mind... I'm feeling overwhelmed by thesis work and job applications..."
                  disabled={isSubmitting}
                />
                <p className="text-xs text-gray-500 mt-2">
                  💡 Be honest about what you're experiencing. Our AI will match you with someone who gets it.
                </p>
              </div>

              <button
                type="submit"
                disabled={isSubmitting || !moodText.trim()}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
              >
                {isSubmitting ? '🔄 Processing...' : '🤝 Find My Peer Match'}
              </button>
            </form>

            <div className="mt-6 p-4 bg-purple-50 rounded-lg border border-purple-200">
              <p className="text-sm text-gray-700">
                <strong className="text-purple-700">How matching works:</strong> Our multi-agent AI system analyzes your mood (80%) and profile (20%) to find compatible peers experiencing similar challenges.
              </p>
            </div>
          </div>

          {/* Right: Recent Activity Feed */}
          <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-blue-200">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <span>📱</span>
              Recent Activity
            </h2>
            <p className="text-sm text-gray-600 mb-4">
              Other BU students seeking support right now
            </p>

            <div className="space-y-3 max-h-[500px] overflow-y-auto">
              {SAMPLE_POSTS.map(post => (
                <div 
                  key={post.id}
                  className={`p-4 rounded-lg border-2 ${urgencyColor(post.urgency)} hover:shadow-md transition-shadow cursor-pointer`}
                >
                  <div className="flex items-start gap-3">
                    <div className="text-3xl flex-shrink-0">{post.avatar}</div>
                    <div className="flex-1 min-w-0">
                      {/* Name and year */}
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-semibold text-gray-900">{post.name}</span>
                        <span className="text-xs text-gray-500">• {post.year}</span>
                      </div>
                      
                      {/* Mood post preview */}
                      <p className="text-gray-800 text-sm line-clamp-2 mb-2">
                        {post.preview}
                      </p>
                      
                      {/* Interests and timestamp */}
                      <div className="flex items-center gap-2 flex-wrap">
                        {post.interests.slice(0, 2).map((interest, idx) => (
                          <span key={idx} className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">
                            {interest}
                          </span>
                        ))}
                        <span className="text-xs text-gray-400 ml-auto">{post.timestamp}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-xs text-gray-600 text-center">
                ✨ {SAMPLE_POSTS.length} students looking for peer support
              </p>
            </div>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center space-y-2">
          <p className="text-sm text-gray-600">
            🔒 Your privacy matters. All matches are confidential.
          </p>
          <p className="text-xs text-gray-500">
            This is peer support, not professional therapy. If you're in crisis, contact BU Police (617-353-2121) or Crisis Text Line (741741).
          </p>
        </div>
      </div>
    </div>
  );
}