from google.adk.agents.llm_agent import Agent
import json, os
from datetime import datetime

MODEL = "gemini-2.5-flash"
SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

# -------------------------
# QUESTION BANK
# -------------------------
QUESTION_BANK = {
    "software_developer": {
        "fresher": {
            "easy": [
                "What is a variable and why do we use functions?",
                "What's the difference between a process and a thread?"
            ],
            "medium": [
                "How does a hash map work? Mention one real use-case.",
                "Explain how HTTP works at a high level."
            ],
            "hard": [
                "Design a simple rate limiter for an API. What tradeoffs matter?",
                "How would you debug a production memory spike step-by-step?"
            ],
        },
        "experienced": {
            "easy": ["Describe SOLID principles briefly."],
            "medium": ["How would you design a pagination system for millions of records?"],
            "hard": ["Design a URL shortener — components, failure modes, scaling challenges."]
        }
    }
}

# -------------------------
# ONBOARDING QUESTIONS
# -------------------------
def get_onboarding_questions():
    return [
        "What’s your name?",
        "Nice! What job role are you preparing for?",
        "Great. What skills or technologies are you familiar with?",
        "Are you a fresher or experienced? If experienced, how many years?",
        "Finally, what areas do you want extra help with? (DSA, Projects, Communication, Confidence)"
    ]

# -------------------------
# CHOOSE INTERVIEW QUESTION
# -------------------------
def choose_question(role_key, level, difficulty, asked_indices):
    bank = QUESTION_BANK.get(role_key, {})
    level_bank = bank.get(level, {})
    difficulty_bank = level_bank.get(difficulty, [])

    for i, q in enumerate(difficulty_bank):
        if i not in asked_indices:
            return q, i

    return None, None

# -------------------------
# SAVE SESSION
# -------------------------
def save_session(session_id: str, session_obj: dict) -> dict:
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    session_obj["_saved_at"] = datetime.utcnow().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(session_obj, f, indent=2)

    return {"status": "ok", "path": path}

# -------------------------
# SIMPLE SCORING
# -------------------------
def simple_score(answer_text: str) -> int:
    if not answer_text:
        return 0

    words = answer_text.split()
    t = len(words)
    score = 0

    if t > 10: score += 3
    if t > 30: score += 3

    keywords = ["tradeoff", "latency", "cache", "shard", "database", "design", "scale"]
    if any(k in answer_text.lower() for k in keywords):
        score += 2

    return max(0, min(10, score))

# -------------------------
# PDF PLACEHOLDER
# -------------------------
def generate_pdf_report(session_id: str, session_data: dict):
    return {"status": "pdf_ready", "session_id": session_id}

# -------------------------
# **ROOT AGENT DESCRIPTION (ONE QUESTION AT A TIME)**
# -------------------------
DESCRIPTION = """
You are an Interview Practice AI Agent designed to be extremely user-friendly,
supportive, and interactive.

==============================
ONBOARDING RULES
==============================
You MUST ask onboarding questions STRICTLY one at a time.

Flow:
1. Ask: “What’s your name?” Wait for user reply.
2. Ask: “What job role are you preparing for?” Wait for reply.
3. Ask: “What skills or technologies do you know?” Wait for reply.
4. Ask: “Are you a fresher or experienced?” Wait for reply.
5. Ask: “Which areas do you want a mock interview?” Wait for reply.

IMPORTANT:
• Never ask more than ONE question in a message.
• Never skip ahead.
• Never combine onboarding steps.
• Use short, friendly responses.

After onboarding → start interview questions automatically.

==============================
INTERVIEW FLOW
==============================
• Ask one interview question at a time.
• Provide hints only if they say “I don’t know”.
• Avoid giving full answers.
• Adapt to the user style:
  - If confused: simplify.
  - If fast: ask direct questions.
  - If chatty: gently bring back to topic.

==============================
SCORING RULES
==============================
For EVERY answer except name:
• Give a score (0–10)
• Provide EXACTLY 2 bullet-point feedback notes (6–12 words)
• Encourage them with positivity

==============================
QUESTION LIMIT
==============================
Total questions allowed: 6–8 (including onboarding + interview).
When limit reached:
• Stop asking questions
• Give a 3–5 line summary
• Give EXACTLY 3 improvement bullets
• End cleanly

==============================
SAVE & PDF COMMANDS
==============================
User says “save”:
Return ONLY:
{"action":"save","session_id":"..."}

User says “pdf”:
Return ONLY:
{"action":"pdf","session_id":"..."}

==============================
END FORMAT
==============================
1. 3–5 line performance summary
2. EXACTLY 3 improvement bullet points
"""

root_agent = Agent(
    model=MODEL,
    name="root_agent",
    description=DESCRIPTION,
)

try:
    root_agent.speech = {"enable_input": True, "enable_output": True}
except:
    pass

AGENT = root_agent

__all__ = [
    "AGENT",
    "get_onboarding_questions",
    "choose_question",
    "save_session",
    "simple_score",
    "generate_pdf_report"
]
