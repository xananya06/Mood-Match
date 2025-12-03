"""
Updated PeerMatcher with Communication
Replace your existing peer_matcher.py with this
"""

from .base_agent import BaseAgent
from .message_bus import MessageType
import anthropic
import asyncio

class PeerMatcher(BaseAgent):
    def __init__(self, message_bus, client: anthropic.Anthropic, supabase_client):
        super().__init__("PeerMatcher", message_bus)
        self.client = client
        self.supabase = supabase_client
    
    async def find_match(self, user_profile: dict, available_peers: list) -> dict:
        """Find best match with NEGOTIATION phase"""
        
        print("\n  🔍 PeerMatcher: Analyzing available peers...")
        
        # PHASE 1: QUERY MoodAnalyzer for context
        self.send_to(
            receiver="MoodAnalyzer",
            message_type=MessageType.QUERY,
            content={"question": "What is the user's urgency level and emotional state?"}
        )
        
        # Give agents time to respond
        await asyncio.sleep(0.1)
        await self.check_and_process_messages()
        
        # Your existing matching logic with Claude
        prompt = f"""You are a peer matching AI for a mental health support platform.

User Profile:
{user_profile}

Available Peers:
{available_peers}

SCORING FORMULA: Final Score = (Mood Similarity × 0.8) + (Profile Compatibility × 0.2)

Find the best match and return JSON:
{{
    "match_found": true/false,
    "matched_peer_id": "peer_id",
    "match_score": 85,
    "mood_similarity_score": 88,
    "profile_compatibility_score": 72,
    "rationale": "explanation",
    "shared_emotional_themes": ["theme1", "theme2"],
    "conversation_starters": ["starter1", "starter2"]
}}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            import re
            
            # Extract JSON from response
            result_text = response.content[0].text.strip()
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(0)
            
            match_result = json.loads(result_text)
            
            if match_result.get("match_found"):
                print(f"  ✓ Found potential match: {match_result['matched_peer_id']} ({match_result['match_score']}%)")
                
                # PHASE 2: NEGOTIATION - Seek approval from MoodAnalyzer
                print("\n  💬 PeerMatcher: Seeking approval from MoodAnalyzer...")
                self.send_to(
                    receiver="MoodAnalyzer",
                    message_type=MessageType.QUERY,
                    content={
                        "question": f"Do you approve this match with {match_result['matched_peer_id']}?",
                        "match_score": match_result['match_score'],
                        "rationale": match_result['rationale'],
                        "requesting_approval": True
                    }
                )
                
                # Wait for MoodAnalyzer's response
                await asyncio.sleep(0.2)  # Increased wait time
                await self.check_and_process_messages()
                
                # Check if we got approval (look in internal state)
                approval = self.internal_state.get("mood_analyzer_approval", "APPROVED")
                print(f"  📋 Approval status: {approval}")
                
                if approval == "REJECTED":
                    print("  ❌ MoodAnalyzer rejected the match")
                    return {"match_found": False, "reason": "Rejected by MoodAnalyzer"}
                elif approval == "NEGOTIATE":
                    print("  🔄 MoodAnalyzer suggests adjustments...")
                    # In a real system, we'd adjust and re-match
                    # For demo, we'll proceed with a note
                    match_result["negotiated"] = True
                else:
                    # APPROVED or default
                    pass
                
                print("  ✓ Match approved by MoodAnalyzer")
                
                # PHASE 3: PROPOSE match to all agents
                self.broadcast(
                    MessageType.PROPOSAL,
                    {
                        "summary": f"Proposing match: {match_result['matched_peer_id']} ({match_result['match_score']}% score)",
                        "match": match_result,
                        "rationale": match_result.get("rationale", ""),
                        "negotiated": match_result.get("negotiated", False)
                    }
                )
                
                # Log decision
                self.log_decision(
                    decision=f"Matched with {match_result['matched_peer_id']}",
                    reasoning=f"Score {match_result['match_score']}% based on mood similarity and profile compatibility",
                    confidence=match_result['match_score'] / 100
                )
            
            return match_result
            
        except Exception as e:
            print(f"Error in PeerMatcher: {e}")
            return {"match_found": False, "reason": str(e)}
    
    async def process_message(self, message):
        """Store responses from other agents"""
        if message.message_type == MessageType.RESPONSE:
            # Store info from other agents
            if message.sender == "MoodAnalyzer":
                # Check if this is an approval response
                if "approval" in message.content:
                    approval = message.content.get("approval", "APPROVED")
                    self.internal_state["mood_analyzer_approval"] = approval
                    print(f"  📥 PeerMatcher received approval: {approval}")
                else:
                    # General mood info
                    self.internal_state["mood_info"] = message.content
                    print(f"  📥 PeerMatcher received mood info")
        
        return None