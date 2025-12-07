# Mood Match 🧘‍♀️🍵
> *Finding you a BU peer when you need one most* 🐾

A multi-agent AI system that matches BU students for peer support based on how you're feeling **today**, not static profiles.

## 💡 The Idea

Mood Match connects you with another BU student experiencing similar emotions. Think of it as a **support buddy finder**, not a dating app - just genuine peer to peer support when you need it most.

## 🤖 How It Works

Four AI agents work together through a message bus:
```
        📊 MoodAnalyzer
        (analyzes emotions)
             ↓
    ┌────────┼────────┐
    ↓        ↓        ↓
🤝 Peer  📍Location  🛡️ Safety
Matcher    Agent     Agent
```

- **📊 MoodAnalyzer** - Analyzes emotional state and urgency level
- **🤝 PeerMatcher** - Finds compatible peers using 80% mood + 20% profile matching
- **📍 LocationAgent** - Suggests BU campus meeting spots based on your mood
- **🛡️ SafetyAgent** - Monitors for crisis and can halt matching if needed

### 🛡️ Safety First
If you're in crisis, the system **immediately halts matching** and displays emergency resources:
- BU Police: 617-353-2121
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text "HELLO" to 741741

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run!
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` and you're ready! ✨

## 📁 What's Inside
```
backend/app/agents/          # 🤖 The AI agents
  ├── mood_analyzer.py       # Analyzes emotions & urgency
  ├── peer_matcher.py        # Matches peers (80/20 algorithm)
  ├── location_agent.py      # Suggests BU meeting spots
  ├── safety_agent.py        # Crisis detection & monitoring
  ├── message_bus.py         # Agent communication system
  ├── multi_agent_coordinator.py   # Orchestrates everything
  └── bu_resources.py        # BU campus resources

backend/app/api/routes/      # 🛣️ API endpoints
backend/app/models/          # 📦 Data models
frontend/src/                # 🎨 React app
```

## 🔬 The Matching Algorithm
```
Final Score = (0.8 × Mood Similarity) + (0.2 × Profile Compatibility)
```

**Mood Similarity**: Emotional state, urgency level, shared themes  
**Profile Compatibility**: Shared interests (+15), similar year (+10), personality (+10)

## 🛠️ Built With

FastAPI • Claude Sonnet 4 (Anthropic) • React • Tailwind CSS

---

*Made with ❤️ for BU students by Ananya*  
*CS 599X1: AI Agents - Fall 2025*
