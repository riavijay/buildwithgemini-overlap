"""ADK Tools for Huddle (Swimmer Performance Hub).
Equipped with rules for:
- Swimmer check-ins and overhead pain monitoring
- Swim workout conflict checking (paddles, fly sets, overhead pressing vs. shoulder impingement)
- Nutrition & intra-workout electrolyte modulation
- Team board summaries
"""
from typing import Dict, List, Any, Optional
from app.store import ATHLETE_PROFILE, TEAM_MEMBERS, SCHEDULE, CHECKINS, TEAM_FEED

def submit_athlete_checkin(
    sleep_hours: float,
    energy_score: int,
    soreness_map: str,
    overhead_mobility: str = "Restricted",
    mood: str = "Focused",
    stress_level: int = 3,
    notes: Optional[str] = ""
) -> Dict[str, Any]:
    """Logs the swimmer's morning check-in and updates shoulder readiness status."""
    has_shoulder_pain = "shoulder" in soreness_map.lower() or "right" in soreness_map.lower()
    
    # Calculate readiness: Green, Amber, Red
    if energy_score <= 4 or sleep_hours < 6.0 or (has_shoulder_pain and "sharp" in soreness_map.lower() and energy_score < 6):
        readiness = "Medical Stand Down"
        flag = "CRITICAL: Severe shoulder pain / fatigue. High risk of rotator cuff tendinopathy."
    elif has_shoulder_pain or energy_score < 7 or sleep_hours < 7.0:
        readiness = "Modified Training"
        flag = "CAUTION: Right shoulder impingement active. Overhead butterfly and paddles contraindicated."
    else:
        readiness = "Full Clearance"
        flag = "OPTIMAL: Swimmer cleared for standard pool volume."

    checkin_entry = {
        "timestamp": "Just now",
        "sleep_hours": sleep_hours,
        "energy_score": energy_score,
        "soreness_map": soreness_map,
        "overhead_mobility": overhead_mobility,
        "mood": mood,
        "stress_level": stress_level,
        "notes": notes
    }
    
    ATHLETE_PROFILE["current_readiness"] = readiness
    ATHLETE_PROFILE["last_checkin"] = checkin_entry
    CHECKINS.insert(0, {
        "date": "Today",
        "sleep_hours": sleep_hours,
        "energy_score": energy_score,
        "soreness": soreness_map,
        "readiness": readiness,
        "status": flag
    })
    
    return {
        "readiness_status": readiness,
        "flag": flag,
        "swimmer": ATHLETE_PROFILE["name"],
        "checkin_summary": checkin_entry
    }

def check_schedule_conflicts(
    session_title: str,
    day: str,
    time_slot: str,
    role: str
) -> Dict[str, Any]:
    """Validates proposed swimming workouts or gym sessions against Liam's shoulder impingement."""
    conflicts = []
    warnings = []
    title_lower = session_title.lower()

    # Rule 1: High Overhead Butterfly or Paddles with shoulder impingement
    if any(keyword in title_lower for keyword in ["butterfly", "fly", "paddles", "overhead", "snatch", "press"]):
        conflicts.append(
            f"CLINICAL SHOULDER CONTRAINDICATION: Proposed '{session_title}' involves overhead catch or heavy shoulder loading. "
            f"Dr. Elena Vance (Physio) has restricted butterfly sprints and paddles while right shoulder pain is active."
        )

    # Rule 2: High intensity pool session after heavy dryland
    if "sprint" in title_lower or "max" in title_lower:
        warnings.append(
            "HIGH IMPULSE CAUTION: Ensure shoulder is warmed with band external rotations and single-arm sculling before exceeding 80% pace."
        )

    # Rule 3: Suggest safe alternative
    suggested_alternative = None
    if conflicts:
        suggested_alternative = "Switch to 4,000m Kickboard Engine (fins/snorkel) + Bilateral Single-Arm Drill to preserve aerobic conditioning without shoulder strain."

    return {
        "safe_to_schedule": len(conflicts) == 0,
        "conflicts": conflicts,
        "warnings": warnings,
        "suggested_alternative": suggested_alternative
    }

def update_nutrition_protocol(
    anti_inflammatory_supplements: str,
    intra_workout_electrolytes: str,
    recovery_minerals: str,
    reasoning: str
) -> Dict[str, Any]:
    """Allows the Sports Nutritionist to modulate supplements, intra-workout electrolytes, and minerals based on multi-week recovery trends."""
    proto = ATHLETE_PROFILE["two_week_progress"]["active_nutrition_protocol"]
    proto["anti_inflammatory"] = anti_inflammatory_supplements
    proto["intra_workout_electrolytes"] = intra_workout_electrolytes
    proto["evening_recovery"] = recovery_minerals

    update_entry = {
        "id": f"f_{len(TEAM_FEED) + 100}",
        "author_name": "Maya Lin, RD",
        "author_role": "Sports Nutritionist",
        "post_type": "NUTRITION_MODULATION",
        "priority": "HIGH",
        "timestamp": "Just now",
        "content": f"Pivoted Swimmer Nutrition Protocol: {reasoning}. Intra-workout: {intra_workout_electrolytes}. Anti-inflammatory: {anti_inflammatory_supplements}."
    }
    TEAM_FEED.insert(0, update_entry)

    return {
        "status": "Nutrition protocol updated successfully",
        "updated_protocol": proto,
        "feed_post": update_entry
    }

def get_athlete_status_board() -> Dict[str, Any]:
    """Returns the unified status board for Liam Vance, including team feed, schedule, and 2-week progress trends."""
    return {
        "athlete_profile": ATHLETE_PROFILE,
        "today_schedule": SCHEDULE,
        "team_feed": TEAM_FEED,
        "two_week_trends": ATHLETE_PROFILE["two_week_progress"]
    }
