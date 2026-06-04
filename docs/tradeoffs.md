# MindMate AI: Tradeoff Discussion

Building a production-grade AI companion involves critical technical and product tradeoffs. Below is a discussion of the choices made during this assignment.

---

## 1. MongoDB vs. PostgreSQL
*   **Choice:** MongoDB (NoSQL)
*   **Tradeoff:** PostgreSQL provides better relational integrity and complex joins, which is useful for audit logs. However, the wellness modules (Journals, Moods, Habits) have very different schemas.
*   **Rationale:** MongoDB's flexible document structure allowed for rapid iteration of the **PRISM-Lite** profile, where we can dynamically add new "Pattern" types without migrating a rigid SQL schema.

## 2. Rule-Based vs. LLM-Based Pattern Detection
*   **Choice:** Hybrid (Rule-Triggered + LLM-Refined)
*   **Tradeoff:** Using a 100% LLM-based detection is highly flexible but prone to "False Patterns" (hallucinations). 100% Rule-based is reliable but "dumb" and misses nuance.
*   **Rationale:** We use rules to fetch evidence from MongoDB (reliable) and then use the LLM (Llama 3.3) to classify the *sentiment* and *urgency* of that evidence. This provides the best of both worlds: clinical reliability with conversational depth.

## 3. Streamlit vs. React/Next.js
*   **Choice:** Streamlit
*   **Tradeoff:** A React frontend would offer better UX control, mobile responsiveness, and granular WebSocket handling.
*   **Rationale:** For a 3-day assignment prototype, Streamlit's ability to render complex data dashboards (bar charts, dataframes) directly from Python allowed us to spend **80% of our time on the Agent logic**, which is the primary focus of the "AI Agent Engineer" role.

## 4. APScheduler vs. Celery/Redis
*   **Choice:** APScheduler
*   **Tradeoff:** Celery is the industry standard for scalable background tasks and retry logic.
*   **Rationale:** APScheduler runs directly inside the FastAPI process, eliminating the need for an external Redis server for the MVP. This makes the project much easier for the evaluator to run on their local machine while still proving the **concept of proactivity**.

## 5. Local Memory vs. Vector Database (RAG)
*   **Choice:** Structured Profile (JSON) over flat Vector Store.
*   **Tradeoff:** Vector search (ChromaDB) is better for "finding that one thing I said 3 months ago."
*   **Rationale:** For mental health *coaching*, knowing that you have **sleep issues 5x** is more important than finding a specific sentence. The structured PRISM-Lite profile provides a cleaner signal for the AI to take **Action**, which is the goal of an Orchestrator.
