"""
tests/test_skillpath.py - Focused Unit & Integration Tests for SkillPath AI
Tests skill-gap math, quiz scoring, feasibility calculations, persistence, adaptive tips, and Flask endpoints.
"""

import pytest
import json
import os
import sqlite3

from app import app
import database
from assessment_data import CAREER_PATHS
from recommendation_engine import (
    analyze_skill_gaps,
    calculate_workload_feasibility,
    generate_adaptive_recommendations
)
from ai_mentor import generate_mentor_reply

@pytest.fixture
def client():
    """Configures test client with temporary or test session."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    with app.test_client() as client:
        yield client

# ==================== 1. Skill Gap Calculations ====================

def test_skill_gap_calculation_basic():
    """Verify deterministic skill gap computation without quiz data."""
    career = "Full-Stack Developer"
    self_skills = {
        "HTML & CSS": "Intermediate",       # Base score: 65
        "JavaScript Core": "Beginner",       # Base score: 40
        "Relational Databases & SQL": "None" # Base score: 15
    }
    gaps = analyze_skill_gaps(career, self_skills)
    assert len(gaps) > 0

    gap_dict = {g["skill_name"]: g for g in gaps}

    # HTML & CSS: target 85, estimated 65 => gap = 20 (Minor)
    html_gap = gap_dict["HTML & CSS"]
    assert html_gap["estimated_score"] == 65
    assert html_gap["gap_value"] == 20
    assert html_gap["gap_level"] == "Minor"

    # JavaScript: target 90, estimated 40 => gap = 50 (Critical)
    js_gap = gap_dict["JavaScript Core"]
    assert js_gap["estimated_score"] == 40
    assert js_gap["gap_value"] == 50
    assert js_gap["gap_level"] == "Critical"
    assert js_gap["priority"] == "High"

def test_skill_gap_blended_with_quiz():
    """Verify that quiz score reconciles with self-assessment properly."""
    career = "Full-Stack Developer"
    self_skills = {"JavaScript Core": "Beginner"} # Base: 40
    quiz_scores = {
        "JavaScript Core": {"correct": 2, "total": 2, "pct": 100}
    }
    gaps = analyze_skill_gaps(career, self_skills, quiz_scores)
    js_gap = next(g for g in gaps if g["skill_name"] == "JavaScript Core")

    # Formula: 0.45 * 40 + 0.55 * 100 = 18 + 55 = 73
    assert js_gap["estimated_score"] == 73
    # Target 90 - 73 = 17 => Minor gap
    assert js_gap["gap_level"] == "Minor"

# ==================== 2. Workload & Feasibility ====================

def test_feasibility_realistic():
    """A 170-hour curriculum at 2.5 hrs/day in 12 weeks should be Realistic."""
    total_hours = 170
    daily_hours = 2.5
    target_weeks = 12
    res = calculate_workload_feasibility(total_hours, daily_hours, target_weeks)
    assert res["status"] == "Realistic"
    assert res["needed_weeks"] <= target_weeks

def test_feasibility_unrealistic():
    """A 170-hour curriculum at 1 hr/day in 4 weeks should be Unrealistic."""
    total_hours = 170
    daily_hours = 1.0
    target_weeks = 4
    res = calculate_workload_feasibility(total_hours, daily_hours, target_weeks)
    assert res["status"] == "Unrealistic"
    assert res["needed_weeks"] > target_weeks * 1.35
    assert res["recommended_daily_hours"] > daily_hours

# ==================== 3. Adaptive Recommendations ====================

def test_adaptive_recommendations_weak_quiz():
    """Weak score in a category triggers diagnostic alert."""
    student = {"name": "Test Student", "daily_hours": 2, "career_goal": "Full-Stack Developer"}
    roadmap = {
        "overall_progress": 10,
        "feasibility_status": "Realistic",
        "stages": [
            {"title": "Frontend", "is_completed": 0, "tasks": [{"title": "HTML", "is_completed": 0}]}
        ]
    }
    quiz_data = {
        "category_scores": {
            "JavaScript Core": {"pct": 40, "correct": 1, "total": 2}
        }
    }
    recs = generate_adaptive_recommendations(student, roadmap, quiz_data)
    badges = [r["badge"] for r in recs]
    assert "Diagnostic Alert" in badges
    alert = next(r for r in recs if r["badge"] == "Diagnostic Alert")
    assert "JavaScript Core" in alert["title"]

# ==================== 4. SQLite Persistence & CRUD ====================

def test_database_init_and_seed():
    """Ensure database schema creates and demo student can be queried."""
    database.init_db()
    demo_id = database.seed_demo_student()
    assert demo_id is not None

    student = database.get_student(demo_id)
    assert student is not None
    assert "Alex Chen" in student["name"]

    roadmap = database.get_active_roadmap(demo_id)
    assert roadmap is not None
    assert len(roadmap["stages"]) > 0
    assert roadmap["total_tasks"] > 0
    assert roadmap["completed_tasks"] > 0

def test_task_toggle_persistence():
    """Ensure task toggling updates both task and stage state."""
    demo_id = database.seed_demo_student()
    roadmap = database.get_active_roadmap(demo_id)
    stage_2 = roadmap["stages"][1]
    uncompleted_task = next(t for t in stage_2["tasks"] if not t["is_completed"])

    # Toggle task to completed
    res = database.toggle_task(uncompleted_task["id"])
    assert res["is_completed"] is True

    # Re-fetch roadmap to ensure persisted in DB
    updated_roadmap = database.get_active_roadmap(demo_id)
    assert updated_roadmap["completed_tasks"] == roadmap["completed_tasks"] + 1

    # Toggle back to incomplete
    res2 = database.toggle_task(uncompleted_task["id"])
    assert res2["is_completed"] is False

# ==================== 5. AI Mentor Offline Fallback ====================

def test_mentor_fallback_mode():
    """Ensure AI mentor responds intelligently even with no API key."""
    os.environ["AI_PROVIDER"] = "none"
    context = {
        "name": "Jordan",
        "career_goal": "Full-Stack Developer",
        "active_stage_title": "Core JavaScript",
        "overall_progress": 25
    }
    reply = generate_mentor_reply("Can you give me a hint on my project?", context)
    assert reply["is_fallback"] == 1
    assert "SkillPath Built-in Mentor" in reply["content"]
    assert "hint" in reply["content"].lower() or "break it" in reply["content"].lower()

# ==================== 6. Flask Web Routes ====================

def test_homepage_route(client):
    """Test landing page renders with 200 OK."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"SkillPath" in response.data
    assert b"Build My Learning Path" in response.data

def test_demo_login_route(client):
    """Test demo login route sets session and redirects to dashboard."""
    response = client.get("/demo", follow_redirects=True)
    assert response.status_code == 200
    assert b"Alex Chen" in response.data
    assert b"Overall Roadmap Completion" in response.data

def test_api_mentor_chat(client):
    """Test mentor chat endpoint returns valid JSON with student session."""
    client.get("/demo") # establish session
    response = client.post("/api/mentor/chat", json={"message": "Explain REST APIs simply"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert "reply" in data
    assert len(data["reply"]) > 20
