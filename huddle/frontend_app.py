from dotenv import load_dotenv
import os
load_dotenv()
"""Huddle — Athlete Performance Team Hub.
Tailored for Liam Vance (Elite Swimmer) managing right shoulder pain.
Step-by-step user flow:
1. Swimmer Check-in & Shoulder Pain Tracker
2. Coach Workout Board & Safety Clash Simulator (Swaps Fly sets for Kick sets)
3. 2-Week Nutrition & Intra-Workout Electrolyte Modulator (Curcumin, Collagen, Sodium Citrate)
4. Gemini Performance Coordinator
"""
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.agent import root_agent
from app.store import ATHLETE_PROFILE, TEAM_MEMBERS, SCHEDULE, CHECKINS, TEAM_FEED
from app.tools import (
    submit_athlete_checkin,
    check_schedule_conflicts,
    update_nutrition_protocol,
    get_athlete_status_board
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

app = FastAPI(title="Huddle - Swimmer Performance Team Hub")

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="huddle", session_service=session_service)

class CheckinRequest(BaseModel):
    sleep_hours: float
    energy_score: int
    soreness_map: str
    overhead_mobility: Optional[str] = "Restricted"
    mood: Optional[str] = "Focused"
    stress_level: Optional[int] = 3
    notes: Optional[str] = ""

class NutritionModulationRequest(BaseModel):
    anti_inflammatory: str
    intra_workout_electrolytes: str
    recovery_minerals: str
    reasoning: str

class ConflictCheckRequest(BaseModel):
    session_title: str
    day: str
    time_slot: str
    role: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_user_session"

@app.get("/api/status")
async def api_get_status():
    return get_athlete_status_board()

@app.post("/api/checkin")
async def api_submit_checkin(req: CheckinRequest):
    result = submit_athlete_checkin(
        sleep_hours=req.sleep_hours,
        energy_score=req.energy_score,
        soreness_map=req.soreness_map,
        overhead_mobility=req.overhead_mobility or "Restricted",
        mood=req.mood or "Focused",
        stress_level=req.stress_level or 3,
        notes=req.notes
    )
    return result

@app.post("/api/nutrition-modulate")
async def api_modulate_nutrition(req: NutritionModulationRequest):
    result = update_nutrition_protocol(
        anti_inflammatory_supplements=req.anti_inflammatory,
        intra_workout_electrolytes=req.intra_workout_electrolytes,
        recovery_minerals=req.recovery_minerals,
        reasoning=req.reasoning
    )
    return result

@app.post("/api/check-conflicts")
async def api_check_conflicts(req: ConflictCheckRequest):
    result = check_schedule_conflicts(
        session_title=req.session_title,
        day=req.day,
        time_slot=req.time_slot,
        role=req.role
    )
    return result

@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    session = await session_service.get_session(
        app_name="huddle",
        user_id="user",
        session_id=req.session_id
    )
    if not session:
        session = await session_service.create_session(
            app_name="huddle",
            user_id="user",
            session_id=req.session_id
        )

    reply_text = ""
    async for event in runner.run_async(
        user_id="user",
        session_id=req.session_id,
        new_message=types.Content(parts=[types.Part(text=req.message)])
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    reply_text += part.text

    return {"reply": reply_text or "Processed by Huddle."}

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Huddle — Swimmer Performance Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0" />
  <style>
    :root {
      --bg-canvas: #0d0f14;
      --app-bg: #13151d;
      --lavender: #b49eff;
      --lime: #e2fc4d;
      --lime-dark: #c4e022;
      --white: #ffffff;
      --card-dark: #1b1e28;
      --text-black: #0c0d11;
      --text-muted: #8b8e9b;
      --text-white: #f8f9fc;
      --amber: #f59e0b;
      --radius-phone: 44px;
      --radius-card: 28px;
      --radius-pill: 9999px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
      background: var(--bg-canvas);
      color: var(--text-white);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 1rem;
    }

    .app-device {
      width: 390px;
      max-width: 100%;
      height: 800px;
      max-height: 94vh;
      background: var(--app-bg);
      border-radius: var(--radius-phone);
      display: flex;
      flex-direction: column;
      position: relative;
      box-shadow: 0 30px 80px -20px rgba(0,0,0,0.8), 0 0 0 8px #242733;
      overflow: hidden;
    }

    /* App Header */
    .app-header {
      padding: 1.25rem 1.4rem 0.8rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 0.7rem;
    }
    .brand-avatar {
      width: 42px;
      height: 42px;
      background: var(--lime);
      color: var(--text-black);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.2rem;
    }
    .brand-title {
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 800;
      font-size: 1.15rem;
      letter-spacing: -0.02em;
    }
    .header-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: var(--amber);
      color: #000;
      padding: 0.3rem 0.75rem;
      border-radius: var(--radius-pill);
      font-size: 0.7rem;
      font-weight: 800;
      text-transform: uppercase;
    }

    /* Flow Viewport */
    .view-viewport {
      flex: 1;
      overflow-y: auto;
      padding: 0.5rem 1.25rem 5.8rem;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
    }
    .view-viewport::-webkit-scrollbar { display: none; }

    /* TAB 1: SWIMMER OVERVIEW & SORENESS */
    .hero-card {
      background: var(--lavender);
      color: var(--text-black);
      border-radius: var(--radius-card);
      padding: 1.4rem;
      position: relative;
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
    }
    .avatar-stack {
      display: flex;
      align-items: center;
    }
    .av-circle {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 2px solid var(--lavender);
      background: #111;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      font-weight: 800;
      margin-left: -8px;
    }
    .av-circle:first-child { margin-left: 0; }
    .tag-row {
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
    }
    .tag-pill {
      background: rgba(0,0,0,0.85);
      color: #fff;
      padding: 0.35rem 0.85rem;
      border-radius: var(--radius-pill);
      font-size: 0.75rem;
      font-weight: 700;
    }
    .alert-banner {
      background: rgba(255,255,255,0.4);
      padding: 0.8rem 1rem;
      border-radius: 18px;
      font-size: 0.82rem;
      line-height: 1.4;
      font-weight: 600;
    }

    /* Stacked Post Cards */
    .stacked-white-sheet {
      background: var(--white);
      color: var(--text-black);
      border-radius: var(--radius-card);
      padding: 1.3rem;
      position: relative;
      box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .stacked-lime-under {
      position: absolute;
      top: -8px;
      left: 12px;
      right: 12px;
      height: 24px;
      background: var(--lime);
      border-radius: 20px;
      z-index: 0;
    }
    .sheet-inner { position: relative; z-index: 1; }
    .author-icon {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #111;
      color: var(--lime);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
    }

    /* TAB 2: CHECK-IN & READINESS */
    .hanging-pin-card {
      background: linear-gradient(180deg, #222633 0%, #171922 100%);
      border-radius: var(--radius-card);
      padding: 1.8rem 1.4rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border: 1px solid rgba(255,255,255,0.08);
    }
    .hanging-pin {
      background: var(--lime);
      color: var(--text-black);
      border-radius: 22px 22px 22px 6px;
      padding: 0.9rem 1.4rem;
      display: inline-flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 16px 36px rgba(0,0,0,0.4);
      min-width: 170px;
    }
    .pin-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: 2px solid var(--lime);
      margin-top: -28px;
      background: #111;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
    }
    .pin-val {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.6rem;
      font-weight: 800;
      margin-top: 0.3rem;
    }
    .pin-dot {
      width: 12px;
      height: 12px;
      background: var(--lime);
      border-radius: 50%;
      border: 2px solid #111;
      margin-top: 0.5rem;
    }

    .form-card {
      background: var(--card-dark);
      border-radius: var(--radius-card);
      padding: 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      border: 1px solid rgba(255,255,255,0.06);
    }
    .input-field {
      background: #12141a;
      border: 1px solid rgba(255,255,255,0.1);
      color: #fff;
      padding: 0.8rem 1rem;
      border-radius: var(--radius-pill);
      font-size: 0.88rem;
      outline: none;
      width: 100%;
    }
    .btn-lime {
      background: var(--lime);
      color: var(--text-black);
      border: none;
      padding: 0.9rem;
      border-radius: var(--radius-pill);
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 0.95rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
    }

    /* TAB 3: COACH WORKOUT & ADAPTIVE CLASH */
    .contour-pool {
      background: #1b1e29;
      border-radius: var(--radius-card);
      padding: 1.2rem;
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
      position: relative;
      overflow: hidden;
    }
    .contour-pool svg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      opacity: 0.25;
      pointer-events: none;
    }
    .stat-capsule {
      background: #fff;
      color: #111;
      padding: 0.45rem 0.9rem;
      border-radius: var(--radius-pill);
      font-size: 0.78rem;
      font-weight: 800;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .workout-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.95rem 1.15rem;
      border-radius: 22px;
      font-weight: 700;
      font-size: 0.88rem;
    }
    .workout-item.purple { background: var(--lavender); color: var(--text-black); }
    .workout-item.white { background: var(--white); color: var(--text-black); }
    .workout-item.dark { background: #222633; color: #fff; }

    /* TAB 4: 2-WEEK NUTRITION & ELECTROLYTES */
    .trend-metric-card {
      background: linear-gradient(135deg, #1b1e2a 0%, #282d3f 100%);
      border-radius: var(--radius-card);
      padding: 1.4rem;
      border: 1px solid rgba(255,255,255,0.08);
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
    }
    .metric-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.8rem;
    }
    .metric-box {
      background: rgba(0,0,0,0.3);
      padding: 0.8rem;
      border-radius: 18px;
    }
    .m-title { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700; }
    .m-val { font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: var(--lime); margin-top: 0.2rem; }

    /* Bottom Capsule Dock */
    .app-dock {
      position: absolute;
      bottom: 1rem;
      left: 1.2rem;
      right: 1.2rem;
      background: var(--white);
      border-radius: var(--radius-pill);
      padding: 0.4rem 0.6rem;
      display: flex;
      align-items: center;
      justify-content: space-around;
      box-shadow: 0 15px 35px rgba(0,0,0,0.3);
      z-index: 100;
    }
    .dock-tab {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      color: #64748b;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
    }
    .dock-tab.active {
      background: var(--lavender);
      color: #111;
    }
  </style>
</head>
<body>

  <div class="app-device">

    <!-- Header -->
    <header class="app-header">
      <div class="brand-group">
        <div class="brand-avatar">H</div>
        <div>
          <div class="brand-title">Huddle</div>
          <div style="font-size:0.7rem; color:var(--text-muted); font-weight:600;">Swimmer Performance Hub</div>
        </div>
      </div>

      <div class="header-badge" id="top-readiness-pill">
        <span class="material-symbols-rounded" style="font-size:14px;">warning</span>
        ⚠️ Modified Training (Shoulder)
      </div>
    </header>

    <!-- TAB 1: SWIMMER OVERVIEW & DIRECTIVES -->
    <div id="tab-overview" class="view-viewport">
      <!-- Athlete Profile Hero -->
      <div class="hero-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div class="avatar-stack">
            <div class="av-circle">LV</div>
            <div class="av-circle">CS</div>
            <div class="av-circle">ML</div>
            <div class="av-circle">+2</div>
          </div>
          <button class="round-btn" onclick="switchTab('coach')" style="width:40px; height:40px; border-radius:50%; background:#111; color:#fff; border:none; cursor:pointer;">
            <span class="material-symbols-rounded" style="font-size:18px;">north_east</span>
          </button>
        </div>

        <div>
          <div style="font-size:0.72rem; font-weight:800; text-transform:uppercase; opacity:0.7;">Focus Swimmer</div>
          <h2 style="font-family:'Space Grotesk',sans-serif; font-size:1.7rem; font-weight:800;" id="swimmer-name">Liam Vance</h2>
        </div>

        <div class="tag-row">
          <span class="tag-pill">200m Butterfly</span>
          <span class="tag-pill">VO2 Max: 74</span>
          <span class="tag-pill">Olympic Trials (4 wks)</span>
        </div>

        <div class="alert-banner">
          <strong>Clinical Condition:</strong> Right subacromial impingement. Butterfly catch phase sharp. High overhead volume contraindicated.
        </div>
      </div>

      <!-- Live Practitioner Feed -->
      <div class="stacked-white-sheet">
        <div class="stacked-lime-under"></div>
        <div class="sheet-inner">
          <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.5rem;">
            <div class="author-icon">EV</div>
            <div>
              <div style="font-weight:800; font-size:0.9rem;">Dr. Elena Vance (Physio)</div>
              <div style="font-size:0.7rem; color:#64748b;">Clinical Directive • High Priority</div>
            </div>
          </div>
          <p style="font-size:0.86rem; line-height:1.45; color:#1e293b;">
            Strictly <strong>NO hand paddles</strong> and <strong>NO max-effort butterfly sprints</strong> today. Shift volume to kick sets with snorkel/fins to rest supraspinatus tendon.
          </p>
        </div>
      </div>

      <div class="stacked-white-sheet" style="background:#f8fafc; border:1px solid #e2e8f0;">
        <div class="sheet-inner">
          <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.5rem;">
            <div class="author-icon" style="background:#e2e8f0; color:#111;">ML</div>
            <div>
              <div style="font-weight:800; font-size:0.9rem;">Maya Lin, RD (Nutritionist)</div>
              <div style="font-size:0.7rem; color:#64748b;">Nutrition Modulation • 10m ago</div>
            </div>
          </div>
          <p style="font-size:0.86rem; line-height:1.45; color:#1e293b;">
            Switched pool bottle to <strong>750mg Sodium Citrate + 35g Cyclic Dextrin</strong> to offset kick-set glycogen burn. Added <strong>Curcumin 500mg</strong> for joint inflammation.
          </p>
        </div>
      </div>
    </div>

    <!-- TAB 2: SWIMMER CHECK-IN -->
    <div id="tab-checkin" class="view-viewport" style="display:none;">
      <div class="hanging-pin-card">
        <div class="hanging-pin">
          <div class="pin-avatar">LV</div>
          <div class="pin-val" id="disp-readiness">MODIFIED TRAINING</div>
          <div style="font-size:0.75rem; font-weight:700;">Shoulder Impingement</div>
          <div class="pin-dot"></div>
        </div>
        <div style="margin-top:1.2rem; font-size:0.82rem; color:#94a3b8; text-align:center;">
          Overhead Mobility: <strong style="color:var(--lime);" id="disp-mobility">Restricted / Tight</strong>
        </div>
      </div>

      <div class="form-card">
        <div style="font-family:'Space Grotesk',sans-serif; font-weight:800; font-size:1.15rem;">Daily Swimmer Morning Check-in</div>
        <p style="font-size:0.78rem; color:var(--text-muted);">Informs Coach Soren and Maya Lin before the 06:00 pool session.</p>

        <div>
          <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Sleep Duration (Hours)</label>
          <input class="input-field" type="number" step="0.1" id="f-sleep" value="7.2">
        </div>
        <div>
          <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Energy Score (1 - 10)</label>
          <input class="input-field" type="number" min="1" max="10" id="f-energy" value="6">
        </div>
        <div>
          <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Shoulder Soreness Location &amp; Score</label>
          <input class="input-field" id="f-soreness" value="Right anterior shoulder 5/10 (sharp catch entry)">
        </div>
        <div>
          <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Overhead Catch Mobility</label>
          <select class="input-field" id="f-mobility">
            <option value="Restricted / Tight">Restricted / Tight (Pain at 170 deg)</option>
            <option value="Mild Discomfort">Mild Discomfort</option>
            <option value="Cleared / Pain-Free">Cleared / Pain-Free</option>
          </select>
        </div>

        <button class="btn-lime" onclick="submitSwimmerCheckin()">
          <span class="material-symbols-rounded">check_circle</span>
          Submit &amp; Alert Swim Coach
        </button>
      </div>
    </div>

    <!-- TAB 3: COACH WORKOUT & ADAPTIVE CLASH -->
    <div id="tab-coach" class="view-viewport" style="display:none;">
      <!-- Pool Contour Header -->
      <div class="contour-pool">
        <svg viewBox="0 0 300 150">
          <path d="M 20,75 Q 80,20 160,30 T 260,80 Q 200,130 80,120 Z" fill="none" stroke="rgba(226,252,77,0.7)" stroke-width="2.5" stroke-dasharray="4,4"/>
          <circle cx="240" cy="80" r="5" fill="#e2fc4d"/>
        </svg>
        <div style="font-size:0.8rem; font-weight:800; color:#fff; z-index:2;">
          🏊 Olympic 50m Pool Deck • 06:00 AM
        </div>
        <div style="display:flex; justify-content:space-between; position:relative; z-index:2;">
          <div class="stat-capsule">
            <span style="font-size:0.65rem; color:#64748b;">Target Volume</span>
            <span>4,500m</span>
          </div>
          <div class="stat-capsule">
            <span style="font-size:0.65rem; color:#64748b;">Overhead Stress</span>
            <span style="color:#ef4444;">RESTRICTED</span>
          </div>
          <div style="width:38px; height:38px; border-radius:50%; background:#fff; display:flex; align-items:center; justify-content:center; color:#111;">
            <span class="material-symbols-rounded">pool</span>
          </div>
        </div>
      </div>

      <!-- Coach Schedule List -->
      <div style="font-family:'Space Grotesk',sans-serif; font-size:1.15rem; font-weight:800;">Today's Workout Plan</div>
      <div style="display:flex; flex-direction:column; gap:0.6rem;" id="coach-sched-box">
        <!-- Rendered dynamically -->
      </div>

      <!-- Coach Safety Clash Simulator -->
      <div class="form-card" style="background:#181b24;">
        <div style="font-family:'Space Grotesk',sans-serif; font-weight:800; font-size:1.1rem; color:var(--lime);">Coach Soren: Test Planned Set</div>
        <p style="font-size:0.78rem; color:#94a3b8;">Huddle validates workout sets against Liam's shoulder status in real time.</p>

        <input class="input-field" id="sim-set" value="10x200m Butterfly with Hand Paddles">
        <button class="btn-lime" style="background:#fff; color:#111;" onclick="checkWorkoutSafety()">
          <span class="material-symbols-rounded">shield</span>
          Test Workout Safety
        </button>
        <div id="sim-result" style="font-size:0.82rem; font-weight:700; line-height:1.45;"></div>
      </div>
    </div>

    <!-- TAB 4: 2-WEEK NUTRITION & ELECTROLYTES -->
    <div id="tab-nutrition" class="view-viewport" style="display:none;">
      <!-- 2-Week Trend Digest -->
      <div class="trend-metric-card">
        <div style="font-size:0.75rem; font-weight:800; text-transform:uppercase; color:var(--lime);">Maya Lin (RD) • 2-Week Trend Digest</div>
        <h3 style="font-family:'Space Grotesk',sans-serif; font-size:1.2rem; font-weight:800;">Shoulder Inflammation vs. Kick Volume</h3>

        <div class="metric-grid">
          <div class="metric-box">
            <div class="m-title">Week 1 Avg Pain</div>
            <div class="m-val">6.2 / 10</div>
          </div>
          <div class="metric-box">
            <div class="m-title">Week 2 Avg Pain</div>
            <div class="m-val" style="color:#fff;">4.1 / 10 (↓)</div>
          </div>
          <div class="metric-box">
            <div class="m-title">External Rotation</div>
            <div class="m-val">+5 deg</div>
          </div>
          <div class="metric-box">
            <div class="m-title">Kick Base Total</div>
            <div class="m-val">32 km</div>
          </div>
        </div>
      </div>

      <!-- Active Prescribed Protocols -->
      <div class="form-card">
        <div style="font-family:'Space Grotesk',sans-serif; font-weight:800; font-size:1.1rem;">Modulate Fuel &amp; Intra-Workout Electrolytes</div>
        <p style="font-size:0.78rem; color:#94a3b8;">Adjusts electrolyte osmolarity and collagen timing based on 14-day shoulder progress.</p>

        <div>
          <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Targeted Anti-Inflammatory</label>
          <input class="input-field" id="n-anti" value="Curcumin 500mg + Omega-3 2,000mg EPA/DHA">
        </div>
        <div>
          <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Pool Bottle Intra-Workout Electrolytes</label>
          <input class="input-field" id="n-intra" value="750mg Sodium Citrate + 35g Cyclic Dextrin">
        </div>
        <div>
          <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Tendon Repair &amp; Evening Minerals</label>
          <input class="input-field" id="n-recov" value="15g Hydrolyzed Collagen + 400mg Magnesium">
        </div>

        <button class="btn-lime" onclick="saveNutritionProtocol()">
          <span class="material-symbols-rounded">science</span>
          Update Swimmer Fueling Plan
        </button>
        <div id="nutrition-status" style="font-size:0.8rem; font-weight:700; color:var(--lime);"></div>
      </div>
    </div>

    <!-- TAB 5: GEMINI AI COORDINATOR -->
    <div id="tab-agent" class="view-viewport" style="display:none; padding-bottom:5.8rem;">
      <div style="display:flex; align-items:center; gap:0.6rem; padding:0.6rem 0; border-bottom:1px solid rgba(255,255,255,0.08);">
        <div style="width:34px; height:34px; border-radius:50%; background:var(--lavender); display:flex; align-items:center; justify-content:center; color:#111;">
          <span class="material-symbols-rounded" style="font-size:18px;">neurology</span>
        </div>
        <div>
          <div style="font-weight:800; font-size:0.95rem;">Huddle Coordinator</div>
          <div style="font-size:0.7rem; color:var(--lime);">Gemini 2.5 Flash on Vertex AI</div>
        </div>
      </div>

      <div style="flex:1; display:flex; flex-direction:column; gap:0.8rem; overflow-y:auto; padding:0.8rem 0;" id="chat-stream">
        <div style="background:#202330; padding:0.85rem 1.1rem; border-radius:20px; font-size:0.88rem; line-height:1.45;">
          Hello! I'm monitoring Liam Vance's right shoulder impingement. I synchronize Coach Soren's pool sets, Dr. Elena's clinical restrictions, and Maya's intra-session fueling. How can I assist?
        </div>
      </div>

      <form id="agent-form" style="display:flex; gap:0.5rem; margin-top:auto;">
        <input class="input-field" id="agent-input" placeholder="Ask Huddle about Liam's shoulder..." autocomplete="off">
        <button type="submit" style="width:44px; height:44px; border-radius:50%; background:var(--lime); color:#111; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center;">
          <span class="material-symbols-rounded">arrow_upward</span>
        </button>
      </form>
    </div>

    <!-- Bottom Capsule Dock with 5 Flow Tabs -->
    <nav class="app-dock">
      <button class="dock-tab active" id="btn-overview" onclick="switchTab('overview')" title="Overview">
        <span class="material-symbols-rounded">home</span>
      </button>
      <button class="dock-tab" id="btn-checkin" onclick="switchTab('checkin')" title="Swimmer Checkin">
        <span class="material-symbols-rounded">bolt</span>
      </button>
      <button class="dock-tab" id="btn-coach" onclick="switchTab('coach')" title="Coach Workouts">
        <span class="material-symbols-rounded">pool</span>
      </button>
      <button class="dock-tab" id="btn-nutrition" onclick="switchTab('nutrition')" title="Nutrition & Electrolytes">
        <span class="material-symbols-rounded">nutrition</span>
      </button>
      <button class="dock-tab" id="btn-agent" onclick="switchTab('agent')" title="AI Coordinator">
        <span class="material-symbols-rounded">chat_bubble</span>
      </button>
    </nav>

  </div>

  <script>
    function switchTab(tabId) {
      const tabs = ['overview', 'checkin', 'coach', 'nutrition', 'agent'];
      tabs.forEach(t => {
        document.getElementById('tab-' + t).style.display = (t === tabId) ? 'flex' : 'none';
        document.getElementById('btn-' + t).className = (t === tabId) ? 'dock-tab active' : 'dock-tab';
      });
      if (tabId === 'coach') loadCoachSchedule();
    }

    async function loadCoachSchedule() {
      const res = await fetch('/api/status');
      const data = await res.json();
      const box = document.getElementById('coach-sched-box');
      box.innerHTML = '';
      const styles = ['purple', 'white', 'dark'];
      data.today_schedule.forEach((s, idx) => {
        const div = document.createElement('div');
        div.className = 'workout-item ' + styles[idx % styles.length];
        div.innerHTML = `
          <div>
            <div style="font-weight:800;">${s.title}</div>
            <div style="font-size:0.75rem; opacity:0.75;">${s.time} • ${s.overhead_risk || s.role}</div>
          </div>
          <span class="material-symbols-rounded" style="font-size:20px;">sports</span>
        `;
        box.appendChild(div);
      });
    }

    async function submitSwimmerCheckin() {
      const payload = {
        sleep_hours: parseFloat(document.getElementById('f-sleep').value),
        energy_score: parseInt(document.getElementById('f-energy').value),
        soreness_map: document.getElementById('f-soreness').value,
        overhead_mobility: document.getElementById('f-mobility').value
      };
      const res = await fetch('/api/checkin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      document.getElementById('disp-readiness').textContent = data.readiness_status.toUpperCase();
      document.getElementById('disp-mobility').textContent = payload.overhead_mobility;
      alert(`✓ Swimmer check-in submitted! Readiness set to ${data.readiness_status}. Coach Soren and Dr. Elena alerted.`);
    }

    async function checkWorkoutSafety() {
      const set = document.getElementById('sim-set').value;
      const res = await fetch('/api/check-conflicts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_title: set,
          day: 'Today',
          time_slot: '06:00 - 08:00',
          role: 'Head Swim Coach'
        })
      });
      const data = await res.json();
      const out = document.getElementById('sim-result');
      if (data.conflicts.length > 0) {
        out.style.color = '#ef4444';
        out.innerHTML = `⛔ <strong>BLOCKED:</strong> ${data.conflicts[0]}<br><span style="color:var(--lime);">💡 Recommended Adaptive Alternative: ${data.suggested_alternative}</span>`;
      } else {
        out.style.color = 'var(--lime)';
        out.innerHTML = `✓ Safe to schedule: Zero overhead torque detected.`;
      }
    }

    async function saveNutritionProtocol() {
      const payload = {
        anti_inflammatory: document.getElementById('n-anti').value,
        intra_workout_electrolytes: document.getElementById('n-intra').value,
        recovery_minerals: document.getElementById('n-recov').value,
        reasoning: "2-week shoulder trend shows lingering 4/10 pain with high kick-set glycogen demands"
      };
      const res = await fetch('/api/nutrition-modulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      document.getElementById('nutrition-status').textContent = '✓ Updated: Intra-workout electrolytes and anti-inflammatory protocol synchronized with swimmer view.';
    }

    document.getElementById('agent-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const inp = document.getElementById('agent-input');
      const text = inp.value.trim();
      if (!text) return;
      const stream = document.getElementById('chat-stream');
      const me = document.createElement('div');
      me.style.cssText = "background:var(--lime); color:#111; font-weight:600; padding:0.85rem 1.1rem; border-radius:20px; font-size:0.88rem; align-self:flex-end;";
      me.textContent = text;
      stream.appendChild(me);
      inp.value = '';
      stream.scrollTop = stream.scrollHeight;

      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      const bot = document.createElement('div');
      bot.style.cssText = "background:#202330; padding:0.85rem 1.1rem; border-radius:20px; font-size:0.88rem; line-height:1.45; align-self:flex-start;";
      bot.textContent = data.reply;
      stream.appendChild(bot);
      stream.scrollTop = stream.scrollHeight;
    });

    loadCoachSchedule();
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTMLResponse(content=HTML_CONTENT)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
