"""
Conversation Facilitator Agent
Guides peer support conversations and provides BU-specific resources when needed.
Ensures safe, supportive interactions and appropriate escalation.
"""

from typing import Dict, List
from anthropic import Anthropic
import os
import sys
sys.path.append('/home/claude')
from app.agents.bu_resources import get_crisis_resources, get_mental_health_resources, get_quiet_spaces

class ConversationFacilitator:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.conversation_history = []
        
    def facilitate_conversation(
        self, 
        message: str, 
        conversation_context: Dict
    ) -> Dict:
        """
        Facilitate an ongoing peer support conversation.
        
        Args:
            message: The latest message in the conversation
            conversation_context: Context about the participants and conversation state
            
        Returns:
            Facilitation response with guidance, resources, and safety checks
        """
        
        # Build BU-specific resources context
        bu_resources_context = self._build_resources_context()
        
        system_prompt = f"""You are a conversation facilitator for BU peer support connections.

Your role is to:
1. Monitor the conversation for safety concerns
2. Provide gentle guidance and conversation prompts when helpful
3. Suggest BU-specific resources when appropriate
4. Recognize when professional help is needed

AVAILABLE BU RESOURCES:
{bu_resources_context}

FACILITATION GUIDELINES:
- Be minimally intrusive - only intervene when helpful
- Offer conversation starters if the chat stalls
- Suggest campus resources naturally when relevant
- Watch for escalating distress or crisis indicators
- Encourage both peers to support each other
- Suggest quiet campus spaces for in-person meetups if appropriate

SAFETY MONITORING:
- Detect mentions of self-harm, suicide, or immediate danger
- Recognize signs of escalating crisis
- Provide appropriate BU emergency resources immediately
- Recommend professional support when peer support isn't enough

Return your facilitation response in JSON format:
{{
    "intervention_needed": true/false,
    "intervention_type": "resource_suggestion/conversation_prompt/safety_check/crisis_escalation",
    "message_to_participants": "..." or null,
    "suggested_resources": ["resource1", "resource2"],
    "crisis_detected": true/false,
    "conversation_health": "healthy/stalling/concerning"
}}"""

        try:
            # Build conversation context
            context_str = f"""
Conversation Context:
{conversation_context}

Latest Message:
{message}

Conversation History (last 5 messages):
{self._format_conversation_history()}

Analyze this conversation and provide facilitation guidance.
"""
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": context_str
                    }
                ]
            )
            
            # Parse response
            import json
            facilitation = json.loads(response.content[0].text)
            
            # Add message to history
            self.conversation_history.append({
                "message": message,
                "facilitation": facilitation
            })
            
            return facilitation
            
        except Exception as e:
            print(f"Error in conversation facilitation: {e}")
            return {
                "intervention_needed": False,
                "intervention_type": None,
                "message_to_participants": None,
                "suggested_resources": [],
                "crisis_detected": False,
                "conversation_health": "unknown"
            }
    
    def _build_resources_context(self) -> str:
        """Build a formatted string of BU resources for the system prompt"""
        crisis_resources = get_crisis_resources()
        mental_health = get_mental_health_resources()
        quiet_spaces = get_quiet_spaces()
        
        resources_text = "CRISIS RESOURCES (24/7):\n"
        for name, info in crisis_resources.items():
            resources_text += f"- {name}: {info['description']} - {info['contact']}\n"
        
        resources_text += "\nMENTAL HEALTH SERVICES:\n"
        for name, info in mental_health.items():
            resources_text += f"- {name}: {info['description']}\n"
            resources_text += f"  Location: {info['location']}\n"
            resources_text += f"  Contact: {info['contact']}\n"
        
        resources_text += "\nQUIET SPACES ON CAMPUS:\n"
        for space in quiet_spaces:
            resources_text += f"- {space['name']}: {space['description']}\n"
            resources_text += f"  Location: {space['location']}\n"
        
        return resources_text
    
    def _format_conversation_history(self) -> str:
        """Format recent conversation history for context"""
        recent = self.conversation_history[-5:] if len(self.conversation_history) > 5 else self.conversation_history
        return "\n".join([item["message"] for item in recent])
    
    def suggest_conversation_starters(self, match_context: Dict) -> List[str]:
        """Generate conversation starters based on match context"""
        
        system_prompt = """Generate 3-4 warm, natural conversation starters for BU students who just matched for peer support.

Make them:
- Authentic and not overly clinical
- Related to their shared context (academic stress, social challenges, etc.)
- Open-ended to encourage dialogue
- BU-specific when appropriate

Examples:
- "Hey! I saw we're both dealing with exam stress - how are you holding up?"
- "Hi! Are you finding it tough to balance everything this semester too?"
- "Hey there! I'm also feeling homesick lately. How long have you been at BU?"

Return as JSON array: ["starter1", "starter2", "starter3"]"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Match context: {match_context}"
                    }
                ]
            )
            
            import json
            starters = json.loads(response.content[0].text)
            return starters
            
        except Exception as e:
            print(f"Error generating conversation starters: {e}")
            return [
                "Hey! How's your day going?",
                "Hi there! Thanks for connecting.",
                "Hello! I appreciate you being here."
            ]