"""
SafetyAgent - Monitors proposals and can object
"""

from .base_agent import BaseAgent
from .message_bus import MessageType

class SafetyAgent(BaseAgent):
    """Safety agent that monitors and can object to matches"""
    
    def __init__(self, message_bus):
        super().__init__("SafetyAgent", message_bus)
        self.crisis_keywords = ["suicide", "harm", "crisis", "hurt", "hopeless"]
        self.risk_threshold = 75  # Require higher match scores for at-risk users
    
    async def process_message(self, message):
        """Monitor broadcasts and object to unsafe matches"""
        
        # Monitor mood broadcasts for risk assessment
        if message.message_type == MessageType.BROADCAST:
            if message.sender == "MoodAnalyzer":
                print(f"  👁️  SafetyAgent: Monitoring mood analysis...")
                analysis = message.content.get("analysis", {})
                urgency = analysis.get("urgency_level", "MODERATE")
                
                # Store risk assessment
                if urgency == "HIGH":
                    self.internal_state["risk_level"] = "HIGH"
                    print(f"  ⚠️  SafetyAgent: HIGH urgency detected - will scrutinize matches")
                else:
                    self.internal_state["risk_level"] = "MODERATE"
        
        # Monitor and potentially object to proposals
        elif message.message_type == MessageType.PROPOSAL:
            print(f"  🛡️  SafetyAgent: Reviewing match proposal for safety...")
            
            match_data = message.content.get("match", {})
            match_score = match_data.get("match_score", 0)
            risk_level = self.internal_state.get("risk_level", "MODERATE")
            
            # Decision logic
            should_object = False
            objection_reason = None
            
            if risk_level == "HIGH" and match_score < self.risk_threshold:
                should_object = True
                objection_reason = f"Match score ({match_score}%) below safety threshold ({self.risk_threshold}%) for HIGH risk user"
            
            if should_object:
                print(f"  🚫 SafetyAgent: OBJECTION raised!")
                # Send objection
                self.broadcast(
                    MessageType.NOTIFICATION,
                    {
                        "alert": "SAFETY_OBJECTION",
                        "reason": objection_reason,
                        "recommendation": "Suggest professional support resources instead"
                    }
                )
                return None  # Objection is the notification, no separate vote needed
            else:
                print(f"  ✅ SafetyAgent: Match appears safe")
                return None  # No objection = silent approval
        
        return None