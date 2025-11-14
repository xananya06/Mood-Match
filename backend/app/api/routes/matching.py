"""
API routes for peer matching - integrated with Multi-Agent Coordinator
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import PeerProfile, MatchResult, MoodMatchSession
from app.agents.multi_agent_coordinator import MultiAgentCoordinator
from app.agents.peer_matcher import PeerMatcher
from app.agents.conversation_facilitator import ConversationFacilitator
from typing import List, Dict
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/match", tags=["matching"])

# Initialize coordinator and agents
coordinator = MultiAgentCoordinator()
peer_matcher = PeerMatcher()
conversation_facilitator = ConversationFacilitator()

# In-memory storage for demo (replace with database in production)
waiting_peers = {}
active_matches = {}

@router.post("/join-queue", response_model=dict)
async def join_matching_queue(mood_entry: dict):
    """
    Add a student to the matching queue using multi-agent analysis
    
    This endpoint:
    1. Processes mood through the coordinator
    2. Checks for crisis (automatic multi-agent validation)
    3. If safe, adds to matching queue
    4. Returns queue status
    """
    try:
        user_id = mood_entry.get("user_id")
        mood_description = mood_entry.get("mood_description")
        
        # Use coordinator to analyze and decide
        coordination_result = coordinator.process_mood_entry(
            user_input=mood_description,
            user_context={"user_id": user_id}
        )
        
        mood_analysis = coordination_result.get("mood_analysis", {})
        
        # Check if crisis detected (with multi-agent validation)
        if mood_analysis.get("crisis_detected"):
            crisis_consultation = coordination_result.get("crisis_consultation", {})
            
            return {
                "status": "crisis_detected",
                "message": "We're concerned about your safety. Please seek immediate professional help.",
                "in_queue": False,
                "crisis_resources": mood_analysis.get("recommended_resources", []),
                "agent_consensus": crisis_consultation.get("consensus", False),
                "validation_message": "Multiple AI agents have validated this requires professional support"
            }
        
        # Add to waiting queue
        waiting_peers[user_id] = {
            "profile": {
                "user_id": user_id,
                "mood_analysis": mood_analysis,
                "seeking_support": True,
                "available_to_support": True,
                "timestamp": datetime.now().isoformat()
            },
            "coordination_result": coordination_result,
            "added_at": datetime.now().isoformat()
        }
        
        return {
            "status": "in_queue",
            "message": "Looking for a peer match for you...",
            "in_queue": True,
            "queue_position": len(waiting_peers),
            "estimated_wait": "1-5 minutes",
            "agents_activated": coordination_result.get("agents_activated", []),
            "matching_initiated": coordination_result.get("matching_initiated", False)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error joining queue: {str(e)}")

@router.post("/find-match", response_model=Dict)
async def find_peer_match(user_id: str):
    """
    Attempt to find a match using multi-agent coordination
    
    The coordinator ensures:
    - Safe matches (no crisis situations)
    - Compatible emotional states
    - Appropriate conversation strategies
    """
    try:
        if user_id not in waiting_peers:
            raise HTTPException(status_code=404, detail="User not in queue")
        
        user_data = waiting_peers[user_id]
        user_profile = user_data["profile"]
        
        # Get other available peers
        available_peers = [
            peer_data["profile"] 
            for peer_id, peer_data in waiting_peers.items() 
            if peer_id != user_id
        ]
        
        if not available_peers:
            return {
                "match_found": False,
                "matched_peer_id": None,
                "match_score": 0,
                "rationale": "No available peers at the moment. Please try again in a few minutes.",
                "conversation_starters": [],
                "safety_flag": False
            }
        
        # Use peer matcher to find best match
        match_result = peer_matcher.find_match(user_profile, available_peers)
        
        # If match found, get conversation strategy from coordinator
        if match_result["match_found"]:
            matched_peer_id = match_result["matched_peer_id"]
            conversation_id = str(uuid.uuid4())
            
            # Get the matched peer's coordination result
            matched_peer_data = waiting_peers.get(matched_peer_id, {})
            
            # Use facilitator to generate conversation starters
            match_context = {
                "peer1": user_profile,
                "peer2": matched_peer_data.get("profile", {})
            }
            
            starters = conversation_facilitator.suggest_conversation_starters(match_context)
            
            # Create conversation session with multi-agent support
            active_matches[conversation_id] = {
                "peer1_id": user_id,
                "peer2_id": matched_peer_id,
                "started_at": datetime.now().isoformat(),
                "conversation_history": [],
                "agent_communications": {
                    "peer1": user_data.get("coordination_result", {}).get("agent_communications", []),
                    "peer2": matched_peer_data.get("coordination_result", {}).get("agent_communications", [])
                },
                "conversation_strategy": user_data.get("coordination_result", {}).get("conversation_strategy", {})
            }
            
            # Remove both from waiting queue
            waiting_peers.pop(user_id, None)
            waiting_peers.pop(matched_peer_id, None)
            
            match_result["conversation_starters"] = starters
            match_result["conversation_id"] = conversation_id
            match_result["multi_agent_support"] = True
            match_result["conversation_strategy"] = active_matches[conversation_id]["conversation_strategy"]
        
        return match_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding match: {str(e)}")

@router.get("/queue-status")
async def get_queue_status(user_id: str):
    """
    Check the status of a user in the matching queue
    """
    try:
        if user_id in waiting_peers:
            user_data = waiting_peers[user_id]
            return {
                "in_queue": True,
                "position": list(waiting_peers.keys()).index(user_id) + 1,
                "total_waiting": len(waiting_peers),
                "coordination_complete": True,
                "agents_used": user_data.get("coordination_result", {}).get("agents_activated", [])
            }
        
        # Check if in active match
        for conv_id, match_data in active_matches.items():
            if user_id in [match_data["peer1_id"], match_data["peer2_id"]]:
                return {
                    "in_queue": False,
                    "matched": True,
                    "conversation_id": conv_id,
                    "multi_agent_monitoring": True
                }
        
        return {
            "in_queue": False,
            "matched": False,
            "message": "Not currently in queue or matched"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking status: {str(e)}")

@router.delete("/leave-queue")
async def leave_matching_queue(user_id: str):
    """
    Remove a user from the matching queue.
    """
    try:
        if user_id in waiting_peers:
            waiting_peers.pop(user_id)
            return {"status": "removed", "message": "Successfully left the queue"}
        
        return {"status": "not_found", "message": "User not in queue"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leaving queue: {str(e)}")

@router.get("/conversation/{conversation_id}/facilitate")
async def get_conversation_facilitation(conversation_id: str, latest_message: str):
    """
    Get real-time conversation facilitation from the multi-agent system
    
    The ConversationFacilitator monitors the conversation and provides:
    - Safety checks
    - Conversation prompts if needed
    - Resource suggestions
    - Crisis detection
    """
    try:
        if conversation_id not in active_matches:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        match_data = active_matches[conversation_id]
        
        # Use conversation facilitator
        facilitation = conversation_facilitator.facilitate_conversation(
            message=latest_message,
            conversation_context=match_data
        )
        
        # Add to conversation history
        match_data["conversation_history"].append({
            "message": latest_message,
            "facilitation": facilitation,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "conversation_id": conversation_id,
            "facilitation": facilitation,
            "multi_agent_monitoring": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error facilitating conversation: {str(e)}")

@router.get("/system-stats")
async def get_system_statistics():
    """
    Get comprehensive multi-agent system statistics
    
    Perfect for demos and monitoring!
    """
    try:
        return {
            "coordinator_stats": coordinator.get_agent_statistics(),
            "queue_stats": {
                "waiting_peers": len(waiting_peers),
                "active_matches": len(active_matches)
            },
            "system_health": "operational"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")