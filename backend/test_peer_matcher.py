import sys
sys.path.insert(0, '.')

from app.agents.peer_matcher import PeerMatcher
from app.demo_data import DEMO_STUDENT_PROFILES, get_student_by_id
import json

print("=" * 60)
print("TESTING PEER MATCHER")
print("=" * 60)

matcher = PeerMatcher()
ananya = get_student_by_id("student_ananya")

student_profile = {
    "user_id": "student_ananya",
    "profile": ananya,
    "mood_analysis": {
        "primary_emotion": "overwhelmed",
        "urgency_level": "MODERATE",
        "needs": ["peer support"]
    },
    "user_input": "I'm feeling overwhelmed juggling my thesis and job applications."
}

available_peers = []
for profile in DEMO_STUDENT_PROFILES:
    if profile["user_id"] != "student_ananya":
        available_peers.append({
            "user_id": profile["user_id"],
            "profile": profile,
            "mood_analysis": {"primary_emotion": "stressed", "urgency_level": "MODERATE"},
            "seeking_support": True,
            "available_to_support": True
        })

print(f"\nAvailable peers: {len(available_peers)}")
for p in available_peers:
    print(f"  - {p['profile']['name']}")

print("\nCalling matcher...")
result = matcher.find_match(student_profile, available_peers)

print("\nRESULT:")
print(json.dumps(result, indent=2))

if result.get("match_found"):
    print(f"\n✅ Matched with {result['matched_peer_id']}")
else:
    print(f"\n❌ No match: {result.get('rationale', 'unknown')}")