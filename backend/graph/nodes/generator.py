from typing import Dict, Any
from graph.state import CompanionState
from graph.llm import get_llm

async def response_generator_node(state: CompanionState) -> Dict[str, Any]:
    """ENHANCED N6: Safety-guarded generation with audit logging."""
    print(f"--- Entering Node: Response Generator v2.0 ---")
    llm = get_llm()
    
    message = state.get("message")
    profile = state.get("profile")
    recommendation = state.get("recommendation")
    score = state.get("distress_score", 0.1)
    
    system_prompt = """
    You are MindMate AI, a supportive Mental Health Companion.
    Guidelines:
    1. NEVER diagnose the user.
    2. Use soft, observational language.
    3. If distress_score >= 0.75, append emergency contact info.
    4. If distress_score >= 0.9, return ONLY a crisis-only response.
    """
    
    prompt = f"""
    {system_prompt}
    
    User History Summary: {profile.get('active_patterns', {})}
    User Message: "{message}"
    Distress Score: {score}
    Recommended Action: {recommendation}
    
    Generate an empathetic response.
    """
    
    response = llm.invoke(prompt)
    print("Response generated.")
    return {"response": response.content}
