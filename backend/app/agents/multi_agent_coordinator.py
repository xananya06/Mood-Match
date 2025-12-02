"""
Multi-Agent Coordinator - UPDATED WITH LOCATIONAGENT
Orchestrates the collaboration between all agents in the Mood Match system.
"""

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime
from anthropic import Anthropic
import os

from app.agents.mood_analyzer import MoodAnalyzer
from app.agents.peer_matcher import PeerMatcher
from app.agents.conversation_facilitator import ConversationFacilitator
from app.agents.location_agent import LocationAgent  # NEW!


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    message_type: str  # request, response, query, alert
    content: Dict
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class MultiAgentCoordinator:
    """
    Meta-agent that orchestrates other agents using:
    - Hierarchical coordination
    - Dynamic strategy selection
    - Communication logging
    """
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Initialize all agents
        self.mood_analyzer = MoodAnalyzer()
        self.peer_matcher = PeerMatcher()
        self.conversation_facilitator = ConversationFacilitator()
        self.location_agent = LocationAgent()  # NEW!
        
        # Communication log
        self.communication_log: List[AgentMessage] = []
        
    def log_communication(self, message: AgentMessage):
        """Log inter-agent communication"""
        self.communication_log.append(message)
        
    def get_communication_log(self) -> List[Dict]:
        """Get formatted communication log"""
        return [
            {
                "sender": msg.sender,
                "recipient": msg.recipient,
                "type": msg.message_type,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in self.communication_log
        ]
    
    def decide_activation_strategy(self, mood_analysis: Dict) -> Dict:
        """
        Coordinator decides which agents to activate and in what order.
        
        Returns:
            {
                "strategy": "sequential" | "parallel" | "crisis",
                "agents": ["agent1", "agent2"],
                "reasoning": "why this strategy"
            }
        """
        urgency = mood_analysis.get("urgency_level", "MODERATE")
        
        system_prompt = """You are the Coordinator agent deciding activation strategy.

Based on mood analysis, decide:
1. Which agents to activate
2. In what order (sequential, parallel, or crisis mode)
3. Reasoning for this decision

AVAILABLE AGENTS:
- MoodAnalyzer: Already ran
- PeerMatcher: Find compatible peers
- ConversationFacilitator: Provide conversation support
- LocationAgent: Recommend meetup locations

STRATEGIES:
- sequential: Activate agents one by one (clear causality)
- parallel: Activate multiple simultaneously (lower latency)
- crisis: Emergency mode with validation

RULES:
- If CRISIS urgency: Use crisis strategy
- If HIGH urgency: Use sequential for safety
- If MODERATE/LOW: Can use parallel

Return JSON:
{
    "strategy": "...",
    "agents": ["agent1", "agent2"],
    "reasoning": "..."
}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Mood Analysis:\n{mood_analysis}\n\nDecide activation strategy."
                    }
                ]
            )
            
            import json
            response_text = response.content[0].text.strip()
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            decision = json.loads(response_text)
            
            # Log decision
            decision_msg = AgentMessage(
                sender="Coordinator",
                recipient="System",
                message_type="decision",
                content=decision
            )
            self.log_communication(decision_msg)
            
            return decision
            
        except Exception as e:
            print(f"Error in activation decision: {e}")
            # Fallback
            return {
                "strategy": "sequential",
                "agents": ["peer_matcher", "conversation_facilitator", "location_agent"],
                "reasoning": "Default sequential strategy"
            }
    
    def process_mood_entry(self, mood_text: str, user_profile: Dict = None) -> Dict:
        """
        Main coordination method - orchestrates all agents.
        
        Args:
            mood_text: User's mood description
            user_profile: Optional user profile data
            
        Returns:
            Complete result with all agent outputs
        """
        # Clear previous log
        self.communication_log = []
        
        result = {
            "success": False,
            "mood_analysis": None,
            "coordination_strategy": None,
            "match_result": None,
            "conversation_support": None,
            "location_recommendations": None,  # NEW!
            "communication_log": []
        }
        
        try:
            # STEP 1: MOOD ANALYSIS (Reactive Agent)
            mood_analysis = self.mood_analyzer.analyze_mood(mood_text)
            result["mood_analysis"] = mood_analysis
            
            mood_msg = AgentMessage(
                sender="MoodAnalyzer",
                recipient="Coordinator",
                message_type="response",
                content=mood_analysis
            )
            self.log_communication(mood_msg)
            
            # STEP 2: DECIDE COORDINATION STRATEGY (Deliberative Agent)
            activation_decision = self.decide_activation_strategy(mood_analysis)
            result["coordination_strategy"] = activation_decision
            
            # STEP 3: CHECK FOR CRISIS
            if mood_analysis.get("urgency_level") == "CRISIS":
                # Crisis mode: Multi-agent validation required
                validation = self.conversation_facilitator.validate_crisis(mood_text)
                
                validation_msg = AgentMessage(
                    sender="ConversationFacilitator",
                    recipient="Coordinator",
                    message_type="alert",
                    content={"crisis_validated": validation}
                )
                self.log_communication(validation_msg)
                
                result["crisis_detected"] = True
                result["crisis_validated"] = validation
                result["success"] = True
                result["communication_log"] = self.get_communication_log()
                return result
            
            # STEP 4: EXECUTE ACTIVATION STRATEGY
            # For now, we'll do sequential activation
            
            result["success"] = True
            result["communication_log"] = self.get_communication_log()
            return result
            
        except Exception as e:
            print(f"Error in coordination: {e}")
            import traceback
            traceback.print_exc()
            result["error"] = str(e)
            result["communication_log"] = self.get_communication_log()
            return result
    
    def get_location_recommendations(
        self, 
        student1_profile: Dict, 
        student2_profile: Dict, 
        match_context: Dict
    ) -> Dict:
        """
        Get location recommendations using LocationAgent
        NEW METHOD FOR INTEGRATION
        """
        try:
            location_recs = self.location_agent.recommend_locations(
                student1_profile,
                student2_profile,
                match_context
            )
            
            # Log communication
            location_message = AgentMessage(
                sender="LocationAgent",
                recipient="Coordinator",
                message_type="response",
                content=location_recs
            )
            self.log_communication(location_message)
            
            return location_recs
        except Exception as e:
            print(f"Error getting location recommendations: {e}")
            return {
                "locations": [],
                "overall_strategy": "Meet somewhere comfortable",
                "timing_suggestion": "Afternoon",
                "conversation_tips": []
            }
    
    def get_statistics(self) -> Dict:
        """Get system statistics"""
        return {
            "total_communications": len(self.communication_log),
            "agents_active": ["MoodAnalyzer", "Coordinator", "PeerMatcher", "ConversationFacilitator", "LocationAgent"],
            "average_messages_per_session": len(self.communication_log)
        }