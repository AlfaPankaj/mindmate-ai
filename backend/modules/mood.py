from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
from db.mongodb import MongoDB

class MoodLog(BaseModel):
    user_id: str
    score: int  
    note: Optional[str] = None
    timestamp: datetime = datetime.now(timezone.utc)

async def log_mood(mood: MoodLog):
    db = MongoDB.db
    result = await db.moods.insert_one(mood.model_dump())
    return str(result.inserted_id)

async def get_mood_history(user_id: str, limit: int = 7) -> List[dict]:
    db = MongoDB.db
    cursor = db.moods.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
    history = await cursor.to_list(length=limit)
    for entry in history:
        entry["_id"] = str(entry["_id"])
    return history
