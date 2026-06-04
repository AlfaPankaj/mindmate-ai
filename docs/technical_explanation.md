# MindMate AI: Technical Explanation & Interview Guide

This document provides a detailed walkthrough of the codebase and a strategy for presenting this system to the Zenark engineering team.

---

## 🛠️ Part 1: Codebase Walkthrough

### 1. The Intelligence Layer (LangGraph)
**File:** `/backend/graph/workflow.py`  
**Purpose:** This is the "Central Nervous System." It defines the stateful reasoning path. Unlike simple chains, it allows the AI to cycle through memory, planning, and tool execution before responding.

```python
def create_companion_graph():
    workflow = StateGraph(CompanionState)
    workflow.add_node("classify", input_classifier_node)
    workflow.add_node("retrieve_memory", memory_retrieval_node)
    # ... other nodes ...
    workflow.add_edge("classify", "retrieve_memory")
    return workflow.compile()
```

### 2. Longitudinal Memory (PRISM-Lite)
**File:** `/backend/db/prism_memory.py`  
**Purpose:** Manages the `User Intent Vector`. It doesn't just store chat logs; it extracts **Patterns** (e.g., "sleep_difficulty") and **Outcome History** (what worked for this specific user).

```python
async def update_pattern(user_id: str, pattern_type: str):
    # Atomic updates to evidence count in MongoDB
    await db.user_profiles.update_one(
        {"user_id": user_id},
        {"$inc": {f"active_patterns.{pattern_type}.evidence_count": 1}}
    )
```

### 3. Reasoning Nodes & Tools Layer
**Files:** `/backend/graph/nodes.py` and `/backend/tools/wellness_tools.py`  
**Purpose:** MindMate uses a decoupled tools layer. The `recommendation_planner_node` in the graph identifies the need for action, and the `tool_execution_node` calls specific logic in the `tools/` folder. This separation allows tools to be tested independently of the AI graph.

*   **`input_classifier_node`**: Uses Llama 3.3 to detect intent and risk.
*   **`wellness_tools.py`**: Contains the logic for `mood_tool`, `habit_tool`, and `exercise_tool`.
*   **`tool_execution_node`**: The bridge that translates AI recommendations into database actions.

### 4. Proactive Scheduling
**File:** `/backend/scheduler/checkin_scheduler.py`  
**Purpose:** Demonstrates **Proactive Behavior**. It runs in the background using `APScheduler`, scans for abandoned habits, and triggers the AI to reach out to the user.

### 5. Frontend Dashboard
**File:** `/frontend/streamlit_app.py`  
**Purpose:** Provides a "Glass Box" view. On the left is the chat; on the right is the real-time data showing the AI's internal "Pattern Bank" and Wellness stats.

---

## 🎙️ Part 2: Interview Presentation Strategy

When you present this to Zenark, do not just show the chat. Follow this **3-Step "Senior Engineer" Pitch**:

### Step 1: The Problem (The "Why")
> "Most wellness apps have isolated modules—Mood, Habits, and Journals don't talk to each other. I built **MindMate AI** to be the 'Central Intelligence Layer' that unifies these silos using a stateful reasoning graph."

### Step 2: The Innovation (The "How")
> "I implemented two proprietary concepts:
> 1. **PRISM-Lite Memory**: A longitudinal system that tracks behavioral patterns over weeks, not just the current session.
> 2. **Hybrid Proactivity**: The AI doesn't just wait for you to type; a background scheduler monitors your habits and triggers personalized, consent-based check-ins when it detects a drop-off."

### Step 3: The Demo (The "Impact")
1.  **Show the Dashboard**: Point out the "Detected Patterns" section.
2.  **Trigger a Scenario**: Type *"I can't sleep again."* Show the terminal logs where the AI detects a `recurring_sleep_difficulty`.
3.  **Show Orchestration**: Point to the **Habit Tracker** table. Type *"I want to start reading books."* Refresh the dashboard to show the AI **automatically created** a new habit in the database.

---

## 💡 Key Talking Points (Buzzwords to Use)
*   **"Agentic Orchestration"**: Explain that you aren't just chatting; you are orchestrating tools.
*   **"Stateful Persistence"**: Explain how LangGraph keeps the conversation coherent.
*   **"Non-Diagnostic Persona"**: Emphasize safety and ethics.
*   **"Schema Normalization"**: Mention how you handle inconsistent data from different modules.

---

### Final Submission Checklist
1.  Ensure `.env` is NOT uploaded to GitHub (use `.env.example`).
2.  Include the `docs/` folder in your repository.
3.  The `technical_explanation.md` (this file) should be in your `docs/` folder.
