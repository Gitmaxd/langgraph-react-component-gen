from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState
from langchain_core.messages import AIMessage

documentation_prompt = """
You are an expert React and Next.js developer tasked with creating comprehensive technical documentation for a React component in a Next.js application. Your goal is to produce clear, detailed, and professional documentation that will be invaluable to other developers working with this component.

Given the React component code, generate thorough documentation in Markdown format. Your documentation should cover the following aspects:

1. Component Overview
   - Briefly describe the purpose and functionality of the component
   - Mention any key features or behaviors

2. Props
   - List and describe all props, including:
     - Prop name
     - Type
     - Whether it's required or optional
     - Default value (if any)
     - Description of its purpose and usage

3. State (if applicable)
   - Describe any internal state used by the component
   - Explain how the state affects the component's behavior

4. Methods/Functions
   - Document any methods or functions within the component
   - Explain their purpose, parameters, and return values

5. Hooks (if used)
   - List and explain any React hooks used in the component
   - Describe how they contribute to the component's functionality

6. Rendering
   - Explain the component's render logic
   - Describe any conditional rendering

7. Styling
   - Mention any styling approach used (e.g., CSS modules, styled-components)
   - Note any class names or style props that can be customized

8. Performance Considerations
   - Highlight any performance optimizations implemented
   - Mention any potential performance impacts to be aware of

9. Accessibility Features
   - Describe any accessibility considerations or implementations

10. Dependencies
    - List any external libraries or components required

11. Example Usage
    - Provide a code snippet demonstrating how to use the component

12. Notes and Caveats
    - Mention any important notes, limitations, or potential gotchas

Ensure your documentation is clear, concise, and follows Markdown best practices for formatting and readability.

Based on the provided React component code, generate the technical documentation as specified above. Return your response in the following format:

1. The complete, unmodified React component code wrapped in a code block.
2. The generated documentation in Markdown format.

Both the code and documentation should be included in your response, clearly separated.
"""

def documentation(state: AgentState, config):
    messages = [
        {"role": "system", "content": documentation_prompt},
        {"role": "user", "content": f"Here is the React component code:\n\n{state.get('code')}"}
    ]
    model = _get_model(config, "openai", "documentation_model")
    response = model.invoke(messages)
    
    # Extract the component code and documentation from the response
    content = response.content
    code_block_start = content.index("```")
    code_block_end = content.index("```", code_block_start + 3) + 3
    component_code = content[code_block_start:code_block_end]
    documentation = content[code_block_end:].strip()
    
    return {
        "messages": [AIMessage(content=response.content)],
        "component_code": component_code,
        "documentation": documentation
    }