from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ToolResult(BaseModel):
    tool_name: str
    success: bool
    error: Optional[str] = None
    executed_at: datetime = datetime.utcnow()

class HabitToolResult(ToolResult):
    habit_id: Optional[str] = None
    habit_name: str
    streak_count: int = 0

class MoodToolResult(ToolResult):
    score: int
    note: Optional[str] = None

class ExerciseToolResult(ToolResult):
    exercise_name: str
    category: str
