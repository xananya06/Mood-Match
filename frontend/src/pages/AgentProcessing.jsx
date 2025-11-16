import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function AgentProcessing() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;
  const [currentStep, setCurrentStep] = useState(0);
  const [showCommunication, setShowCommunication] = useState(false);

  const agentSteps = [
    {
      agent: "🧠 MoodAnalyzer",
      status: "Analyzing emotional state...",
      detail: "Detecting emotions, urgency level, and support needs",
      color: "purple",
      complete: false
    },
    {
      agent: "🎯 Coordinator",
      status: "Orchestrating multi-agent collaboration...",
      detail: "Deciding which agents to activate and coordination strategy",
      color: "blue",
      complete: false
    },
    {
      agent: "🤝 PeerMatcher",
      status: "Finding compatible peers...",
      detail: "Matching based on emotions, avoiding previous matches",
      color: "green",
      complete: false
    },
    {
      agent: "💬 ConversationFacilitator",
      status: "Preparing conversation strategies...",
      detail: "Generating starters and safety guidelines",
      color: "pink",
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
          // Show communication log briefly
          setShowCommunication(true);
          // After all steps, navigate to match result
          setTimeout(() => navigate('/match', { state: { result } }), 2000);
          return prev;
        }
      });
    }, 1500);

    return () => clearInterval(timer);
  }, []);

  const getColorClass = (color) => {
    const colors = {
      purple: 'bg-purple-50 border-purple-300',
      blue: 'bg-blue-50 border-blue-300',
      green: 'bg-green-50 border-green-300',
      pink: 'bg-pink-50 border-pink-300'
    };
    return colors[color] || colors.purple;
  };

  const getIconColor = (color) => {
    const colors = {
      purple: 'bg-purple-200',
      blue: 'bg-blue-200',
      green: 'bg-green-200',
      pink: 'bg-pink-200'
    };
    return colors[color] || colors.purple;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="w-24 h-24 bg-gradient-to-br from-purple-400 to-blue-400 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
              <span className="text-5xl">🤖</span>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Multi-Agent System Active
            </h1>
            <p className="text-gray-600 text-lg">
              Our AI agents are collaborating to find your perfect match...
            </p>
          </div>

          {/* Agent Communication Flow */}
          <div className="space-y-4 mb-8">
            {agentSteps.map((step, index) => (
              <div 
                key={index}
                className={`flex items-center gap-4 p-5 rounded-xl border-2 transition-all duration-500 ${
                  index <= currentStep
                    ? `${getColorClass(step.color)} shadow-md transform scale-105`
                    : 'bg-gray-50 border-gray-200 opacity-50'
                }`}
              >
                <div className={`w-14 h-14 rounded-full flex items-center justify-center text-2xl ${
                  index <= currentStep ? getIconColor(step.color) : 'bg-gray-200'
                } transition-all duration-300`}>
                  {step.agent.split(' ')[0]}
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900 text-lg">{step.agent.split(' ')[1]}</h3>
                  <p className="text-sm text-gray-700 font-semibold">{step.status}</p>
                  {index <= currentStep && (
                    <p className="text-xs text-gray-500 mt-1">{step.detail}</p>
                  )}
                </div>
                <div className="flex-shrink-0">
                  {index < currentStep && (
                    <div className="text-green-500 animate-bounce">
                      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                  {index === currentStep && (
                    <div className="animate-spin">
                      <svg className="w-8 h-8 text-purple-600" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Mood Analysis Results */}
          {result?.mood_analysis && (
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 mb-6 border-2 border-blue-200">
              <h3 className="font-bold text-gray-900 mb-4 text-lg flex items-center gap-2">
                <span>📊</span>
                Analysis Complete:
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                <div className="bg-white p-3 rounded-lg shadow-sm">
                  <p className="text-gray-600 text-xs mb-1">Primary Emotion:</p>
                  <p className="font-bold text-gray-900 capitalize text-lg">
                    {result.mood_analysis.primary_emotion}
                  </p>
                </div>
                <div className="bg-white p-3 rounded-lg shadow-sm">
                  <p className="text-gray-600 text-xs mb-1">Urgency Level:</p>
                  <p className={`font-bold text-lg ${
                    result.mood_analysis.urgency_level === 'HIGH' ? 'text-red-600' :
                    result.mood_analysis.urgency_level === 'MODERATE' ? 'text-yellow-600' :
                    'text-green-600'
                  }`}>
                    {result.mood_analysis.urgency_level}
                  </p>
                </div>
                <div className="bg-white p-3 rounded-lg shadow-sm">
                  <p className="text-gray-600 text-xs mb-1">Support Needs:</p>
                  <p className="font-semibold text-gray-900 text-sm">
                    {result.mood_analysis.needs?.[0] || 'General support'}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Agent Communications Log */}
          {showCommunication && result?.agent_communications && result.agent_communications.length > 0 && (
            <div className="bg-gray-50 rounded-xl p-5 border-2 border-gray-200 animate-fadeIn">
              <h3 className="font-bold text-gray-700 mb-3 flex items-center gap-2">
                <span>🔗</span>
                Agent Communications ({result.agent_communications.length}):
              </h3>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {result.agent_communications.map((comm, index) => (
                  <div key={index} className="text-xs bg-white p-3 rounded-lg border border-gray-200 shadow-sm">
                    <span className="font-bold text-purple-600">{comm.from}</span>
                    <span className="text-gray-400 mx-2">→</span>
                    <span className="font-bold text-blue-600">{comm.to}</span>
                    <span className="text-gray-500 ml-3 px-2 py-0.5 bg-gray-100 rounded">
                      {comm.type}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Loading Progress */}
          <div className="mt-6">
            <div className="w-full bg-gray-200 rounded-full h-3 shadow-inner">
              <div 
                className="bg-gradient-to-r from-purple-600 to-blue-600 h-3 rounded-full transition-all duration-500 shadow-lg"
                style={{ width: `${((currentStep + 1) / agentSteps.length) * 100}%` }}
              />
            </div>
            <div className="flex justify-between mt-2">
              <p className="text-sm text-gray-500">
                Step {currentStep + 1} of {agentSteps.length}
              </p>
              <p className="text-sm font-semibold text-gray-700">
                {Math.round(((currentStep + 1) / agentSteps.length) * 100)}% complete
              </p>
            </div>
          </div>

          {/* Fun Fact */}
          <div className="mt-6 text-center">
            <p className="text-xs text-gray-500 italic">
              💡 Did you know? Our agents exchange {result?.agent_communications?.length || 12}+ messages to find your perfect match!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AgentProcessing;