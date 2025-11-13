# Mood Match🧘‍♀️🍵
> *Finding you a BU peer when you need one most* 🐾

A multi-agent AI system that matches BU students for peer support conversations. 

## 💡 The Idea

Ever feel stressed about finals? Homesick? Just need someone who *gets it*? 

Mood Match connects you with another BU student who's feeling similar things. Think of it as a **support buddy finder**, not a dating app - just genuine peer-to-peer support when you need it.

## 🤖 How It Works

Four AI agents work together to help you:

```
        🎯 Coordinator
        (the brain)
             ↓
   ┌─────────┼─────────┐
   ↓         ↓         ↓
💭 Mood    🤝 Peer   💬 Conversation
Analyzer   Matcher   Facilitator
```

- **💭 Mood Analyzer** - Understands how you're feeling
- **🤝 Peer Matcher** - Finds you a compatible peer
- **💬 Conversation Facilitator** - Helps guide the chat & suggests BU resources
- **🎯 Coordinator** - Makes sure all agents work together smoothly

### 🛡️ Safety First
If you're in crisis, the system **skips matching** and gives you immediate professional resources like BU Police and Student Health Services.

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
  ├── mood_analyzer.py       # Understands emotions
  ├── peer_matcher.py        # Finds matches
  ├── conversation_facilitator.py  # Guides chats
  ├── multi_agent_coordinator.py   # Orchestrates everything
  └── bu_resources.py        # BU campus resources

backend/app/api/routes/      # 🛣️ API endpoints
backend/app/models/          # 📦 Data models
frontend/src/                # 🎨 React app (work in progress!)
```


## 🛠️ Built With

FastAPI • Claude (Anthropic) • Supabase • React • Tailwind

---

*Made with 💜 for BU students*
