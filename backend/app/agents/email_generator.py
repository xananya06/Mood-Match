"""
Updated EmailGenerator (minimal changes)
Replace your existing email_generator.py with this
"""

from .base_agent import BaseAgent
from .message_bus import MessageType
import anthropic

class EmailGenerator(BaseAgent):
    def __init__(self, message_bus, client: anthropic.Anthropic):
        super().__init__("EmailGenerator", message_bus)
        self.client = client
    
    async def generate_email(self, user_profile: dict, match_result: dict, location: dict) -> dict:
        """Generate introduction email"""
        
        # Your existing email generation logic
        prompt = f"""Create a warm introduction email for two matched students.

User: {user_profile}
Match: {match_result}
Location: {location}

Return JSON with:
- subject (string)
- body (string)
- tone (string)"""

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
            
            return result
            
        except Exception as e:
            print(f"Error in EmailGenerator: {e}")
            return {
                "subject": "You've been matched!",
                "body": "We found someone who might be a good peer support match for you.",
                "tone": "warm"
            }
    
    async def process_message(self, message):
        """Email generator doesn't need to process messages"""
        return None