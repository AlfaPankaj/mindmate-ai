from modules.habit import create_habit, Habit
from modules.mood import log_mood, MoodLog
from modules.exercise import log_exercise_completion, ExerciseLog

async def habit_tool(user_id: str, action: str, name: str = None):
    if action == "create_habit":
        await create_habit(Habit(user_id=user_id, name=name))
        return f"Habit '{name}' created."

async def mood_tool(user_id: str, score: int, note: str):
    await log_mood(MoodLog(user_id=user_id, score=score, note=note))
    return "Mood logged."

async def exercise_tool(user_id: str, category: str):
    await log_exercise_completion(ExerciseLog(
        user_id=user_id, 
        exercise_name=f"{category} exercise", 
        duration_actual=2
    ))
    return f"{category} exercise logged."
