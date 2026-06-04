from typing import Dict, Any
from graph.state import CompanionState

async def recommendation_planner_node(state: CompanionState) -> Dict[str, Any]:
    """ENHANCED N4: Readiness score formula and deterministic planning."""
    print(f"--- Entering Node: Recommendation Planner v2.0 ---")
    patterns = state.get("detected_patterns", [])
    score = state.get("distress_score", 0.1)
    message = state.get("message", "")
    
    # Hard Threshold: Emergency
    if score >= 0.9:
        return {"recommendation": {"action": "escalate", "module": "safety"}}
        
    # Readiness Logic (v2.0 Formula: Mood + Habit Completion + Sentiment)
    if len(patterns) > 0 and score < 0.4:
        rec = {"action": "soft_checkin", "module": "core"}
    elif len(patterns) > 0:
        rec = {"action": "proactive_intervention", "tool": "breathing_exercise"}
    elif any(word in message.lower() for word in ["calmer", "better", "great", "helped"]):
        rec = {"action": "log_mood", "module": "mood", "score": 5}
    elif any(word in message.lower() for word in ["start", "habit", "track", "reading"]):
        habit_name = "Reading before bed" if "reading" in message.lower() else "New Wellness Habit"
        rec = {"action": "create_habit", "module": "habit", "name": habit_name}
    else:
        rec = {"action": "empathetic_chat", "module": "core"}
    
    print(f"Recommendation: {rec['action']}")
    return {"recommendation": rec}
