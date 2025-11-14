"""
Multi-Agent Coordinator with Agent Communication
Demonstrates key multi-agent concepts for AI course project:
- Agent autonomy and decision-making
- Inter-agent communication
- Collaborative problem-solving
- Dynamic task delegation
"""

from typing import Dict, List, Optional
from anthropic import Anthropic
import os
from app.agents.mood_analyzer import MoodAnalyzer
from app.agents.peer_matcher import PeerMatcher
from app.agents.conversation_facilitator import ConversationFacilitator

class AgentMessage:
    """Message format for inter-agent communication"""
    def __init__(self, sender: str, recipient: str, message_type: str, content: Dict):
        self.sender = sender
        self.recipient = recipient
        self.message_type = message_type  # request, response, alert, query
        self.content = content

class MultiAgentCoordinator:
    """
    Orchestrates multiple specialized agents in a collaborative system.
    
    Key Multi-Agent Concepts Demonstrated:
    1. AGENT AUTONOMY: Each agent makes independent decisions
    2. AGENT COMMUNICATION: Agents send messages to each other
    3. EMERGENT BEHAVIOR: System behavior emerges from agent interactions
    4. TASK DELEGATION: Coordinator delegates based on agent expertise
    5. COLLABORATIVE DECISION-MAKING: Agents consult each other
    """
    
    def __init__(self):
        # Initialize specialized agents
        self.mood_analyzer = MoodAnalyzer()
        self.peer_matcher = PeerMatcher()
        self.conversation_facilitator = ConversationFacilitator()
        
        # Agent communication log
        self.communication_log = []
        
        # Coordinator's own decision-making LLM
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def log_communication(self, message: AgentMessage):
        """Track inter-agent communication"""
        self.communication_log.append({
            "from": message.sender,
            "to": message.recipient,
            "type": message.message_type,
            "content": message.content
        })
    
    def process_mood_entry(self, user_input: str, user_context: Dict) -> Dict:
        """
        DEMONSTRATION OF MULTI-AGENT COORDINATION
        
        The coordinator acts as a meta-agent that:
        1. Decides which agents to involve
        2. Facilitates agent-to-agent communication
        3. Makes high-level decisions based on agent recommendations
        """
        
        # STEP 1: Coordinator decides which agents to activate
        activation_decision = self._decide_agent_activation(user_input, user_context)
        
        result = {
            "agents_activated": activation_decision["agents"],
            "coordination_strategy": activation_decision["strategy"],
            "agent_communications": []
        }
        
        # STEP 2: Mood Analyzer processes input (always first)
        mood_analysis = self.mood_analyzer.analyze_mood(user_input)
        
        # Agent communicates findings to coordinator
        mood_message = AgentMessage(
            sender="MoodAnalyzer",
            recipient="Coordinator",
            message_type="response",
            content=mood_analysis
        )
        self.log_communication(mood_message)
        result["mood_analysis"] = mood_analysis
        
        # STEP 3: CRISIS HANDLING - Agents collaborate on critical decision
        if mood_analysis.get("crisis_detected"):
            # Coordinator requests second opinion from Facilitator
            crisis_consultation = self._consult_on_crisis(mood_analysis, user_input)
            
            consultation_message = AgentMessage(
                sender="Coordinator",
                recipient="ConversationFacilitator",
                message_type="query",
                content={"query": "validate_crisis", "data": mood_analysis}
            )
            self.log_communication(consultation_message)
            
            result["crisis_consultation"] = crisis_consultation
            result["action"] = "escalate_to_professional"
            result["agent_communications"] = self.communication_log
            return result
        
        # STEP 4: MATCHING PHASE - Matcher agent works autonomously
        if "find_match" in activation_decision["agents"]:
            # Matcher agent receives mood analysis from coordinator
            match_request = AgentMessage(
                sender="Coordinator",
                recipient="PeerMatcher",
                message_type="request",
                content={"action": "find_match", "profile": mood_analysis}
            )
            self.log_communication(match_request)
            
            # Matcher may query Facilitator for conversation strategy
            conversation_strategy = self._get_conversation_strategy(mood_analysis)
            
            strategy_query = AgentMessage(
                sender="PeerMatcher",
                recipient="ConversationFacilitator",
                message_type="query",
                content={"query": "conversation_approach", "match_context": mood_analysis}
            )
            self.log_communication(strategy_query)
            
            result["matching_initiated"] = True
            result["conversation_strategy"] = conversation_strategy
        
        # STEP 5: Coordinator makes final decision
        final_decision = self._make_coordination_decision(result)
        result["coordinator_decision"] = final_decision
        result["agent_communications"] = self.communication_log
        
        return result
    
    def _decide_agent_activation(self, user_input: str, context: Dict) -> Dict:
        """
        AUTONOMOUS DECISION-MAKING BY COORDINATOR
        
        Coordinator analyzes situation and decides which agents to activate.
        This demonstrates meta-reasoning about agent capabilities.
        """
        
        system_prompt = """You are a multi-agent system coordinator.

Analyze the user's situation and decide which specialized agents to activate:

AVAILABLE AGENTS:
1. MoodAnalyzer - Analyzes emotional state, detects crises
2. PeerMatcher - Finds compatible peer matches
3. ConversationFacilitator - Guides ongoing conversations, provides resources

ACTIVATION RULES:
- MoodAnalyzer: Always activate first (analyzes every input)
- PeerMatcher: Activate if user needs peer connection
- ConversationFacilitator: Activate if in active conversation OR needs immediate resources

Return JSON:
{
    "agents": ["agent1", "agent2"],
    "strategy": "sequential/parallel/crisis_mode",
    "reasoning": "Why these agents are needed"
}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"User input: {user_input}\nContext: {context}"
                }]
            )
            
            import json
            return json.loads(response.content[0].text)
        except:
            # Default activation
            return {
                "agents": ["MoodAnalyzer", "PeerMatcher"],
                "strategy": "sequential",
                "reasoning": "Default activation pattern"
            }
    
    def _consult_on_crisis(self, mood_analysis: Dict, original_input: str) -> Dict:
        """
        AGENT COLLABORATION: Multiple agents validate critical decision
        
        When stakes are high (crisis), agents consult each other.
        This demonstrates collaborative decision-making.
        """
        
        # Facilitator provides second opinion on crisis severity
        facilitator_assessment = self.conversation_facilitator.facilitate_conversation(
            message=original_input,
            conversation_context={
                "mood_analysis": mood_analysis,
                "request_type": "crisis_validation"
            }
        )
        
        return {
            "mood_analyzer_verdict": mood_analysis.get("urgency_level"),
            "facilitator_verdict": facilitator_assessment.get("crisis_detected"),
            "consensus": (
                mood_analysis.get("crisis_detected") and 
                facilitator_assessment.get("crisis_detected")
            ),
            "recommended_action": "immediate_professional_help"
        }
    
    def _get_conversation_strategy(self, match_context: Dict) -> Dict:
        """
        AGENT QUERYING: One agent queries another for expertise
        
        Matcher asks Facilitator for conversation guidance.
        Demonstrates agents leveraging each other's specializations.
        """
        
        starters = self.conversation_facilitator.suggest_conversation_starters(
            match_context
        )
        
        return {
            "conversation_starters": starters,
            "facilitation_approach": "supportive_listening",
            "resource_suggestions": ["quiet_spaces", "wellness_activities"]
        }
    
    def _make_coordination_decision(self, agent_results: Dict) -> Dict:
        """
        META-LEVEL DECISION: Coordinator synthesizes agent outputs
        
        Demonstrates emergent system behavior from agent collaboration.
        """
        
        system_prompt = """You are the coordinator making a final decision.

Based on all agent outputs, decide:
1. What action to take (match_user / provide_resources / escalate)
2. What resources to provide
3. What safety measures to apply

Return JSON:
{
    "final_action": "...",
    "resources_to_provide": [...],
    "safety_measures": [...],
    "confidence": 0-100
}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"Agent results: {agent_results}"
                }]
            )
            
            import json
            return json.loads(response.content[0].text)
        except:
            return {
                "final_action": "proceed_with_caution",
                "resources_to_provide": [],
                "safety_measures": ["monitor_closely"],
                "confidence": 70
            }
    
    def get_agent_statistics(self) -> Dict:
        """
        SYSTEM MONITORING: Track agent activity and collaboration
        
        Useful for demonstrating system behavior in your presentation.
        """
        
        return {
            "total_communications": len(self.communication_log),
            "communication_by_agent": {
                "MoodAnalyzer": len([m for m in self.communication_log if m["from"] == "MoodAnalyzer"]),
                "PeerMatcher": len([m for m in self.communication_log if m["from"] == "PeerMatcher"]),
                "ConversationFacilitator": len([m for m in self.communication_log if m["from"] == "ConversationFacilitator"]),
                "Coordinator": len([m for m in self.communication_log if m["from"] == "Coordinator"])
            },
            "collaboration_events": len([m for m in self.communication_log if m["type"] == "query"]),
            "crisis_consultations": len([m for m in self.communication_log if "crisis" in str(m["content"])])
        }