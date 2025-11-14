"""
API routes for peer matching
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import PeerProfile, MatchResult, MoodMatchSession
from app.agents.peer_matcher import PeerMatcher
from app.agents.conversation_facilitator import ConversationFacilitator
from typing import List
import uuid

router = APIRouter(prefix="/api/match", tags=["matching"])

# Initialize agents
peer_matcher = PeerMatcher()
conversation_facilitator = ConversationFacilitator()

# In-memory storage for demo (replace with database in production)
waiting_peers = {}
active_matches = {}

@router.post("/join-queue", response_model=dict)
async def join_matching_queue(peer_profile: PeerProfile):
    """
    Add a student to the matching queue.
    Returns queue status and estimated wait time.
    """
    try:
        # Check if user is in crisis
        if peer_profile.mood_analysis.crisis_detected:
            return {
                "status": "crisis_detected",
                "message": "We're concerned about your safety. Please seek immediate professional help.",
                "in_queue": False,
                "crisis_resources": []  # Would include actual resources
            }
        
        # Add to waiting queue
        waiting_peers[peer_profile.user_id] = {
            "profile": peer_profile.dict(),
            "added_at": peer_profile.timestamp
        }
        
        return {
            "status": "in_queue",
            "message": "Looking for a peer match for you...",
            "in_queue": True,
            "queue_position": len(waiting_peers),
            "estimated_wait": "1-5 minutes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error joining queue: {str(e)}")

@router.post("/find-match", response_model=MatchResult)
async def find_peer_match(user_id: str):
    """
    Attempt to find a match for the given user from the waiting queue.
    """
    try:
        if user_id not in waiting_peers:
            raise HTTPException(status_code=404, detail="User not in queue")
        
        user_profile = waiting_peers[user_id]["profile"]
        
        # Get other available peers
        available_peers = [
            peer_data["profile"] 
            for peer_id, peer_data in waiting_peers.items() 
            if peer_id != user_id
        ]
        
        if not available_peers:
            return MatchResult(
                match_found=False,
                matched_peer_id=None,
                match_score=0,
                rationale="No available peers at the moment. Please try again in a few minutes.",
                conversation_starters=[],
                safety_flag=False
            )
        
        # Find best match
        match_result = peer_matcher.find_match(user_profile, available_peers)
        
        # If match found, set up conversation
        if match_result["match_found"]:
            matched_peer_id = match_result["matched_peer_id"]
            conversation_id = str(uuid.uuid4())
            
            # Create conversation session
            active_matches[conversation_id] = {
                "peer1_id": user_id,
                "peer2_id": matched_peer_id,
                "started_at": user_profile["timestamp"],
                "conversation_history": []
            }
            
            # Remove both from waiting queue
            waiting_peers.pop(user_id, None)
            waiting_peers.pop(matched_peer_id, None)
            
            # Generate conversation starters
            starters = conversation_facilitator.suggest_conversation_starters(
                {"peer1": user_profile, "peer2": available_peers[0]}  # Simplified
            )
            match_result["conversation_starters"] = starters
            match_result["conversation_id"] = conversation_id
        
        return MatchResult(**match_result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding match: {str(e)}")

@router.get("/queue-status")
async def get_queue_status(user_id: str):
    """
    Check the status of a user in the matching queue.
    """
    try:
        if user_id in waiting_peers:
            return {
                "in_queue": True,
                "position": list(waiting_peers.keys()).index(user_id) + 1,
                "total_waiting": len(waiting_peers)
            }
        
        # Check if in active match
        for conv_id, match_data in active_matches.items():
            if user_id in [match_data["peer1_id"], match_data["peer2_id"]]:
                return {
                    "in_queue": False,
                    "matched": True,
                    "conversation_id": conv_id
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