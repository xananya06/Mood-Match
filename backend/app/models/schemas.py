"""
Pydantic models for Mood Match API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class MoodEntry(BaseModel):
    """Student's mood/situation description"""
    user_id: str = Field(..., description="Anonymous user identifier")
    mood_description: str = Field(..., description="How the student is feeling")
    context: Optional[str] = Field(None, description="Additional context (academic, social, personal)")
    timestamp: datetime = Field(default_factory=datetime.now)

class MoodAnalysis(BaseModel):
    """Result from mood analyzer agent"""
    primary_emotion: str
    urgency_level: str  # CRISIS, HIGH, MODERATE, LOW
    needs: List[str]
    matching_criteria: Dict
    crisis_detected: bool
    recommended_resources: List[str]

class PeerProfile(BaseModel):
    """Profile for matching"""
    user_id: str
    mood_analysis: MoodAnalysis
    seeking_support: bool
    available_to_support: bool
    timestamp: datetime

class MatchResult(BaseModel):
    """Result from peer matcher agent"""
    match_found: bool
    matched_peer_id: Optional[str]
    match_score: int  # 0-100
    rationale: str
    conversation_starters: List[str]
    safety_flag: bool

class ConversationMessage(BaseModel):
    """Message in a peer support conversation"""
    conversation_id: str
    sender_id: str
    message_text: str
    timestamp: datetime = Field(default_factory=datetime.now)

class FacilitationResponse(BaseModel):
    """Response from conversation facilitator"""
    intervention_needed: bool
    intervention_type: Optional[str]
    message_to_participants: Optional[str]
    suggested_resources: List[str]
    crisis_detected: bool
    conversation_health: str

class ResourceRecommendation(BaseModel):
    """BU resource recommendation"""
    resource_name: str
    resource_type: str  # crisis, mental_health, academic, wellness
    description: str
    location: Optional[str]
    contact: Optional[str]
    emergency: bool

class MoodMatchSession(BaseModel):
    """Complete matching session"""
    session_id: str
    user_id: str
    mood_entry: MoodEntry
    mood_analysis: MoodAnalysis
    match_result: Optional[MatchResult]
    conversation_id: Optional[str]
    status: str  # waiting, matched, in_conversation, completed
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)