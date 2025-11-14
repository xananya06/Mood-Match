"""
Mood Analyzer Agent
Analyzes student's emotional state and determines appropriate matching criteria and support needs.
Designed specifically for BU students seeking peer support.
"""

from typing import Dict, List
from anthropic import Anthropic
import os

class MoodAnalyzer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def analyze_mood(self, user_input: str) -> Dict:
        """
        Analyze the user's mood and context to determine:
        1. Primary emotional state
        2. Severity/urgency level
        3. Relevant support needs
        4. Matching criteria for peer support
        
        Args:
            user_input: Student's description of how they're feeling
            
        Returns:
            Dictionary with mood analysis results
        """
        
        system_prompt = """You are a compassionate but VIGILANT mood analyzer for BU students seeking peer support.

Your PRIMARY role is SAFETY - err on the side of caution.

CRITICAL SAFETY PROTOCOL - MARK AS CRISIS IF YOU SEE ANY OF THESE:
- ANY mention of self-harm, hurting oneself, or harming others
- ANY mention of suicide, suicidal thoughts, or wanting to die
- Phrases like: "don't want to be here", "want to end it", "hurt myself", "kill myself"
- Having a plan to harm self or others
- Feeling hopeless WITH specific thoughts of self-harm
- Mentions of methods of self-harm
- "I have a plan" combined with distress

DO NOT SECOND-GUESS - If ANY of the above are present, SET crisis_detected to TRUE.

Classify urgency as:
- CRISIS: ANY mention of self-harm/suicide/danger → IMMEDIATE professional help required
- HIGH: Severe distress, overwhelming feelings, can't cope
- MODERATE: Stressed but managing, seeking support
- LOW: General support, minor stress

IMPORTANT: Better to over-detect crisis than under-detect. When in doubt, mark as CRISIS.

Return ONLY valid JSON in this EXACT format:
{
    "primary_emotion": "...",
    "urgency_level": "CRISIS",
    "needs": ["immediate_help"],
    "matching_criteria": {
        "similar_experience": "crisis",
        "support_type": "professional",
        "context": "emergency"
    },
    "crisis_detected": true,
    "recommended_resources": ["BU Police", "Crisis Hotline"]
}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )
            
            # Parse the response
            import json
            analysis = json.loads(response.content[0].text)
            
            return analysis
            
        except Exception as e:
            print(f"Error in mood analysis: {e}")
            # Return safe default
            return {
                "primary_emotion": "uncertain",
                "urgency_level": "MODERATE",
                "needs": ["peer support"],
                "matching_criteria": {
                    "similar_experience": "general support",
                    "support_type": "listener",
                    "context": "student life"
                },
                "crisis_detected": False,
                "recommended_resources": []
            }
    
    def check_for_crisis(self, analysis: Dict) -> bool:
        """
        Check if the analysis indicates a crisis situation
        """
        return analysis.get("crisis_detected", False) or analysis.get("urgency_level") == "CRISIS"