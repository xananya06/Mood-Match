import { useLocation, useNavigate } from 'react-router-dom';

function CrisisAlert() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  const crisisResources = [
    {
      name: "BU Police Emergency",
      contact: "911 or (617) 353-2121",
      description: "24/7 emergency response for life-threatening situations",
      urgent: true
    },
    {
      name: "Crisis Text Line",
      contact: "Text 'HOME' to 741741",
      description: "24/7 text-based crisis support",
      urgent: true
    },
    {
      name: "National Suicide Prevention Lifeline", 
      contact: "988 or 1-800-273-8255",
      description: "24/7 suicide prevention hotline",
      urgent: true
    },
    {
      name: "BU Student Health Services",
      contact: "(617) 353-3569",
      description: "Professional counseling and psychiatric services",
      urgent: false
    }
  ];

  return (
    <div className="min-h-screen bg-red-50 flex items-center justify-center p-4">
      <div className="max-w-3xl w-full">
        {/* Alert Header */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border-4 border-red-500">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-3xl">🚨</span>
            </div>
            <div>
              <h1 className="text-3xl font-bold text-red-600">
                We're Here to Help
              </h1>
              <p className="text-lg text-gray-700 mt-1">
                Your safety is our priority
              </p>
            </div>
          </div>

          {/* Multi-Agent Detection Notice */}
          <div className="bg-red-100 border-l-4 border-red-500 p-4 mb-6">
            <p className="text-red-800 font-semibold">
              🤖 Multiple AI agents have identified that you may need immediate professional support
            </p>
            {result?.mood_analysis && (
              <p className="text-red-700 text-sm mt-2">
                Urgency Level: <strong>{result.mood_analysis.urgency_level}</strong>
              </p>
            )}
          </div>

          {/* Crisis Resources */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              Immediate Support Resources:
            </h2>

            {crisisResources.map((resource, index) => (
              <div 
                key={index}
                className={`p-5 rounded-lg border-2 ${
                  resource.urgent 
                    ? 'bg-red-50 border-red-300' 
                    : 'bg-blue-50 border-blue-300'
                }`}
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-gray-900 text-lg">
                    {resource.name}
                  </h3>
                  {resource.urgent && (
                    <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full font-semibold">
                      24/7
                    </span>
                  )}
                </div>
                <p className="text-gray-700 mb-2">{resource.description}</p>
                <a 
                  href={`tel:${resource.contact.replace(/[^0-9]/g, '')}`}
                  className="text-lg font-bold text-blue-600 hover:text-blue-800"
                >
                  📞 {resource.contact}
                </a>
              </div>
            ))}
          </div>

          {/* Important Message */}
          <div className="mt-8 p-6 bg-yellow-50 border-2 border-yellow-300 rounded-lg">
            <h3 className="font-bold text-yellow-900 mb-2">
              ⚠️ Important
            </h3>
            <p className="text-yellow-800">
              If you're in immediate danger, please call <strong>911</strong> or 
              go to your nearest emergency room. These feelings are temporary, and 
              help is available. You matter, and people care about you.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="mt-8 flex gap-4">
            <button
              onClick={() => window.location.href = 'tel:988'}
              className="flex-1 bg-red-600 text-white py-4 rounded-lg font-bold text-lg hover:bg-red-700 transition-colors"
            >
              📞 Call 988 Now
            </button>
            <button
              onClick={() => navigate('/')}
              className="flex-1 bg-gray-200 text-gray-800 py-4 rounded-lg font-semibold text-lg hover:bg-gray-300 transition-colors"
            >
              Return Home
            </button>
          </div>
        </div>

        {/* Additional Support */}
        <div className="mt-6 text-center text-gray-600 text-sm">
          <p>This page was designed with care to support BU students</p>
          <p className="mt-2">You're not alone. Help is available 24/7.</p>
        </div>
      </div>
    </div>
  );
}

export default CrisisAlert;