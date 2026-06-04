from fastapi import FastAPI, Body, BackgroundTasks
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from db.mongodb import MongoDB
from core.config import get_settings
from graph.workflow import companion_orchestrator
from scheduler.checkin_scheduler import setup_scheduler
from graph.crisis import crisis_pre_filter

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect_to_storage()
    app.state.scheduler = setup_scheduler()
    yield
    await MongoDB.close_storage_connection()
    app.state.scheduler.shutdown()

app = FastAPI(
    title="MindMate AI v2.0",
    description="Production-hardened intelligence orchestrator for mental health.",
    version="2.0.0",
    lifespan=lifespan
)

@app.post("/chat")
async def chat(background_tasks: BackgroundTasks, user_id: str = Body(...), message: str = Body(...)):
    """
    Enhanced endpoint with N0: Crisis Pre-filter and Async Memory Updates.
    """
    # 1. N0: Crisis Pre-filter (Sub-millisecond regex scan)
    crisis_response = crisis_pre_filter(message)
    if crisis_response:
        background_tasks.add_task(log_crisis_event, user_id, message)
        return {"response": crisis_response, "intent": "crisis", "risk": "crisis"}

    initial_state = {
        "user_id": user_id,
        "message": message,
        "is_proactive": False,
        "detected_patterns": [] 
    }
    
    # 2. Invoke the Orchestrator
    result = await companion_orchestrator.ainvoke(initial_state)
    
    # 3. N7: Async Memory Updater (Decoupled from response latency)
    background_tasks.add_task(async_memory_updater, user_id, result)
    
    return {
        "response": result.get("response"),
        "intent": result.get("intent_category"),
        "patterns": result.get("detected_patterns"),
        "recommendation": result.get("recommendation")
    }

async def log_crisis_event(user_id: str, message: str):
    db = MongoDB.db
    if db is not None:
        await db.crisis_logs.insert_one({
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.now(timezone.utc)
        })

async def async_memory_updater(user_id: str, result: dict):
    """Handles PRISM-Lite and Vector Memory updates in background."""
    from db.prism_memory import update_pattern
    from memory.prism_vector import vector_memory
    
    category = result.get("intent_category")
    if category and category != "general_chat":
        await update_pattern(user_id, category)
        
    # Update semantic ChromaDB memory
    vector_memory.add_memory(
        user_id, 
        result.get("message", ""), 
        {"intent": category, "timestamp": str(datetime.now(timezone.utc))}
    )

@app.get("/profile/{user_id}")
async def get_profile(user_id: str):
    from db.prism_memory import get_prism_profile
    profile = await get_prism_profile(user_id)
    return profile.model_dump() if profile else {"error": "Profile not found"}

@app.get("/habits/{user_id}")
async def habits(user_id: str):
    from modules.habit import get_habits
    return await get_habits(user_id)

@app.get("/moods/{user_id}")
async def moods(user_id: str):
    from modules.mood import get_mood_history
    return await get_mood_history(user_id)

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "database": "connected" if MongoDB.client else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
