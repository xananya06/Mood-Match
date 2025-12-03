#!/usr/bin/env python3
"""
Test script to check what the find-match API is actually returning
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_match():
    print("=" * 60)
    print("TESTING MOOD MATCH API")
    print("=" * 60)
    
    # Step 1: Analyze mood
    print("\n📝 Step 1: Analyzing mood...")
    mood_data = {
        "mood_text": "I'm feeling overwhelmed juggling my thesis and job applications. Some days I wonder if I'm doing enough.",
        "user_id": "student_ananya"
    }
    
    response = requests.post(f"{BASE_URL}/api/analyze-mood", json=mood_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return
    
    analysis = response.json()
    print(f"✅ Mood Analysis: {analysis.get('mood_analysis', {}).get('primary_emotion')}")
    
    # Step 2: Find match
    print("\n🔍 Step 2: Finding match...")
    match_data = {
        "user_id": "student_ananya",
        "mood_analysis": analysis.get("mood_analysis", {})
    }
    
    response = requests.post(f"{BASE_URL}/api/find-match", json=match_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return
    
    match_result = response.json()
    
    # Print full response
    print("\n" + "=" * 60)
    print("FULL MATCH RESULT:")
    print("=" * 60)
    print(json.dumps(match_result, indent=2))
    print("=" * 60)
    
    # Summary
    print("\n📊 SUMMARY:")
    print(f"   Match Found: {match_result.get('match_found')}")
    if match_result.get('match_found'):
        print(f"   Matched Peer: {match_result.get('matched_peer', {}).get('name')}")
        print(f"   Match Score: {match_result.get('match_score')}%")
        print(f"   Mood Similarity: {match_result.get('mood_similarity_score')}%")
        print(f"   Profile Compatibility: {match_result.get('profile_compatibility_score')}%")
        
        # Check for locations
        if match_result.get('location_recommendations'):
            print(f"   Location Recommendations: {len(match_result.get('location_recommendations', {}).get('locations', []))} locations")
    else:
        print(f"   Message: {match_result.get('message', 'No message')}")

if __name__ == "__main__":
    try:
        test_match()
    except Exception as e:
        print(f"\n❌ Error running test: {e}")
        import traceback
        traceback.print_exc()