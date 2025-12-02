"""
Email Generator Agent
Composes personalized notification emails for matched students.
NO conversation features - just email notifications.
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
        match_context: Dict
    ) -> Dict:
        """Generate personalized email notification for matched student"""
        
        system_prompt = """You are an empathetic email composer for BU Mood Match.

Write warm, personalized emails notifying students they've been matched with a peer.

EMAIL STRUCTURE:
1. Warm greeting
2. "We found you a match!"
3. Why this match works (2-3 specific shared emotional themes)
4. Next steps: "You'll both receive each other's BU email to connect"
5. Safety reminder (brief)
6. Encouraging sign-off

TONE: Warm, supportive, student-friendly. NO corporate jargon.

Return JSON:
{
    "subject": "...",
    "body": "..." (HTML format with <p> tags),
    "preview_text": "..."
}"""

        try:
            context = f"""
Student emotion: {student_profile.get('mood_analysis', {}).get('primary_emotion', 'stressed')}
Peer emotion: {matched_peer_profile.get('mood_analysis', {}).get('primary_emotion', 'stressed')}
Match score: {match_context.get('match_score', 85)}%
Shared themes: {', '.join(match_context.get('shared_emotional_themes', ['mutual support']))}

Generate personalized match notification email.
"""
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": context}]
            )
            
            import json
            response_text = response.content[0].text.strip()
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            email_content = json.loads(response_text)
            
            # Add metadata
            email_content["to"] = "xananya@bu.edu"  # Hardcoded for demo
            email_content["from"] = "moodmatch@bu.edu"
            email_content["peer_email"] = f"{matched_peer_profile.get('user_id')}@bu.edu"
            
            return email_content
            
        except Exception as e:
            print(f"Error generating email: {e}")
            return {
                "subject": "You've been matched with a BU peer!",
                "body": "<p>We found you a compatible peer for support.</p><p>They're experiencing similar feelings and looking for connection too.</p>",
                "preview_text": "New peer match available",
                "to": "xananya@bu.edu",
                "from": "moodmatch@bu.edu",
                "peer_email": f"{matched_peer_profile.get('user_id')}@bu.edu"
            }