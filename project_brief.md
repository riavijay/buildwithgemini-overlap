# My agent: Overlap
One-liner: A conversational agent that helps hybrid workers choose the days worth commuting with a catalog of team schedules, anchor events, and teammate plans.

Tool coverage:
- Memory: User's team affiliation ("Design Team"), "My People" favorites list (e.g. Sarah K., Leo M.), typical weekly pattern, and home office location (HQ Floor 4).
- Tools: 
  - `get_weekly_overlap_summary`: Calculates attendee counts, identifies the "Best Day", and surfaces team events.
  - `update_day_plan`: Sets user status (Office / Remote / Off) for specific weekdays.
  - `get_team_schedule`: Fetches detailed member timelines and anchor events for a selected date.
  - `toggle_favorite_teammate`: Adds or removes colleagues from "My People".
- Catalog/UI: Weekly day cards (Mon–Fri), team timeline rows, anchor events (Team Lunch, Design Crit), and teammate roster cards.
- Image gen: Generates a commemorative team sticker or celebratory card for high-overlap days ("Worth the commute ✨").
- Sandbox: Computes commute efficiency scores, co-location percentages, and calculates the optimal office days maximizing "My People" overlap.

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch (pick what fits): Overlap optimization algorithm via Python sandbox, automated Sunday nudge simulation.
