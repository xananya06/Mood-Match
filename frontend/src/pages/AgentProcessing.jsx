import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function AgentProcessing() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;
  const [currentStep, setCurrentStep] = useState(0);

  const agentSteps = [
    {
      agent: "MoodAnalyzer",
      status: "Analyzing emotional state...",
      icon: "🧠",
      complete: true
    },
    {
      agent: "Coordinator",
      status: "Deciding coordination strategy...",
      icon: "🎯",
      complete: true
    },
    {
      agent: "PeerMatcher",
      status: "Finding compatible peers...",
      icon: "🤝",
      complete: true
    },
    {
      agent: "ConversationFacilitator",
      status: "Generating conversation starters...",
      icon: "💬",
      complete: false
    }
  ];

  useEffect(() => {
    // Simulate agent processing steps
    const timer = setInterval(() => {
      setCurrentStep(prev => {
        if (prev < agentSteps.length - 1) {
          return prev + 1;
        } else {
          clearInterval(timer);
          // After all steps, navigate to match result
          setTimeout(() => navigate('/match', { state: { result } }), 1000);
          return prev;
        }
      });
    }, 1500);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
              <span className="text-4xl">🤖</span>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Multi-Agent System Processing
            </h1>
            <p className="text-gray-600">
              Our AI agents are collaborating to help you...
            </p>
          </div>

          {/* Agent Communication Flow */}
          <div className="space-y-4 mb-8">
            {agentSteps.map((step, index) => (
              <div 
                key={index}
                className={`flex items-center gap-4 p-4 rounded-lg border-2 transition-all duration-500 ${
                  index <= currentStep
                    ? 'bg-purple-50 border-purple-300'
                    : 'bg-gray-50 border-gray-200 opacity-50'
                }`}
              >
                <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${
                  index <= currentStep ? 'bg-purple-200' : 'bg-gray-200'
                }`}>
                  {step.icon}
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900">{step.agent}</h3>
                  <p className="text-sm text-gray-600">{step.status}</p>
                </div>
                {index <= currentStep && (
                  <div className="text-green-500">
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Mood Analysis Results */}
          {result?.mood_analysis && (
            <div className="bg-blue-50 rounded-lg p-6 mb-6">
              <h3 className="font-bold text-gray-900 mb-3">Analysis Complete:</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-600">Primary Emotion:</p>
                  <p className="font-semibold text-gray-900 capitalize">
                    {result.mood_analysis.primary_emotion}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600">Urgency Level:</p>
                  <p className={`font-semibold ${
                    result.mood_analysis.urgency_level === 'HIGH' ? 'text-red-600' :
                    result.mood_analysis.urgency_level === 'MODERATE' ? 'text-yellow-600' :
                    'text-green-600'
                  }`}>
                    {result.mood_analysis.urgency_level}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Agent Communications Log */}
          {result?.agent_communications && result.agent_communications.length > 0 && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="font-semibold text-gray-700 mb-3 text-sm">
                🔗 Agent Communications ({result.agent_communications.length}):
              </h3>
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {result.agent_communications.map((comm, index) => (
                  <div key={index} className="text-xs bg-white p-2 rounded border border-gray-200">
                    <span className="font-semibold text-purple-600">{comm.from}</span>
                    {' → '}
                    <span className="font-semibold text-blue-600">{comm.to}</span>
                    <span className="text-gray-500 ml-2">({comm.type})</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Loading Progress */}
          <div className="mt-6">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${((currentStep + 1) / agentSteps.length) * 100}%` }}
              />
            </div>
            <p className="text-center text-sm text-gray-500 mt-2">
              {Math.round(((currentStep + 1) / agentSteps.length) * 100)}% complete
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AgentProcessing;