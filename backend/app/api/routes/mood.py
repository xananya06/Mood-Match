"""
API routes for mood entry and analysis
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import MoodEntry, MoodAnalysis, ResourceRecommendation
from app.agents.mood_analyzer import MoodAnalyzer
from app.agents.bu_resources import get_crisis_resources, get_mental_health_resources
from typing import List

router = APIRouter(prefix="/api/mood", tags=["mood"])

# Initialize mood analyzer
mood_analyzer = MoodAnalyzer()

@router.post("/analyze", response_model=MoodAnalysis)
async def analyze_mood(mood_entry: MoodEntry):
    """
    Analyze a student's mood and determine support needs.
    Returns mood analysis with urgency level and matching criteria.
    """
    try:
        # Analyze the mood
        analysis = mood_analyzer.analyze_mood(mood_entry.mood_description)
        
        return MoodAnalysis(**analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing mood: {str(e)}")

@router.post("/crisis-check", response_model=dict)
async def check_for_crisis(mood_entry: MoodEntry):
    """
    Quick crisis check for immediate safety assessment.
    Returns crisis status and immediate resources if needed.
    """
    try:
        analysis = mood_analyzer.analyze_mood(mood_entry.mood_description)
        is_crisis = mood_analyzer.check_for_crisis(analysis)
        
        response = {
            "crisis_detected": is_crisis,
            "urgency_level": analysis["urgency_level"]
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