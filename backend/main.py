from fastapi import FastAPI, Body
from contextlib import asynccontextmanager
from db.mongodb import MongoDB
from core.config import get_settings
from graph.workflow import companion_orchestrator
from scheduler.checkin_scheduler import setup_scheduler

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect_to_storage()
    app.state.scheduler = setup_scheduler()
    yield
    await MongoDB.close_storage_connection()
    app.state.scheduler.shutdown()

app = FastAPI(
    title="MindMate AI API",
    description="The central intelligence orchestrator for mental health wellness modules.",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/chat")
async def chat(user_id: str = Body(...), message: str = Body(...)):
    """
    Main endpoint to interact with the AI Companion.
    """
    initial_state = {
        "user_id": user_id,
        "message": message,
        "is_proactive": False,
        "detected_patterns": [] 
    }
    
    result = await companion_orchestrator.ainvoke(initial_state)
    
    return {
        "response": result.get("response"),
        "intent": result.get("intent_category"),
        "patterns": result.get("detected_patterns"),
        "recommendation": result.get("recommendation")
    }

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
