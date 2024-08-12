from react_component_gen.model import _get_model
from react_component_gen.state import AgentState
from typing import TypedDict
from langchain_core.messages import RemoveMessage
from langsmith import Client  # Import the Client class

# Initialize the LangSmith client
client = Client()

# Pull the prompt from LangSmith
gather_component_prompt = client.pull_prompt("gitmaxd/gather-component-prompt")

# Define the DefineComponent class to structure the requirements
class DefineComponent(TypedDict):
    requirements: str

# Function to gather component requirements
def gather_component_requirements(state: AgentState, config):
    # Prepare the messages with the system role using the pulled prompt
    messages = gather_component_prompt.format_messages(**{}) + state['messages']
    
    # Retrieve the model and bind tools
    model = _get_model(config, "openai", "gather_model").bind_tools([DefineComponent])
    
    # Invoke the model with the messages
    response = model.invoke(messages)
    
    # Process the response and handle tool calls
    if len(response.tool_calls) == 0:
        return {"messages": [response]}
    else:
        requirements = response.tool_calls[0]['args']['requirements']
        delete_messages = [RemoveMessage(id=m.id) for m in state['messages']]
        return {"requirements": requirements, "messages": delete_messages}
