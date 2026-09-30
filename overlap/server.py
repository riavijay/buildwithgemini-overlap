"""FastAPI Backend Server for Overlap - The Hybrid Work Planner.
Exposes REST endpoints for weekly summaries, day details, planning, and Gemini chat.
"""
from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.agent import root_agent
from app.tools import (
    get_weekly_overlap_summary,
    update_day_plan,
    get_day_detail,
    toggle_favorite,
    calculate_commute_value
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

app = FastAPI(title="Overlap Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="overlap", session_service=session_service)

class PlanUpdateRequest(BaseModel):
    day: str
    status: str

class FavoriteToggleRequest(BaseModel):
    teammate_id: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "maya_session"

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    import os
    file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(file_path, "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/week-summary")
async def api_week_summary():
    return get_weekly_overlap_summary()

@app.get("/api/day/{day}")
async def api_day_detail(day: str):
    return get_day_detail(day)

@app.post("/api/plan")
async def api_update_plan(req: PlanUpdateRequest):
    return update_day_plan(day=req.day, status=req.status)

@app.post("/api/favorites/toggle")
async def api_toggle_favorite(req: FavoriteToggleRequest):
    return toggle_favorite(teammate_id=req.teammate_id)

@app.get("/api/commute-value/{day}")
async def api_commute_value(day: str):
    return calculate_commute_value(day=day)

@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    session = await session_service.get_session(
        app_name="overlap",
        user_id="u_maya",
        session_id=req.session_id
    )
    if not session:
        session = await session_service.create_session(
            app_name="overlap",
            user_id="u_maya",
            session_id=req.session_id
        )

    reply_text = ""
    async for event in runner.run_async(
        user_id="u_maya",
        session_id=req.session_id,
        new_message=types.Content(parts=[types.Part(text=req.message)])
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    reply_text += part.text

    return {"reply": reply_text or "Processed by Overlap."}

@app.get("/api/health")
async def api_health():
    return {"status": "ok", "app": "Overlap", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
