# Overlap — The Hybrid Work Planner

> **Know who's in. Make the commute worth it.**

**Overlap** is an employee-first hybrid work coordination application built during the Google Cloud *Build with Gemini* lab. It answers one essential question in under 5 seconds: **"Which days are my favorite collaborators in the office, so I can choose the days worth commuting?"**

---

## ✨ Key Features

- **Personalized Overlap Highlights**: Instantly surfaces your peak collaboration day (e.g., *Wednesday — 5 of 5 favourites in*).
- **One-Tap Day Planning**: Confirm your presence with a single tap (`[I'm in Office]` vs `[Work Remote]`).
- **Audience Scope Filtering**: Seamlessly toggle between:
  - **Favourites (5)**: Your starred inner circle (all from Design).
  - **Design (6)**: Direct functional team members.
  - **All Teams (10)**: Everyone on the floor across Product, Design, and Engineering.
- **Anchor Events**: Coordinate around shared moments like *Team Pizza Lunch* and *Design Crit*.
- **Plan Your Week**: Interactive bottom sheet allowing you to cycle and lock in your schedule across all weekdays.
- **Overlap AI Coordinator**: Conversational assistant powered by Gemini 2.5 Flash on Vertex AI.

---

## 🛠️ Architecture & Tech Stack

- **Agent Engine & Reasoning**: Google GenAI SDK with ADK runner (`gemini-2.5-flash` on Vertex AI).
- **Backend API**: FastAPI with domain tools for weekly overlap summaries, day details, and commute efficiency calculations.
- **Frontend**: Clean, touch-optimized mobile interface with zero external CSS frameworks, geometric Plus Jakarta Sans typography, and fluid transitions.

---

## 🚀 Running Locally

### Prerequisites
- Python 3.10+
- Google Cloud Project with Vertex AI enabled

### Setup & Launch
```bash
# Clone the repository
git clone https://github.com/riavijay/buildwithgemini-overlap.git
cd buildwithgemini-overlap/overlap

# Set up environment
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=<your-gcp-project-id>
export GOOGLE_CLOUD_LOCATION=us-central1

# Install requirements & start server
pip install -r requirements.txt
python3 server.py
```
Open `http://localhost:8080` in your browser.
