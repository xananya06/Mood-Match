"""
Location Agent
Recommends BU-specific hangout locations based on matched student profiles and mood states.
Uses contextual reasoning to suggest appropriate venues.
"""

from typing import Dict, List
from anthropic import Anthropic
import os

from app.demo_data import get_location_recommendations

class LocationAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def recommend_locations(
        self, 
        student_profile: Dict,
        student2_profile: Dict,
        match_context: Dict
    ) -> Dict:
        """
        Recommend 3 BU locations for matched students to meet.
        
        Args:
            student_profile: First student's profile with interests, personality, etc.
            student2_profile: Second student's profile
            match_context: Contains shared_emotional_themes, mood analysis
            
        Returns:
            Dictionary with location recommendations and reasoning
        """
        
        system_prompt = """You are a location recommendation agent for BU students.

Your role is to analyze two matched students and recommend appropriate BU locations for them to meet.

CRITICAL FACTORS TO CONSIDER:
1. **Mood State**: Are they stressed (need quiet)? Lonely (need social)? Overwhelmed (need active outlet)?
2. **Shared Interests**: What do they both enjoy?
3. **Emotional Themes**: What are they experiencing (academic pressure, homesickness, etc.)?
4. **Practical Considerations**: Time of day, accessibility, comfort level

RECOMMENDATION PRINCIPLES:
- **Stressed/Anxious**: Quiet spaces (library, cafe, outdoor)
- **Lonely/Isolated**: Social but not overwhelming (dining hall, game room, coffee shop)
- **Overwhelmed**: Active spaces (gym, outdoor walk) or very quiet (chapel, gallery)
- **Shared Creative Interests**: Arts spaces, music venues
- **Shared Active Interests**: Gym, outdoor areas
- **Need Comfort**: Food places, cozy cafes

AVAILABLE LOCATION TYPES:
- Study/Quiet: Libraries, quiet cafes
- Food/Social: Dining halls, restaurants, cafes
- Outdoor/Active: BU Beach, Esplanade, FitRec
- Creative/Arts: Gallery, music spaces, creative venues
- Spiritual/Meditation: Marsh Chapel

Return your recommendations in JSON format:
{
    "top_3_locations": [
        {
            "location_name": "...",
            "reasoning": "Why this location works for both students",
            "vibe": "What to expect",
            "best_for": "What need it addresses"
        }
    ],
    "overall_strategy": "What type of meetup environment would work best",
    "timing_suggestion": "When to meet (time of day)",
    "conversation_tips": ["Tip 1", "Tip 2"]
}"""

        try:
            # Build context
            context = f"""
STUDENT 1 PROFILE:
Name: {student_profile.get('name', 'Student A')}
Interests: {', '.join(student_profile.get('interests', []))}
Personality: {student_profile.get('personality', 'N/A')}
Current Focus: {student_profile.get('current_focus', 'N/A')}
Mood: {student_profile.get('mood_post', 'N/A')}

STUDENT 2 PROFILE:
Name: {student2_profile.get('name', 'Student B')}
Interests: {', '.join(student2_profile.get('interests', []))}
Personality: {student2_profile.get('personality', 'N/A')}
Current Focus: {student2_profile.get('current_focus', 'N/A')}
Mood: {student2_profile.get('mood_post', 'N/A')}

MATCH CONTEXT:
Shared Emotional Themes: {', '.join(match_context.get('shared_emotional_themes', []))}
Match Score: {match_context.get('match_score', 0)}%

Based on their profiles and emotional states, recommend 3 BU locations where they should meet.
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
            
            # Parse response
            import json
            response_text = response.content[0].text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            location_recommendations = json.loads(response_text)
            
            # Enhance with actual BU location data
            mood_themes = match_context.get('shared_emotional_themes', [])
            actual_locations = get_location_recommendations(
                student_profile, 
                student2_profile, 
                mood_themes
            )
            
            # Merge AI reasoning with actual location data
            enhanced_recommendations = []
            for i, ai_rec in enumerate(location_recommendations.get('top_3_locations', [])[:3]):
                if i < len(actual_locations):
                    actual_loc = actual_locations[i]
                    enhanced_recommendations.append({
                        "location_name": actual_loc["name"],
                        "address": actual_loc["address"],
                        "vibe": actual_loc["vibe"],
                        "emoji": actual_loc["emoji"],
                        "reasoning": ai_rec.get("reasoning", "Good spot for connecting"),
                        "good_for": actual_loc["good_for"],
                        "amenities": actual_loc["amenities"],
                        "best_time": actual_loc["best_time"]
                    })
            
            return {
                "locations": enhanced_recommendations,
                "overall_strategy": location_recommendations.get("overall_strategy", "Comfortable space for peer support"),
                "timing_suggestion": location_recommendations.get("timing_suggestion", "Afternoon or early evening"),
                "conversation_tips": location_recommendations.get("conversation_tips", [
                    "Start with what you're both experiencing",
                    "Be honest about your feelings",
                    "Listen actively and validate each other"
                ])
            }
            
        except Exception as e:
            print(f"Error in location recommendation: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback to simple recommendation
            mood_themes = match_context.get('shared_emotional_themes', [])
            fallback_locations = get_location_recommendations(
                student_profile, 
                student2_profile, 
                mood_themes
            )
            
            return {
                "locations": fallback_locations,
                "overall_strategy": "Comfortable peer support setting",
                "timing_suggestion": "Afternoon",
                "conversation_tips": [
                    "Share what you're going through",
                    "Listen without judgment",
                    "Support each other"
                ]
            }