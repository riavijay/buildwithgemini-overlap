"""Domain tools for Overlap - The Hybrid Work Planner.
Used by the FastAPI endpoints and the ADK Gemini agent.
"""
from typing import Dict, List, Any, Optional
from app.store import USER_PROFILE, TEAM_MEMBERS, WEEKLY_SCHEDULE

def get_weekly_overlap_summary(user_id: str = "u_maya") -> Dict[str, Any]:
    """Calculates weekly attendee counts, identifies the 'Best Day' to commute,
    and returns Mon-Fri day summaries with 'My People' overlap counts."""
    my_people_set = set(USER_PROFILE["my_people_ids"])
    days_summary = []
    best_day = None
    max_my_people_count = -1
    max_total_attendees = -1

    for day_name, data in WEEKLY_SCHEDULE.items():
        members = data["members"]
        user_status = members.get(user_id, {}).get("status", "NOT_SURE")
        
        # Calculate who is in the office
        office_members = []
        my_people_in_office = []
        
        for m_id, m_status in members.items():
            if m_status["status"] == "OFFICE":
                member_info = TEAM_MEMBERS.get(m_id, {"id": m_id, "name": m_id, "avatar": "??"})
                office_members.append(member_info)
                if m_id in my_people_set:
                    my_people_in_office.append(member_info)

        total_in_office = len(office_members)
        my_people_count = len(my_people_in_office)

        # Microcopy logic
        if total_in_office >= 8:
            microcopy = "Worth the commute ✨"
        elif total_in_office >= 5:
            microcopy = "Good collaboration day"
        elif total_in_office <= 2:
            microcopy = "Quiet day, bring headphones"
        else:
            microcopy = "Light office presence"

        # Check for best day (primary: most of my people, secondary: total office count)
        if (my_people_count > max_my_people_count) or (my_people_count == max_my_people_count and total_in_office > max_total_attendees):
            max_my_people_count = my_people_count
            max_total_attendees = total_in_office
            best_day = day_name

        days_summary.append({
            "day": day_name,
            "date_str": data["date_str"],
            "user_status": user_status,
            "total_in_office": total_in_office,
            "my_people_count": my_people_count,
            "my_people_avatars": [m["avatar"] for m in my_people_in_office[:4]],
            "has_events": len(data["events"]) > 0,
            "event_count": len(data["events"]),
            "microcopy": microcopy
        })

    best_day_info = {
        "day": best_day,
        "date_str": WEEKLY_SCHEDULE[best_day]["date_str"],
        "my_people_count": max_my_people_count,
        "total_in_office": max_total_attendees,
        "events": WEEKLY_SCHEDULE[best_day]["events"],
        "avatars": [TEAM_MEMBERS[m]["avatar"] for m in my_people_set if WEEKLY_SCHEDULE[best_day]["members"].get(m, {}).get("status") == "OFFICE"][:4]
    }

    return {
        "user": USER_PROFILE,
        "best_day": best_day_info,
        "days": days_summary
    }

def update_day_plan(day: str, status: str, user_id: str = "u_maya") -> Dict[str, Any]:
    """Updates the user's status (OFFICE, REMOTE, OFF, NOT_SURE) for a specific day."""
    if day not in WEEKLY_SCHEDULE:
        return {"success": False, "error": f"Invalid day '{day}'"}
    
    status_upper = status.upper()
    if status_upper not in ["OFFICE", "REMOTE", "OFF", "NOT_SURE"]:
        return {"success": False, "error": f"Invalid status '{status}'"}

    WEEKLY_SCHEDULE[day]["members"][user_id] = {
        "status": status_upper,
        "in_time": "09:00" if status_upper == "OFFICE" else None
    }

    # Recalculate summary
    summary = get_weekly_overlap_summary(user_id)
    return {
        "success": True,
        "day": day,
        "new_status": status_upper,
        "updated_summary": summary
    }

def get_day_detail(day: str, user_id: str = "u_maya") -> Dict[str, Any]:
    """Returns detailed attendee timeline, anchor events, and 'My People' for a specific day."""
    if day not in WEEKLY_SCHEDULE:
        return {"error": f"Invalid day '{day}'"}

    data = WEEKLY_SCHEDULE[day]
    my_people_set = set(USER_PROFILE["my_people_ids"])
    
    office_list = []
    remote_list = []
    off_list = []

    for m_id, member_state in data["members"].items():
        member_meta = TEAM_MEMBERS.get(m_id, {"id": m_id, "name": m_id, "role": "Teammate", "team": "Design", "avatar": "??"})
        item = {
            "id": m_id,
            "name": member_meta["name"],
            "role": member_meta["role"],
            "team": member_meta["team"],
            "avatar": member_meta["avatar"],
            "status": member_state["status"],
            "in_time": member_state.get("in_time"),
            "is_my_people": m_id in my_people_set
        }
        if member_state["status"] == "OFFICE":
            office_list.append(item)
        elif member_state["status"] == "REMOTE":
            remote_list.append(item)
        else:
            off_list.append(item)

    # Sort office list with My People first
    office_list.sort(key=lambda x: (not x["is_my_people"], x["name"]))

    return {
        "day": day,
        "date_str": data["date_str"],
        "user_status": data["members"].get(user_id, {}).get("status", "NOT_SURE"),
        "office_location": USER_PROFILE["office_location"],
        "events": data["events"],
        "attendee_counts": {
            "office": len(office_list),
            "remote": len(remote_list),
            "off": len(off_list),
            "my_people_in_office": sum(1 for m in office_list if m["is_my_people"])
        },
        "office_attendees": office_list,
        "remote_attendees": remote_list,
        "off_attendees": off_list
    }

def toggle_favorite(teammate_id: str) -> Dict[str, Any]:
    """Stars or unstars a teammate in Maya's 'My People' list."""
    if teammate_id not in TEAM_MEMBERS:
        return {"success": False, "error": "Teammate not found"}

    if teammate_id in USER_PROFILE["my_people_ids"]:
        USER_PROFILE["my_people_ids"].remove(teammate_id)
        is_starred = False
    else:
        USER_PROFILE["my_people_ids"].append(teammate_id)
        is_starred = True

    return {
        "success": True,
        "teammate_id": teammate_id,
        "teammate_name": TEAM_MEMBERS[teammate_id]["name"],
        "is_starred": is_starred,
        "my_people_count": len(USER_PROFILE["my_people_ids"])
    }

def calculate_commute_value(day: str, user_id: str = "u_maya") -> Dict[str, Any]:
    """Calculates commute value score (1-100) based on team overlap, My People presence, and anchor events."""
    if day not in WEEKLY_SCHEDULE:
        return {"error": "Invalid day"}

    detail = get_day_detail(day, user_id)
    my_people_in = detail["attendee_counts"]["my_people_in_office"]
    total_in = detail["attendee_counts"]["office"]
    event_count = len(detail["events"])

    # Score algorithm: 15 pts per My Person (max 60) + 4 pts per general teammate (max 30) + 10 pts per event (max 20)
    score = min(100, (my_people_in * 15) + (total_in * 4) + (event_count * 10))

    if score >= 75:
        verdict = "High Value Commute ✨"
        recommendation = "Definitely go in. Peak collaboration with your core crew and scheduled team events."
    elif score >= 50:
        verdict = "Moderate Value Commute"
        recommendation = "Good for co-working or in-person 1-on-1s."
    else:
        verdict = "Low Value Commute (Work From Home Suggested)"
        recommendation = "Best to stay remote for heads-down deep focus."

    return {
        "day": day,
        "commute_score": score,
        "verdict": verdict,
        "recommendation": recommendation,
        "my_people_in_office": my_people_in,
        "total_in_office": total_in,
        "events": detail["events"]
    }
