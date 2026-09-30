"""Data store for Huddle - Athlete Performance Team Hub.
Configured for elite swimmer Liam Vance (200m Butterfly) managing right shoulder pain.
"""
from typing import Dict, List, Any
from datetime import datetime

# Focus Athlete Profile
ATHLETE_PROFILE: Dict[str, Any] = {
    "athlete_id": "ath_002",
    "name": "Liam Vance",
    "age": 21,
    "sport": "Competitive Swimming (200m Butterfly & Freestyle)",
    "events": ["200m Butterfly", "100m Butterfly", "400m Freestyle"],
    "primary_metric": "VO2 Max 74 ml/kg/min | Resting HR 41 bpm",
    "injury_notes": "Right subacromial shoulder impingement. Sharp pain at overhead catch phase. Contraindicated for paddles and high-intensity overhead butterfly sets.",
    "current_readiness": "Modified Training",
    "last_checkin": {
        "timestamp": "Today 05:45 AM",
        "sleep_hours": 7.2,
        "energy_score": 6,
        "soreness_map": "Right anterior shoulder 5/10 (sharp catch entry)",
        "overhead_mobility": "Restricted / Tight",
        "mood": "Determined but cautious",
        "stress_level": 4,
        "notes": "Felt anterior pinching during yesterday's warm-up sculling."
    },
    "two_week_progress": {
        "week_1_avg_pain": "6.2 / 10",
        "week_2_avg_pain": "4.1 / 10 (Improving)",
        "overhead_mobility_trend": "Gaining 5 deg external rotation",
        "total_kick_volume_km": "32 km",
        "active_nutrition_protocol": {
            "anti_inflammatory": "Curcumin 500mg + Omega-3 2,000mg EPA/DHA daily",
            "collagen_repair": "15g Hydrolyzed Collagen + 50mg Vit C 45m pre-rehab",
            "intra_workout_electrolytes": "750mg Sodium Citrate + 35g Cyclic Dextrin in pool bottle",
            "evening_recovery": "400mg Magnesium Bisglycinate + Tart Cherry"
        }
    }
}

# The Support Team
TEAM_MEMBERS: List[Dict[str, Any]] = [
    {"name": "Liam Vance", "role": "Swimmer", "avatar_init": "LV", "access": "Athlete View"},
    {"name": "Coach Soren", "role": "Head Swim Coach", "avatar_init": "CS", "access": "Full Pool & Workout Admin"},
    {"name": "Maya Lin, RD", "role": "Sports Nutritionist", "avatar_init": "ML", "access": "Dietary & Intra-workout Modulator"},
    {"name": "Dr. Elena Vance", "role": "Physiotherapist", "avatar_init": "EV", "access": "Medical & Load Restriction Admin"},
    {"name": "Dave Miller", "role": "Strength & Conditioning Coach", "avatar_init": "DM", "access": "Dryland & Gym Program"}
]

# Daily Performance Schedule
SCHEDULE: List[Dict[str, Any]] = [
    {
        "id": "s_01",
        "time": "06:00 - 08:00",
        "title": "Morning Swim: Aerobic Engine & Kick Focus",
        "role": "Head Swim Coach",
        "intensity": "MODERATE",
        "overhead_risk": "LOW (Fins & Snorkel, No Paddles)",
        "notes": "Adapted set: 4,000m kickboard base + bilateral single-arm drills to rest right shoulder."
    },
    {
        "id": "s_02",
        "time": "11:00 - 12:00",
        "title": "Scapular Stability & Rotator Cuff Rehab",
        "role": "Physiotherapist",
        "intensity": "LOW",
        "overhead_risk": "CONTROLLED",
        "notes": "Isometric external rotations, prone Y/T/W raises, cervical-thoracic release."
    },
    {
        "id": "s_03",
        "time": "14:30 - 15:30",
        "title": "Dryland Core & Lower Body Power",
        "role": "S&C Coach",
        "intensity": "HIGH",
        "overhead_risk": "ZERO",
        "notes": "Trap bar deadlifts, medicine ball scoop throws (underhand only), core anti-rotation."
    },
    {
        "id": "s_04",
        "time": "16:30 - 17:00",
        "title": "Nutritionist Fuel Check & Electrolyte Review",
        "role": "Sports Nutritionist",
        "intensity": "RECOVERY",
        "overhead_risk": "NONE",
        "notes": "Evaluate 14-day tendon inflammation trends, restock intra-session sodium bottle."
    }
]

# 14-Day Check-in History
CHECKINS: List[Dict[str, Any]] = [
    {
        "date": "Today",
        "sleep_hours": 7.2,
        "energy_score": 6,
        "soreness": "Right anterior shoulder 5/10",
        "readiness": "Modified Training",
        "status": "Adaptive Swim Only"
    },
    {
        "date": "Yesterday",
        "sleep_hours": 8.0,
        "energy_score": 7,
        "soreness": "Right shoulder 4/10",
        "readiness": "Modified Training",
        "status": "Dryland Completed"
    },
    {
        "date": "5 Days Ago",
        "sleep_hours": 6.8,
        "energy_score": 5,
        "soreness": "Right shoulder 7/10 (Sharp flare-up)",
        "readiness": "Red",
        "status": "Pulled from Fly sets"
    }
]

# Team Feed & Handoffs
TEAM_FEED: List[Dict[str, Any]] = [
    {
        "id": "f_101",
        "author_name": "Maya Lin, RD",
        "author_role": "Sports Nutritionist",
        "post_type": "NUTRITION_MODULATION",
        "priority": "HIGH",
        "timestamp": "10 mins ago",
        "content": "Updated Liam's 2-week anti-inflammatory protocol: Added Curcumin 500mg + Collagen Peptides pre-rehab. Switched pool hydration to 750mg Sodium Citrate + Cyclic Dextrin to support heavy kick-set glycolytic depletion."
    },
    {
        "id": "f_102",
        "author_name": "Dr. Elena Vance",
        "author_role": "Physiotherapist",
        "post_type": "RESTRICTION",
        "priority": "CRITICAL",
        "timestamp": "1 hr ago",
        "content": "RIGHT SHOULDER RESTRICTION: Liam's impingement is sensitive at the catch phase. Strictly NO butterfly sprint sets, NO hand paddles, and NO overhead barbell presses today."
    },
    {
        "id": "f_103",
        "author_name": "Coach Soren",
        "author_role": "Head Swim Coach",
        "post_type": "WORKOUT_ADAPTATION",
        "priority": "NORMAL",
        "timestamp": "2 hrs ago",
        "content": "Read Liam's morning 5/10 check-in. Adjusted morning board to 4,000m aerobic kick volume (snorkel/fins) with zero overhead load. Preserved aerobic stimulus without shoulder irritation."
    }
]
