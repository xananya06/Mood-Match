"""
BU Student Profiles for Demo
5 realistic profiles based on common BU student experiences
"""

DEMO_STUDENT_PROFILES = [
    {
        "user_id": "student_ananya",
        "name": "Ananya",
        "year": "MS AI (Graduating Dec 2025)",
        "major": "Artificial Intelligence",
        "interests": ["AI/ML", "Singing", "Writing", "Indie Music"],
        "personality": "Thoughtful, ambitious, values authenticity",
        "current_focus": "Thesis + Job Applications",
        "communication_style": "Direct and genuine, dislikes corporate jargon",
        "bio": "MS AI student juggling thesis work and job hunting. I love singing, writing, and building things that help people. Looking for someone who gets the grad school grind.",
        "mood_post": "I'm feeling overwhelmed juggling my thesis and job applications. Some days I wonder if I'm doing enough. Could use someone who understands the pressure of graduating soon.",
        "avatar": "👩‍💻"
    },
    {
        "user_id": "student_marcus",
        "name": "Marcus",
        "year": "Junior, CS Major",
        "major": "Computer Science",
        "interests": ["Gaming", "Basketball", "Hackathons", "Hip-hop"],
        "personality": "Energetic, collaborative, naturally encouraging",
        "current_focus": "Internship Search",
        "communication_style": "Casual and supportive",
        "bio": "CS junior trying to land a summer internship. I'm into gaming, basketball, and building cool projects. Always down to help someone debug code or life.",
        "mood_post": "Internship rejections are hitting different this year. Applied to 50+ places and only got 2 interviews. Starting to doubt myself and wonder if I'm good enough for this field.",
        "avatar": "👨‍💻"
    },
    {
        "user_id": "student_priya",
        "name": "Priya",
        "year": "Senior, Business Analytics",
        "major": "Business Analytics",
        "interests": ["Data visualization", "Yoga", "K-pop", "Coffee culture"],
        "personality": "Calm, analytical, good listener",
        "current_focus": "Career transition to tech",
        "communication_style": "Empathetic and thoughtful",
        "bio": "BA senior transitioning into data science. International student from Mumbai. I love analyzing patterns - in data and in life. Great listener if you need one.",
        "mood_post": "Missing home a lot lately. Everything here still feels temporary even after 3 years. My family doesn't really understand what I'm going through with recruiting season.",
        "avatar": "👩‍💼"
    },
    {
        "user_id": "student_jake",
        "name": "Jake",
        "year": "Sophomore, Engineering",
        "major": "Mechanical Engineering",
        "interests": ["Rock climbing", "EDM", "3D printing", "Sci-fi"],
        "personality": "Adventurous, creative problem-solver",
        "current_focus": "Managing course load",
        "communication_style": "Optimistic but honest about struggles",
        "bio": "ME sophomore who loves building things and climbing walls (literally). Trying to balance GPA and actually learning. Always down to grab food and vent about problem sets.",
        "mood_post": "Thermodynamics is destroying me. I study for hours but still bomb the exams. Feel like everyone else just 'gets it' and I'm falling behind. Starting to question if engineering is for me.",
        "avatar": "🧑‍🔧"
    },
    {
        "user_id": "student_sara",
        "name": "Sara",
        "year": "First-year, Undecided",
        "major": "Exploring Psychology/Neuroscience",
        "interests": ["Poetry", "Mental health advocacy", "Indie folk", "Journaling"],
        "personality": "Introspective, empathetic, still finding herself",
        "current_focus": "Adjusting to college life",
        "communication_style": "Vulnerable and authentic",
        "bio": "First-year trying to figure out my major and life. I write poetry and care a lot about mental health. Still getting used to being away from home and finding my people.",
        "mood_post": "Honestly feeling really lonely. Everyone seems to have found their friend groups already and I'm still eating lunch alone most days. Is it supposed to be this hard to connect?",
        "avatar": "👩‍🎓"
    }
]

# BU-specific locations with context
BU_HANGOUT_LOCATIONS = {
    "study_quiet": [
        {
            "name": "Mugar Library - 5th Floor",
            "address": "771 Commonwealth Ave",
            "vibe": "Quiet study space with great views",
            "good_for": ["Focused conversation", "Academic stress", "Need to decompress"],
            "amenities": ["Whiteboards", "Private study rooms", "Windows overlooking campus"],
            "best_time": "Weekday afternoons",
            "emoji": "📚"
        },
        {
            "name": "George Sherman Union - 2nd Floor Lounge",
            "address": "775 Commonwealth Ave",
            "vibe": "Comfortable couches, not too loud",
            "good_for": ["Casual chat", "Need coffee", "Want background noise"],
            "amenities": ["Coffee shop nearby", "Comfortable seating", "Student atmosphere"],
            "best_time": "Anytime",
            "emoji": "☕"
        }
    ],
    "outdoor_active": [
        {
            "name": "BU Beach",
            "address": "Behind Marsh Plaza, 735 Comm Ave",
            "vibe": "Outdoor green space, relaxing",
            "good_for": ["Need fresh air", "Stress relief", "Casual hangout"],
            "amenities": ["Grass to sit on", "Good people watching", "Away from buildings"],
            "best_time": "Nice weather days",
            "emoji": "🌳"
        },
        {
            "name": "Charles River Esplanade",
            "address": "Along Storrow Drive",
            "vibe": "Walking path by the river",
            "good_for": ["Need to move", "Deep conversations", "Nature lovers"],
            "amenities": ["Scenic views", "Walking/running path", "Benches"],
            "best_time": "Evenings, weekends",
            "emoji": "🌊"
        }
    ],
    "food_social": [
        {
            "name": "Terrier Dining Room (West Campus)",
            "address": "1019 Commonwealth Ave",
            "vibe": "Dining hall, social atmosphere",
            "good_for": ["Meal time", "Social setting", "Budget friendly"],
            "amenities": ["Variety of food", "Long tables", "Social atmosphere"],
            "best_time": "Lunch or dinner hours",
            "emoji": "🍽️"
        },
        {
            "name": "Questrom Cafe",
            "address": "595 Commonwealth Ave",
            "vibe": "Coffee shop in business school",
            "good_for": ["Coffee chat", "Professional vibe", "Between classes"],
            "amenities": ["Coffee", "Snacks", "Good seating"],
            "best_time": "Afternoon",
            "emoji": "☕"
        },
        {
            "name": "Dumpling House",
            "address": "950 Commonwealth Ave",
            "vibe": "Casual Chinese restaurant",
            "good_for": ["Comfort food", "Budget-friendly", "Off-campus feel"],
            "amenities": ["Good food", "Student favorite", "Quick service"],
            "best_time": "Dinner time",
            "emoji": "🥟"
        }
    ],
    "creative_energetic": [
        {
            "name": "FitRec Center",
            "address": "915 Commonwealth Ave",
            "vibe": "Gym and fitness center",
            "good_for": ["Need to move", "Release stress", "Active types"],
            "amenities": ["Gym equipment", "Classes", "Pool"],
            "best_time": "After classes",
            "emoji": "💪"
        },
        {
            "name": "GSU Game Room",
            "address": "775 Commonwealth Ave, Lower Level",
            "vibe": "Pool tables, games, laid back",
            "good_for": ["Want distraction", "Competitive fun", "Low pressure"],
            "amenities": ["Pool tables", "Board games", "Ping pong"],
            "best_time": "Evenings",
            "emoji": "🎮"
        }
    ],
    "arts_culture": [
        {
            "name": "BU Arts Initiative Gallery",
            "address": "808 Commonwealth Ave",
            "vibe": "Art gallery, quiet, inspiring",
            "good_for": ["Creative types", "Need inspiration", "Quiet reflection"],
            "amenities": ["Art exhibits", "Quiet space", "Free entry"],
            "best_time": "Weekday afternoons",
            "emoji": "🎨"
        },
        {
            "name": "Marsh Chapel",
            "address": "735 Commonwealth Ave",
            "vibe": "Peaceful, spiritual space",
            "good_for": ["Need quiet", "Meditation", "Spiritual support"],
            "amenities": ["Quiet seating", "Beautiful architecture", "Meditation room"],
            "best_time": "Anytime quiet hours",
            "emoji": "⛪"
        }
    ]
}

def get_student_by_id(user_id: str):
    """Get student profile by ID"""
    for student in DEMO_STUDENT_PROFILES:
        if student["user_id"] == user_id:
            return student
    return None

def get_all_students_except(exclude_user_id: str):
    """Get all student profiles except the specified one"""
    return [s for s in DEMO_STUDENT_PROFILES if s["user_id"] != exclude_user_id]

def get_location_recommendations(student1_profile: dict, student2_profile: dict, mood_themes: list):
    """
    Get location recommendations based on two student profiles and mood themes
    Returns top 3 recommended locations with reasoning
    """
    recommendations = []
    
    # Analyze what type of locations would work
    interests1 = set(student1_profile.get("interests", []))
    interests2 = set(student2_profile.get("interests", []))
    shared_interests = interests1.intersection(interests2)
    
    # Check mood themes
    needs_quiet = any(theme in ["stress", "overwhelm", "anxiety", "academic pressure"] for theme in mood_themes)
    needs_active = any(theme in ["restless", "need movement", "energetic"] for theme in mood_themes)
    needs_comfort = any(theme in ["loneliness", "homesick", "sad", "isolation"] for theme in mood_themes)
    
    # Select appropriate location categories
    if needs_quiet and ("study" in str(interests1) or "study" in str(interests2)):
        recommendations.extend(BU_HANGOUT_LOCATIONS["study_quiet"])
    
    if needs_active or any(sport in shared_interests for sport in ["Basketball", "Rock climbing", "Gaming"]):
        recommendations.extend(BU_HANGOUT_LOCATIONS["creative_energetic"])
    
    if needs_comfort or needs_quiet:
        recommendations.extend(BU_HANGOUT_LOCATIONS["food_social"])
        recommendations.extend(BU_HANGOUT_LOCATIONS["outdoor_active"])
    
    if any(art in shared_interests for art in ["Poetry", "Writing", "Music", "Singing"]):
        recommendations.extend(BU_HANGOUT_LOCATIONS["arts_culture"])
    
    # Default: always include these as backup
    if not recommendations:
        recommendations.extend(BU_HANGOUT_LOCATIONS["study_quiet"])
        recommendations.extend(BU_HANGOUT_LOCATIONS["food_social"][:1])
    
    # Return top 3 unique locations
    seen_names = set()
    unique_recommendations = []
    for loc in recommendations:
        if loc["name"] not in seen_names:
            seen_names.add(loc["name"])
            unique_recommendations.append(loc)
        if len(unique_recommendations) >= 3:
            break
    
    return unique_recommendations