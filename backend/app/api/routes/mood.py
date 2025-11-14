"""
API routes for mood entry and analysis
Now integrated with Multi-Agent Coordinator!
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import MoodEntry, MoodAnalysis, ResourceRecommendation
from app.agents.multi_agent_coordinator import MultiAgentCoordinator
from app.agents.bu_resources import get_crisis_resources, get_mental_health_resources
from typing import List, Dict

router = APIRouter(prefix="/api/mood", tags=["mood"])

# Initialize the multi-agent coordinator (replaces standalone mood_analyzer)
coordinator = MultiAgentCoordinator()

@router.post("/analyze", response_model=Dict)
async def analyze_mood(mood_entry: MoodEntry):
    """
    Analyze a student's mood using the MULTI-AGENT SYSTEM
    
    This triggers the entire coordinator workflow:
    1. MoodAnalyzer processes the input
    2. If crisis detected, agents collaborate on validation
    3. If appropriate, matching is initiated
    4. Conversation strategies are generated
    5. All agent communications are logged
    
    Returns comprehensive multi-agent system results!
    """
    try:
        # Use the multi-agent coordinator!
        # This orchestrates all agents working together
        result = coordinator.process_mood_entry(
            user_input=mood_entry.mood_description,
            user_context={
                "user_id": mood_entry.user_id,
                "context": mood_entry.context,
                "timestamp": str(mood_entry.timestamp)
            }
        )
        
        # The result includes:
        # - mood_analysis: from MoodAnalyzer
        # - agents_activated: which agents were used
        # - coordination_strategy: how agents collaborated
        # - agent_communications: full communication log
        # - crisis_consultation: if crisis was detected
        # - matching_initiated: if matching started
        # - conversation_strategy: recommended approach
        # - coordinator_decision: final system decision
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in multi-agent analysis: {str(e)}")

@router.post("/crisis-check", response_model=dict)
async def check_for_crisis(mood_entry: MoodEntry):
    """
    Quick crisis check using multi-agent collaboration
    
    If crisis is detected, multiple agents validate the decision
    Returns crisis status and immediate resources if needed.
    """
    try:
        # Process through coordinator
        result = coordinator.process_mood_entry(
            user_input=mood_entry.mood_description,
            user_context={"user_id": mood_entry.user_id}
        )
        
        mood_analysis = result.get("mood_analysis", {})
        is_crisis = mood_analysis.get("crisis_detected", False)
        
        response = {
            "crisis_detected": is_crisis,
            "urgency_level": mood_analysis.get("urgency_level", "MODERATE"),
            "agent_consensus": result.get("crisis_consultation", {}) if is_crisis else None
        }
        
        # If crisis detected, include immediate resources
        if is_crisis:
            crisis_resources = get_crisis_resources()
            response["immediate_resources"] = [
                {
                    "name": name,
                    "description": info["description"],
                    "contact": info["contact"],
                    "emergency": info["emergency"]
                }
                for name, info in crisis_resources.items()
            ]
            response["message"] = "We're concerned about your safety. Please reach out to one of these resources immediately for professional help."
            
            # Show that multiple agents agreed this is a crisis
            if result.get("crisis_consultation"):
                response["validation"] = "Multiple AI agents have validated this as requiring immediate professional support"
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking for crisis: {str(e)}")

@router.get("/resources", response_model=List[ResourceRecommendation])
async def get_bu_resources(resource_type: str = "all"):
    """
    Get BU-specific support resources.
    
    Query params:
    - resource_type: crisis, mental_health, academic, wellness, or all
    """
    try:
        resources = []
        
        if resource_type in ["crisis", "all"]:
            crisis_resources = get_crisis_resources()
            for name, info in crisis_resources.items():
                resources.append(ResourceRecommendation(
                    resource_name=name,
                    resource_type="crisis",
                    description=info["description"],
                    location=info.get("location"),
                    contact=info["contact"],
                    emergency=info["emergency"]
                ))
        
        if resource_type in ["mental_health", "all"]:
            mental_health = get_mental_health_resources()
            for name, info in mental_health.items():
                resources.append(ResourceRecommendation(
                    resource_name=name,
                    resource_type="mental_health",
                    description=info["description"],
                    location=info.get("location"),
                    contact=info["contact"],
                    emergency=info.get("emergency", False)
                ))
        
        return resources
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resources: {str(e)}")

@router.get("/agent-stats", response_model=Dict)
async def get_agent_statistics():
    """
    Get statistics about agent activity and collaboration
    
    Useful for monitoring the multi-agent system and for demos!
    Shows:
    - Total agent communications
    - Communications by each agent
    - Collaboration events (queries between agents)
    - Crisis consultations
    """
    try:
        stats = coordinator.get_agent_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching agent stats: {str(e)}")