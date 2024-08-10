import re
from react_component_gen.state import AgentState


def extract_react_code(text):
    pattern = r'```(?:javascript|jsx)\s*(.*?)\s*(```|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


error_parsing = """Make sure your response contains a code block in the following format:

```javascript
// or
```jsx
...
```

When trying to parse out that code block, got this error: {error}"""


def check(state: AgentState):
    last_answer = state['messages'][-1]
    try:
        code_blocks = extract_react_code(last_answer.content)
    except Exception as e:
        return {"messages": [{"role": "user", "content": error_parsing.format(error=str(e))}]}
    if len(code_blocks) == 0:
        return {"messages": [{"role": "user", "content": error_parsing.format(error="Did not find a React component code block!")}]}
    if len(code_blocks) > 1:
        return {"messages": [{"role": "user", "content": error_parsing.format(error="Found multiple React component code blocks!")}]}
    
    component_code = code_blocks[0][0]
    issues = validate_react_component(component_code)
    
    if issues:
        return {"messages": [{"role": "user", "content": f"The React component has the following issues:\n{', '.join(issues)}"}]}
    
    return {"code": f"```jsx\n{component_code}\n```"}


def validate_react_component(code):
    issues = []
    
    if "import React" not in code and "import { " not in code:
        issues.append("Missing React import")
    if "function" not in code and "const" not in code:
        issues.append("No component function found")
    if "return (" not in code:
        issues.append("No JSX return statement found")
    if "export default" not in code and "export const" not in code:
        issues.append("Missing export statement")
    
    return issues