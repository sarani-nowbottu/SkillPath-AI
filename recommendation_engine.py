"""
recommendation_engine.py - Deterministic Skill-Gap Analysis, Workload Feasibility & Adaptive Recommendations
Implements transparent logic without relying on black-box LLMs for calculations.
"""

import math
from assessment_data import CAREER_PATHS

# Baseline proficiency scores corresponding to self-assessment
SELF_LEVEL_MAP = {
    "None": 15,
    "Beginner": 40,
    "Intermediate": 65,
    "Advanced": 85
}

def analyze_skill_gaps(career_goal, student_self_skills=None, quiz_category_scores=None):
    """
    Computes deterministic skill gaps by comparing student self-assessment and
    quiz category scores against the benchmark target profile for the career goal.
    
    Returns a list of skill gap dictionaries sorted by urgency.
    """
    if student_self_skills is None:
        student_self_skills = {}
    if quiz_category_scores is None:
        quiz_category_scores = {}

    career_data = CAREER_PATHS.get(career_goal, CAREER_PATHS["Full-Stack Developer"])
    benchmarks = career_data["benchmark_skills"]

    gap_results = []

    for b in benchmarks:
        skill_name = b["skill"]
        target = b["target"]
        base_priority = b["priority"]
        why_text = b["why"]

        # 1. Determine self-level score
        self_level = student_self_skills.get(skill_name, "Beginner")
        base_score = SELF_LEVEL_MAP.get(self_level, 40)

        # 2. Reconcile with quiz results if tested
        # Check if skill name matches or is contained in quiz categories
        matched_quiz_pct = None
        for cat_name, cat_data in quiz_category_scores.items():
            if cat_name.lower() in skill_name.lower() or skill_name.lower() in cat_name.lower():
                matched_quiz_pct = cat_data.get("pct")
                break

        if matched_quiz_pct is not None:
            # 50% weight to self-assessment + 50% weight to diagnostic test
            estimated_score = round((0.45 * base_score) + (0.55 * matched_quiz_pct))
        else:
            estimated_score = base_score

        # Bound between 10 and 95
        estimated_score = max(10, min(95, estimated_score))

        # 3. Compute Gap
        gap_value = target - estimated_score

        if gap_value <= 5:
            gap_level = "None"
            priority = "Completed" if estimated_score >= target else "Low"
        elif gap_value <= 20:
            gap_level = "Minor"
            priority = "Medium" if base_priority == "High" else "Low"
        elif gap_value <= 40:
            gap_level = "Moderate"
            priority = base_priority
        else:
            gap_level = "Critical"
            priority = "High"

        gap_results.append({
            "skill_name": skill_name,
            "self_level": self_level,
            "estimated_score": estimated_score,
            "target_score": target,
            "gap_value": gap_value,
            "gap_level": gap_level,
            "priority": priority,
            "why_text": why_text
        })

    # Sort: Critical & High Priority first
    priority_order = {"High": 1, "Medium": 2, "Low": 3, "Completed": 4}
    gap_order = {"Critical": 1, "Moderate": 2, "Minor": 3, "None": 4}
    gap_results.sort(key=lambda x: (priority_order.get(x["priority"], 3), gap_order.get(x["gap_level"], 3)))

    return gap_results

def calculate_workload_feasibility(total_hours, daily_hours, target_weeks):
    """
    Reconciles total required curriculum hours against student's available daily hours
    and target deadline. Recommends adjustments if the schedule is unrealistic.
    """
    daily_hours = max(0.5, float(daily_hours))
    target_weeks = max(1, int(target_weeks))
    weekly_hours = daily_hours * 7

    needed_weeks = round(total_hours / weekly_hours, 1)
    available_total_hours = round(weekly_hours * target_weeks, 1)

    if needed_weeks <= target_weeks:
        status = "Realistic"
        note = (
            f"At {daily_hours} hrs/day (~{round(weekly_hours, 1)} hrs/week), you can comfortably complete "
            f"this {round(total_hours)}h roadmap in ~{math.ceil(needed_weeks)} weeks, well within your {target_weeks}-week target."
        )
        recommended_daily_hours = daily_hours
    elif needed_weeks <= (target_weeks * 1.35):
        status = "Challenging"
        rec_daily = round(total_hours / (target_weeks * 7), 1)
        note = (
            f"At {daily_hours} hrs/day, this roadmap requires ~{math.ceil(needed_weeks)} weeks. "
            f"To finish in your {target_weeks}-week goal, increase study time slightly to ~{rec_daily} hrs/day, "
            f"or prioritize the core high-priority stages."
        )
        recommended_daily_hours = rec_daily
    else:
        status = "Unrealistic"
        rec_daily = round(total_hours / (target_weeks * 7), 1)
        note = (
            f"Your target of {target_weeks} weeks allows only {available_total_hours}h of study time, "
            f"but this thorough roadmap requires {round(total_hours)}h. "
            f"We recommend extending your timeframe to {math.ceil(needed_weeks)} weeks (at {daily_hours} hrs/day) "
            f"to prevent burnout and ensure deep mastery."
        )
        recommended_daily_hours = rec_daily

    return {
        "status": status,
        "total_hours": total_hours,
        "weekly_hours": round(weekly_hours, 1),
        "target_weeks": target_weeks,
        "needed_weeks": math.ceil(needed_weeks),
        "note": note,
        "recommended_daily_hours": recommended_daily_hours
    }

def generate_adaptive_recommendations(student, roadmap_data, quiz_data=None, skills=None):
    """
    Generates dynamic, transparent recommendations based on student's current progress,
    assessment results, and roadmap pace.
    """
    recommendations = []

    if not roadmap_data or not roadmap_data.get("stages"):
        return recommendations

    stages = roadmap_data["stages"]
    overall_pct = roadmap_data.get("overall_progress", 0)

    # 1. Analyze Quiz Results for Weak Points
    if quiz_data and quiz_data.get("category_scores"):
        cat_scores = quiz_data["category_scores"]
        for cat, stats in cat_scores.items():
            if stats.get("pct", 100) < 60:
                recommendations.append({
                    "badge": "Diagnostic Alert",
                    "badge_type": "warning",
                    "title": f"Reinforce {cat} Fundamentals",
                    "action": f"Review Stage resources for {cat} before advancing to higher-level mini-projects.",
                    "rationale": f"You scored {stats.get('pct')}% in the diagnostic test for {cat}. Strengthening fundamentals now prevents bottlenecks later."
                })
                break  # Don't overwhelm with multiple quiz alerts

    # 2. Active Stage Next Steps
    active_stage = None
    for stage in stages:
        if not stage.get("is_completed"):
            active_stage = stage
            break

    if active_stage:
        pending_tasks = [t for t in active_stage.get("tasks", []) if not t.get("is_completed")]
        if pending_tasks:
            next_task = pending_tasks[0]
            recommendations.append({
                "badge": "Next Recommended Action",
                "badge_type": "action",
                "title": f"Work on: {next_task['title']}",
                "action": f"Focus on this topic in {active_stage['title']}.",
                "rationale": f"This is the immediate prerequisite needed to unlock the '{active_stage.get('mini_project', {}).get('title', 'Mini-Project')}' project."
            })
        else:
            recommendations.append({
                "badge": "Milestone Reached",
                "badge_type": "success",
                "title": f"Ready to build: {active_stage.get('mini_project', {}).get('title', 'Mini-Project')}",
                "action": "Complete the stage mini-project and mark the stage as finished.",
                "rationale": "You completed all theory checklist tasks for this stage! Building the project solidifies practical muscle memory."
            })
    elif overall_pct >= 100:
        recommendations.append({
            "badge": "Roadmap Complete",
            "badge_type": "success",
            "title": "Ready for Technical Interviews!",
            "action": "Review your portfolio repositories, rehearse project explanations with the AI Mentor, and apply for roles.",
            "rationale": "You completed 100% of your roadmap checklist and hands-on projects."
        })

    # 3. Schedule / Pacing Recommendation
    feasibility = roadmap_data.get("feasibility_status", "Realistic")
    if feasibility == "Challenging" and overall_pct < 50:
        recommendations.append({
            "badge": "Pacing Adjustment",
            "badge_type": "info",
            "title": "Maintain Consistent Daily Rhythm",
            "action": f"Aim for {student.get('daily_hours', 2)} hours uninterrupted focus each day.",
            "rationale": "Your target schedule is compact. Consistent daily practice yields better retention than weekend cramming."
        })
    elif feasibility == "Unrealistic":
        recommendations.append({
            "badge": "Schedule Feasibility",
            "badge_type": "warning",
            "title": "Focus on Core High-Yield Topics",
            "action": "Prioritize Stage 1 & 2 tasks; defer optional stretch goals until primary skills are solidified.",
            "rationale": roadmap_data.get("feasibility_note", "Pacing alert")
        })

    return recommendations
