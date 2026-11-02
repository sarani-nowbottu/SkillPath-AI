"""
streamlit_app.py - Streamlit UI for SkillPath AI (Learning Path Generator)
Created for NxtWave MCP Mega Workshop Project 5 Submission.
"""

import streamlit as st
import json
from assessment_data import CAREER_PATHS, ALL_SKILLS_LIST
from recommendation_engine import analyze_skill_gaps, calculate_workload_feasibility
from ai_mentor import generate_mentor_reply

st.set_page_config(
    page_title="SkillPath AI - Learning Path Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        color: white;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎓 SkillPath AI — Learning Path Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">NxtWave MCP Mega Workshop • Project 5: Personalized Career Learning Roadmap</div>', unsafe_allow_html=True)

# ==================== SIDEBAR USER INPUTS ====================
with st.sidebar:
    st.header("👤 Student Profile & Goals")
    student_name = st.text_input("Student Name", value="Alex Chen")
    education_level = st.selectbox(
        "Current Education",
        ["1st Year B.Tech / BCA", "2nd Year B.Tech / BCA", "3rd Year B.Tech / BCA", "4th Year / Final Year", "Graduate / Transitioner"],
        index=1
    )
    career_goal = st.selectbox(
        "Target Career Role",
        list(CAREER_PATHS.keys()),
        index=0
    )
    daily_hours = st.slider("Daily Study Time (Hours)", min_value=1.0, max_value=8.0, value=2.5, step=0.5)
    target_weeks = st.slider("Target Duration (Weeks)", min_value=4, max_value=24, value=12, step=1)
    
    st.markdown("---")
    st.subheader("🛠️ Current Skills")
    existing_skills = st.multiselect(
        "Select skills you already know:",
        options=ALL_SKILLS_LIST[:12],
        default=["HTML & CSS", "Relational Databases & SQL"]
    )
    
    generate_btn = st.button("🚀 Generate Learning Path", use_container_width=True)

# Fetch Career Metadata
career_info = CAREER_PATHS[career_goal]
total_curriculum_hours = sum(s["duration_hours"] for s in career_info["stages"])

# ==================== MAIN DISPLAY ====================
tab1, tab2 = st.tabs(["📋 Diagnostic Assessment", "🗺️ Generated Learning Roadmap"])

with tab1:
    st.subheader(f"Diagnostic Assessment: {career_goal}")
    st.write("Answer these foundational questions to evaluate your baseline:")
    
    user_answers = {}
    for idx, q in enumerate(career_info["quiz"]):
        st.markdown(f"**Q{idx+1}. {q['question']}** *(Category: {q['category']})*")
        user_answers[q["id"]] = st.radio(
            f"Select answer for Q{idx+1}:",
            options=q["options"],
            key=f"quiz_{q['id']}",
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)

# If Generate Button Clicked or State exists
if generate_btn or "generated" in st.session_state:
    st.session_state["generated"] = True
    
    # Calculate Quiz Score
    score = 0
    total_q = len(career_info["quiz"])
    cat_scores = {}
    for q in career_info["quiz"]:
        cat = q["category"]
        if cat not in cat_scores:
            cat_scores[cat] = {"correct": 0, "total": 0, "pct": 0}
        cat_scores[cat]["total"] += 1
        
        selected_opt = user_answers.get(q["id"])
        correct_opt = q["options"][q["correct_index"]]
        if selected_opt == correct_opt:
            score += 1
            cat_scores[cat]["correct"] += 1

    for cat in cat_scores:
        t = cat_scores[cat]["total"]
        c = cat_scores[cat]["correct"]
        cat_scores[cat]["pct"] = round((c / t) * 100) if t > 0 else 0

    # Skill Gap Calculation
    self_skill_dict = {s: "Intermediate" for s in existing_skills}
    gaps = analyze_skill_gaps(career_goal, self_skill_dict, cat_scores)
    feasibility = calculate_workload_feasibility(total_curriculum_hours, daily_hours, target_weeks)

    with tab2:
        st.success(f"🎉 Learning Path Generated for **{student_name}** targeting **{career_goal}**!")
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Curriculum Hours", f"{total_curriculum_hours}h")
        with col2:
            st.metric("Pacing", f"{daily_hours}h / day")
        with col3:
            st.metric("Estimated Timeline", f"{feasibility['needed_weeks']} Weeks", delta=f"{target_weeks - feasibility['needed_weeks']}w margin")
        with col4:
            st.metric("Feasibility", feasibility["status"])

        st.info(f"💡 **Pacing Insight**: {feasibility['note']}")

        # Skill-Gap Analysis Visualizer
        st.subheader("📊 Skill-Gap Analysis & Industry Benchmarks")
        for g in gaps[:5]:
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"**{g['skill_name']}** — *{g['why_text']}*")
                st.progress(g['estimated_score'] / 100)
            with c2:
                st.write(f"Current: **{g['estimated_score']}%** / Target: **{g['target_score']}%**")
            with c3:
                badge_color = "🔴" if g['gap_level'] == 'Critical' else ("🟠" if g['gap_level'] == 'Moderate' else "🟢")
                st.write(f"{badge_color} **{g['gap_level']}** ({g['priority']} Priority)")

        st.markdown("---")

        # Roadmap Stages
        st.subheader(f"🗺️ Step-by-Step Learning Stages for {career_goal}")
        for stage in career_info["stages"]:
            with st.expander(f"📌 Stage {stage['order']}: {stage['title']} (~{stage['duration_hours']} Hours)", expanded=(stage['order'] == 1)):
                st.write(f"*{stage['description']}*")
                
                colA, colB = st.columns([1, 1])
                with colA:
                    st.markdown("**Learning Topics Checklist:**")
                    for top in stage["topics"]:
                        st.checkbox(f"Master: {top}", key=f"chk_{stage['order']}_{top}")
                    
                    st.markdown("**Verified Free Resources:**")
                    for r in stage["resources"]:
                        st.markdown(f"- [{r['title']}]({r['url']})")
                
                with colB:
                    st.markdown("**🛠️ Hands-on Mini-Project:**")
                    mp = stage["mini_project"]
                    st.info(f"**{mp['title']}** ({mp['difficulty']})\n\n"
                            f"**Problem**: {mp['problem']}\n\n"
                            f"**Skills Practiced**: {mp['skills']}\n\n"
                            f"**Completion Criteria**: {mp['completion_criteria']}")

        # AI Career Mentor Advice
        st.markdown("---")
        st.subheader("🤖 AI Career Mentor Strategic Advice")
        mentor_context = {
            "name": student_name,
            "career_goal": career_goal,
            "active_stage_title": career_info["stages"][0]["title"],
            "overall_progress": 0
        }
        advice = generate_mentor_reply("What should I focus on first?", mentor_context)
        st.markdown(advice["content"])
else:
    with tab2:
        st.info("👈 Fill out your profile and click **'🚀 Generate Learning Path'** in the sidebar to view your personalized roadmap!")
