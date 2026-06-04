# MindMate AI: Proactive Mental Health Companion

MindMate AI is a production-grade AI Companion Orchestrator designed to unify isolated wellness modules (Mood, Habits, Journals, etc.) into an intelligent, personalized layer. It leverages **LangGraph** for explicit reasoning, **ChromaDB** for semantic recall, and **PRISM-Lite** for longitudinal memory.

## 🚀 Key Features

*   **Stateful Orchestration (LangGraph):** Moves beyond simple LLM chains to a node-based architecture that handles Intent Classification, Risk Analysis, and Tool Execution through a persistent state.
*   **Semantic Memory (ChromaDB):** Implements semantic recall to recognize paraphrased past concerns (e.g., "racing mind at 2 AM" vs "can't sleep"), solving the limitations of keyword-based search.
*   **Longitudinal Intelligence (PRISM-Lite):** Learns behavioral patterns over time and stores them as structured intelligence in MongoDB to enable true personalization.
*   **Zero-Latency Safety Shield:** A hardcoded pre-filter that scans for 12 critical crisis phrases to provide instant, guaranteed clinical resources without waiting for LLM reasoning.
*   **Hybrid Proactivity:** Initiates conversations based on background data triggers (e.g., abandoned habits) or real-time mood dips, always respecting user consent.
*   **Real-time Intelligence Dashboard:** A dual-pane UI that visualizes the AI's internal "Pattern Bank" alongside current wellness data and habit streaks.

## 📸 Visual Walkthrough

### 1. Unified Intelligence Dashboard
The dashboard provides a "Glass Box" view of the AI's reasoning, displaying detected longitudinal patterns, habit streaks, and mood history in real-time.

![MindMate Dashboard](src/webpage_1.png)
*Initial view showing PRISM-Lite patterns and wellness logs.*

![MindMate Interaction](src/webpage_3.png)
*Active conversation showing semantic pattern detection and bar-chart mood visualization.*

### 2. Backend Orchestration
Witness the "Brain" in action. The terminal logs show how LangGraph moves through Classification, Memory Retrieval, and Tool Execution nodes for every message.

![Backend Logs](src/backend_server_teminal_01.png)
*LangGraph node execution and tool-calling logs.*

## 🛠️ Tech Stack

*   **Agent Framework:** LangGraph + LangChain
*   **LLM:** NVIDIA LLaMA 3.3 70B Instruct
*   **Vector DB:** ChromaDB (for Semantic Recall)
*   **Backend:** FastAPI + MongoDB (Motor)
*   **Frontend:** Streamlit
*   **Observability:** LangSmith
*   **Scheduling:** APScheduler

## 🏁 Getting Started

### 1. Prerequisites
*   Python 3.10+
*   MongoDB (Local or Atlas)
*   NVIDIA Developer API Key

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/AlfaPankaj/mindmate-ai
cd mindmate-ai

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your NVIDIA_API_KEY, MONGODB_URI, and LANGCHAIN_API_KEY
```

### 3. Seed Demo Data
```bash
python data/seed_db.py
```

### 4. Run the System
```bash
# Start Backend (Term 1)
cd backend
python main.py

# Start Frontend (Term 2)
cd frontend
streamlit run streamlit_app.py
```

## 🧠 Architecture Deep-Dive
For detailed technical information on the reasoning nodes, memory schemas, and the normalization layer, please refer to:
*   `docs/architecture.md`
*   `docs/technical_specs.md`
*   `docs/technical_explanation.md` (Presentation strategy)
*   `docs/manual_test_guide.md` (Scenario walkthroughs)

## ⚖️ Safety & Ethics
MindMate AI follows a "Safety-First" architecture. All user inputs pass through a Zero-Latency Crisis Pre-filter and a dedicated Safety node. The system is designed to complement professional therapy, not replace it, and includes explicit human-escalation pathways for genuine crises.
