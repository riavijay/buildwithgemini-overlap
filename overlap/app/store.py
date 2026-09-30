"""Data store for Overlap - The Hybrid Work Planner.
Stores user profile, 'My People' favorites, weekly plans, and anchor events.
"""
from typing import Dict, List, Any

# Current user: Maya Chen
USER_PROFILE: Dict[str, Any] = {
    "user_id": "u_maya",
    "name": "Maya Chen",
    "role": "Lead Product Designer",
    "team": "Design team",
    "avatar_init": "MC",
    "office_location": "HQ, Floor 4",
    "my_people_ids": ["u_sarah", "u_leo", "u_priya", "u_elena", "u_alex"]
}

# Team roster
TEAM_MEMBERS: Dict[str, Dict[str, Any]] = {
    "u_maya": {"id": "u_maya", "name": "Maya Chen", "role": "Product Designer", "team": "Design", "avatar": "MC"},
    "u_sarah": {"id": "u_sarah", "name": "Sarah K.", "role": "Senior UX Researcher", "team": "Design", "avatar": "SK"},
    "u_leo": {"id": "u_leo", "name": "Leo M.", "role": "Staff Product Designer", "team": "Design", "avatar": "LM"},
    "u_priya": {"id": "u_priya", "name": "Priya N.", "role": "Design Systems Lead", "team": "Design", "avatar": "PN"},
    "u_elena": {"id": "u_elena", "name": "Elena R.", "role": "Engineering Lead", "team": "Frontend", "avatar": "ER"},
    "u_alex": {"id": "u_alex", "name": "Alex T.", "role": "Product Manager", "team": "Product", "avatar": "AT"},
    "u_marcus": {"id": "u_marcus", "name": "Marcus C.", "role": "Brand Designer", "team": "Design", "avatar": "MC2"},
    "u_hannah": {"id": "u_hannah", "name": "Hannah B.", "role": "Motion Designer", "team": "Design", "avatar": "HB"},
    "u_david": {"id": "u_david", "name": "David W.", "role": "Data Analyst", "team": "Analytics", "avatar": "DW"},
    "u_jordan": {"id": "u_jordan", "name": "Jordan P.", "role": "Content Strategist", "team": "Content", "avatar": "JP"},
    "u_claire": {"id": "u_claire", "name": "Claire S.", "role": "Engineering Director", "team": "Leadership", "avatar": "CS"}
}

# Team schedules for this week (Mon - Fri)
# Status options: OFFICE, REMOTE, OFF, NOT_SURE
WEEKLY_SCHEDULE: Dict[str, Dict[str, Any]] = {
    "Monday": {
        "date_str": "Mon 17 Jun",
        "events": [],
        "members": {
            "u_maya": {"status": "REMOTE", "in_time": None},
            "u_sarah": {"status": "REMOTE", "in_time": None},
            "u_leo": {"status": "REMOTE", "in_time": None},
            "u_priya": {"status": "OFFICE", "in_time": "09:30"},
            "u_elena": {"status": "OFFICE", "in_time": "10:00"},
            "u_alex": {"status": "REMOTE", "in_time": None},
            "u_marcus": {"status": "OFF", "in_time": None},
            "u_hannah": {"status": "REMOTE", "in_time": None},
            "u_david": {"status": "OFFICE", "in_time": "09:00"},
            "u_jordan": {"status": "REMOTE", "in_time": None},
            "u_claire": {"status": "REMOTE", "in_time": None}
        }
    },
    "Tuesday": {
        "date_str": "Tue 18 Jun",
        "events": [
            {"id": "ev_01", "title": "Design Systems Sync", "time": "11:00 AM", "location": "Room Orbit", "color": "sunshine"}
        ],
        "members": {
            "u_maya": {"status": "REMOTE", "in_time": None},
            "u_sarah": {"status": "OFFICE", "in_time": "09:00"},
            "u_leo": {"status": "REMOTE", "in_time": None},
            "u_priya": {"status": "OFFICE", "in_time": "09:00"},
            "u_elena": {"status": "REMOTE", "in_time": None},
            "u_alex": {"status": "OFFICE", "in_time": "09:15"},
            "u_marcus": {"status": "OFFICE", "in_time": "10:00"},
            "u_hannah": {"status": "REMOTE", "in_time": None},
            "u_david": {"status": "OFFICE", "in_time": "08:45"},
            "u_jordan": {"status": "REMOTE", "in_time": None},
            "u_claire": {"status": "OFFICE", "in_time": "09:30"}
        }
    },
    "Wednesday": {
        "date_str": "Wed 19 Jun",
        "events": [
            {"id": "ev_02", "title": "Team Pizza Lunch", "time": "12:30 PM", "location": "Floor 4 Kitchen", "color": "sunshine", "joinable": True},
            {"id": "ev_03", "title": "Design Crit", "time": "15:00 PM", "location": "Studio B", "color": "sunshine", "joinable": False}
        ],
        "members": {
            "u_maya": {"status": "OFFICE", "in_time": "09:00"},
            "u_sarah": {"status": "OFFICE", "in_time": "09:00"},
            "u_leo": {"status": "OFFICE", "in_time": "09:15"},
            "u_priya": {"status": "OFFICE", "in_time": "09:30"},
            "u_elena": {"status": "OFFICE", "in_time": "10:00"},
            "u_alex": {"status": "OFFICE", "in_time": "08:30"},
            "u_marcus": {"status": "OFFICE", "in_time": "09:00"},
            "u_hannah": {"status": "OFFICE", "in_time": "09:45"},
            "u_david": {"status": "REMOTE", "in_time": None},
            "u_jordan": {"status": "OFFICE", "in_time": "10:15"},
            "u_claire": {"status": "OFFICE", "in_time": "09:00"}
        }
    },
    "Thursday": {
        "date_str": "Thu 20 Jun",
        "events": [
            {"id": "ev_04", "title": "Q3 Roadmap Workshop", "time": "14:00 PM", "location": "The Arena", "color": "sunshine"}
        ],
        "members": {
            "u_maya": {"status": "OFFICE", "in_time": "09:00"},
            "u_sarah": {"status": "OFFICE", "in_time": "09:15"},
            "u_leo": {"status": "OFFICE", "in_time": "09:30"},
            "u_priya": {"status": "REMOTE", "in_time": None},
            "u_elena": {"status": "OFFICE", "in_time": "09:00"},
            "u_alex": {"status": "REMOTE", "in_time": None},
            "u_marcus": {"status": "REMOTE", "in_time": None},
            "u_hannah": {"status": "OFFICE", "in_time": "10:00"},
            "u_david": {"status": "OFFICE", "in_time": "09:00"},
            "u_jordan": {"status": "REMOTE", "in_time": None},
            "u_claire": {"status": "OFFICE", "in_time": "09:30"}
        }
    },
    "Friday": {
        "date_str": "Fri 21 Jun",
        "events": [],
        "members": {
            "u_maya": {"status": "REMOTE", "in_time": None},
            "u_sarah": {"status": "REMOTE", "in_time": None},
            "u_leo": {"status": "REMOTE", "in_time": None},
            "u_priya": {"status": "REMOTE", "in_time": None},
            "u_elena": {"status": "REMOTE", "in_time": None},
            "u_alex": {"status": "REMOTE", "in_time": None},
            "u_marcus": {"status": "OFF", "in_time": None},
            "u_hannah": {"status": "REMOTE", "in_time": None},
            "u_david": {"status": "REMOTE", "in_time": None},
            "u_jordan": {"status": "REMOTE", "in_time": None},
            "u_claire": {"status": "REMOTE", "in_time": None}
        }
    }
}
