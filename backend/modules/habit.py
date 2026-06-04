from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
from db.mongodb import MongoDB

class Habit(BaseModel):
    user_id: str
    name: str
    frequency: str = "daily"
    status: str = "active"  
    streak: int = 0
    last_completed: Optional[datetime] = None
    created_at: datetime = datetime.now(timezone.utc)

async def create_habit(habit: Habit):
    db = MongoDB.db
    result = await db.habits.insert_one(habit.model_dump())
    return str(result.inserted_id)

async def get_habits(user_id: str) -> List[dict]:
    db = MongoDB.db
    cursor = db.habits.find({"user_id": user_id})
    habits = await cursor.to_list(length=100)
    for habit in habits:
        habit["_id"] = str(habit["_id"])
    return habits

async def update_habit_status(habit_id: str, status: str):
    db = MongoDB.db
    from bson import ObjectId
    await db.habits.update_one({"_id": ObjectId(habit_id)}, {"$set": {"status": status}})
