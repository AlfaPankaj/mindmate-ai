# MindMate AI: Tradeoff Discussion

Building a production-grade AI companion involves critical technical and product tradeoffs. Below is a discussion of the choices made for this system.

---

## 1. MongoDB vs. PostgreSQL
*   **Choice:** MongoDB (NoSQL)
*   **Tradeoff:** PostgreSQL provides better relational integrity, but wellness data (Journals, Moods, Habits) have highly divergent schemas.
*   **Rationale:** MongoDB's document model allowed us to store the **PRISM-Lite** User Intent Vector (UIV) as a single nested object. This makes fetching the user's entire history a single database hit, significantly reducing latency compared to complex SQL joins.

## 2. Rule-Based vs. LLM-Based Safety
*   **Choice:** Multi-Layered (Regex + LLM-Scoring)
*   **Tradeoff:** Relying purely on an LLM for safety (N1 Node) is flexible but has 2-3s of latency. Regex (N0 Node) is rigid but instant.
*   **Rationale:** We use **Regex (N0)** to guarantee instant safety for known crisis phrases. We then use the **LLM (N1)** to detect nuanced distress (e.g., "hopelessness") that regex might miss. This layered defense is essential for clinical responsibility.

## 3. ChromaDB vs. Keyword Search
*   **Choice:** ChromaDB (Vector Search)
*   **Tradeoff:** Keyword search is 100% predictable but fails if the user paraphrases (e.g., "I'm exhausted" vs "Can't sleep"). Vector search adds overhead but understands meaning.
*   **Rationale:** We integrated **ChromaDB** because longitudinal wellness support depends on recognizing **Semantic Patterns**. If a user mentions "racing mind" today and "insomnia" tomorrow, the AI must link them to form a coherent pattern.

## 4. Async Tasks vs. Synchronous Flow
*   **Choice:** Asynchronous Memory Updates (BackgroundTask)
*   **Tradeoff:** Synchronous updates ensure the DB is updated *before* the user sees the response.
*   **Rationale:** User perception of speed is the most important factor in engagement. By moving memory persistence to **FastAPI BackgroundTasks**, we shaved ~1.5 seconds off every message response time, maintaining a snappy, conversational feel while ensuring the data is "eventually consistent."

## 5. Local Chroma Store vs. Cloud Vector DB
*   **Choice:** Local Persistent Storage
*   **Tradeoff:** Cloud stores like Qdrant/Pinecone scale better but require more infra management for an MVP.
*   **Rationale:** For this prototype, a local Chroma persistent client allowed us to demonstrate **Semantic Memory** without adding complex cloud dependencies, keeping the system portable for the assignment evaluator.
