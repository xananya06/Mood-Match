"""
API routes for peer matching with email generation
CLEANED - No conversation features, email-only
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import PeerProfile, MatchResult, MoodMatchSession
from app.agents.multi_agent_coordinator import MultiAgentCoordinator
from app.agents.peer_matcher import PeerMatcher
from app.agents.email_generator import EmailGenerator
from app.agents.email_sender import EmailSender
from typing import List, Dict
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/match", tags=["matching"])

# Initialize coordinator and agents
coordinator = MultiAgentCoordinator()
peer_matcher = PeerMatcher()
email_generator = EmailGenerator()
email_sender = EmailSender()

# In-memory storage
waiting_peers = {}
completed_matches = {}

# DEMO peers
DEMO_PEERS = [
    {
        "user_id": "demo_peer_1",
        "profile": {
            "user_id": "demo_peer_1",
            "mood_analysis": {
                "primary_emotion": "stressed",
                "urgency_level": "MODERATE",
                "needs": ["listener", "emotional support"],
                "matching_criteria": {
                    "similar_experience": "academic stress",
                    "support_type": "listener",
                    "context": "finals week"
                }
            },
            "seeking_support": True,
            "available_to_support": True,
            "timestamp": datetime.now().isoformat()
        },
        "added_at": datetime.now().isoformat()
    },
    {
        "user_id": "demo_peer_2",
        "profile": {
            "user_id": "demo_peer_2",
            "mood_analysis": {
                "primary_emotion": "lonely",
                "urgency_level": "MODERATE",
                "needs": ["companion", "social connection"],
                "matching_criteria": {
                    "similar_experience": "homesickness",
                    "support_type": "companion",
                    "context": "adjusting to BU"
                }
            },
            "seeking_support": True,
            "available_to_support": True,
            "timestamp": datetime.now().isoformat()
        },
        "added_at": datetime.now().isoformat()
    }
]

for peer in DEMO_PEERS:
    waiting_peers[peer["user_id"]] = peer

@router.post("/join-queue", response_model=dict)
async def join_matching_queue(mood_entry: dict):
    """Add student to matching queue"""
    try:
        user_id = mood_entry.get("user_id")
        mood_description = mood_entry.get("mood_description")
        
        coordination_result = coordinator.process_mood_entry(
            user_input=mood_description,
            user_context={"user_id": user_id}
        )
        
        mood_analysis = coordination_result.get("mood_analysis", {})
        
        # Crisis check
        if mood_analysis.get("crisis_detected"):
            return {
                "status": "crisis_detected",
                "message": "We're concerned about your safety. Please seek immediate professional help.",
                "in_queue": False,
                "crisis_resources": mood_analysis.get("recommended_resources", [])
            }
        
        # Add to queue
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
        
        match_stats = peer_matcher.get_match_statistics(user_id)
        
        return {
            "status": "in_queue",
            "message": "Looking for a peer match for you...",
            "in_queue": True,
            "queue_position": len(waiting_peers),
            "agents_activated": coordination_result.get("agents_activated", []),
            "your_previous_matches": match_stats["total_matches"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error joining queue: {str(e)}")

@router.post("/find-match", response_model=Dict)
async def find_peer_match(user_id: str):
    """Find match and send emails"""
    try:
        if user_id not in waiting_peers:
            raise HTTPException(status_code=404, detail="User not in queue")
        
        user_data = waiting_peers[user_id]
        user_profile = user_data["profile"]
        
        # Get available peers
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
                "rationale": "No available peers at the moment.",
                "safety_flag": False
            }
        
        # Find match
        match_result = peer_matcher.find_match(user_profile, available_peers)
        
        if match_result["match_found"]:
            matched_peer_id = match_result["matched_peer_id"]
            matched_peer_data = waiting_peers.get(matched_peer_id, {})
            
            # Generate emails
            match_context = {
                "match_score": match_result.get("match_score", 85),
                "shared_emotional_themes": match_result.get("shared_emotional_themes", [])
            }
            
            email1 = email_generator.generate_match_email(
                student_profile=user_profile,
                matched_peer_profile=matched_peer_data.get("profile", {}),
                match_context=match_context
            )
            
            email2 = email_generator.generate_match_email(
                student_profile=matched_peer_data.get("profile", {}),
                matched_peer_profile=user_profile,
                match_context=match_context
            )
            
            # Send emails
            email_sent_1 = email_sender.send_match_notification(
                to_email=email1["to"],
                subject=email1["subject"],
                body=email1["body"]
            )
            
            email_sent_2 = email_sender.send_match_notification(
                to_email=email2["to"],
                subject=email2["subject"],
                body=email2["body"]
            )
            
            # Store match
            match_id = str(uuid.uuid4())
            completed_matches[match_id] = {
                "peer1_id": user_id,
                "peer2_id": matched_peer_id,
                "matched_at": datetime.now().isoformat(),
                "emails_sent": email_sent_1 and email_sent_2,
                "match_metadata": match_result
            }
            
            # Remove from queue
            waiting_peers.pop(user_id, None)
            waiting_peers.pop(matched_peer_id, None)
            
            match_result["match_id"] = match_id
            match_result["emails_sent"] = email_sent_1 and email_sent_2
            match_result["email_preview"] = {
                "subject": email1["subject"],
                "to": email1["to"]
            }
        
        return match_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding match: {str(e)}")

@router.get("/queue-status")
async def get_queue_status(user_id: str):
    """Check user status in queue"""
    try:
        if user_id in waiting_peers:
            match_stats = peer_matcher.get_match_statistics(user_id)
            
            return {
                "in_queue": True,
                "position": list(waiting_peers.keys()).index(user_id) + 1,
                "total_waiting": len(waiting_peers),
                "your_match_history": match_stats
            }
        
        return {
            "in_queue": False,
            "matched": False,
            "message": "Not currently in queue"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking status: {str(e)}")

@router.get("/system-stats")
async def get_system_statistics():
    """Get system statistics"""
    try:
        total_unique_users = len(peer_matcher.match_history)
        total_matches_made = sum(len(matches) for matches in peer_matcher.match_history.values()) // 2
        
        return {
            "coordinator_stats": coordinator.get_agent_statistics(),
            "queue_stats": {
                "waiting_peers": len(waiting_peers),
                "completed_matches": len(completed_matches)
            },
            "match_history_stats": {
                "total_users_matched": total_unique_users,
                "total_matches_created": total_matches_made
            },
            "system_health": "operational"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")
    
    