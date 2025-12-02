import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const agentSteps = [
  {
    agent: "🧠 MoodAnalyzer",
    status: "Analyzing emotional state...",
    detail: "Detecting emotions, urgency level, and support needs",
    color: "purple",
  },
  {
    agent: "🎯 Coordinator",
    status: "Orchestrating multi-agent collaboration...",
    detail: "Deciding which agents to activate and coordination strategy",
    color: "blue",
  },
  {
    agent: "🤝 PeerMatcher",
    status: "Finding compatible peers...",
    detail: "Matching based on mood (80%) + profile (20%)",
    color: "green",
  },
  {
    agent: "📍 LocationAgent",
    status: "Finding perfect meetup spots...",
    detail: "Recommending BU locations based on your match",
    color: "orange",
  },
  {
    agent: "💬 EmailGenerator",
    status: "Crafting personalized notification...",
    detail: "Creating email with location suggestions",
    color: "pink",
  }
];

export default function AgentProcessing() {
  const navigate = useNavigate();
  const location = useLocation();
  const { moodText, userId } = location.state || {};

  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!moodText) {
      navigate('/');
      return;
    }

    processWithAgents();
  }, []);

  const processWithAgents = async () => {
    try {
      // Animate through steps
      for (let i = 0; i < agentSteps.length; i++) {
        setCurrentStep(i);
        await new Promise(resolve => setTimeout(resolve, 1200));
      }

      // Call backend
      console.log('🚀 Calling backend...');
      
      const analyzeResponse = await fetch('http://localhost:8000/api/analyze-mood', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mood_text: moodText,
          user_id: userId || 'student_ananya'
        })
      });

      if (!analyzeResponse.ok) {
        throw new Error('Analysis failed');
      }

      const analysisResult = await analyzeResponse.json();
      console.log('✅ Analysis done:', analysisResult);

      if (analysisResult.crisis_detected) {
        navigate('/crisis', { state: { analysisResult } });
        return;
      }

      const matchResponse = await fetch('http://localhost:8000/api/find-match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId || 'student_ananya',
          mood_analysis: analysisResult.mood_analysis
        })
      });

      if (!matchResponse.ok) {
        throw new Error('Matching failed');
      }

      const matchResult = await matchResponse.json();
      console.log('✅ Match result:', matchResult);
      
      // Force navigation after 500ms
      setTimeout(() => {
        console.log('🎉 Navigating to result...');
        navigate('/result', { 
          state: { 
            result: matchResult,
            moodText,
            analysisResult 
          },
          replace: true
        });
      }, 500);

    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-red-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md border-2 border-red-300">
          <div className="text-6xl mb-4 text-center">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4 text-center">Error</h2>
          <p className="text-gray-600 mb-6 text-center">{error}</p>
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <div className="text-6xl mb-4 animate-bounce">🤖</div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Multi-Agent Processing
          </h1>
          <p className="text-gray-600">
            5 specialized AI agents working together
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8 border-2 border-purple-200">
          <div className="flex items-start gap-3">
            <div className="text-3xl">👩‍💻</div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-gray-500 mb-2">YOUR MOOD:</p>
              <p className="text-gray-800 italic">"{moodText}"</p>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          {agentSteps.map((step, index) => {
            const isActive = index === currentStep;
            const isComplete = index < currentStep;

            return (
              <div
                key={index}
                className={`
                  rounded-2xl p-6 border-2 transition-all
                  ${isActive ? 'shadow-lg scale-105 ring-4 ring-purple-200 bg-purple-50 border-purple-300' : ''}
                  ${isComplete ? 'opacity-75 bg-green-50 border-green-300' : ''}
                  ${!isActive && !isComplete ? 'opacity-40 bg-gray-50 border-gray-200' : ''}
                `}
              >
                <div className="flex items-start gap-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${isComplete ? 'bg-green-200' : isActive ? 'bg-purple-200' : 'bg-gray-200'}`}>
                    {isComplete ? (
                      <span className="text-2xl">✓</span>
                    ) : isActive ? (
                      <span className="text-2xl animate-spin">⚙️</span>
                    ) : (
                      <span className="text-2xl">⏳</span>
                    )}
                  </div>

                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 mb-1">
                      {step.agent}
                    </h3>
                    <p className="text-gray-700 font-medium mb-1">
                      {isComplete ? '✅ Complete' : isActive ? step.status : 'Waiting...'}
                    </p>
                    <p className="text-sm text-gray-600">{step.detail}</p>

                    {isActive && (
                      <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
                        <div className="bg-gradient-to-r from-purple-600 to-blue-600 h-full rounded-full animate-pulse w-3/4"></div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-8 bg-blue-50 rounded-lg p-6 border-2 border-blue-200">
          <h3 className="font-bold text-gray-900 mb-2">💡 What's happening?</h3>
          <p className="text-sm text-gray-700">
            Our multi-agent system analyzes your mood (80% weight) and profile (20% weight) to find the best peer match, then recommends specific BU locations where you should meet.
          </p>
        </div>
      </div>
    </div>
  );
}