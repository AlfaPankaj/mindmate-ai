from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.prism_memory import get_prism_profile
from modules.habit import get_habits
from graph.workflow import companion_orchestrator
import logging

logger = logging.getLogger(__name__)

async def evaluate_proactive_triggers():
    """
    Scans the database for users who need a proactive check-in.
    Example: User abandoned a habit for 3+ days.
    """
    from db.mongodb import MongoDB
    db = MongoDB.db
    
    if db is None:
        return

    cursor = db.user_profiles.find({"preferences.checkin_enabled": True})
    
    async for profile_data in cursor:
        user_id = profile_data["user_id"]
        
        habits = await get_habits(user_id)
        abandoned_found = any(h.get("status") == "abandoned" for h in habits)
        
        if abandoned_found:
            logger.info(f"Triggering proactive check-in for user: {user_id}")
            
            initial_state = {
                "user_id": user_id,
                "message": "[SYSTEM_TRIGGER: HABIT_ABANDONED]",
                "is_proactive": True
            }
            
            await companion_orchestrator.ainvoke(initial_state)

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(evaluate_proactive_triggers, 'interval', minutes=60)
    scheduler.start()
    return scheduler
