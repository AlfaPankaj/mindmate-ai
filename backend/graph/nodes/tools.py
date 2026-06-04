from typing import Dict, Any
from graph.state import CompanionState

async def tool_execution_node(state: CompanionState) -> Dict[str, Any]:
    """ENHANCED N5: Decoupled tool execution with typed results."""
    print(f"--- Entering Node: Tool Execution v2.0 ---")
    rec = state.get("recommendation", {})
    user_id = state["user_id"]
    
    from tools.wellness_tools import mood_tool, habit_tool, exercise_tool
    
    if rec.get("action") == "log_mood":
        await mood_tool(user_id, score=rec.get("score", 3), note=state["message"])
        
    elif rec.get("action") == "suggest_exercise":
        await exercise_tool(user_id, category=rec.get("category", "breathing"))

    elif rec.get("action") == "create_habit":
        await habit_tool(user_id, action="create_habit", name=rec.get("name", "New Habit"))

    return {}
