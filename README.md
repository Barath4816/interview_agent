📘 ADK Interview Agent

A fully interactive, human-like interview coaching agent built using Google ADK, designed to simulate real interview sessions with onboarding, scoring, session saving, and PDF report generation.

🚀 Features

✅ 1. Human-like Interview Flow Warm, friendly tone

Asks onboarding questions one at a time

Asks 6–8 total questions, then automatically ends

✅ 2. Onboarding Stage

The agent asks in this exact order:

Candidate’s name

Job role

Skills / technologies

Fresher or experienced

Areas requiring help


Includes:

Role-based question bank

Difficulty levels: Easy, Medium, Hard

Fresher vs Experienced branching



📊 Scoring

After each answer:

Score from 0–10

Provides max 2 short bullet feedback points

Encouraging tone

📁 Session Handling

All session files are stored in:

/sessions/


Functions included:

save_session() → saves JSON session

generate_pdf_report() → mock PDF handler

Users can trigger:

save


→ returns
{"action":"save","session_id":"..."}

pdf


→ returns
{"action":"pdf","session_id":"..."}

🛠️ Technology Used

Google ADK

Python 3.9+

Gemini 2.5 Flash Model

📂 Project Structure
interview_agent/
│
├── agent.py
├── __init__.py
├── sessions/        # Auto-created session storage
├── README.md
└── ...

🧩 Code Overview
Root Agent

Located in agent.py:

Uses ADK’s Agent class

Contains full behavioral description

Handles interview flow logic

Question Engine

QUESTION_BANK dictionary manages:

Job roles

Levels (fresher/experienced)

Difficulty separation

Session Persistence

Stores sessions as .json with:

User answers

Scores

Timestamps

Question order

🏁 End of Interview

After 6–8 total questions:

Gives 3–5 line performance summary

Gives exactly 3 improvement bullet points

Session ends cleanly

▶️ How to Run
1. Install dependencies
pip install google-adk

2. Import the agent in your main server
from interview_agent import AGENT

3. Start chatting

Use ADK’s web UI or integrate the AGENT into your endpoint.
