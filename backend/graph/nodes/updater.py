from typing import Dict, Any
from graph.state import CompanionState
from db.prism_memory import get_prism_profile, update_pattern

async def memory_update_node(state: CompanionState) -> Dict[str, Any]:
    """ENHANCED N7: Background-ready memory update."""
    print(f"--- Entering Node: Memory Update v2.0 ---")
    user_id = state["user_id"]
    category = state.get("intent_category")
    patterns = state.get("detected_patterns", [])
    
    if category and category != "general_chat":
        await update_pattern(user_id, category)
        
    for pattern in patterns:
        await update_pattern(user_id, pattern)
        
    profile = await get_prism_profile(user_id)
    print("Memory logic completed.")
    return {"profile": profile.model_dump() if profile else {}}
