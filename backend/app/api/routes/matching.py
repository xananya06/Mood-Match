"""
Matching Routes - UPDATED WITH PROFILES AND LOCATIONAGENT
Handles peer matching requests using demo student profiles.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

from app.agents.multi_agent_coordinator import MultiAgentCoordinator
from app.agents.peer_matcher import PeerMatcher
from app.agents.email_generator import EmailGenerator
from app.agents.location_agent import LocationAgent
from app.demo_data import DEMO_STUDENT_PROFILES, get_student_by_id, get_all_students_except

router = APIRouter()

# Initialize agents
coordinator = MultiAgentCoordinator()
peer_matcher = PeerMatcher()
email_generator = EmailGenerator()
location_agent = LocationAgent()

# Use demo student profiles as waiting peers
waiting_peers = {}
for profile in DEMO_STUDENT_PROFILES:
    waiting_peers[profile["user_id"]] = {
        "profile": profile,
        "mood_analysis": {
            "primary_emotion": profile.get("mood_post", "")[:50],
            "urgency_level": "MODERATE",
            "needs": ["peer support"],
            "matching_criteria": {
                "similar_experience": profile.get("current_focus", "general support"),
                "support_type": "listener",
                "context": "student life"
            }
        },
        "seeking_support": True,
        "available_to_support": True,
        "timestamp": datetime.now().isoformat(),
        "added_at": datetime.now().isoformat()
    }


class MoodEntryRequest(BaseModel):
    mood_text: str
    user_id: Optional[str] = "student_ananya"  # Default to Ananya for demo


class MatchRequest(BaseModel):
    user_id: str
    mood_analysis: Dict


@router.post("/analyze-mood")
async def analyze_mood(request: MoodEntryRequest):
    """
    Analyze user's mood entry and coordinate agents.
    """
    try:
        # Get user profile
        user_profile = get_student_by_id(request.user_id)
        if not user_profile:
            user_profile = {
                "user_id": request.user_id,
                "name": "Student",
                "interests": [],
                "mood_post": request.mood_text
            }
        
        # Process through coordinator
        result = coordinator.process_mood_entry(
            mood_text=request.mood_text,
            user_profile=user_profile
        )
        
        # Add user profile to result
        result["user_profile"] = user_profile
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/find-match")
async def find_match(request: MatchRequest):
    """
    Find a compatible peer match using profiles + mood.
    NOW WITH LOCATION RECOMMENDATIONS!
    """
    try:
        user_id = request.user_id
        mood_analysis = request.mood_analysis
        
        # Get user profile
        user_profile = get_student_by_id(user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get available peers (excluding self)
        available_peers_list = []
        for peer_id, peer_data in waiting_peers.items():
            if peer_id != user_id:
                available_peers_list.append({
                    "user_id": peer_id,
                    "profile": peer_data["profile"],
                    "mood_analysis": peer_data["mood_analysis"],
                    "seeking_support": peer_data["seeking_support"],
                    "available_to_support": peer_data["available_to_support"]
                })
        
        if not available_peers_list:
            return {
                "match_found": False,
                "message": "No peers currently available",
                "waiting_count": 0
            }
        
        # Prepare student profile for matching
        student_profile_for_matching = {
            "user_id": user_id,
            "profile": user_profile,
            "mood_analysis": mood_analysis,
            "user_input": mood_analysis.get("user_input", "")
        }
        
        # Find match using PeerMatcher
        match_result = peer_matcher.find_match(
            student_profile=student_profile_for_matching,
            available_peers=available_peers_list
        )
        
        if not match_result.get("match_found"):
            return {
                "match_found": False,
                "message": "No compatible matches found at this time",
                "waiting_count": len(available_peers_list)
            }
        
        # Get matched peer data
        matched_peer_id = match_result.get("matched_peer_id")
        matched_peer_data = waiting_peers.get(matched_peer_id)
        
        if not matched_peer_data:
            raise HTTPException(status_code=500, detail="Matched peer data not found")
        
        # Build match context
        match_context = {
            "match_score": match_result.get("match_score", 85),
            "mood_similarity_score": match_result.get("mood_similarity_score", 85),
            "profile_compatibility_score": match_result.get("profile_compatibility_score", 85),
            "shared_emotional_themes": match_result.get("shared_emotional_themes", []),
            "shared_interests": match_result.get("shared_interests", []),
            "conversation_starters": match_result.get("conversation_starters", [])
        }
        
        # Get location recommendations - NEW!
        try:
            location_recommendations = location_agent.recommend_locations(
                student_profile=user_profile,
                student2_profile=matched_peer_data.get("profile", {}),
                match_context=match_context
            )
        except Exception as e:
            print(f"Error getting locations: {e}")
            location_recommendations = None
        
        # Generate emails with location recommendations
        try:
            email1 = email_generator.generate_match_email(
                student_profile=user_profile,
                matched_peer_profile=matched_peer_data.get("profile", {}),
                match_context=match_context,
                location_recommendations=location_recommendations
            )
            
            email2 = email_generator.generate_match_email(
                student_profile=matched_peer_data.get("profile", {}),
                matched_peer_profile=user_profile,
                match_context=match_context,
                location_recommendations=location_recommendations
            )
        except Exception as e:
            print(f"Error generating emails: {e}")
            email1 = {"subject": "Match Found", "body": "You have a new match!"}
            email2 = {"subject": "Match Found", "body": "You have a new match!"}
        
        # Remove both from waiting pool (simulate)
        # In production, you'd actually remove them
        # del waiting_peers[user_id]
        # del waiting_peers[matched_peer_id]
        
        # Build response
        result = {
            "match_found": True,
            "match_score": match_result.get("match_score", 85),
            "mood_similarity_score": match_result.get("mood_similarity_score", 85),
            "profile_compatibility_score": match_result.get("profile_compatibility_score", 85),
            "matched_peer": {
                "name": matched_peer_data["profile"].get("name", "Peer"),
                "avatar": matched_peer_data["profile"].get("avatar", "👤"),
                "year": matched_peer_data["profile"].get("year", "BU Student"),
                "interests": matched_peer_data["profile"].get("interests", []),
                "bio": matched_peer_data["profile"].get("bio", ""),
                "user_id": matched_peer_id
            },
            "match_rationale": match_result.get("rationale", "Compatible based on shared experiences"),
            "shared_emotional_themes": match_result.get("shared_emotional_themes", []),
            "shared_interests": match_result.get("shared_interests", []),
            "conversation_starters": match_result.get("conversation_starters", []),
            "location_recommendations": location_recommendations,  # NEW!
            "email_preview": email1,
            "peer_email_preview": email2,
            "safety_resources": match_result.get("safety_flag", False)
        }
        
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/waiting-peers")
async def get_waiting_peers():
    """Get count and summary of waiting peers"""
    return {
        "count": len(waiting_peers),
        "peers": [
            {
                "user_id": peer_id,
                "name": data["profile"].get("name", "Anonymous"),
                "avatar": data["profile"].get("avatar", "👤"),
                "timestamp": data["added_at"]
            }
            for peer_id, data in waiting_peers.items()
        ]
    }


@router.get("/system-stats")
async def get_system_stats():
    """Get system statistics"""
    return {
        "waiting_peers": len(waiting_peers),
        "total_profiles": len(DEMO_STUDENT_PROFILES),
        "agents_active": 5,  # MoodAnalyzer, Coordinator, PeerMatcher, LocationAgent, EmailGenerator
        "coordinator_stats": coordinator.get_statistics()
    }