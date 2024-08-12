from react_component_gen.model import _get_model
from react_component_gen.state import AgentState
from langsmith import Client  # Import the LangSmith Client class

# Initialize the LangSmith client
client = Client()

# Pull the prompt from LangSmith
draft_component_prompt = client.pull_prompt("gitmaxd/draft-component-prompt")

def create_draft_component(state: AgentState, config):
    # Format the prompt with the user's requirements and any existing state messages
    messages = draft_component_prompt.format_messages() + [
        {"role": "user", "content": state.get('requirements')}
    ] + state['messages']
    
    # Retrieve the model and invoke it
    model = _get_model(config, "anthropic", "draft_model")
    response = model.invoke(messages)
    
    return {"messages": [response]}
  