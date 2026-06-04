import json
from typing import Dict, Any
from graph.state import CompanionState
from graph.llm import get_llm

llm = get_llm()

async def input_classifier_node(state: CompanionState) -> Dict[str, Any]:
    """ENHANCED N1: Computes distress_score and classifies intent."""
    print(f"--- Entering Node: Input Classifier v2.0 ---")
    message = state.get("message", "")
    
    prompt = f"""
    Analyze this message from a mental health user.
    1. Classify Intent: sleep_issue, habit_problem, mood_low, journal_reflection, general_chat.
    2. Compute Distress Score (0.0 to 1.0): 0.9 is crisis, 0.1 is neutral.
    
    Return ONLY a JSON object:
    {{"category": "category_name", "distress_score": 0.0}}
    
    Message: "{message}"
    """
    
    response = llm.invoke(prompt)
    try:
        result = json.loads(response.content)
        score = result.get("distress_score", 0.1)
        risk = "safe"
        if score >= 0.9: risk = "crisis"
        elif score >= 0.75: risk = "high"
        
        return {
            "intent_category": result.get("category", "general_chat"),
            "risk_level": risk,
            "distress_score": score
        }
    except:
        return {"intent_category": "general_chat", "risk_level": "safe", "distress_score": 0.1}
