# MindMate AI: Technical Deep-Dive & Workflow Specifications

This document provides a granular technical explanation of the production-hardened systems powering MindMate AI.

---

## 1. LangGraph: The Orchestration Engine

MindMate uses a stateful, cyclic graph with 8 nodes to move beyond linear LLM chains.

### 1.1 Node Execution Workflow (The v2.0 Pipeline)
1.  **N0: Crisis Pre-filter:** Sub-millisecond regex scan for 12 hard crisis phrases. Bypasses the graph if matched.
2.  **N1: Input Classifier:** Computes a **Distress Score (0.0-1.0)** and identifies intent (sleep, habit, etc.).
3.  **N2: Memory Retrieval:** Fetches the structured MongoDB profile + **ChromaDB Semantic Memories**.
4.  **N3: Pattern Detection:** Cross-module correlation (Mood <-> Habit) and semantic pattern matching.
5.  **N4: Recommendation Planner:** Deterministic decision using the **Readiness Matrix formula**.
6.  **N5: Tool Execution:** Orchestrates DB writes to normalized wellness modules (Habits, Moods).
7.  **N6: Safety-Guarded Generator:** Enforces a strictly supportive, non-diagnostic persona.
8.  **N7: Async Memory Updater:** Updates PRISM-Lite and Vector stores via **FastAPI BackgroundTasks**.

### 1.2 The State Object
```python
class CompanionState(TypedDict):
    user_id: str
    message: str
    profile: dict           # Fetched in N2
    module_data: dict       # Fetched in N2 (includes Semantic Recall)
    intent_category: str    # Set in N1
    distress_score: float   # Computed in N1
    detected_patterns: list # Set in N3
    recommendation: dict    # Planned in N4
    response: str           # Generated in N6
```

---

## 2. PRISM-Lite: Longitudinal Memory

The **User Intent Vector (UIV)** stores the "Long-term Intelligence" in MongoDB.

### 2.1 Enriched UIV Schema
```json
{
  "user_id": "u123",
  "active_patterns": {
    "sleep_difficulty": {"evidence_count": 4, "last_seen": "2026-06-03"}
  },
  "emotional_trajectory": {
    "mood_trend_7d": "declining",
    "last_positive_session": "2026-05-28"
  },
  "temporal_patterns": {
    "peak_engagement_hour": 21
  }
}
```

---

## 3. Semantic Store (ChromaDB)
MindMate implements **Semantic Recall** to solve the keyword gap.
*   **Ingestion:** Key user messages are embedded and stored with `user_id` and `timestamp` metadata.
*   **Retrieval:** In Node N2, we run a **Cosine Similarity Search** using the current user's message to find similar past distress or wellness events within a 14-day window.

---

## 4. Normalization & Graceful Degradation
*   **Normalization Layer:** All wellness modules (Habits, Moods) pass through a schema validator to ensure integers, floats, and strings are standardized before they reach the Pattern node.
*   **Circuit Breakers:** If the Habit module API is unreachable, the orchestrator defaults to a cached profile state, ensuring the AI never crashes during a demo.
