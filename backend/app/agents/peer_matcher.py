"""
Peer Matcher Agent
Matches students based on emotional states, needs, and contexts.
Ensures appropriate peer support connections for BU students.
"""

from typing import Dict, List
from anthropic import Anthropic
import os

class PeerMatcher:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def find_match(self, student_profile: Dict, available_peers: List[Dict]) -> Dict:
        """
        Find the best peer match for the student.
        
        Args:
            student_profile: The student's mood analysis and preferences
            available_peers: List of available peers seeking connections
            
        Returns:
            Match result with peer info and match rationale
        """
        
        system_prompt = """You are a peer matching specialist for BU students seeking support.

Your role is to match students who can provide mutual peer support. Consider:

1. EMOTIONAL COMPATIBILITY
   - Similar experiences or challenges
   - Complementary support needs (someone seeking support + someone able to give it)
   - Appropriate emotional states (avoid matching two people in crisis)

2. SUPPORT TYPE ALIGNMENT
   - Listener: Someone who needs to be heard
   - Advisor: Someone seeking practical guidance
   - Companion: Someone wanting presence/company

3. BU-SPECIFIC CONTEXT
   - Academic stress (exams, deadlines, major-related)
   - Social challenges (homesickness, making friends)
   - Life transitions (new to BU, graduating, personal changes)

4. SAFETY CONSIDERATIONS
   - DO NOT match if either person shows crisis indicators
   - Ensure both are in a state to support each other
   - Consider time zones and availability

Return matching decision in JSON format:
{
    "match_found": true/false,
    "matched_peer_id": "..." or null,
    "match_score": 0-100,
    "rationale": "Why this is a good match",
    "conversation_starters": ["starter1", "starter2"],
    "safety_flag": true/false
}"""

        try:
            # Prepare context for matching
            context = f"""
Student seeking support:
{student_profile}

Available peers:
{available_peers}

Find the best match or indicate if no safe match is available.
"""
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": context
                    }
                ]
            )
            
            # Parse response - handle markdown formatting
            import json
            response_text = response.content[0].text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            match_result = json.loads(response_text)
            
            return match_result
            
        except Exception as e:
            print(f"Error in peer matching: {e}")
            return {
                "match_found": False,
                "matched_peer_id": None,
                "match_score": 0,
                "rationale": "Unable to find match at this time",
                "conversation_starters": [],
                "safety_flag": False
            }
    
    def validate_match_safety(self, student1: Dict, student2: Dict) -> bool:
        """
        Validate that a match is safe for both parties.
        Returns False if either person is in crisis or match seems unsafe.
        """
        # Check for crisis indicators
        if student1.get("urgency_level") == "CRISIS" or student2.get("urgency_level") == "CRISIS":
            return False
            
        # Both should not be in high distress
        if student1.get("urgency_level") == "HIGH" and student2.get("urgency_level") == "HIGH":
            return False
            
        return True