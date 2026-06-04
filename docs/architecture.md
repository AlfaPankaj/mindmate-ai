# MindMate AI: Technical Implementation Plan

## 1. Executive Summary
MindMate AI is a **Mental Health AI Companion Orchestrator** designed to unify isolated wellness modules (Mood, Habits, Journaling, etc.) into a single intelligent layer. Unlike traditional chatbots, MindMate uses **LangGraph** for explicit reasoning, **Hybrid Proactivity** for user engagement, and **PRISM-Lite Memory** to learn behavioral patterns over time.

---

## 2. MVP Scope: The "Sleep Pattern" Vertical Slice
To demonstrate maximum impact for the assignment, the MVP will focus on a high-signal vertical slice: **Recurring Sleep Difficulty**.

### Vertical Slice Workflow:
1.  **Detection:** User mentions sleep issues across 2-3 conversations.
2.  **Analysis:** LangGraph identifies the "Intention-Action Gap" (user wants better sleep but skips habits).
3.  **Proactivity:** Background scheduler triggers a soft check-in.
4.  **Intervention:** AI recommends a specific breathing exercise and creates a "Wind-down" reminder.
5.  **Validation:** AI tracks if the habit is completed and updates the long-term profile.

---

## 3. Core Architecture

### 3.1 The LangGraph Orchestrator
The "Brain" is modeled as a stateful graph to ensure safety and explainability.

| Node | Responsibility |
| :--- | :--- |
| **Input Classifier** | Categorizes intent (e.g., `sleep_issue`, `risk_check`). |
| **Memory Retrieval** | Fetches PRISM-Lite facts with **Consent-Aware Filters**. |
| **Pattern Detection** | Rule-based + LLM analysis with **Normalized Module Data**. |
| **Risk & Safety** | **Hybrid Verification** (Keywords + LLM) for nuanced safety. |
| **Recommendation Planner** | Decides action based on **Outcome Feedback History**. |
| **Tool Execution** | Directly interacts with Mood/Habit/Journal APIs. |
| **Response Generator** | Crafts the final, personalized output. |

### 3.2 Hybrid Proactivity Engine
*   **Manual:** "Daily Check-in" button in UI.
*   **Scheduled:** **Adaptive Check-ins** via APScheduler. Backs off if ignored, increases if acted upon.
*   **Event-Driven:** Triggered immediately by a "Low Mood" entry.

### 3.3 Tech Stack
*   **Backend:** FastAPI + Python 3.10+
*   **Frontend:** Streamlit (Dual-pane: Chat + Module Dashboard)
*   **Orchestration:** LangGraph + LangChain
*   **Database:** MongoDB (Flexible document storage)
*   **LLM:** NVIDIA API (LLaMA 3 70B Instruct)

---

## 4. Technical Depth & Innovation

### 4.1 Explicit Reasoning vs. Black-Box Chaining
By using LangGraph, we expose the *why* behind every AI action. The system logs state transitions, proving it follows a structured reasoning path.

### 4.2 Systems Thinking: Handling Real-World Gaps
To move beyond a "demo-only" build, the prototype implements:
*   **Schema Normalization:** A layer to bridge data silos between inconsistent modules.
*   **Consent Gradients:** Users control how deeply the AI "mines" their history (balancing personalization vs. privacy).
*   **Outcome Feedback Loop:** The AI tracks if a suggestion (e.g., breathing exercise) actually helped, refining its `Recommendation Planner` score.

### 4.3 Responsible AI (Hybrid Safety Node)
The Safety Node combines keyword screening with a secondary **lightweight LLM verification** pass. This reduces false positives (e.g., academic research vs. genuine intent) while maintaining a clinical safety net.

---

## 5. Evaluation & Metrics
The prototype will be evaluated on the following simulated metrics:
1.  **Pattern Precision:** Accuracy of identifying "Sleep Difficulty" vs. a one-off comment.
2.  **Conversion Rate:** % of proactive suggestions that result in a user taking action.
3.  **Outcome Efficacy:** % of user-reported "Helped" outcomes vs. "No Change."
4.  **Safety Reliability:** False positive/negative rate of the Hybrid Risk Node.

---

## 6. Project Roadmap

### Phase 1: Foundation (Day 1)
*   Setup FastAPI environment and MongoDB schemas.
*   Build mock APIs for Mood, Habit, and Journal modules.
*   Setup Streamlit basic layout.

### Phase 2: The Graph (Day 2)
*   Implement LangGraph nodes for Classifier, Memory, and Safety.
*   Connect to NVIDIA API for LLaMA 3 inference.
*   Define Tool calling logic for DB updates.

### Phase 3: Proactivity & Demo (Day 3)
*   Implement APScheduler for background triggers.
*   Develop the "Sleep Vertical Slice" demo scenario.
*   Finalize Documentation (README, Tradeoffs, Architecture).
