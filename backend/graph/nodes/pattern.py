from typing import Dict, Any
from graph.state import CompanionState

async def pattern_detection_node(state: CompanionState) -> Dict[str, Any]:
    """ENHANCED N3: Cross-module correlation and semantic pattern matching."""
    print(f"--- Entering Node: Pattern Detection v2.0 ---")
    category = state.get("intent_category")
    module_data = state.get("module_data", {})
    semantic_history = module_data.get("semantic_memories", [])
    
    patterns = []
    
    # Semantic match check
    if any("sleep" in str(m).lower() for m in semantic_history):
        patterns.append("recurring_semantic_sleep_difficulty")
        
    # Cross-module: Poor sleep -> Low mood
    moods = module_data.get("recent_moods", [])
    if len(moods) > 0 and moods[0].get("score", 5) < 3 and category == "sleep_issue":
        patterns.append("sleep_mood_correlation_detected")
    
    print(f"Detected Patterns: {patterns}")
    return {"detected_patterns": patterns}
