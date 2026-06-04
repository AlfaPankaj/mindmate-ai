# MindMate AI: Technical Explanation & Interview Guide

This document provides a granular walkthrough of the production-hardened features of MindMate AI.

---

## 🛠️ Part 1: Codebase Walkthrough

### 1. Zero-Latency Crisis Pre-filter (N0)
**File:** `/backend/graph/nodes/crisis.py`  
**Rationale:** Clinical safety. We use a regex-based pre-filter to ensure users in immediate danger get hotline numbers instantly, bypassing the LLM.

```python
CRISIS_PHRASES = [r"\bwant to die\b", r"\bend my life\b", ...]
def crisis_pre_filter(message: str):
    # Regex scan for hard crisis phrases
    # Returns static clinical resource response if matched
```

### 2. Semantic Memory & Retrieval (N2)
**File:** `/backend/memory/prism_vector.py` and `/backend/graph/nodes/retrieval.py`  
**Rationale:** Overcoming the keyword gap. We use **ChromaDB** to find semantically similar sessions.

```python
# Retrieval logic
semantic_memories = vector_memory.search_memories(user_id, message, n_results=3)
# Injects previous "racing mind" context even if user now says "I'm tired"
```

### 3. Computable Readiness Planner (N4)
**File:** `/backend/graph/nodes/planner.py`  
**Rationale:** Deterministic intervention. We move from LLM-guessing to a scored formula based on habit completion and mood trends.

```python
if len(patterns) > 0 and distress_score < 0.4:
    rec = {"action": "soft_checkin"} # Low readiness -> Soft nudge
elif len(patterns) > 0:
    rec = {"action": "proactive_intervention"} # High readiness -> Specific tool
```

### 4. Asynchronous Memory Updater (N7)
**File:** `/backend/main.py` and `/backend/graph/nodes/updater.py`  
**Rationale:** Performance optimization. We use **FastAPI BackgroundTasks** to update MongoDB and ChromaDB after the response is sent.

```python
@app.post("/chat")
async def chat(background_tasks: BackgroundTasks, ...):
    response = await orchestrator.ainvoke(...)
    background_tasks.add_task(async_memory_updater, user_id, result)
    return response # User gets response 1-2s faster
```

---

## 🎙️ Part 2: Interview Presentation Strategy

### 1. The "Orchestrator" Narrative
Don't say "I built a chatbot." Say:
> *"I built a **Wellness Orchestrator**. The system unifies isolated data silos—mood, habits, and journals—into a central intelligence layer using a persistent state graph."*

### 2. Highlighting Clinical Safety
Explain the layered defense:
> *"Safety isn't an afterthought. I implemented a three-layer defense:
> 1. A hardcoded **Regex Pre-filter** for instant crisis response.
> 2. An **LLM-based Distress Scorer** for nuanced risk detection.
> 3. A strictly **Non-Diagnostic Clinical Persona** node."*

### 3. Demonstrating "Learning"
Point to the **Detected Patterns** in the UI:
> *"MindMate doesn't just chat; it learns. Using **ChromaDB**, it recognizes when a user's current 'mind racing' is actually a recurrence of a sleep pattern identified two weeks ago, allowing for longitudinal support."*

---

## 💡 Key Terminology for your Interview
*   **"Stateful Persistence"**: How LangGraph keeps the companion coherent.
*   **"Semantic Recall"**: Using Vector DBs to understand meaning, not just words.
*   **"Graceful Degradation"**: How normalization handles messy data from different modules.
*   **"Asynchronous Consistency"**: How background tasks keep the UI fast.
