"""
database.py - SQLite Database Schema & Access Layer for SkillPath AI
Provides parameterized queries, relational integrity, demo seeding, and progress tracking.
"""

import sqlite3
import json
import os
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "skillpath.db")

def get_db_connection():
    """Returns a SQLite connection with foreign keys enabled and Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initializes database schema with required tables and indexes."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        education_level TEXT NOT NULL,
        career_goal TEXT NOT NULL,
        custom_goal TEXT,
        daily_hours REAL NOT NULL DEFAULT 2.0,
        target_weeks INTEGER NOT NULL DEFAULT 12,
        learning_style TEXT NOT NULL DEFAULT 'Project-first',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS student_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        skill_name TEXT NOT NULL,
        self_level TEXT NOT NULL DEFAULT 'Beginner',
        estimated_score INTEGER NOT NULL DEFAULT 40,
        target_score INTEGER NOT NULL DEFAULT 85,
        gap_level TEXT NOT NULL DEFAULT 'Moderate',
        priority TEXT NOT NULL DEFAULT 'Medium',
        why_text TEXT,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        career_goal TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        percentage REAL NOT NULL,
        category_scores_json TEXT NOT NULL,
        answers_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        career_goal TEXT NOT NULL,
        total_estimated_hours REAL NOT NULL,
        total_estimated_weeks REAL NOT NULL,
        feasibility_status TEXT NOT NULL DEFAULT 'Realistic',
        feasibility_note TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS roadmap_stages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roadmap_id INTEGER NOT NULL,
        stage_order INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        estimated_hours REAL NOT NULL,
        is_completed INTEGER DEFAULT 0,
        mini_project_json TEXT,
        topics_json TEXT,
        resources_json TEXT,
        FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS stage_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stage_id INTEGER NOT NULL,
        task_order INTEGER NOT NULL,
        title TEXT NOT NULL,
        is_completed INTEGER DEFAULT 0,
        completed_at TIMESTAMP,
        FOREIGN KEY (stage_id) REFERENCES roadmap_stages(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS mentor_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        is_fallback INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_skills_student ON student_skills(student_id);
    CREATE INDEX IF NOT EXISTS idx_roadmaps_student ON roadmaps(student_id);
    CREATE INDEX IF NOT EXISTS idx_stages_roadmap ON roadmap_stages(roadmap_id);
    CREATE INDEX IF NOT EXISTS idx_tasks_stage ON stage_tasks(stage_id);
    CREATE INDEX IF NOT EXISTS idx_quiz_student ON quiz_attempts(student_id);
    """)

    conn.commit()
    conn.close()

def seed_demo_student():
    """
    Creates or resets a realistic Demo Student profile ('Alex Chen')
    with an active Full-Stack roadmap, completed tasks, quiz attempt, and chat history.
    Allows reviewers to explore the entire application immediately.
    """
    from assessment_data import CAREER_PATHS
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if demo student exists
    cursor.execute("SELECT id FROM students WHERE name = 'Alex Chen (Demo)'")
    existing = cursor.fetchone()
    if existing:
        demo_id = existing['id']
        cursor.execute("DELETE FROM students WHERE id = ?", (demo_id,))
        conn.commit()

    # Insert Demo Student
    cursor.execute("""
        INSERT INTO students (name, education_level, career_goal, daily_hours, target_weeks, learning_style)
        VALUES ('Alex Chen (Demo)', '2nd Year B.Tech (CSE)', 'Full-Stack Developer', 2.5, 12, 'Project-first')
    """)
    demo_id = cursor.lastrowid

    # Insert Skills & Gaps
    skills = [
        ("HTML & CSS", "Intermediate", 70, 85, "Minor", "High", "Essential for semantic web structure, accessible layouts, and modern responsive UI."),
        ("JavaScript Core", "Beginner", 45, 90, "Critical", "High", "The programming language of the modern web, powering client interactivity and server runtimes."),
        ("Frontend Frameworks (React/Vue)", "None", 20, 75, "Critical", "Medium", "Industry standard for building maintainable, component-driven single-page applications."),
        ("Backend APIs & Node.js/Python", "Beginner", 40, 80, "Moderate", "High", "Powers business logic, authentication, and secure client-server communication."),
        ("Relational Databases & SQL", "Intermediate", 65, 80, "Minor", "High", "Critical for persistent data storage, schema design, and querying structured records."),
        ("Git & Collaboration", "Intermediate", 60, 75, "Minor", "Medium", "Foundational for source control, team collaboration, and CI/CD pipelines."),
        ("Deployment & Web Security", "Beginner", 30, 65, "Moderate", "Low", "Ensures your applications run securely in production with HTTPS, CORS, and hosting.")
    ]
    for name, s_lvl, est, tgt, gap, pri, why in skills:
        cursor.execute("""
            INSERT INTO student_skills (student_id, skill_name, self_level, estimated_score, target_score, gap_level, priority, why_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (demo_id, name, s_lvl, est, tgt, gap, pri, why))

    # Insert Quiz Attempt
    category_scores = {
        "HTML & CSS": {"correct": 1, "total": 1, "pct": 100},
        "JavaScript Core": {"correct": 1, "total": 2, "pct": 50},
        "Backend APIs & Node.js/Python": {"correct": 0, "total": 1, "pct": 0},
        "Relational Databases & SQL": {"correct": 1, "total": 1, "pct": 100},
        "Git & Collaboration": {"correct": 1, "total": 1, "pct": 100}
    }
    cursor.execute("""
        INSERT INTO quiz_attempts (student_id, career_goal, score, total_questions, percentage, category_scores_json)
        VALUES (?, 'Full-Stack Developer', 4, 6, 66.7, ?)
    """, (demo_id, json.dumps(category_scores)))

    # Insert Roadmap
    career_info = CAREER_PATHS["Full-Stack Developer"]
    total_hours = sum(s["duration_hours"] for s in career_info["stages"])
    total_weeks = round(total_hours / (2.5 * 7), 1)

    cursor.execute("""
        INSERT INTO roadmaps (student_id, career_goal, total_estimated_hours, total_estimated_weeks, feasibility_status, feasibility_note)
        VALUES (?, 'Full-Stack Developer', ?, ?, 'Realistic', 'At 2.5 hours/day (~17.5 hrs/week), you can comfortably complete this 170-hour roadmap in ~10 weeks, well within your 12-week goal!')
    """, (demo_id, total_hours, total_weeks))
    roadmap_id = cursor.lastrowid

    # Insert Stages and Tasks
    for stage_idx, stage in enumerate(career_info["stages"]):
        # First stage completed in demo, second in progress
        is_stage_done = 1 if stage_idx == 0 else 0
        cursor.execute("""
            INSERT INTO roadmap_stages (roadmap_id, stage_order, title, description, estimated_hours, is_completed, mini_project_json, topics_json, resources_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            roadmap_id,
            stage["order"],
            stage["title"],
            stage["description"],
            stage["duration_hours"],
            is_stage_done,
            json.dumps(stage["mini_project"]),
            json.dumps(stage["topics"]),
            json.dumps(stage["resources"])
        ))
        stage_id = cursor.lastrowid

        for task_idx, topic in enumerate(stage["topics"]):
            # If stage 1, all tasks complete; if stage 2, first task complete
            task_done = 1 if (stage_idx == 0 or (stage_idx == 1 and task_idx == 0)) else 0
            cursor.execute("""
                INSERT INTO stage_tasks (stage_id, task_order, title, is_completed)
                VALUES (?, ?, ?, ?)
            """, (stage_id, task_idx + 1, f"Study & Implement: {topic}", task_done))

    # Insert Seeded Mentor Chat
    cursor.execute("""
        INSERT INTO mentor_messages (student_id, role, content, is_fallback)
        VALUES 
        (?, 'user', 'Hi Mentor! Where should I focus my learning first based on my assessment?', 1),
        (?, 'assistant', 'Hello Alex! Based on your diagnostic assessment and skill-gap report, you scored 100% on HTML/CSS and SQL fundamentals, which is fantastic! However, your JavaScript score was 50% and Backend APIs need work. \n\nMy strong recommendation is Stage 2: Core JavaScript & DOM Manipulation. Before rushing into React or Node.js, solidify asynchronous JavaScript, Promises, and DOM events. This will make your backend and full-stack journey 3x faster!', 1)
    """, (demo_id, demo_id))

    conn.commit()
    conn.close()
    return demo_id

def get_student(student_id):
    """Retrieves student by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_latest_quiz(student_id):
    """Retrieves latest quiz attempt for a student."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_attempts WHERE student_id = ? ORDER BY id DESC LIMIT 1", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        data = dict(row)
        data["category_scores"] = json.loads(data["category_scores_json"])
        return data
    return None

def get_student_skills(student_id):
    """Retrieves all skill gap rows for a student."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_skills WHERE student_id = ? ORDER BY priority DESC, gap_level DESC", (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_active_roadmap(student_id):
    """Retrieves current active roadmap along with stages and task completion stats."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM roadmaps WHERE student_id = ? AND status = 'active' ORDER BY id DESC LIMIT 1", (student_id,))
    rm = cursor.fetchone()
    if not rm:
        conn.close()
        return None

    roadmap_data = dict(rm)
    cursor.execute("SELECT * FROM roadmap_stages WHERE roadmap_id = ? ORDER BY stage_order ASC", (rm["id"],))
    stages = cursor.fetchall()

    total_tasks = 0
    completed_tasks = 0
    stage_list = []

    for stage_row in stages:
        s = dict(stage_row)
        s["mini_project"] = json.loads(s["mini_project_json"]) if s["mini_project_json"] else None
        s["topics"] = json.loads(s["topics_json"]) if s["topics_json"] else []
        s["resources"] = json.loads(s["resources_json"]) if s["resources_json"] else []

        # Get tasks for this stage
        cursor.execute("SELECT * FROM stage_tasks WHERE stage_id = ? ORDER BY task_order ASC", (s["id"],))
        tasks = [dict(t) for t in cursor.fetchall()]
        s["tasks"] = tasks

        s_total = len(tasks)
        s_done = sum(1 for t in tasks if t["is_completed"])
        s["tasks_total"] = s_total
        s["tasks_completed"] = s_done
        s["progress_pct"] = round((s_done / s_total * 100), 1) if s_total > 0 else 0

        # Update stage is_completed status if all tasks done
        if s_total > 0 and s_done == s_total and not s["is_completed"]:
            cursor.execute("UPDATE roadmap_stages SET is_completed = 1 WHERE id = ?", (s["id"],))
            s["is_completed"] = 1
        elif s_total > 0 and s_done < s_total and s["is_completed"]:
            cursor.execute("UPDATE roadmap_stages SET is_completed = 0 WHERE id = ?", (s["id"],))
            s["is_completed"] = 0

        total_tasks += s_total
        completed_tasks += s_done
        stage_list.append(s)

    conn.commit()
    conn.close()

    roadmap_data["stages"] = stage_list
    roadmap_data["total_tasks"] = total_tasks
    roadmap_data["completed_tasks"] = completed_tasks
    roadmap_data["overall_progress"] = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
    return roadmap_data

def toggle_task(task_id):
    """Toggles task completed status and updates timestamp."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_completed, stage_id FROM stage_tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if not task:
        conn.close()
        return None

    new_state = 0 if task["is_completed"] else 1
    completed_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S") if new_state else None

    cursor.execute("UPDATE stage_tasks SET is_completed = ?, completed_at = ? WHERE id = ?", (new_state, completed_at, task_id))

    # Check if all tasks in stage are completed to update stage is_completed
    stage_id = task["stage_id"]
    cursor.execute("SELECT COUNT(*) as total, SUM(is_completed) as done FROM stage_tasks WHERE stage_id = ?", (stage_id,))
    stats = cursor.fetchone()
    if stats["total"] > 0 and stats["total"] == stats["done"]:
        cursor.execute("UPDATE roadmap_stages SET is_completed = 1 WHERE id = ?", (stage_id,))
    else:
        cursor.execute("UPDATE roadmap_stages SET is_completed = 0 WHERE id = ?", (stage_id,))

    conn.commit()
    conn.close()
    return {"task_id": task_id, "is_completed": bool(new_state), "stage_id": stage_id}

def save_chat_message(student_id, role, content, is_fallback=0):
    """Saves a mentor conversation turn."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mentor_messages (student_id, role, content, is_fallback)
        VALUES (?, ?, ?, ?)
    """, (student_id, role, content, is_fallback))
    conn.commit()
    conn.close()

def get_chat_history(student_id, limit=20):
    """Retrieves recent mentor messages for a student."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM mentor_messages WHERE student_id = ? ORDER BY id ASC LIMIT ?
    """, (student_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def reset_student(student_id):
    """Safely resets roadmap and assessments for a student while keeping profile."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM roadmaps WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM quiz_attempts WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM student_skills WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM mentor_messages WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
