from typing import Literal

from langgraph.graph import StateGraph, END, MessagesState
from langchain_core.messages import AIMessage

from react_component_gen.check import check
from react_component_gen.critique import critique
from react_component_gen.documentation import documentation
from react_component_gen.draft import create_draft_component
from react_component_gen.gather_component_requirements import gather_component_requirements
from react_component_gen.state import AgentState, OutputState, GraphConfig

def route_critique(state: AgentState) -> Literal["create_draft_component", "documentation"]:
    if state['accepted']:
        return "documentation"
    else:
        return "create_draft_component"

def route_check(state: AgentState) -> Literal["critique", "create_draft_component"]:
    if isinstance(state['messages'][-1], AIMessage):
        return "critique"
    else:
        return "create_draft_component"

def route_start(state: AgentState) -> Literal["create_draft_component", "gather_component_requirements"]:
    if state.get('requirements'):
        return "create_draft_component"
    else:
        return "gather_component_requirements"

def route_gather(state: AgentState) -> Literal["create_draft_component", END]:
    if state.get('requirements'):
        return "create_draft_component"
    else:
        return END


workflow = StateGraph(AgentState, input=MessagesState, output=OutputState, config_schema=GraphConfig)
workflow.add_node(create_draft_component)
workflow.add_node(gather_component_requirements)
workflow.add_node(critique)
workflow.add_node(check)
workflow.add_node(documentation)

workflow.set_conditional_entry_point(route_start)
workflow.add_conditional_edges("gather_component_requirements", route_gather)
workflow.add_edge("create_draft_component", "check")
workflow.add_conditional_edges("check", route_check)
workflow.add_conditional_edges("critique", route_critique)

workflow.add_edge("documentation", END)

graph = workflow.compile()
