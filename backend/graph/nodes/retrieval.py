from typing import Dict, Any
from graph.state import CompanionState
from db.prism_memory import get_prism_profile, create_initial_profile
from modules.mood import get_mood_history
from modules.habit import get_habits
from memory.prism_vector import vector_memory

async def memory_retrieval_node(state: CompanionState) -> Dict[str, Any]:
    """ENHANCED N2: Queries BOTH MongoDB UIV and ChromaDB Vector Store."""
    print(f"--- Entering Node: Memory Retrieval v2.0 ---")
    user_id = state["user_id"]
    message = state["message"]
    
    # 1. Structured Data from MongoDB
    profile = await get_prism_profile(user_id)
    if not profile:
        profile = await create_initial_profile(user_id)
        
    moods = await get_mood_history(user_id, limit=7)
    habits = await get_habits(user_id)
    
    # 2. Semantic Data from ChromaDB (Semantic Recall)
    semantic_memories = vector_memory.search_memories(user_id, message, n_results=3)
    
    return {
        "profile": profile.model_dump(),
        "module_data": {
            "recent_moods": moods,
            "active_habits": habits,
            "semantic_memories": semantic_memories.get("documents", [[]])[0]
        }
    }
