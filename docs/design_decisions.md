# MindMate AI: Design Decisions

This document explains the rationale behind the key architectural and product decisions made for the MindMate AI Companion.

---

## 1. Why LangGraph?
**Decision:** Using a stateful graph instead of linear LangChain chains.
**Rationale:**
*   **Predictability:** Linear chains often "hallucinate" the next step. LangGraph allows us to define rigid nodes (e.g., Safety, Memory Retrieval) that the AI *must* pass through.
*   **State Management:** LangGraph maintains a persistent `CompanionState`, allowing the AI to "remember" its reasoning steps during a single interaction.
*   **Cycles:** Mental health support often requires iterative loops (e.g., asking for more info). Graphs support this naturally, while chains do not.

## 2. PRISM-Lite Memory Architecture
**Decision:** Storing structured "User Patterns" in MongoDB instead of raw chat logs for long-term memory.
**Rationale:**
*   **Efficiency:** Reading 100 past chat logs is slow and token-intensive. Reading one `UserPattern` object (e.g., `sleep_difficulty: evidence_count=4`) is near-instant and provides direct "longitudinal intelligence."
*   **Learning:** By updating the `evidence_count` and `last_seen` timestamps, the AI "learns" user behavior trends over weeks, enabling true personalization.

## 3. Hybrid Proactivity Triggers
**Decision:** Combining manual UI buttons, background scheduled cron jobs, and event-driven triggers.
**Rationale:**
*   **Safety & Consent:** Blind proactivity (cron jobs only) can feel invasive or unsafe in mental health. By using a "Hybrid" approach, we ensure the AI only reaches out when evidence is high AND user consent is active.
*   **Immediate Support:** Event-driven triggers (like logging a low mood) allow the AI to offer help in the moment of need, not hours later.

## 4. Decoupled Tools Layer
**Decision:** Moving tool logic to `/backend/tools` separate from the reasoning nodes.
**Rationale:**
*   **Scalability:** Allows adding new modules (e.g., a "Nutrition" tracker) by simply adding a new tool file without modifying the core AI brain.
*   **Testability:** Tools can be unit-tested with mock database data to ensure the platform logic is sound before testing the AI's reasoning.

## 5. Non-Diagnostic Clinical Persona
**Decision:** Strict system prompting and a dedicated Generator node.
**Rationale:**
*   **Ethics:** As an AI companion, MindMate must avoid making medical claims (e.g., "You have insomnia").
*   **Trust:** By using observational language ("I noticed your sleep logs...") rather than clinical labels, we build a supportive, peer-like relationship with the user.
