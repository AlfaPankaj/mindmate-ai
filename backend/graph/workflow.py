from langgraph.graph import StateGraph, END
from graph.state import CompanionState
from graph.nodes.classifier import input_classifier_node
from graph.nodes.retrieval import memory_retrieval_node
from graph.nodes.pattern import pattern_detection_node
from graph.nodes.planner import recommendation_planner_node
from graph.nodes.tools import tool_execution_node
from graph.nodes.generator import response_generator_node
from graph.nodes.updater import memory_update_node

def create_companion_graph():
    # 1. Initialize the Graph
    workflow = StateGraph(CompanionState)

    # 2. Add Nodes
    workflow.add_node("classify", input_classifier_node)
    workflow.add_node("retrieve_memory", memory_retrieval_node)
    workflow.add_node("detect_patterns", pattern_detection_node)
    workflow.add_node("plan_recommendation", recommendation_planner_node)
    workflow.add_node("execute_tools", tool_execution_node)
    workflow.add_node("generate_response", response_generator_node)
    workflow.add_node("update_memory", memory_update_node)

    # 3. Define the Flow
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
