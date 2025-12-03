"""
Updated LocationAgent with Communication
Replace your existing location_agent.py with this
"""

from .base_agent import BaseAgent
from .message_bus import MessageType
import anthropic

class LocationAgent(BaseAgent):
    def __init__(self, message_bus, client: anthropic.Anthropic):
        super().__init__("LocationAgent", message_bus)
        self.client = client
    
    async def recommend_location(self, mood_themes: list, student_a: dict, student_b: dict) -> dict:
        """Recommend meeting location"""
        
        # Your existing location logic
        prompt = f"""Recommend a meeting location on BU campus for two students.

Mood themes: {mood_themes}
Student A: {student_a}
Student B: {student_b}

Return JSON with:
- location (string)
- reasoning (string)
- address (string)
- alternative_locations (list)"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            import re
            
            # Extract JSON from response
            response_text = response.content[0].text.strip()
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            result = json.loads(response_text)
            
            # Log decision
            self.log_decision(
                decision=f"Recommended: {result['location']}",
                reasoning=result['reasoning'],
                confidence=0.9
            )
            
            return result
            
        except Exception as e:
            print(f"Error in LocationAgent: {e}")
            return {
                "location": "Mugar Library - 5th Floor",
                "reasoning": "Quiet study space",
                "address": "771 Commonwealth Ave"
            }
    
    async def process_message(self, message):
        """Respond to queries"""
        
        # Respond to queries
        if message.message_type == MessageType.QUERY:
            if "environment" in message.content.get("question", "").lower():
                return self.send_to(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "answer": "Quiet spaces like Mugar Library",
                        "reasoning": "Low-stimulation environments work best for anxiety"
                    },
                    in_reply_to=message.message_id
                )
        
        return None