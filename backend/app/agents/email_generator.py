"""
Email Generator Agent - Enhanced with Location Recommendations
Composes personalized notification emails for matched students with meetup suggestions.
"""

from typing import Dict
from anthropic import Anthropic
import os

class EmailGenerator:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def generate_match_email(
        self, 
        student_profile: Dict,
        matched_peer_profile: Dict,
        match_context: Dict,
        location_recommendations: Dict = None
    ) -> Dict:
        """Generate personalized email notification with location recommendations"""
        
        system_prompt = """You are an empathetic email composer for BU Mood Match.

Write warm, personalized emails notifying students they've been matched with a peer.

EMAIL STRUCTURE:
1. Warm greeting with student name
2. "We found you a match!" with peer's name
3. Why this match works:
   - 2-3 shared emotional themes from mood similarity
   - 1-2 shared interests or compatible traits from profiles
4. Suggested meetup locations (3 options with emoji and brief reasoning)
5. Conversation starters (2-3 natural ice breakers)
6. Safety reminder (brief but important)
7. Encouraging sign-off

TONE: Warm, supportive, student-friendly. NO corporate jargon. Like a friend helping you out.

LOCATION PRESENTATION:
Format each location as:
- **[Emoji] Location Name**
  - *Why it works*: Brief reason specific to their match
  - *Vibe*: What to expect

Return JSON:
{
    "subject": "...",
    "body": "..." (HTML format with <p>, <h3>, <ul>, <li>, <strong> tags),
    "preview_text": "..."
}"""

        try:
            # Build location section
            location_section = ""
            if location_recommendations and location_recommendations.get('locations'):
                location_section = "\n\nSUGGESTED MEETUP LOCATIONS:\n"
                for loc in location_recommendations['locations'][:3]:
                    location_section += f"""
- {loc.get('emoji', '📍')} {loc['location_name']}
  Address: {loc.get('address', 'N/A')}
  Why: {loc.get('reasoning', 'Great spot for connecting')}
  Vibe: {loc.get('vibe', 'Comfortable atmosphere')}
"""
                location_section += f"\nTiming suggestion: {location_recommendations.get('timing_suggestion', 'Afternoon or early evening')}"
            
            # Build context for email generation
            context = f"""
RECIPIENT PROFILE:
Name: {student_profile.get('name', 'there')}
Current feeling: {student_profile.get('mood_analysis', {}).get('primary_emotion', 'stressed')}

MATCHED PEER:
Name: {matched_peer_profile.get('name', 'your match')}
Interests: {', '.join(matched_peer_profile.get('interests', [])[:3])}
Year: {matched_peer_profile.get('year', 'BU student')}

MATCH DETAILS:
Overall Match Score: {match_context.get('match_score', 85)}%
Mood Similarity: {match_context.get('mood_similarity_score', match_context.get('match_score', 85))}%
Profile Compatibility: {match_context.get('profile_compatibility_score', match_context.get('match_score', 85))}%
Shared Emotional Themes: {', '.join(match_context.get('shared_emotional_themes', ['mutual support']))}
Shared Interests: {', '.join(match_context.get('shared_interests', []))}
{location_section}

CONVERSATION STARTERS:
{chr(10).join(['- ' + starter for starter in match_context.get('conversation_starters', ['Hey! How are you doing?'])[:3]])}

Generate a warm, personalized email announcing this match.
"""
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                system=system_prompt,
                messages=[{"role": "user", "content": context}]
            )
            
            import json
            response_text = response.content[0].text.strip()
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            # Extract just the JSON object, ignore extra text
            try:
                first_brace = response_text.find('{')
                if first_brace == -1:
                    raise ValueError("No JSON object found")
                
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
                
                json_str = response_text[first_brace:last_brace + 1]
                email_content = json.loads(json_str)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Email JSON parse error: {e}")
                # Use fallback below
                raise
            
            # Add metadata
            email_content["to"] = "xananya@bu.edu"  # Hardcoded for demo
            email_content["from"] = "moodmatch@bu.edu"
            email_content["peer_email"] = f"{matched_peer_profile.get('user_id', 'peer')}@bu.edu"
            email_content["match_score"] = match_context.get('match_score', 85)
            
            return email_content
            
        except Exception as e:
            print(f"Error generating email: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback email
            return {
                "subject": f"You matched with {matched_peer_profile.get('name', 'a BU peer')}!",
                "body": f"""
<p>Hi {student_profile.get('name', 'there')}!</p>

<p>Great news! We found you a compatible peer at BU.</p>

<h3>Your Match: {matched_peer_profile.get('name', 'Your Peer')}</h3>
<p><strong>Match Score:</strong> {match_context.get('match_score', 85)}%</p>

<p><strong>Why you matched:</strong></p>
<ul>
  <li>Both experiencing similar feelings and challenges</li>
  <li>Compatible interests and backgrounds</li>
</ul>

<h3>Suggested Meetup Spots:</h3>
<ul>
  <li><strong>☕ George Sherman Union</strong> - Great for casual coffee and conversation</li>
  <li><strong>🌳 BU Beach</strong> - Outdoor space for a relaxed chat</li>
  <li><strong>📚 Mugar Library</strong> - Quiet study space if you want to connect while working</li>
</ul>

<p><strong>Safety Reminder:</strong> This is peer support, not professional therapy. If you feel uncomfortable, you can end the conversation anytime.</p>

<p>Good luck! 💜</p>
<p>- Mood Match Team</p>
""",
                "preview_text": f"You matched with {matched_peer_profile.get('name', 'a BU peer')}!",
                "to": "xananya@bu.edu",
                "from": "moodmatch@bu.edu",
                "peer_email": f"{matched_peer_profile.get('user_id', 'peer')}@bu.edu",
                "match_score": match_context.get('match_score', 85)
            }