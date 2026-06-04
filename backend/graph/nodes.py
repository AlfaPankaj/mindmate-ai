import json
from typing import Dict, Any
from graph.state import CompanionState
from graph.llm import get_llm
from db.prism_memory import get_prism_profile, create_initial_profile
from modules.mood import get_mood_history
from modules.habit import get_habits
from modules.journal import get_journal_history

llm = get_llm()

async def input_classifier_node(state: CompanionState) -> Dict[str, Any]:
    """Classifies the user input into categories and risk levels."""
    print(f"--- Entering Node: Input Classifier ---")
    message = state.get("message", "")
    
    prompt = f"""
    Classify the following user message from a mental health app user.
    Categories: sleep_issue, habit_problem, mood_low, journal_reflection, general_chat, crisis.
    Risk Levels: safe, mild, high, crisis.
    
    Return ONLY a JSON object like:
    {{"category": "category_name", "risk": "risk_level"}}
    
    Message: "{message}"
    """
    
    response = llm.invoke(prompt)
    try:
        result = json.loads(response.content)
        print(f"Intent: {result.get('category')} | Risk: {result.get('risk')}")
        return {
            "intent_category": result.get("category", "general_chat"),
            "risk_level": result.get("risk", "safe")
        }
    except:
        return {"intent_category": "general_chat", "risk_level": "safe"}

async def memory_retrieval_node(state: CompanionState) -> Dict[str, Any]:
    """Fetches user profile and recent module data."""
    print(f"--- Entering Node: Memory Retrieval ---")
    user_id = state["user_id"]
    
    profile = await get_prism_profile(user_id)
    if not profile:
        profile = await create_initial_profile(user_id)
        
    moods = await get_mood_history(user_id, limit=7)
    habits = await get_habits(user_id)
    journals = await get_journal_history(user_id, limit=3)
    
    print(f"Retrieved {len(habits)} habits and {len(moods)} mood logs.")
    
    module_data = {
        "recent_moods": moods,
        "active_habits": habits,
        "recent_journals": journals
    }
    
    return {
        "profile": profile.model_dump(),
        "module_data": module_data
    }

async def pattern_detection_node(state: CompanionState) -> Dict[str, Any]:
    """Correlates current message with history to find recurring patterns."""
    print(f"--- Entering Node: Pattern Detection ---")
    category = state.get("intent_category")
    profile = state.get("profile", {})
    module_data = state.get("module_data", {})
    
    patterns = []
    active_patterns = profile.get("active_patterns", {})
    
    if category == "sleep_issue":
        if "sleep_difficulty" in active_patterns:
            patterns.append("recurring_sleep_difficulty")
        
    habits = module_data.get("active_habits", [])
    if category == "habit_problem":
        for habit in habits:
            if habit.get("status") == "abandoned":
                patterns.append("habit_dropoff_detected")
    
    print(f"Detected Patterns: {patterns}")
    return {"detected_patterns": patterns}

async def recommendation_planner_node(state: CompanionState) -> Dict[str, Any]:
    """Decides on the best intervention tool."""
    print(f"--- Entering Node: Recommendation Planner ---")
    patterns = state.get("detected_patterns", [])
    category = state.get("intent_category")
    risk = state.get("risk_level", "safe")
    
    if risk in ["high", "crisis"]:
        print("Safety Alert: Escalating to safety module.")
        return {"recommendation": {"action": "escalate", "module": "safety"}}
        
    rec = {"action": "empathetic_chat", "module": "core"}
    if "recurring_sleep_difficulty" in patterns:
        rec = {"action": "suggest_exercise", "category": "breathing"}
    elif category == "mood_low":
        rec = {"action": "log_mood", "module": "mood", "score": 2}
    elif any(word in state["message"].lower() for word in ["calmer", "better", "great", "helped"]):
        rec = {"action": "log_mood", "module": "mood", "score": 5}
    elif any(word in state["message"].lower() for word in ["start", "habit", "track", "reading"]):
        habit_name = "Reading before bed" if "reading" in state["message"].lower() else "New Wellness Habit"
        rec = {"action": "create_habit", "module": "habit", "name": habit_name}
    
    print(f"Recommendation: {rec['action']}")
    return {"recommendation": rec}
async def tool_execution_node(state: CompanionState) -> Dict[str, Any]:
    """Executes the recommended tool using the decentralized tools layer."""
    print(f"--- Entering Node: Tool Execution ---")
    rec = state.get("recommendation", {})
    user_id = state["user_id"]

    from tools.wellness_tools import mood_tool, habit_tool, exercise_tool

    if rec.get("action") == "log_mood":
        await mood_tool(user_id, score=rec.get("score", 3), note=state["message"])
        print("Action: Mood Tool executed.")

    elif rec.get("action") == "suggest_exercise":
        await exercise_tool(user_id, category=rec.get("category", "breathing"))
        print("Action: Exercise Tool executed.")

    elif rec.get("action") == "create_habit":
        await habit_tool(user_id, action="create_habit", name=rec.get("name", "New Habit"))
        print("Action: Habit Tool executed.")

    return {}


async def response_generator_node(state: CompanionState) -> Dict[str, Any]:
    """Generates the final clinical-style response."""
    print(f"--- Entering Node: Response Generator ---")
    llm = get_llm()
    
    message = state.get("message")
    profile = state.get("profile")
    recommendation = state.get("recommendation")
    risk = state.get("risk_level")
    
    system_prompt = """
    You are MindMate AI, a supportive Mental Health Companion.
    Guidelines:
    1. NEVER diagnose the user (e.g., don't say 'You have depression').
    2. Use soft, observational language ('I noticed...', 'It sounds like...').
    3. Be action-oriented but gentle.
    4. If the risk level is high/crisis, provide emergency contact info immediately.
    """
    
    prompt = f"""
    {system_prompt}
    
    User History Summary: {profile.get('active_patterns', {})}
    User Message: "{message}"
    Risk Level: {risk}
    Recommended Action: {recommendation}
    
    Generate an empathetic response to the user.
    """
    
    response = llm.invoke(prompt)
    print("Response generated.")
    return {"response": response.content}

async def memory_update_node(state: CompanionState) -> Dict[str, Any]:
    """Updates the PRISM-Lite profile based on the session outcome."""
    print(f"--- Entering Node: Memory Update ---")
    user_id = state["user_id"]
    category = state.get("intent_category")
    patterns = state.get("detected_patterns", [])
    
    from db.prism_memory import update_pattern
    
    if category and category != "general_chat":
        await update_pattern(user_id, category)
        
    for pattern in patterns:
        await update_pattern(user_id, pattern)
        
    print("PRISM-Lite profile updated in MongoDB.")
    return {"profile": await get_prism_profile(user_id)}
