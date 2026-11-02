"""
ai_mentor.py - Context-Aware Career Mentor with Dual Online/Offline Operation
Supports Groq, Gemini, OpenAI, and a comprehensive rule-based offline fallback.
"""

import os
import json
import requests

SYSTEM_PROMPT = """You are SkillPath AI, an expert, supportive senior software engineer and career mentor for college students.
Your mission is to help the student master concepts, understand their personalized roadmap, and prepare for tech careers.

Guidelines:
1. Speak in clear, beginner-friendly language without unnecessary academic jargon.
2. Use relatable analogies to explain complex programming concepts.
3. When asked for help with coding tasks, provide guiding hints, thought processes, and architectural advice rather than dumping full answers immediately.
4. Keep responses focused, encouraging, and actionable.
5. Emphasize why concepts matter in real-world software engineering.
"""

def generate_mentor_reply(user_query, student_context, conversation_history=None):
    """
    Generates a mentor response given the user query and rich student context.
    If an AI provider is configured and reachable, it calls the LLM API.
    Otherwise, it invokes the comprehensive built-in offline mentor.
    """
    provider = os.getenv("AI_PROVIDER", "none").strip().lower()
    api_key = os.getenv("AI_API_KEY", "").strip()

    # If provider is not 'none' and key exists, attempt live AI call
    if provider in ["groq", "openai", "gemini"] and api_key:
        try:
            return call_online_llm(provider, api_key, user_query, student_context, conversation_history)
        except Exception as e:
            # Graceful fallback on API error/timeout
            fallback_res = generate_rule_based_reply(user_query, student_context)
            fallback_res["content"] = (
                f"> **Notice**: Online AI provider ({provider}) was temporarily unavailable ({str(e)[:70]}). "
                f"Switched to SkillPath Built-in Mentor.\n\n" + fallback_res["content"]
            )
            return fallback_res

    # Default: Transparent offline rule-based mentor
    return generate_rule_based_reply(user_query, student_context)

def call_online_llm(provider, api_key, user_query, student_context, conversation_history):
    """Calls external LLM API (Groq, OpenAI, or Gemini) securely from backend."""
    model = os.getenv("AI_MODEL", "").strip()
    
    # Build context briefing
    context_str = (
        f"Student Name: {student_context.get('name', 'Student')}\n"
        f"Education: {student_context.get('education_level', 'College')}\n"
        f"Target Career: {student_context.get('career_goal', 'Software Engineer')}\n"
        f"Daily Study Hours: {student_context.get('daily_hours', 2)} hrs/day\n"
        f"Current Active Stage: {student_context.get('active_stage_title', 'Fundamentals')}\n"
        f"Roadmap Progress: {student_context.get('overall_progress', 0)}%\n"
        f"Latest Diagnostic Score: {student_context.get('quiz_score', 'Not taken yet')}\n"
    )

    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nCurrent Student Context:\n{context_str}"}
    ]

    # Include recent chat history
    if conversation_history:
        for msg in conversation_history[-6:]:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})

    messages.append({"role": "user", "content": user_query})

    if provider in ["groq", "openai"]:
        url = "https://api.groq.com/openai/v1/chat/completions" if provider == "groq" else "https://api.openai.com/v1/chat/completions"
        default_model = "llama-3.3-70b-versatile" if provider == "groq" else "gpt-4o-mini"
        target_model = model or default_model

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": 0.6,
            "max_tokens": 800
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            reply_text = data["choices"][0]["message"]["content"]
            return {"content": reply_text, "is_fallback": 0, "provider": provider}
        else:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:120]}")

    elif provider == "gemini":
        target_model = model or "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={api_key}"
        
        # Format for Gemini generateContent
        gemini_prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context_str}\n\nStudent asks: {user_query}"
        payload = {
            "contents": [{"parts": [{"text": gemini_prompt}]}]
        }
        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"content": reply_text, "is_fallback": 0, "provider": "gemini"}
        else:
            raise RuntimeError(f"Gemini error {resp.status_code}: {resp.text[:120]}")

    raise ValueError(f"Unsupported provider: {provider}")

def generate_rule_based_reply(user_query, student_context):
    """
    Intelligent, deterministic rule-based mentor.
    Clearly labeled as offline fallback to avoid misleading users.
    Provides structured advice tailored to student's exact goal, stage, and gaps.
    """
    query_lower = user_query.lower()
    name = student_context.get("name", "Student")
    career = student_context.get("career_goal", "Full-Stack Developer")
    stage_title = student_context.get("active_stage_title", "Fundamentals")
    overall_progress = student_context.get("overall_progress", 0)

    # Header clearly identifying mode
    badge = "🤖 *[SkillPath Built-in Mentor (Offline Rule-Based Mode)]*\n\n"

    # 1. HINT OR STUCK REQUEST
    if any(k in query_lower for k in ["hint", "stuck", "clue", "help me code", "don't understand"]):
        body = (
            f"Here is a mentoring hint for **{stage_title}**:\n\n"
            f"1. **Break it into the smallest step**: Don't try to solve the entire feature at once. Start by printing or `console.log()`ing your inputs to verify data flow.\n"
            f"2. **State before UI**: First ensure your data model is correct (e.g. an array of objects or SQLite table schema) before writing rendering code.\n"
            f"3. **Check the DevTools**: If you're building web features, inspect the Network tab for HTTP response codes and the Console for uncaught exceptions.\n\n"
            f"💡 *Guiding Question*: What does your function receive as an input, and what exact data structure should it return?"
        )

    # 2. CONCEPT EXPLANATION REQUESTS
    elif any(k in query_lower for k in ["explain", "what is", "how does", "difference between", "why do we need"]):
        if "sql" in query_lower or "database" in query_lower:
            body = (
                f"**Databases in a Nutshell**:\n\n"
                f"Think of a **Relational Database (SQL)** like a structured Excel workbook with strict rules: sheets are tables, columns are types, and rows are records. "
                f"Foreign keys are like hyperlinks connecting related rows (e.g. connecting a Student ID to their Course Registrations).\n\n"
                f"**Why it matters for {career}**: Knowing when to use an Index (like a book's index) allows queries over millions of records to execute in milliseconds instead of seconds."
            )
        elif "javascript" in query_lower or "async" in query_lower or "promise" in query_lower:
            body = (
                f"**Asynchronous JavaScript & Promises**:\n\n"
                f"Imagine ordering food at a cafe. A **synchronous** system would force everyone in line to freeze until your burger is cooked. "
                f"An **asynchronous** system gives you a buzzer (a **Promise**). You step aside, the line continues, and when the food is ready, the buzzer rings (`resolve`).\n\n"
                f"**Why it matters**: Web browsers are single-threaded. Async code ensures fetching data from an API never freezes the user interface."
            )
        elif "api" in query_lower or "rest" in query_lower:
            body = (
                f"**RESTful APIs Explained**:\n\n"
                f"An API is like a restaurant waiter. You (the client) look at a menu of available dishes (endpoints), give your order to the waiter with specific instructions (HTTP request), "
                f"and the waiter brings back your meal from the kitchen (HTTP JSON response).\n\n"
                f"- `GET`: Inspect an existing dish.\n"
                f"- `POST`: Order a new meal.\n"
                f"- `PUT/PATCH`: Modify your sides.\n"
                f"- `DELETE`: Send back an item."
            )
        else:
            body = (
                f"In software engineering, mastering fundamentals gives you high leverage. For **{stage_title}**, "
                f"the key principle is to learn how components communicate.\n\n"
                f"Always ask: Where does the data originate, what transforms it, and where is it stored? "
                f"Feel free to ask specifically about JavaScript, SQL, REST APIs, or OOP!"
            )

    # 3. PRACTICE / QUIZ QUESTIONS
    elif any(k in query_lower for k in ["practice", "quiz", "question", "test me"]):
        body = (
            f"Here is a quick diagnostic practice drill for **{career}**:\n\n"
            f"**Question**: Suppose your web application slows down significantly when querying user records with their associated orders. What is the first thing you should inspect?\n"
            f"- A) Add another server immediately\n"
            f"- B) Run `EXPLAIN` on the SQL query to verify index usage and prevent full table scans\n"
            f"- C) Convert all data to localStorage\n"
            f"- D) Restart the computer\n\n"
            f"*(Reply with your choice, and I will explain the engineering reasoning behind it!)*"
        )

    # 4. MINI-PROJECT ADVICE
    elif any(k in query_lower for k in ["project", "mini-project", "build", "portfolio"]):
        body = (
            f"For your current stage (**{stage_title}**), focus on building something that solves an actual user need:\n\n"
            f"1. **Scope It Small**: A working 3-feature app with clean Git commits is 10x more impressive to an interviewer than an unfinished giant clone.\n"
            f"2. **Clean README**: Every portfolio project must have a screenshot, clear local run instructions, and an explanation of the technical trade-offs you made.\n"
            f"3. Check the **Stage Mini-Project** card on your dashboard for the exact requirements and stretch goals!"
        )

    # 5. GENERAL / GREETING
    else:
        body = (
            f"Hello {name}! You are currently on track for **{career}** with **{overall_progress}%** of your roadmap completed.\n\n"
            f"Your current focus is **{stage_title}**.\n\n"
            f"How can I help you today?\n"
            f"• *'Give me a hint on my project'*\n"
            f"• *'Explain REST APIs simply'*\n"
            f"• *'Give me a practice interview question'*\n"
            f"• *'Why does this skill matter in interviews?'*"
        )

    return {
        "content": badge + body,
        "is_fallback": 1,
        "provider": "rule_based_fallback"
    }
