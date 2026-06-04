from langgraph.graph import StateGraph, END
from graph.state import CompanionState
from graph.nodes import (
    input_classifier_node,
    memory_retrieval_node,
    pattern_detection_node,
    recommendation_planner_node,
    tool_execution_node,
    response_generator_node,
    memory_update_node
)

def create_companion_graph():
    workflow = StateGraph(CompanionState)

    workflow.add_node("classify", input_classifier_node)
    workflow.add_node("retrieve_memory", memory_retrieval_node)
    workflow.add_node("detect_patterns", pattern_detection_node)
    workflow.add_node("plan_recommendation", recommendation_planner_node)
    workflow.add_node("execute_tools", tool_execution_node)
    workflow.add_node("generate_response", response_generator_node)
    workflow.add_node("update_memory", memory_update_node)

    workflow.set_entry_point("classify")
    
    workflow.add_edge("classify", "retrieve_memory")
    workflow.add_edge("retrieve_memory", "detect_patterns")
    workflow.add_edge("detect_patterns", "plan_recommendation")
    workflow.add_edge("plan_recommendation", "execute_tools")
    workflow.add_edge("execute_tools", "generate_response")
    workflow.add_edge("generate_response", "update_memory")
    workflow.add_edge("update_memory", END)

    return workflow.compile()

companion_orchestrator = create_companion_graph()
