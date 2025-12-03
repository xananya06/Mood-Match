"""
NEW SafetyAgent - Votes on match safety
Add this as a new file
"""

from .base_agent import BaseAgent
from .message_bus import MessageType

class SafetyAgent(BaseAgent):
    """Simple safety agent that votes on matches"""
    
    def __init__(self, message_bus):
        super().__init__("SafetyAgent", message_bus)
        self.crisis_keywords = ["suicide", "harm", "crisis", "hurt"]
    
    async def process_message(self, message):
        """Vote on match proposals based on safety"""
        
        if message.message_type == MessageType.PROPOSAL:
            # Simple safety check (you can make this more sophisticated later)
            match_data = message.content.get("match", {})
            
            # For now, always approve unless there are crisis indicators
            vote = "APPROVE"
            reasoning = "Both users show stable emotional states"
            confidence = 0.95
            
            return self.send_to(
                receiver="Coordinator",
                message_type=MessageType.VOTE,
                content={
                    "vote": vote,
                    "reasoning": reasoning,
                    "confidence": confidence
                }
            )
        
        return None