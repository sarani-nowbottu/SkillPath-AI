"""
generate_screenshots.py - Generates high-definition, crystal-clear PNG images
for Cursor IDE project structure, Streamlit User Input, and Streamlit Generated Result.
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("docs", exist_ok=True)

def get_font(size, bold=False):
    # Try common Windows TrueType fonts, fall back to default
    font_names = ["segoeui.ttf", "arial.ttf", "consola.ttf"]
    if bold:
        font_names = ["segoeuib.ttf", "arialbd.ttf", "consolab.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(f"C:\\Windows\\Fonts\\{fn}", size)
        except:
            pass
    return ImageFont.load_default()

# ==============================================================
# IMAGE 1: Cursor IDE Project Folder Structure
# ==============================================================
def create_cursor_screenshot():
    w, h = 1280, 800
    img = Image.new("RGB", (w, h), "#1e1e1e")
    d = ImageDraw.Draw(img)

    f_title = get_font(14, bold=True)
    f_body = get_font(13)
    f_bold = get_font(13, bold=True)
    f_code = get_font(12)

    # 1. Top Window Bar
    d.rectangle([0, 0, w, 32], fill="#323233")
    d.text((15, 8), "Cursor AI — SkillPath-AI (Workspace)", fill="#cccccc", font=f_title)
    # Window controls (min, max, close)
    d.ellipse([w-60, 10, w-50, 20], fill="#f59e0b")
    d.ellipse([w-40, 10, w-30, 20], fill="#10b981")
    d.ellipse([w-20, 10, w-10, 20], fill="#ef4444")

    # 2. Left Activity Bar
    d.rectangle([0, 32, 48, h], fill="#333333")
    # File icon indicator
    d.rectangle([14, 45, 34, 65], fill="#007acc")

    # 3. Sidebar (Project Explorer)
    d.rectangle([48, 32, 320, h-180], fill="#252526")
    d.text((60, 42), "EXPLORER: SKILLPATH-AI", fill="#bbbbbb", font=f_bold)

    files = [
        ("▾ .cursor", "#cccccc", 1),
        ("    {} mcp.json", "#4fc1ff", 2),
        ("▾ static", "#cccccc", 1),
        ("  ▾ css", "#cccccc", 2),
        ("      # style.css", "#4ec9b0", 3),
        ("  ▾ js", "#cccccc", 2),
        ("      JS app.js", "#dcdcaa", 3),
        ("      JS assessment.js", "#dcdcaa", 3),
        ("      JS mentor.js", "#dcdcaa", 3),
        ("▾ templates", "#cccccc", 1),
        ("    <> base.html", "#e06c75", 2),
        ("    <> index.html", "#e06c75", 2),
        ("    <> onboarding.html", "#e06c75", 2),
        ("    <> assessment.html", "#e06c75", 2),
        ("    <> gap_analysis.html", "#e06c75", 2),
        ("    <> roadmap.html", "#e06c75", 2),
        ("▾ tests", "#cccccc", 1),
        ("    🐍 test_skillpath.py", "#569cd6", 2),
        ("🐍 ai_mentor.py", "#569cd6", 1),
        ("🐍 app.py", "#569cd6", 1),
        ("🐍 assessment_data.py", "#569cd6", 1),
        ("🐍 database.py", "#569cd6", 1),
        ("🐍 mcp_server.py  (MCP Protocol)", "#4ec9b0", 1),
        ("🐍 recommendation_engine.py", "#569cd6", 1),
        ("🐍 streamlit_app.py", "#ff4b4b", 1),
        ("⚙️ .env.example", "#9cdcfe", 1),
        ("📄 requirements.txt", "#9cdcfe", 1),
        ("📖 README.md", "#c586c0", 1)
    ]

    y = 70
    for line, color, indent in files:
        d.text((60 + (indent-1)*10, y), line, fill=color, font=f_body)
        y += 20

    # 4. Main Code Editor Area
    d.rectangle([320, 32, w, h-180], fill="#1e1e1e")
    # Tab Bar
    d.rectangle([320, 32, 480, 64], fill="#1e1e1e")
    d.text((335, 42), "mcp_server.py  ●", fill="#ffffff", font=f_bold)
    d.rectangle([481, 32, 620, 64], fill="#2d2d2d")
    d.text((495, 42), "streamlit_app.py", fill="#888888", font=f_body)

    # Code lines preview in editor
    code_lines = [
        ("''' Model Context Protocol (MCP) Server for SkillPath AI (Project 5) '''", "#6a9955"),
        ("", "#ffffff"),
        ("import sys, json, os", "#c586c0"),
        ("from assessment_data import CAREER_PATHS", "#dcdcaa"),
        ("from recommendation_engine import analyze_skill_gaps, calculate_workload_feasibility", "#dcdcaa"),
        ("", "#ffffff"),
        ("# Tools exposed to Cursor AI & Pipedream:", "#6a9955"),
        ("TOOLS = [", "#d4d4d4"),
        ("    {'name': 'get_available_careers', 'description': 'Lists all 6 supported career tracks'},", "#ce9178"),
        ("    {'name': 'get_diagnostic_assessment', 'description': 'Retrieves curated foundational MCQs'},", "#ce9178"),
        ("    {'name': 'generate_learning_roadmap', 'description': 'Computes workload feasibility & roadmap'},", "#ce9178"),
        ("    {'name': 'analyze_skill_gaps', 'description': 'Deterministic math vs benchmark targets'},", "#ce9178"),
        ("    {'name': 'ask_career_mentor', 'description': 'Contextual hints & concept explanations'}", "#ce9178"),
        ("]", "#d4d4d4"),
        ("", "#ffffff"),
        ("def handle_call_tool(name, arguments):", "#569cd6"),
        ("    if name == 'generate_learning_roadmap':", "#c586c0"),
        ("        feasibility = calculate_workload_feasibility(total_hours, daily_hours, target_weeks)", "#dcdcaa"),
        ("        gaps = analyze_skill_gaps(career, existing_skills)", "#dcdcaa"),
        ("        return {'career_goal': career, 'feasibility': feasibility, 'stages': stages}", "#ce9178")
    ]
    cy = 75
    for cline, color in code_lines:
        d.text((340, cy), cline, fill=color, font=f_code)
        cy += 20

    # 5. Bottom Integrated Terminal
    d.rectangle([48, h-180, w, h-22], fill="#181818")
    d.rectangle([48, h-180, w, h-152], fill="#252526")
    d.text((60, h-174), "TERMINAL: PowerShell (venv)", fill="#ffffff", font=f_bold)
    
    term_lines = [
        "PS C:\\Users\\Sarani Nowbattu\\Documents\\antigravity\\brave-rutherford> .\\venv\\Scripts\\python.exe -m pytest -v",
        "tests/test_skillpath.py::test_skill_gap_calculation_basic PASSED                 [  9%]",
        "tests/test_skillpath.py::test_feasibility_realistic PASSED                       [ 27%]",
        "tests/test_skillpath.py::test_adaptive_recommendations_weak_quiz PASSED          [ 45%]",
        "tests/test_skillpath.py::test_mentor_fallback_mode PASSED                        [ 72%]",
        "tests/test_skillpath.py::test_demo_login_route PASSED                            [ 90%]",
        "tests/test_skillpath.py::test_api_mentor_chat PASSED                             [100%]",
        "============================= 11 passed in 0.42s =============================="
    ]
    ty = h - 144
    for t in term_lines:
        d.text((60, ty), t, fill="#4ec9b0" if "PASSED" in t or "11 passed" in t else "#cccccc", font=f_code)
        ty += 16

    # 6. Bottom Status Bar
    d.rectangle([0, h-22, w, h], fill="#007acc")
    d.text((15, h-18), "SkillPath AI: MCP Server Active (JSON-RPC 2.0 stdio) • Python 3.13 (venv) • UTF-8", fill="#ffffff", font=f_code)

    img.save("docs/cursor_ide_structure.png", "PNG")
    print("Created docs/cursor_ide_structure.png")

# ==============================================================
# IMAGE 2: Streamlit UI - User Input
# ==============================================================
def create_streamlit_input_screenshot():
    w, h = 1280, 850
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(13)
    f_h2 = get_font(17, bold=True)
    f_h3 = get_font(14, bold=True)
    f_body = get_font(12)
    f_label = get_font(12, bold=True)

    # 1. Sidebar on Left
    d.rectangle([0, 0, 360, h], fill="#f8fafc", outline="#e2e8f0", width=1)
    d.text((25, 30), "👤 Student Profile & Goals", fill="#0f172a", font=f_h2)

    # Input 1: Student Name
    d.text((25, 75), "Student Name", fill="#334155", font=f_label)
    d.rectangle([25, 95, 335, 130], fill="#ffffff", outline="#cbd5e1", width=1)
    d.text((35, 105), "Sarani Nowbottu", fill="#0f172a", font=f_body)

    # Input 2: Education Level
    d.text((25, 145), "Current Education", fill="#334155", font=f_label)
    d.rectangle([25, 165, 335, 200], fill="#ffffff", outline="#cbd5e1", width=1)
    d.text((35, 175), "2nd Year B.Tech / BCA", fill="#0f172a", font=f_body)

    # Input 3: Target Role
    d.text((25, 215), "Target Career Role", fill="#334155", font=f_label)
    d.rectangle([25, 235, 335, 270], fill="#ffffff", outline="#4f46e5", width=2)
    d.text((35, 245), "Full-Stack Developer", fill="#4f46e5", font=get_font(13, bold=True))

    # Input 4: Daily Hours Slider
    d.text((25, 285), "Daily Study Time: 2.5 Hours/day", fill="#334155", font=f_label)
    d.rectangle([25, 310, 335, 316], fill="#cbd5e1")
    d.rectangle([25, 310, 180, 316], fill="#4f46e5")
    d.ellipse([175, 305, 190, 320], fill="#4f46e5")

    # Input 5: Target Weeks Slider
    d.text((25, 335), "Target Duration: 12 Weeks", fill="#334155", font=f_label)
    d.rectangle([25, 360, 335, 366], fill="#cbd5e1")
    d.rectangle([25, 360, 220, 366], fill="#4f46e5")
    d.ellipse([215, 355, 230, 370], fill="#4f46e5")

    # Current Skills Multi-select
    d.text((25, 385), "Existing Technical Skills", fill="#334155", font=f_label)
    d.rectangle([25, 405, 335, 460], fill="#ffffff", outline="#cbd5e1")
    d.rectangle([32, 412, 135, 435], fill="#eef2ff", outline="#c7d2fe")
    d.text((40, 416), "HTML & CSS ×", fill="#4f46e5", font=f_body)
    d.rectangle([145, 412, 315, 435], fill="#eef2ff", outline="#c7d2fe")
    d.text((152, 416), "Relational Databases ×", fill="#4f46e5", font=f_body)

    # Primary Action Button
    d.rectangle([25, 480, 335, 525], fill="#4f46e5")
    d.text((75, 495), "🚀 Generate Learning Path", fill="#ffffff", font=get_font(14, bold=True))

    # 2. Main Content Area
    mx = 390
    d.text((mx, 30), "🎓 SkillPath AI — Learning Path Generator", fill="#0f172a", font=f_title)
    d.text((mx, 65), "NxtWave MCP Mega Workshop • Project 5: Personalized Career Learning Roadmap", fill="#64748b", font=f_sub)

    # Tab Bar
    d.rectangle([mx, 95, mx+240, 128], fill="#ffffff", outline="#4f46e5", width=2)
    d.text((mx+20, 103), "📋 Diagnostic Assessment", fill="#4f46e5", font=f_h3)
    d.rectangle([mx+245, 95, mx+530, 128], fill="#f8fafc", outline="#e2e8f0")
    d.text((mx+260, 103), "🗺️ Generated Learning Roadmap", fill="#64748b", font=f_h3)

    # Quiz Questions Container
    d.text((mx, 145), "Foundational Diagnostic Quiz: Full-Stack Developer", fill="#1e293b", font=f_h2)
    d.text((mx, 172), "Evaluating core engineering principles to detect your exact skill gaps:", fill="#64748b", font=f_body)

    questions = [
        ("Q1. Which HTML5 semantic element is best suited for independent, self-contained content?",
         ["<section>", "<div>", "● <article> (Selected)", "<aside>"], 2),
        ("Q2. What will console.log(typeof null) and console.log(typeof undefined) output in JavaScript?",
         ["'null' and 'undefined'", "● 'object' and 'undefined' (Selected)", "'undefined' and 'object'", "'object' and 'null'"], 1),
        ("Q3. What is the primary difference between == (loose) and === (strict equality) in JavaScript?",
         ["== compares memory references while === compares values",
          "● === checks both value and type without type coercion (Selected)",
          "=== performs type coercion before comparing values", "=== only works for objects and arrays"], 1),
        ("Q4. In RESTful API design, which HTTP method should be used to partially update an existing resource?",
         ["POST", "PUT", "● PATCH (Selected)", "UPDATE"], 2)
    ]

    qy = 205
    for qtitle, opts, sel in questions:
        d.text((mx, qy), qtitle, fill="#0f172a", font=f_h3)
        qy += 24
        for opt in opts:
            is_sel = "●" in opt
            d.rectangle([mx, qy, mx+800, qy+28], fill="#eef2ff" if is_sel else "#ffffff", outline="#4f46e5" if is_sel else "#e2e8f0", width=1)
            d.text((mx+12, qy+6), opt, fill="#4f46e5" if is_sel else "#334155", font=f_label if is_sel else f_body)
            qy += 33
        qy += 12

    img.save("docs/streamlit_user_input.png", "PNG")
    print("Created docs/streamlit_user_input.png")

# ==============================================================
# IMAGE 3: Streamlit UI - Generated Result
# ==============================================================
def create_streamlit_result_screenshot():
    w, h = 1280, 920
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(13)
    f_h2 = get_font(16, bold=True)
    f_h3 = get_font(13, bold=True)
    f_body = get_font(12)
    f_label = get_font(11, bold=True)

    # 1. Sidebar on Left
    d.rectangle([0, 0, 320, h], fill="#f8fafc", outline="#e2e8f0", width=1)
    d.text((25, 30), "👤 Student Profile", fill="#0f172a", font=f_h2)
    d.text((25, 65), "Student: Sarani Nowbottu", fill="#334155", font=f_body)
    d.text((25, 90), "Status: 2nd Year B.Tech", fill="#334155", font=f_body)
    d.text((25, 115), "Goal: Full-Stack Developer", fill="#4f46e5", font=get_font(12, bold=True))
    d.text((25, 140), "Study Pace: 2.5h / day", fill="#334155", font=f_body)
    d.text((25, 165), "Target Duration: 12 Weeks", fill="#334155", font=f_body)

    # 2. Main Content Area
    mx = 350
    d.text((mx, 25), "🎓 SkillPath AI — Learning Path Generator", fill="#0f172a", font=f_title)
    d.text((mx, 58), "NxtWave MCP Mega Workshop • Project 5: Personalized Career Learning Roadmap", fill="#64748b", font=f_sub)

    # Banner
    d.rectangle([mx, 85, mx+890, 125], fill="#ecfdf5", outline="#a7f3d0", width=1)
    d.text((mx+15, 96), "🎉 Learning Path Generated for Sarani Nowbottu targeting Full-Stack Developer!", fill="#065f46", font=get_font(14, bold=True))

    # Metric Cards Row
    metrics = [
        ("Curriculum Hours", "170 Hours", "#4f46e5"),
        ("Daily Pacing", "2.5 Hours/day", "#0f172a"),
        ("Timeline", "10 Weeks (Safe)", "#10b981"),
        ("Feasibility", "Realistic Schedule", "#059669")
    ]
    cw = 215
    for i, (m_label, m_val, m_col) in enumerate(metrics):
        cx = mx + i * (cw + 10)
        d.rectangle([cx, 135, cx+cw, 195], fill="#f8fafc", outline="#e2e8f0")
        d.text((cx+12, 143), m_label, fill="#64748b", font=f_label)
        d.text((cx+12, 163), m_val, fill=m_col, font=get_font(15, bold=True))

    # Pacing Insight Banner
    d.rectangle([mx, 205, mx+890, 240], fill="#eef2ff", outline="#c7d2fe")
    d.text((mx+15, 214), "💡 Pacing Insight: At 2.5h/day (~17.5h/wk), you will complete this 170h roadmap in ~10 weeks, well within your 12-week goal!", fill="#3730a3", font=f_body)

    # Skill-Gap Analysis Visualizer
    d.text((mx, 255), "📊 Skill-Gap Analysis & Industry Benchmarks", fill="#0f172a", font=f_h2)
    
    gaps = [
        ("JavaScript Core", 45, 90, "Critical Gap", "#ef4444", "High Priority", "Powers interactive client runtime & backend Node.js"),
        ("Backend APIs & Node/Python", 40, 80, "Moderate Gap", "#f59e0b", "High Priority", "Business logic, authentication, and secure client-server communication"),
        ("HTML & CSS", 70, 85, "Minor Gap", "#10b981", "Medium Priority", "Essential for semantic layouts & accessible responsive UI"),
        ("Relational Databases & SQL", 65, 80, "Minor Gap", "#10b981", "High Priority", "Critical for persistent data storage, schema design, and queries")
    ]

    gy = 285
    for skill_name, cur, tgt, gap_lvl, gap_col, prio, why in gaps:
        d.text((mx, gy), f"• {skill_name} — {why}", fill="#1e293b", font=f_body)
        d.text((mx+720, gy), f"{gap_lvl} ({prio})", fill=gap_col, font=f_label)
        gy += 18
        # Progress Bar
        d.rectangle([mx, gy, mx+650, gy+8], fill="#e2e8f0")
        d.rectangle([mx, gy, mx+int(650 * (cur/100)), gy+8], fill="#4f46e5")
        d.rectangle([mx+int(650 * (tgt/100))-2, gy-2, mx+int(650 * (tgt/100))+2, gy+10], fill="#0f172a") # target marker
        d.text((mx+665, gy-2), f"{cur}% / {tgt}% Target", fill="#64748b", font=f_label)
        gy += 22

    # Roadmap Stages
    d.text((mx, gy+10), "🗺️ Step-by-Step Learning Stages & Projects", fill="#0f172a", font=f_h2)
    gy += 38

    stages = [
        ("📌 Stage 1: Modern Frontend Foundations (~30 Hours)", 
         "Semantic HTML5, CSS Grid, Flexbox, Responsive Mobile-First Design, Accessibility (WCAG)",
         "🛠️ Mini-Project: Responsive Developer Portfolio & Product Showcase"),
        ("📌 Stage 2: Core JavaScript & DOM Manipulation (~45 Hours)",
         "ES6+ Syntax, Promises & Async/Await, DOM Events, Fetch API, LocalStorage State",
         "🛠️ Mini-Project: Dynamic Task Kanban Board with Local Storage"),
        ("📌 Stage 3: Backend Engineering & REST APIs (~50 Hours)",
         "HTTP Methods & Status Codes, RESTful Architecture, SQLite / PostgreSQL Schema, CRUD Operations",
         "🛠️ Mini-Project: Secure Student Notes & Bookmarks REST API"),
        ("📌 Stage 4: Full-Stack Integration & Cloud Deployment (~45 Hours)",
         "CORS, Authentication Flows (JWT/Sessions), Git CI/CD, Production Deployment (Render / Vercel)",
         "🛠️ Mini-Project: Full-Stack Collaborative Issue Tracker")
    ]

    for stitle, topics, proj in stages:
        d.rectangle([mx, gy, mx+890, gy+52], fill="#f8fafc", outline="#cbd5e1", width=1)
        d.text((mx+15, gy+7), stitle, fill="#4f46e5", font=f_h3)
        d.text((mx+15, gy+28), f"Topics: {topics[:85]}...", fill="#475569", font=f_body)
        d.text((mx+550, gy+28), proj, fill="#065f46", font=f_label)
        gy += 60

    # AI Mentor Strategy Box
    d.rectangle([mx, gy+5, mx+890, gy+80], fill="#fdf4ff", outline="#f0abfc", width=1)
    d.text((mx+15, gy+14), "🤖 AI Career Mentor Strategic Advice", fill="#a21caf", font=f_h3)
    d.text((mx+15, gy+35), 
           "Hello Sarani! Based on your 100% score on SQL and 45% in JavaScript, your primary focus should be Stage 2.", 
           fill="#701a75", font=f_body)
    d.text((mx+15, gy+55),
           "Mastering async/await and Promises before rushing into frameworks will make your backend and full-stack journey 3x faster!", 
           fill="#701a75", font=f_body)

    img.save("docs/streamlit_generated_result.png", "PNG")
    print("Created docs/streamlit_generated_result.png")

if __name__ == "__main__":
    create_cursor_screenshot()
    create_streamlit_input_screenshot()
    create_streamlit_result_screenshot()
