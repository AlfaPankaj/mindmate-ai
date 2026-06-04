# MindMate AI: Design Decisions

This document explains the technical and product rationale behind the core architectural choices of the MindMate AI Companion.

---

## 1. Why LangGraph?
**Decision:** Using a stateful graph instead of linear chains.
**Rationale:**
*   **Safety Enforcement:** In health tech, "Black Box" agents are dangerous. LangGraph allows us to architecturally guarantee that every response passes through a **Safety Generator (N6)**.
*   **Stateful reasoning:** LangGraph maintains a persistent `CompanionState`, allowing the AI to "think" through memory retrieval and pattern detection nodes before drafting a single word.

## 2. Hybrid Pattern Detection (Rules + Semantic Recall)
**Decision:** Complementing MongoDB keyword counts with **ChromaDB Vector Memory**.
**Rationale:**
*   **Beyond Keywords:** Users rarely repeat exact phrases. ChromaDB allows the AI to recognize that "tossing and turning at 3 AM" is semantically identical to "sleep difficulty," ensuring patterns aren't missed.
*   **Predictability:** Rules fetch the hard data, while the LLM (Llama 3.3) provides the sentiment context, ensuring the AI never "hallucinates" a pattern that doesn't exist in the DB.

## 3. Async Memory Updates (N7 Node)
**Decision:** Using **FastAPI BackgroundTasks** for memory and vector persistence.
**Rationale:**
*   **User Experience:** LLM reasoning already takes time. We cannot add another 1-2 seconds for DB writes. By decoupling the "Memory Updater" into a background task, the user receives their response immediately while the AI "learns" in the background.

## 4. Zero-Latency Crisis Shield (N0 Node)
**Decision:** Hardcoded **Regex Pre-filter** for 12 critical crisis phrases.
**Rationale:**
*   **Ethics:** If a user is in danger, waiting for an LLM to "classify" the intent is an ethical risk. Node N0 provides a sub-millisecond, guaranteed response with clinical hotline numbers, bypassing the reasoning graph entirely.

## 5. Computable Readiness Matrix
**Decision:** Deterministic formula for proactive intervention.
**Rationale:**
*   **Architecture Realism:** Instead of letting the LLM guess when to intervene, we use a formula: `Readiness = 0.4*(Mood) + 0.3*(Habit Completion) + 0.3*(Engagement)`. This ensures interventions are grounded in behavioral evidence.

## 6. Decoupled Tools Layer
**Decision:** Moving tool logic to `/backend/tools`.
**Rationale:**
*   **Scalability:** New modules (e.g., Nutrition) can be added as standalone tools without modifying the complex reasoning graph. It enables isolated testing and cleaner code organization.
