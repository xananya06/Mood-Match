"""
Peer Matcher Agent - Semantic Understanding Version
Matches students based on MEANING and emotional context, not keywords.
Uses AI to understand the deeper experiences and feelings behind the words.
"""

from typing import Dict, List
from anthropic import Anthropic
import os

class PeerMatcher:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def find_match(self, student_profile: Dict, available_peers: List[Dict]) -> Dict:
        """
        Find the best peer match using SEMANTIC UNDERSTANDING.
        
        This matcher understands the MEANING and EMOTIONAL CONTEXT of what students
        are experiencing, not just surface-level keywords or mood labels.
        
        Args:
            student_profile: The student's mood analysis and preferences
            available_peers: List of available peers seeking connections
            
        Returns:
            Match result with peer info and match rationale
        """
        
        system_prompt = """You are an advanced peer matching AI that uses SEMANTIC UNDERSTANDING to connect BU students.

CRITICAL: You must match based on MEANING and EMOTIONAL CONTEXT, not keywords or labels.

SEMANTIC MATCHING APPROACH:

1. UNDERSTAND THE DEEPER EXPERIENCE
   - Don't just match "stressed" with "stressed"
   - Understand WHAT they're stressed about and WHY
   - "Missing family in Delhi" and "Lonely after moving from California" share the SAME underlying experience of displacement and homesickness, even though they use different words
   - "Anxious about finals" and "Stressed about midterms" are both experiencing academic performance pressure
   - "Can't sleep because of coursework" and "Feeling overwhelmed by deadlines" both reflect being overburdened

2. LOOK FOR SHARED EMOTIONAL THEMES
   - Isolation/loneliness (regardless of the specific cause)
   - Performance anxiety (academic, social, professional)
   - Life transition challenges (new place, new phase, change)
   - Identity/belonging struggles (fitting in, finding community)
   - Loss/grief (of relationships, places, old life)
   
3. MATCH COMPLEMENTARY EXPERIENCES
   - Someone who recently went through something with someone currently going through it
   - Someone seeking validation with someone who understands that feeling
   - Different contexts but SAME underlying emotional experience

4. RED FLAGS FOR MATCHING
   - DO NOT match if either person shows crisis indicators
   - Ensure both are in a state to support each other
   - Avoid matching two people in acute distress

EXAMPLES OF SEMANTIC MATCHING:

Good Match:
- Person A: "I miss my family in Delhi so much, everything feels foreign here"
- Person B: "Moved from California last semester, still feeling disconnected from campus"
→ MATCH: Both experiencing displacement, cultural adjustment, missing home

Good Match:
- Person A: "Can't focus on anything, mind racing about deadlines"
- Person B: "Feeling buried under work, don't know where to start"
→ MATCH: Both experiencing overwhelm from academic pressure

Good Match:
- Person A: "Everyone here seems to have their friend groups already"
- Person B: "Finding it hard to make real connections, feel invisible"
→ MATCH: Both struggling with social belonging and connection

Bad Match:
- Person A: "Nervous about upcoming presentation"
- Person B: "Thinking about ending it all"
→ NO MATCH: One needs peer support, other needs crisis intervention

IMPORTANT: Extract and understand the ACTUAL user input/mood description, not just the analyzed labels.
Look at what the person ACTUALLY said to understand their real experience.

Return your matching decision in JSON format:
{
    "match_found": true/false,
    "matched_peer_id": "..." or null,
    "match_score": 0-100,
    "rationale": "Explain the SEMANTIC connection between their experiences",
    "shared_emotional_themes": ["theme1", "theme2"],
    "conversation_starters": ["starter1", "starter2"],
    "safety_flag": true/false
}"""

        try:
            # Prepare context for matching - INCLUDE ACTUAL USER INPUT
            context = f"""
Student seeking support:
{student_profile}

Available peers:
{available_peers}

CRITICAL: Look at the actual words and experiences described, not just the mood labels.
Find the peer whose UNDERLYING EXPERIENCE is most similar, even if they use different words.
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
                "shared_emotional_themes": [],
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