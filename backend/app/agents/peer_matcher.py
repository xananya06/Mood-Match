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
        # Track match history to prevent repeat matches
        self.match_history = {}  # user_id -> [list of matched_peer_ids]
        
    def find_match(self, student_profile: Dict, available_peers: List[Dict]) -> Dict:
        """
        Find the best peer match using SEMANTIC UNDERSTANDING + PROFILE COMPATIBILITY.
        
        This matcher understands:
        1. MEANING and EMOTIONAL CONTEXT of mood descriptions
        2. PROFILE COMPATIBILITY based on interests, personality, experiences
        
        Args:
            student_profile: The student's mood analysis, profile data, and preferences
            available_peers: List of available peers with their profiles
            
        Returns:
            Match result with peer info, match rationale, and compatibility scores
        """
        
        # Filter out peers this user has already matched with
        user_id = student_profile.get("user_id")
        previous_matches = self.match_history.get(user_id, [])
        
        filtered_peers = [
            peer for peer in available_peers 
            if peer.get("user_id") not in previous_matches
        ]
        
        if not filtered_peers:
            # If all peers have been matched before, allow rematching
            filtered_peers = available_peers
        
        system_prompt = """You are an advanced peer matching AI that uses SEMANTIC UNDERSTANDING + PROFILE COMPATIBILITY to connect BU students.

CRITICAL: You must match based on TWO factors:
1. MOOD SEMANTIC SIMILARITY (80% weight)
2. PROFILE COMPATIBILITY (20% weight)

MOOD MATCHING APPROACH:

1. UNDERSTAND THE DEEPER EXPERIENCE
   - Don't just match "stressed" with "stressed"
   - Understand WHAT they're stressed about and WHY
   - "Job application anxiety" and "Thesis stress" share academic performance pressure
   - "Missing family" and "Feeling disconnected" both reflect isolation/loneliness
   
2. LOOK FOR SHARED EMOTIONAL THEMES
   - Academic pressure (exams, applications, imposter syndrome)
   - Social isolation (loneliness, making friends, belonging)
   - Life transitions (new environment, career uncertainty)
   - Identity struggles (finding purpose, self-doubt)
   - Homesickness (missing family, cultural adjustment)

PROFILE MATCHING APPROACH:

1. SHARED INTERESTS (High weight)
   - Same hobbies, music taste, activities
   - Example: Both like "Indie Music" or "Gaming"
   
2. COMPLEMENTARY PERSONALITIES (Medium weight)
   - "Good listener" + "Needs to talk"
   - "Encouraging" + "Self-doubting"
   - Both "Thoughtful" types can connect deeply
   
3. SIMILAR LIFE STAGE (Medium weight)
   - Both seniors/grad students (understand timeline pressure)
   - Both international students (shared adjustment experience)
   - Both job hunting (shared stress)
   
4. COMPATIBLE COMMUNICATION STYLES (Low weight)
   - Both prefer direct communication
   - Both value authenticity

SCORING FORMULA:
Final Match Score = (Mood Similarity × 0.8) + (Profile Compatibility × 0.2)

- Mood Similarity: 0-100 based on semantic emotional theme overlap
- Profile Compatibility: 0-100 based on interests + personality + life stage

EXAMPLES OF GOOD MATCHES:

Match 1:
- Student A: "Overwhelmed by thesis and job apps" (MS student, loves singing)
- Student B: "Internship rejections hitting hard" (Junior CS, into gaming)
→ MOOD: Both experiencing career anxiety (85% similarity)
→ PROFILE: Different interests but both tech-focused students (60% compatibility)
→ FINAL SCORE: (85×0.8) + (60×0.2) = 68 + 12 = 80%

Match 2:
- Student A: "Missing home, family doesn't understand" (International, loves data viz)
- Student B: "Feeling lonely, hard to connect" (First-year, into poetry)
→ MOOD: Both experiencing isolation/belonging struggles (90% similarity)
→ PROFILE: Both introspective, value authentic connection (75% compatibility)
→ FINAL SCORE: (90×0.8) + (75×0.2) = 72 + 15 = 87%

Match 3:
- Student A: "Doubting if engineering is for me" (Sophomore, rock climbing)
- Student B: "Imposter syndrome in tech" (Senior, data analytics)
→ MOOD: Both experiencing self-doubt in technical field (95% similarity)
→ PROFILE: Both in STEM, different years but compatible (70% compatibility)  
→ FINAL SCORE: (95×0.8) + (70×0.2) = 76 + 14 = 90%

RED FLAGS FOR MATCHING:
- DO NOT match if either person shows crisis indicators
- Ensure both are in a state to support each other
- Avoid matching two people in acute distress

IMPORTANT: Look at BOTH mood description AND profile data (interests, personality, major, etc.)

Return your matching decision in JSON format:
{
    "match_found": true/false,
    "matched_peer_id": "..." or null,
    "mood_similarity_score": 0-100,
    "profile_compatibility_score": 0-100,
    "match_score": 0-100,
    "rationale": "Explain BOTH mood connection AND profile compatibility",
    "shared_emotional_themes": ["theme1", "theme2"],
    "shared_interests": ["interest1", "interest2"],
    "conversation_starters": ["starter1", "starter2"],
    "safety_flag": true/false
}"""

        try:
            # Prepare context for matching - INCLUDE ACTUAL USER INPUT
            context = f"""
Student seeking support:
{student_profile}

Available peers:
{filtered_peers}

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
            
            # Parse JSON with error handling - handle extra text after JSON
            try:
                # Try to find just the JSON object
                import re
                # Find first { and last } to extract just the JSON
                first_brace = response_text.find('{')
                if first_brace == -1:
                    raise ValueError("No JSON object found in response")
                
                # Count braces to find matching closing brace
                brace_count = 0
                last_brace = -1
                for i in range(first_brace, len(response_text)):
                    if response_text[i] == '{':
                        brace_count += 1
                    elif response_text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            last_brace = i
                            break
                
                if last_brace == -1:
                    raise ValueError("Could not find matching closing brace")
                
                json_str = response_text[first_brace:last_brace + 1]
                match_result = json.loads(json_str)
                
            except (json.JSONDecodeError, ValueError) as json_err:
                print(f"JSON Parse Error: {json_err}")
                print(f"Raw response text (first 500 chars): {response_text[:500]}")
                # Return default no-match
                return {
                    "match_found": False,
                    "matched_peer_id": None,
                    "mood_similarity_score": 0,
                    "profile_compatibility_score": 0,
                    "match_score": 0,
                    "rationale": "Unable to process matching response",
                    "shared_emotional_themes": [],
                    "shared_interests": [],
                    "conversation_starters": [],
                    "safety_flag": False
                }
            
            # Record the match in history
            if match_result.get("match_found") and match_result.get("matched_peer_id"):
                if user_id not in self.match_history:
                    self.match_history[user_id] = []
                self.match_history[user_id].append(match_result["matched_peer_id"])
            
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
    
    def get_match_statistics(self, user_id: str) -> Dict:
        """
        Get matching statistics for a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            Dictionary with match statistics
        """
        matches = self.match_history.get(user_id, [])
        return {
            "total_matches": len(matches),
            "matched_peers": matches,
            "can_match_again": True  # Always true for demo
        }