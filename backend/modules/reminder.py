from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
from db.mongodb import MongoDB

class Reminder(BaseModel):
    user_id: str
    text: str
    due_at: datetime
    is_completed: bool = False
    priority: str = "medium" 
    created_at: datetime = datetime.now(timezone.utc)

async def create_reminder(reminder: Reminder):
    db = MongoDB.db
    result = await db.reminders.insert_one(reminder.model_dump())
    return str(result.inserted_id)

async def get_pending_reminders(user_id: str) -> List[dict]:
    db = MongoDB.db
    cursor = db.reminders.find({"user_id": user_id, "is_completed": False}).sort("due_at", 1)
    return await cursor.to_list(length=50)

async def mark_reminder_complete(reminder_id: str):
    db = MongoDB.db
    from bson import ObjectId
    await db.reminders.update_one({"_id": ObjectId(reminder_id)}, {"$set": {"is_completed": True}})
