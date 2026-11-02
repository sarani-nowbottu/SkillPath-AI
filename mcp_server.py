"""
mcp_server.py - Model Context Protocol (MCP) Server for SkillPath AI (Project 5)
Enables Cursor AI, Pipedream, and Claude to interface with SkillPath AI as MCP tools.
Implements JSON-RPC 2.0 over standard I/O (STDIO) according to the MCP specification.
"""

import sys
import json
import os
from assessment_data import CAREER_PATHS, ALL_SKILLS_LIST
from recommendation_engine import analyze_skill_gaps, calculate_workload_feasibility
from ai_mentor import generate_mentor_reply

# Tool definitions exposed to MCP clients (Cursor AI, Claude Desktop, Pipedream)
TOOLS = [
    {
        "name": "get_available_careers",
        "description": "Lists all available career pathways supported by SkillPath AI with their required benchmark skills.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_diagnostic_assessment",
        "description": "Retrieves the diagnostic skill quiz questions for a chosen career path to evaluate student readiness.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "career_goal": {
                    "type": "string",
                    "description": "Target career role (e.g. 'Full-Stack Developer', 'Python Developer', 'Data Analyst', 'AI/ML Engineer', 'Java Developer', 'Backend Developer')"
                }
            },
            "required": ["career_goal"]
        }
    },
    {
        "name": "generate_learning_roadmap",
        "description": "Generates a personalized learning roadmap with duration feasibility analysis, stages, verified resources, and mini-projects.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "career_goal": {"type": "string", "description": "Target career path"},
                "daily_hours": {"type": "number", "description": "Available study hours per day (e.g., 2.0)"},
                "target_weeks": {"type": "integer", "description": "Student goal duration in weeks (e.g., 12)"},
                "existing_skills": {"type": "object", "description": "Dictionary of skill -> level ('Beginner', 'Intermediate', 'Advanced')"}
            },
            "required": ["career_goal", "daily_hours", "target_weeks"]
        }
    },
    {
        "name": "analyze_skill_gaps",
        "description": "Performs deterministic skill gap analysis comparing student's proficiency against industry benchmarks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "career_goal": {"type": "string", "description": "Target career path"},
                "existing_skills": {"type": "object", "description": "Dictionary of skill -> level"},
                "quiz_scores": {"type": "object", "description": "Optional category scores from quiz"}
            },
            "required": ["career_goal"]
        }
    },
    {
        "name": "ask_career_mentor",
        "description": "Provides contextual hints, explanations, interview prep, or mini-project guidance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Student query or request for advice"},
                "career_goal": {"type": "string", "description": "Student's target career role"},
                "active_stage": {"type": "string", "description": "Current learning stage title"}
            },
            "required": ["query"]
        }
    }
]

def handle_call_tool(name, arguments):
    """Executes the requested tool and returns the result."""
    if name == "get_available_careers":
        careers = {k: {"description": v["description"], "skills_count": len(v["benchmark_skills"])} for k, v in CAREER_PATHS.items()}
        return {"careers": careers}

    elif name == "get_diagnostic_assessment":
        career = arguments.get("career_goal", "Full-Stack Developer")
        career_data = CAREER_PATHS.get(career, CAREER_PATHS["Full-Stack Developer"])
        questions = []
        for q in career_data["quiz"]:
            questions.append({
                "id": q["id"],
                "category": q["category"],
                "question": q["question"],
                "options": q["options"]
            })
        return {"career": career, "questions": questions}

    elif name == "generate_learning_roadmap":
        career = arguments.get("career_goal", "Full-Stack Developer")
        daily_hours = float(arguments.get("daily_hours", 2.0))
        target_weeks = int(arguments.get("target_weeks", 12))
        existing_skills = arguments.get("existing_skills", {})

        career_data = CAREER_PATHS.get(career, CAREER_PATHS["Full-Stack Developer"])
        total_hours = sum(s["duration_hours"] for s in career_data["stages"])
        feasibility = calculate_workload_feasibility(total_hours, daily_hours, target_weeks)
        gaps = analyze_skill_gaps(career, existing_skills)

        return {
            "career_goal": career,
            "feasibility": feasibility,
            "skill_gaps": gaps[:4],
            "stages": career_data["stages"]
        }

    elif name == "analyze_skill_gaps":
        career = arguments.get("career_goal", "Full-Stack Developer")
        existing_skills = arguments.get("existing_skills", {})
        quiz_scores = arguments.get("quiz_scores", {})
        gaps = analyze_skill_gaps(career, existing_skills, quiz_scores)
        return {"career_goal": career, "gaps": gaps}

    elif name == "ask_career_mentor":
        query = arguments.get("query", "")
        career = arguments.get("career_goal", "Full-Stack Developer")
        active_stage = arguments.get("active_stage", "Core Fundamentals")
        context = {
            "name": "MCP Student",
            "career_goal": career,
            "active_stage_title": active_stage,
            "overall_progress": 25
        }
        res = generate_mentor_reply(query, context)
        return res

    else:
        raise ValueError(f"Unknown tool: {name}")

def run_stdio_server():
    """Standard JSON-RPC 2.0 server loop for Cursor / Claude Desktop / Pipedream integration."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments", {})
                result = handle_call_tool(name, arguments)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method {method} not found"}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if "req" in locals() and isinstance(req, dict) else None,
                "error": {"code": -32000, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("--- Testing SkillPath AI MCP Tools ---")
        careers = handle_call_tool("get_available_careers", {})
        print("Available Careers:", list(careers["careers"].keys()))
        quiz = handle_call_tool("get_diagnostic_assessment", {"career_goal": "Full-Stack Developer"})
        print(f"Full-Stack Quiz Loaded: {len(quiz['questions'])} questions.")
        roadmap = handle_call_tool("generate_learning_roadmap", {
            "career_goal": "Full-Stack Developer",
            "daily_hours": 2.5,
            "target_weeks": 12
        })
        print(f"Feasibility Status: {roadmap['feasibility']['status']}")
        print("All MCP tool tests passed successfully!")
    else:
        run_stdio_server()
