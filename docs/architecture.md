# MindMate AI: Technical Implementation Plan

## 1. Executive Summary
MindMate AI is a **Mental Health AI Companion Orchestrator** designed to unify isolated wellness modules (Mood, Habits, Journaling, etc.) into a single intelligent layer. Unlike traditional chatbots, MindMate uses **LangGraph** for explicit reasoning, **Hybrid Proactivity** for user engagement, and **PRISM-Lite Memory** with **Semantic Recall** to learn behavioral patterns over time.

---

## 2. MVP Scope: The "Sleep Pattern" Vertical Slice
To demonstrate maximum impact for the assignment, the MVP focuses on a high-signal vertical slice: **Recurring Sleep Difficulty**.

### Vertical Slice Workflow:
1.  **Detection:** User mentions sleep issues across conversations (e.g., "I'm tired" -> "Can't sleep").
2.  **Analysis:** LangGraph identifies the **Semantic Correlation** between disparate utterances using ChromaDB.
3.  **Proactivity:** Background scheduler triggers a soft check-in if habits are abandoned.
4.  **Intervention:** AI recommends a specific breathing exercise and creates a "Wind-down" habit.
5.  **Validation:** AI tracks if the habit is completed and updates the long-term emotional trajectory.

---

## 3. Core Architecture

### 3.1 The LangGraph Orchestrator (Production-Hardened)
The "Brain" is modeled as a stateful graph with 8 distinct nodes to ensure safety and auditability.

| Node | Responsibility |
| :--- | :--- |
| **N0: Crisis Pre-filter** | **Hardcoded Regex scan** for 12 crisis phrases. Zero-latency response. |
| **N1: Input Classifier** | Categorizes intent and computes a **Distress Score (0.0-1.0)**. |
| **N2: Memory Retrieval** | Fetches MongoDB profile and **ChromaDB Semantic Memories**. |
| **N3: Pattern Detection** | **Cross-module correlation** (e.g., Sleep <-> Mood) + Semantic matching. |
| **N4: Recommendation Planner** | Deterministic decision based on the **Readiness Matrix formula**. |
| **N5: Tool Execution** | **Decoupled layer** interacting with normalized wellness APIs. |
| **N6: Safety-Guarded Generator** | Enforces clinical persona; appends resources for distress_score >= 0.75. |
| **N7: Async Memory Updater** | **FastAPI BackgroundTask**; updates UIV and Vector store without latency. |

### 3.2 Hybrid Proactivity Engine
*   **Manual:** "Daily Check-in" button in UI.
*   **Scheduled:** **Adaptive Check-ins** via APScheduler. Backs off if ignored, increases if acted upon.
*   **Event-Driven:** Immediate AI intervention triggered by a "Low Mood" or "Crisis" entry.

### 3.3 Tech Stack
*   **Backend:** FastAPI (Async)
*   **Frontend:** Streamlit (Dual-pane Dashboard)
*   **Orchestration:** LangGraph + LangChain
*   **Semantic Store:** ChromaDB
*   **Database:** MongoDB Atlas (Motor Driver)
*   **LLM:** NVIDIA API (LLaMA 3.3 70B Instruct)

---

## 4. Technical Depth & Innovation

### 4.1 Explicit Reasoning vs. Black-Box Chaining
By using LangGraph, we expose the *why* behind every AI action. The system logs state transitions, proving it follows a structured reasoning path rather than guessing.

### 4.2 Systems Thinking: Handling Real-World Gaps
*   **Schema Normalization:** Bridges data silos between inconsistent modules.
*   **Consent Gradients:** Users control profiling depth (Personalization vs. Privacy).
*   **Outcome Feedback Loop:** Tracks if suggestions (e.g., breathing) helped, refining future planning.
*   **Zero-Latency Crisis Path:** Bypasses LLM reasoning entirely for imminent risks.

---

## 5. Evaluation & Metrics
The prototype evaluates the system on:
1.  **Pattern Precision:** Accuracy of identifying "Sleep Difficulty" vs. one-off comments.
2.  **Conversion Rate:** % of proactive suggestions resulting in user action.
3.  **Outcome Efficacy:** % of user-reported "Helped" outcomes.
4.  **Safety Reliability:** 100% adherence to Crisis Pre-filter protocols.
