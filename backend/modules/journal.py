from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
from db.mongodb import MongoDB

class JournalEntry(BaseModel):
    user_id: str
    content: str
    themes: List[str] = []
    sentiment: Optional[float] = None  
    timestamp: datetime = datetime.now(timezone.utc)

async def create_journal_entry(entry: JournalEntry):
    db = MongoDB.db
    result = await db.journals.insert_one(entry.model_dump())
    return str(result.inserted_id)

async def get_journal_history(user_id: str, limit: int = 10):
    db = MongoDB.db
    cursor = db.journals.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
    entries = await cursor.to_list(length=limit)
    for entry in entries:
        entry["_id"] = str(entry["_id"])
    return entries
