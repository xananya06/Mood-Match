# BU-specific resources for Mood Match
# Campus locations, support services, and emergency contacts

BU_SUPPORT_SERVICES = {
    "mental_health": {
        "Student Health Services - Behavioral Medicine": {
            "description": "Professional counseling and psychiatric services",
            "location": "881 Commonwealth Avenue",
            "hours": "Mon-Fri 8:30am-5pm",
            "contact": "(617) 353-3569",
            "emergency": False,
            "walk_in": "Limited walk-in hours available"
        },
        "Center for Psychiatric Rehabilitation": {
            "description": "Support for students with mental health conditions",
            "location": "940 Commonwealth Avenue",
            "contact": "(617) 353-3549",
            "emergency": False
        }
    },
    
    "crisis_support": {
        "BU Police Emergency": {
            "description": "24/7 emergency response for life-threatening situations",
            "contact": "911 or (617) 353-2121",
            "emergency": True
        },
        "Crisis Text Line": {
            "description": "24/7 text-based crisis support",
            "contact": "Text 'HOME' to 741741",
            "emergency": True
        },
        "National Suicide Prevention Lifeline": {
            "description": "24/7 suicide prevention hotline",
            "contact": "988 or 1-800-273-8255",
            "emergency": True
        }
    },
    
    "academic_support": {
        "Dean of Students Office": {
            "description": "Academic concerns, personal challenges, advocacy",
            "location": "100 Bay State Road",
            "contact": "(617) 353-4126",
            "emergency": False
        },
        "Educational Resource Center": {
            "description": "Academic coaching, study strategies, time management",
            "location": "100 Bay State Road",
            "contact": "(617) 353-3658",
            "emergency": False
        }
    },
    
    "wellness": {
        "FitRec (Fitness & Recreation Center)": {
            "description": "Gym, fitness classes, stress relief through exercise",
            "location": "915 Commonwealth Avenue",
            "hours": "Varies by semester",
            "emergency": False
        },
        "Marsh Chapel": {
            "description": "Quiet meditation space, spiritual support",
            "location": "735 Commonwealth Avenue",
            "emergency": False
        }
    }
}

BU_QUIET_SPACES = [
    {
        "name": "Marsh Chapel Meditation Room",
        "location": "735 Commonwealth Avenue",
        "description": "Peaceful space for reflection and meditation",
        "access": "Open during chapel hours"
    },
    {
        "name": "Mugar Library Study Rooms",
        "location": "771 Commonwealth Avenue",
        "description": "Individual study rooms for focused work",
        "access": "Reserve through library website"
    },
    {
        "name": "GSU Upper Floors",
        "location": "775 Commonwealth Avenue",
        "description": "Quieter study spaces away from main traffic",
        "access": "Open during GSU hours"
    },
    {
        "name": "BU Beach",
        "location": "Behind Marsh Plaza",
        "description": "Outdoor green space for relaxation",
        "access": "Open 24/7"
    }
]

BU_WELLNESS_ACTIVITIES = [
    "Group fitness classes at FitRec",
    "Meditation sessions at Sargent Choice",
    "Walking along the Esplanade",
    "Student organization meetings",
    "Intramural sports"
]

def get_crisis_resources():
    """Return immediate crisis resources"""
    return BU_SUPPORT_SERVICES["crisis_support"]

def get_mental_health_resources():
    """Return mental health support services"""
    return BU_SUPPORT_SERVICES["mental_health"]

def get_quiet_spaces():
    """Return list of quiet spaces on campus"""
    return BU_QUIET_SPACES

def get_all_resources():
    """Return all BU resources"""
    return {
        "support_services": BU_SUPPORT_SERVICES,
        "quiet_spaces": BU_QUIET_SPACES,
        "wellness_activities": BU_WELLNESS_ACTIVITIES
    }