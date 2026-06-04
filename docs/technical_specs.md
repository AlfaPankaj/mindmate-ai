# MindMate AI: Technical Deep-Dive & Workflow Specifications

This document provides a granular technical explanation of the core systems powering MindMate AI, specifically focusing on the **LangGraph Orchestration** and the **PRISM-Lite Memory** architecture.

---

## 1. LangGraph: The Orchestration Engine

MindMate uses **LangGraph** to move beyond linear LLM chains. It treats the AI's "thought process" as a stateful, cyclic graph.

### 1.1 The State Object
The entire graph shares a `CompanionState` object, which is passed from node to node:
```python
class CompanionState(TypedDict):
    user_id: str
    message: str            # Current user input
    profile: dict           # PRISM-Lite data (Consent-aware)
    module_data: dict       # Normalized data from Habit/Mood/Journal modules
    intent_category: str    # e.g., "sleep_issue", "crisis"
    detected_patterns: list # Recurring issues found in this session
    recommendation: dict    # The chosen tool/action (Weighted by past outcomes)
    response: str           # Final string sent to user
    safety_flag: bool       # Set by the Hybrid Safety Node
```

### 1.2 Node-by-Node Execution Workflow
1.  **Input Classifier Node:** Categorizes input. If keyword-matched for risk, flags for `Hybrid Safety Node`.
2.  **Memory & State Retrieval Node:**
    *   *Action:* Queries MongoDB for user profile and **normalized** module data.
    *   *Consent Filter:* Only fetches memories matching the user's current `consent_depth` (Recent vs. Historical).
3.  **Pattern Detection Node:** Compares normalized data across silos to find cross-module trends.
4.  **Recommendation & Tool Node:**
    *   *Logic:* Scores actions based on `Pattern Strength` + `Outcome History` (e.g., if user hated breathing exercises last time, it suggests journaling instead).
5.  **Hybrid Safety Node:**
    *   *Double Check:* Rule-based screening + lightweight LLM verification pass to reduce false positives.
6.  **Memory Update Node:** Stores the interaction and **tracks recommendation outcomes** (e.g., "Did the user click the exercise?").

---

## 2. PRISM-Lite: The Memory & Learning System

### 2.1 Storage Structure (MongoDB)
```json
{
  "user_id": "u123",
  "privacy_settings": {"allow_historical_patterns": true},
  "outcome_history": {
    "breathing_exercise": {"score": -1, "last_used": "2026-06-01"},
    "journal_prompt": {"score": 2, "last_used": "2026-06-02"}
  },
  "active_patterns": {...}
}
```

---

## 3. Hybrid Proactivity Workflow

### 3.1 Adaptive Scheduler
The scheduler (APScheduler) implements a **Response-Based Cooldown**:
*   *If Proactive Check-in was Acted Upon:* Interval remains 24h or decreases slightly.
*   *If Proactive Check-in was Ignored:* Interval increases to 36h-48h to prevent fatigue.

---

## 4. Normalization Layer (The "Data Silo" Bridge)
To handle inconsistent inputs from isolated modules, MindMate implements a `normalization_service`:
*   *Mood:* Maps 1-5 or 1-10 scales to a standard 0.0-1.0 float.
*   *Timestamps:* Forces all module data into UTC ISO8601.
*   *Enums:* Standardizes "Sad", "Low", "Upset" into a single `mood_category`.

---

## 5. Value Proposition for Zenark
*   **For Users:** It feels like the AI "knows" them. It doesn't repeat advice they've already ignored.
*   **For Clinicians:** The system provides a "Memory Dashboard" that summarizes user patterns, saving doctors hours of manual review.
*   **Technical Edge:** By using LangGraph, we solve the "State Explosion" problem of complex AI agents, making the system predictable and scalable.
