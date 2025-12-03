"""
Base Agent Class with Message Bus Integration
All agents inherit from this to enable communication
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from .message_bus import MessageBus, AgentMessage, MessageType
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all agents with communication capabilities"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        self.agent_id = agent_id
        self.message_bus = message_bus
        self.last_message_check = datetime.now()
        self.internal_state = {}  # For storing agent's internal state
        
    def broadcast(self, message_type: MessageType, content: Dict[str, Any]) -> AgentMessage:
        """Send a message to all agents"""
        return self.message_bus.broadcast(
            sender=self.agent_id,
            message_type=message_type,
            content=content
        )
    
    def send_to(self, receiver: str, message_type: MessageType, 
                content: Dict[str, Any], in_reply_to: Optional[str] = None) -> AgentMessage:
        """Send a direct message to another agent"""
        return self.message_bus.send_to(
            sender=self.agent_id,
            receiver=receiver,
            message_type=message_type,
            content=content,
            in_reply_to=in_reply_to
        )
    
    def get_messages(self, message_type: Optional[MessageType] = None) -> List[AgentMessage]:
        """Get messages addressed to this agent since last check"""
        messages = self.message_bus.get_messages_for(
            agent_id=self.agent_id,
            message_type=message_type,
            since=self.last_message_check
        )
        self.last_message_check = datetime.now()
        return messages
    
    def get_all_broadcasts(self) -> List[AgentMessage]:
        """Get all broadcast messages since last check"""
        all_messages = self.message_bus.get_messages_for(
            agent_id=self.agent_id,
            since=self.last_message_check
        )
        self.last_message_check = datetime.now()
        return [m for m in all_messages if m.receiver == "ALL"]
    
    @abstractmethod
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """
        Process an incoming message and optionally return a response
        Each agent implements its own message processing logic
        """
        pass
    
    async def check_and_process_messages(self) -> List[AgentMessage]:
        """Check for new messages and process them"""
        messages = self.get_messages()
        responses = []
        
        for msg in messages:
            response = await self.process_message(msg)
            if response:
                responses.append(response)
                
        return responses
    
    def log_decision(self, decision: str, reasoning: str, confidence: float = 1.0) -> Dict[str, Any]:
        """Log an agent decision with reasoning (for explainability)"""
        log_entry = {
            "agent": self.agent_id,
            "decision": decision,
            "reasoning": reasoning,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
        
        # Broadcast decision to other agents
        self.broadcast(
            message_type=MessageType.NOTIFICATION,
            content={
                "summary": f"{self.agent_id} decided: {decision}",
                **log_entry
            }
        )
        
        return log_entry
    
    def get_state(self) -> Dict[str, Any]:
        """Get current agent state (for debugging/monitoring)"""
        return {
            "agent_id": self.agent_id,
            "state": self.internal_state,
            "last_check": self.last_message_check.isoformat()
        }


# Example: Communication-enabled MoodAnalyzer
class CommunicativeMoodAnalyzer(BaseAgent):
    """MoodAnalyzer that broadcasts findings and responds to queries"""
    
    def __init__(self, message_bus: MessageBus):
        super().__init__("MoodAnalyzer", message_bus)
        self.analysis_history = []
        
    async def analyze_mood(self, user_input: str, anthropic_client) -> Dict[str, Any]:
        """Analyze mood and broadcast findings"""
        
        # TODO: Replace with actual Claude API call
        # For now, simulating the analysis
        analysis = {
            "primary_emotion": "overwhelmed",
            "urgency_level": "MODERATE",
            "emotional_themes": ["career anxiety", "self-doubt"],
            "needs": ["peer support", "reassurance"]
        }
        
        # Store in history
        self.analysis_history.append(analysis)
        self.internal_state["last_analysis"] = analysis
        
        # Broadcast findings to all agents
        self.broadcast(
            message_type=MessageType.BROADCAST,
            content={
                "summary": f"User shows {analysis['urgency_level']} urgency with {analysis['primary_emotion']}",
                "analysis": analysis,
                "user_input": user_input
            }
        )
        
        # Log decision
        self.log_decision(
            decision=f"Classified as {analysis['urgency_level']} urgency",
            reasoning=f"Primary emotion '{analysis['primary_emotion']}' indicates moderate support need",
            confidence=0.85
        )
        
        return analysis
    
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Respond to queries about mood analysis"""
        
        if message.message_type == MessageType.QUERY:
            query = message.content.get("question", "")
            
            if "urgency" in query.lower():
                return self.send_to(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "summary": "Urgency level is MODERATE",
                        "answer": self.internal_state.get("last_analysis", {}).get("urgency_level", "UNKNOWN"),
                        "reasoning": "Based on emotional tone and language patterns"
                    },
                    in_reply_to=message.message_id
                )
            
            elif "emotion" in query.lower():
                return self.send_to(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "summary": "Primary emotion identified",
                        "answer": self.internal_state.get("last_analysis", {}).get("primary_emotion", "UNKNOWN"),
                        "themes": self.internal_state.get("last_analysis", {}).get("emotional_themes", [])
                    },
                    in_reply_to=message.message_id
                )
        
        return None


# Example: Communication-enabled PeerMatcher
class CommunicativePeerMatcher(BaseAgent):
    """PeerMatcher that queries other agents and proposes matches"""
    
    def __init__(self, message_bus: MessageBus):
        super().__init__("PeerMatcher", message_bus)
        self.mood_analysis = None
        self.location_preferences = None
        
    async def find_match(self, user_profile: Dict[str, Any], available_peers: List[Dict]) -> Dict[str, Any]:
        """Find match with agent communication"""
        
        # Step 1: Query MoodAnalyzer for latest analysis
        self.send_to(
            receiver="MoodAnalyzer",
            message_type=MessageType.QUERY,
            content={
                "summary": "Requesting latest mood analysis",
                "question": "What is the user's primary emotion and urgency level?"
            }
        )
        
        # Step 2: Query LocationAgent for preferences
        self.send_to(
            receiver="LocationAgent",
            message_type=MessageType.QUERY,
            content={
                "summary": "Requesting location preferences",
                "question": "What type of environment would work best for this user's mood?"
            }
        )
        
        # Step 3: Wait a moment for responses (in real implementation, this would be async)
        await self.check_and_process_messages()
        
        # Step 4: Use gathered info to find best match
        # TODO: Replace with actual matching logic
        best_match = {
            "match_found": True,
            "matched_peer_id": "student_marcus",
            "match_score": 87,
            "mood_similarity_score": 90,
            "profile_compatibility_score": 75
        }
        
        # Step 5: Propose the match to all agents
        proposal = self.broadcast(
            message_type=MessageType.PROPOSAL,
            content={
                "summary": f"Proposing match with {best_match['matched_peer_id']} ({best_match['match_score']}% score)",
                "match": best_match,
                "rationale": "Strong career anxiety alignment and compatible profiles"
            }
        )
        
        # Log decision
        self.log_decision(
            decision=f"Matched with {best_match['matched_peer_id']}",
            reasoning=f"Score: {best_match['match_score']}% based on mood similarity ({best_match['mood_similarity_score']}%) and profile compatibility ({best_match['profile_compatibility_score']}%)",
            confidence=0.87
        )
        
        self.internal_state["last_proposal_id"] = proposal.message_id
        return best_match
    
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process responses from other agents"""
        
        if message.message_type == MessageType.RESPONSE:
            if message.sender == "MoodAnalyzer":
                self.mood_analysis = message.content.get("answer")
                print(f"  📥 PeerMatcher received mood info: {self.mood_analysis}")
                
            elif message.sender == "LocationAgent":
                self.location_preferences = message.content.get("answer")
                print(f"  📥 PeerMatcher received location info: {self.location_preferences}")
        
        return None


if __name__ == "__main__":
    print("🧪 Testing Communicative Agents\n")
    
    import asyncio
    
    async def test_agent_communication():
        # Create message bus
        bus = MessageBus()
        
        # Create agents
        mood_agent = CommunicativeMoodAnalyzer(bus)
        matcher_agent = CommunicativePeerMatcher(bus)
        
        # Simulate workflow
        print("1️⃣ MoodAnalyzer analyzes user input...")
        await mood_agent.analyze_mood("I'm overwhelmed with my thesis and job search", None)
        
        print("\n2️⃣ PeerMatcher requests information from other agents...")
        await matcher_agent.find_match(
            user_profile={"name": "Ananya"},
            available_peers=[{"id": "student_marcus"}]
        )
        
        print("\n" + "="*60)
        print("📊 Message Bus Summary:")
        print("="*60)
        summary = bus.get_summary()
        print(f"Total messages: {summary['total_messages']}")
        print(f"\nTimeline:")
        for event in summary['timeline']:
            print(f"  {event['time'][-12:-7]} | {event['sender']:20s} → {event['type']:15s} | {event['summary']}")
    
    asyncio.run(test_agent_communication())