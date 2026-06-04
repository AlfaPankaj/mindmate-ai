from datetime import datetime, timezone
from typing import List
from pydantic import BaseModel
from db.mongodb import MongoDB

class Exercise(BaseModel):
    name: str
    category: str  
    duration_minutes: int
    description: str

class ExerciseLog(BaseModel):
    user_id: str
    exercise_name: str
    completed_at: datetime = datetime.now(timezone.utc)
    duration_actual: int

async def get_recommended_exercises(category: str = None) -> List[dict]:
    db = MongoDB.db
    query = {"category": category} if category else {}
    cursor = db.exercises.find(query)
    return await cursor.to_list(length=20)

async def log_exercise_completion(log: ExerciseLog):
    db = MongoDB.db
    result = await db.exercise_logs.insert_one(log.model_dump())
    return str(result.inserted_id)
