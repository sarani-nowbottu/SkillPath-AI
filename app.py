"""
app.py - Main Flask Application for SkillPath AI
Personalized Career Learning Path Generator for College Students & Beginners
"""

import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

import database
from assessment_data import CAREER_PATHS, ALL_SKILLS_LIST
from recommendation_engine import (
    analyze_skill_gaps,
    calculate_workload_feasibility,
    generate_adaptive_recommendations
)
from ai_mentor import generate_mentor_reply

# Load environment configuration
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "skillpath-default-secret-key-2026")

# Ensure database is initialized on startup
with app.app_context():
    database.init_db()

def get_current_student():
    """Helper to fetch currently logged-in student from session."""
    student_id = session.get("student_id")
    if student_id:
        student = database.get_student(student_id)
        if student:
            return student
    return None

# ==================== WEB ROUTES ====================

@app.route("/")
def index():
    """Feature A: Professional Landing Page."""
    student = get_current_student()
    preview_career = CAREER_PATHS["Full-Stack Developer"]
    return render_template(
        "index.html",
        student=student,
        careers=CAREER_PATHS,
        preview_career=preview_career
    )

@app.route("/demo")
def demo_login():
    """One-click instant login as seeded demo student 'Alex Chen'."""
    demo_id = database.seed_demo_student()
    session["student_id"] = demo_id
    flash("Switched to Demo Student profile ('Alex Chen - Full-Stack Developer'). Explore all features freely!", "success")
    return redirect(url_for("dashboard"))

@app.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    """Feature B: Student Profile Setup & Career Goal Selection."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        education_level = request.form.get("education_level", "").strip()
        career_goal = request.form.get("career_goal", "").strip()
        custom_goal = request.form.get("custom_goal", "").strip()
        learning_style = request.form.get("learning_style", "Project-first").strip()

        try:
            daily_hours = float(request.form.get("daily_hours", 2.0))
            if daily_hours <= 0 or daily_hours > 16:
                raise ValueError()
        except ValueError:
            flash("Please enter a realistic daily study commitment between 0.5 and 12 hours.", "error")
            return redirect(url_for("onboarding"))

        try:
            target_weeks = int(request.form.get("target_weeks", 12))
            if target_weeks < 1 or target_weeks > 52:
                raise ValueError()
        except ValueError:
            flash("Please enter a target preparation timeframe between 1 and 52 weeks.", "error")
            return redirect(url_for("onboarding"))

        if not name or not education_level or not career_goal:
            flash("Please complete your name, education level, and target career goal.", "error")
            return redirect(url_for("onboarding"))

        if career_goal == "Custom" and custom_goal:
            career_goal = custom_goal

        # Gather self-assessed skills
        self_skills = {}
        for key, val in request.form.items():
            if key.startswith("skill_level_"):
                skill_name = key.replace("skill_level_", "")
                self_skills[skill_name] = val

        # Save student in database
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (name, education_level, career_goal, custom_goal, daily_hours, target_weeks, learning_style)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, education_level, career_goal, custom_goal, daily_hours, target_weeks, learning_style))
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()

        session["student_id"] = student_id
        session["self_skills"] = self_skills

        # Pre-compute preliminary skill gaps
        gaps = analyze_skill_gaps(career_goal, self_skills)
        conn = database.get_db_connection()
        cursor = conn.cursor()
        for g in gaps:
            cursor.execute("""
                INSERT INTO student_skills (student_id, skill_name, self_level, estimated_score, target_score, gap_level, priority, why_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, g["skill_name"], g["self_level"], g["estimated_score"], g["target_score"], g["gap_level"], g["priority"], g["why_text"]))
        conn.commit()
        conn.close()

        flash(f"Welcome, {name}! Let's take a quick 4-minute diagnostic quiz to personalize your path.", "info")
        return redirect(url_for("assessment"))

    student = get_current_student()
    return render_template(
        "onboarding.html",
        student=student,
        careers=CAREER_PATHS,
        all_skills=ALL_SKILLS_LIST
    )

@app.route("/assessment")
def assessment():
    """Feature C: Skill Assessment Quiz."""
    student = get_current_student()
    if not student:
        flash("Please set up your student profile first.", "info")
        return redirect(url_for("onboarding"))

    career_key = student["career_goal"]
    career_info = CAREER_PATHS.get(career_key, CAREER_PATHS["Full-Stack Developer"])
    questions = career_info.get("quiz", [])

    latest_quiz = database.get_latest_quiz(student["id"])

    return render_template(
        "assessment.html",
        student=student,
        career_key=career_key,
        questions=questions,
        latest_quiz=latest_quiz
    )

@app.route("/api/assessment/submit", methods=["POST"])
def submit_assessment():
    """Processes diagnostic quiz answers, computes scores, and generates roadmap."""
    student = get_current_student()
    if not student:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    answers = data.get("answers", {})

    career_key = student["career_goal"]
    career_info = CAREER_PATHS.get(career_key, CAREER_PATHS["Full-Stack Developer"])
    questions = career_info.get("quiz", [])

    total_q = len(questions)
    correct_count = 0
    category_breakdown = {}

    for q in questions:
        cat = q["category"]
        if cat not in category_breakdown:
            category_breakdown[cat] = {"correct": 0, "total": 0, "pct": 0}
        category_breakdown[cat]["total"] += 1

        selected_idx = answers.get(q["id"])
        if selected_idx is not None and int(selected_idx) == q["correct_index"]:
            correct_count += 1
            category_breakdown[cat]["correct"] += 1

    for cat in category_breakdown:
        tot = category_breakdown[cat]["total"]
        cor = category_breakdown[cat]["correct"]
        category_breakdown[cat]["pct"] = round((cor / tot) * 100) if tot > 0 else 0

    pct_overall = round((correct_count / total_q) * 100, 1) if total_q > 0 else 0

    # Save Quiz Attempt in DB
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_attempts (student_id, career_goal, score, total_questions, percentage, category_scores_json, answers_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student["id"], career_key, correct_count, total_q, pct_overall, json.dumps(category_breakdown), json.dumps(answers)))

    # Re-calculate skill gaps with quiz evidence
    self_skills = session.get("self_skills", {})
    updated_gaps = analyze_skill_gaps(career_key, self_skills, category_breakdown)

    # Refresh student_skills table
    cursor.execute("DELETE FROM student_skills WHERE student_id = ?", (student["id"],))
    for g in updated_gaps:
        cursor.execute("""
            INSERT INTO student_skills (student_id, skill_name, self_level, estimated_score, target_score, gap_level, priority, why_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student["id"], g["skill_name"], g["self_level"], g["estimated_score"], g["target_score"], g["gap_level"], g["priority"], g["why_text"]))

    # Generate Personalized Roadmap
    total_hours = sum(s["duration_hours"] for s in career_info["stages"])
    feasibility = calculate_workload_feasibility(total_hours, student["daily_hours"], student["target_weeks"])

    # Deactivate any previous roadmaps
    cursor.execute("UPDATE roadmaps SET status = 'archived' WHERE student_id = ?", (student["id"],))

    cursor.execute("""
        INSERT INTO roadmaps (student_id, career_goal, total_estimated_hours, total_estimated_weeks, feasibility_status, feasibility_note)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student["id"], career_key, total_hours, feasibility["needed_weeks"], feasibility["status"], feasibility["note"]))
    roadmap_id = cursor.lastrowid

    # Create Roadmap Stages and Tasks
    for stage_idx, stage in enumerate(career_info["stages"]):
        cursor.execute("""
            INSERT INTO roadmap_stages (roadmap_id, stage_order, title, description, estimated_hours, is_completed, mini_project_json, topics_json, resources_json)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?)
        """, (
            roadmap_id,
            stage["order"],
            stage["title"],
            stage["description"],
            stage["duration_hours"],
            json.dumps(stage["mini_project"]),
            json.dumps(stage["topics"]),
            json.dumps(stage["resources"])
        ))
        stage_id = cursor.lastrowid

        for task_idx, topic in enumerate(stage["topics"]):
            cursor.execute("""
                INSERT INTO stage_tasks (stage_id, task_order, title, is_completed)
                VALUES (?, ?, ?, 0)
            """, (stage_id, task_idx + 1, f"Study & Implement: {topic}"))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "score": correct_count,
        "total": total_q,
        "percentage": pct_overall,
        "categories": category_breakdown,
        "redirect_url": url_for("gap_analysis")
    })

@app.route("/gap-analysis")
def gap_analysis():
    """Feature D: Skill-Gap Analysis Report & Industry Target Comparison."""
    student = get_current_student()
    if not student:
        flash("Please set up your profile first.", "info")
        return redirect(url_for("onboarding"))

    skills = database.get_student_skills(student["id"])
    latest_quiz = database.get_latest_quiz(student["id"])
    roadmap = database.get_active_roadmap(student["id"])

    # If no roadmap exists yet, calculate preliminary feasibility
    career_info = CAREER_PATHS.get(student["career_goal"], CAREER_PATHS["Full-Stack Developer"])
    total_hours = sum(s["duration_hours"] for s in career_info["stages"])
    feasibility = calculate_workload_feasibility(total_hours, student["daily_hours"], student["target_weeks"])

    return render_template(
        "gap_analysis.html",
        student=student,
        skills=skills,
        latest_quiz=latest_quiz,
        roadmap=roadmap,
        feasibility=feasibility
    )

@app.route("/dashboard")
@app.route("/roadmap")
def dashboard():
    """Features E, G, H, I, K: Dynamic Learning Dashboard & Interactive Roadmap."""
    student = get_current_student()
    if not student:
        # Prompt user to onboard or explore demo
        return redirect(url_for("onboarding"))

    roadmap = database.get_active_roadmap(student["id"])
    skills = database.get_student_skills(student["id"])
    latest_quiz = database.get_latest_quiz(student["id"])

    # If no active roadmap, generate one now
    if not roadmap:
        career_key = student["career_goal"]
        career_info = CAREER_PATHS.get(career_key, CAREER_PATHS["Full-Stack Developer"])
        total_hours = sum(s["duration_hours"] for s in career_info["stages"])
        feasibility = calculate_workload_feasibility(total_hours, student["daily_hours"], student["target_weeks"])

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO roadmaps (student_id, career_goal, total_estimated_hours, total_estimated_weeks, feasibility_status, feasibility_note)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student["id"], career_key, total_hours, feasibility["needed_weeks"], feasibility["status"], feasibility["note"]))
        roadmap_id = cursor.lastrowid

        for stage in career_info["stages"]:
            cursor.execute("""
                INSERT INTO roadmap_stages (roadmap_id, stage_order, title, description, estimated_hours, is_completed, mini_project_json, topics_json, resources_json)
                VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?)
            """, (
                roadmap_id,
                stage["order"],
                stage["title"],
                stage["description"],
                stage["duration_hours"],
                json.dumps(stage["mini_project"]),
                json.dumps(stage["topics"]),
                json.dumps(stage["resources"])
            ))
            stage_id = cursor.lastrowid
            for task_idx, topic in enumerate(stage["topics"]):
                cursor.execute("""
                    INSERT INTO stage_tasks (stage_id, task_order, title, is_completed)
                    VALUES (?, ?, ?, 0)
                """, (stage_id, task_idx + 1, f"Study & Implement: {topic}"))
        conn.commit()
        conn.close()
        roadmap = database.get_active_roadmap(student["id"])

    # Feature H: Adaptive Recommendations
    recommendations = generate_adaptive_recommendations(student, roadmap, latest_quiz, skills)

    # Chat history for mentor drawer
    chat_history = database.get_chat_history(student["id"])

    return render_template(
        "roadmap.html",
        student=student,
        roadmap=roadmap,
        skills=skills,
        latest_quiz=latest_quiz,
        recommendations=recommendations,
        chat_history=chat_history
    )

@app.route("/api/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    """Toggles checklist task completion and returns updated overall progress."""
    student = get_current_student()
    if not student:
        return jsonify({"error": "Unauthorized"}), 401

    result = database.toggle_task(task_id)
    if not result:
        return jsonify({"error": "Task not found"}), 404

    # Recalculate roadmap stats
    roadmap = database.get_active_roadmap(student["id"])
    return jsonify({
        "success": True,
        "task_id": task_id,
        "is_completed": result["is_completed"],
        "stage_id": result["stage_id"],
        "overall_progress": roadmap["overall_progress"] if roadmap else 0,
        "completed_tasks": roadmap["completed_tasks"] if roadmap else 0,
        "total_tasks": roadmap["total_tasks"] if roadmap else 0
    })

@app.route("/api/mentor/chat", methods=["POST"])
def mentor_chat():
    """Feature F: Conversational AI Mentor endpoint with robust offline fallback."""
    student = get_current_student()
    if not student:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    user_query = data.get("message", "").strip()
    if not user_query:
        return jsonify({"error": "Empty message"}), 400

    # Save user message
    database.save_chat_message(student["id"], "user", user_query)

    # Gather rich student context
    roadmap = database.get_active_roadmap(student["id"])
    latest_quiz = database.get_latest_quiz(student["id"])
    
    active_stage_title = "Fundamentals"
    overall_progress = 0
    if roadmap and roadmap.get("stages"):
        overall_progress = roadmap.get("overall_progress", 0)
        for s in roadmap["stages"]:
            if not s.get("is_completed"):
                active_stage_title = s.get("title")
                break

    student_context = {
        "name": student["name"],
        "education_level": student["education_level"],
        "career_goal": student["career_goal"],
        "daily_hours": student["daily_hours"],
        "active_stage_title": active_stage_title,
        "overall_progress": overall_progress,
        "quiz_score": f"{latest_quiz['percentage']}%" if latest_quiz else "Not taken"
    }

    chat_history = database.get_chat_history(student["id"])
    reply_obj = generate_mentor_reply(user_query, student_context, chat_history)

    # Save assistant message
    database.save_chat_message(
        student["id"],
        "assistant",
        reply_obj["content"],
        is_fallback=reply_obj.get("is_fallback", 0)
    )

    return jsonify({
        "success": True,
        "reply": reply_obj["content"],
        "is_fallback": reply_obj.get("is_fallback", 0),
        "provider": reply_obj.get("provider", "rule_based_fallback")
    })

@app.route("/profile", methods=["GET", "POST"])
def profile():
    """Student Profile Management & Schedule Recalibration."""
    student = get_current_student()
    if not student:
        return redirect(url_for("onboarding"))

    if request.method == "POST":
        try:
            daily_hours = float(request.form.get("daily_hours", student["daily_hours"]))
            target_weeks = int(request.form.get("target_weeks", student["target_weeks"]))
            learning_style = request.form.get("learning_style", student["learning_style"])

            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students 
                SET daily_hours = ?, target_weeks = ?, learning_style = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (daily_hours, target_weeks, learning_style, student["id"]))

            # Recalculate roadmap feasibility note
            roadmap = database.get_active_roadmap(student["id"])
            if roadmap:
                feasibility = calculate_workload_feasibility(roadmap["total_estimated_hours"], daily_hours, target_weeks)
                cursor.execute("""
                    UPDATE roadmaps 
                    SET total_estimated_weeks = ?, feasibility_status = ?, feasibility_note = ?
                    WHERE id = ?
                """, (feasibility["needed_weeks"], feasibility["status"], feasibility["note"], roadmap["id"]))

            conn.commit()
            conn.close()
            flash("Study profile updated and roadmap schedule recalibrated successfully!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Error updating profile: {str(e)}", "error")

    roadmap = database.get_active_roadmap(student["id"])
    return render_template("profile.html", student=student, roadmap=roadmap)

@app.route("/api/reset", methods=["POST"])
def reset_progress():
    """Resets student roadmap and assessments with confirmation."""
    student = get_current_student()
    if not student:
        return jsonify({"error": "Unauthorized"}), 401

    database.reset_student(student["id"])
    flash("Your learning path has been reset. You can now start fresh!", "info")
    return jsonify({"success": True, "redirect_url": url_for("onboarding")})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", code=404, message="The requested page could not be found."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500, message="An internal server error occurred."), 500

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    print(f"Starting SkillPath AI on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
