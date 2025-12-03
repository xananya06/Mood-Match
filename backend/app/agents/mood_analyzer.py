"""
Updated MoodAnalyzer with Communication
Replace your existing mood_analyzer.py with this
"""

from .base_agent import BaseAgent
from .message_bus import MessageType
import anthropic

class MoodAnalyzer(BaseAgent):
    def __init__(self, message_bus, client: anthropic.Anthropic):
        super().__init__("MoodAnalyzer", message_bus)
        self.client = client
    
    async def analyze_mood(self, user_input: str) -> dict:
        """Analyze user mood and BROADCAST findings"""
        
        prompt = f"""Analyze this user's emotional state:

User input: "{user_input}"

Return a JSON object with:
- primary_emotion (string)
- urgency_level (LOW/MODERATE/HIGH)
- emotional_themes (list of strings)
- matching_criteria (dict with relevant emotional factors)

Focus on emotional nuance and what kind of peer support would help."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            import re
            
            # Get the text response
            response_text = response.content[0].text.strip()
            
            # Extract JSON from response (handle markdown, extra text, etc.)
            # Look for content between curly braces
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            analysis = json.loads(response_text)
            
            # Store in internal state
            self.internal_state["last_analysis"] = analysis
            
            # BROADCAST findings to all agents
            self.broadcast(
                MessageType.BROADCAST,
                {
                    "summary": f"User emotion: {analysis['primary_emotion']} ({analysis['urgency_level']} urgency)",
                    "analysis": analysis,
                    "user_input": user_input
                }
            )
            
            # Log decision
            self.log_decision(
                decision=f"Classified as {analysis['urgency_level']} urgency",
                reasoning=f"Primary emotion '{analysis['primary_emotion']}' detected",
                confidence=0.85
            )
            
            return analysis
            
        except Exception as e:
            print(f"Error in MoodAnalyzer: {e}")
            return {
                "primary_emotion": "unknown",
                "urgency_level": "MODERATE",
                "emotional_themes": [],
                "matching_criteria": {}
            }
    
    async def process_message(self, message):
        """Respond to queries from other agents"""
        if message.message_type == MessageType.QUERY:
            question = message.content.get("question", "").lower()
            
            # Handle approval requests from PeerMatcher
            if message.content.get("requesting_approval"):
                print(f"  📨 MoodAnalyzer: Reviewing match proposal...")
                
                match_score = message.content.get("match_score", 0)
                last_analysis = self.internal_state.get("last_analysis", {})
                urgency = last_analysis.get("urgency_level", "MODERATE")
                
                # Decision logic
                if urgency == "HIGH" and match_score < 80:
                    print(f"  ⚠️  MoodAnalyzer: Score too low for HIGH urgency user")
                    approval = "NEGOTIATE"
                elif match_score < 70:
                    print(f"  ❌ MoodAnalyzer: Match score too low ({match_score}%)")
                    approval = "REJECTED"
                else:
                    print(f"  ✅ MoodAnalyzer: Match approved ({match_score}% score)")
                    approval = "APPROVED"
                
                # Send response back
                self.send_to(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "approval": approval,
                        "reasoning": f"Urgency: {urgency}, Score: {match_score}%"
                    },
                    in_reply_to=message.message_id
                )
                
                # Store in sender's state so they can access it
                # (In real system, sender would read their messages)
                return approval
            
            if "urgency" in question or "emotional state" in question:
                last_analysis = self.internal_state.get("last_analysis", {})
                return self.send_to(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "answer": last_analysis.get("urgency_level", "UNKNOWN"),
                        "emotion": last_analysis.get("primary_emotion", "UNKNOWN"),
                        "themes": last_analysis.get("emotional_themes", []),
                        "reasoning": "From recent mood analysis"
                    },
                    in_reply_to=message.message_id
                )
            
            elif "emotion" in question:
                return self.send_to(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "answer": self.internal_state.get("last_analysis", {}).get("primary_emotion", "UNKNOWN"),
                        "themes": self.internal_state.get("last_analysis", {}).get("emotional_themes", [])
                    },
                    in_reply_to=message.message_id
                )
        
        return None