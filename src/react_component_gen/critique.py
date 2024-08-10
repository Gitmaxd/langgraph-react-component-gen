from react_component_gen.model import _get_model
from react_component_gen.state import AgentState
from langchain_core.messages import AIMessage
from langchain_core.pydantic_v1 import BaseModel


file_contents = """
### 1. **Basic Render Test**

```javascript
import React from 'react';
import { render } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders without crashing', () => {
  render(<MyComponent />);
});
```

### 2. **Prop Validation Test**

```javascript
import React from 'react';
import { render } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders correctly with required props', () => {
  const props = { /* specify required props here */ };
  render(<MyComponent {...props} />);
});

test('renders correctly with optional props', () => {
  const props = { /* specify optional props here */ };
  render(<MyComponent {...props} />);
});
```

### 3. **Snapshot Test**

```javascript
import React from 'react';
import { render } from '@testing-library/react';
import MyComponent from './MyComponent';
import { create } from 'react-test-renderer';

test('matches snapshot', () => {
  const tree = create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

### 4. **Event Handling Test**

```javascript
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import MyComponent from './MyComponent';

test('handles click event', () => {
  const handleClick = jest.fn();
  const { getByText } = render(<MyComponent onClick={handleClick} />);
  fireEvent.click(getByText('Click Me'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

### 5. **Accessibility Test**

```javascript
import React from 'react';
import { render } from '@testing-library/react';
import { axe } from 'jest-axe';
import MyComponent from './MyComponent';

test('should have no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
"""

critique_prompt = """You are an expert React and Next.js developer tasked with critiquing a junior developer's attempt at building a React component for a Next.js application. 
Here are some example tests for React components. This should contain relevant information on how to create and test high-quality React components.

<react_test_examples>
{file}
</react_test_examples>

Based on the conversation below, critique the developer's React component. If the component seems to be implemented correctly, then call the `Accept` tool.

Focus your critique on the following aspects:
1. Proper use of React hooks and functional components
2. Adherence to Next.js conventions and best practices
3. Code organization and readability
4. Performance considerations
5. Proper typing (if TypeScript is used)
6. Appropriate use of props and state
7. Error handling and edge cases
8. Accessibility (a11y) considerations

Do NOT overly critique the specific implementation details or styling choices. Concentrate on ensuring the component 
is well-structured, follows React and Next.js best practices, and would perform well in a production environment."""


class Accept(BaseModel):
    logic: str
    accept: bool


def _swap_messages(messages):
    new_messages = []
    for m in messages:
        if isinstance(m, AIMessage):
            new_messages.append({"role": "user", "content": m.content})
        else:
            new_messages.append({"role": "assistant", "content": m.content})
    return new_messages


def critique(state: AgentState, config):
    file_contents = """
    [Your multi-line string with React test examples will go here]
    """
    messages = [
        {"role": "user", "content": critique_prompt.format(file=file_contents)},
        {"role": "assistant", "content": state.get('requirements')},
    ] + _swap_messages(state['messages'])
    model = _get_model(config, "openai", "critique_model").with_structured_output(Accept)
    response = model.invoke(messages)
    accepted = response.accept
    if accepted:
        return {
            "messages": [
                {"role": "user", "content": response.logic},
                {"role": "assistant", "content": "okay, sending to user"}],
            "accepted": True
        }
    else:
        return {
            "messages": [
                {"role": "user", "content": response.logic},
            ],
            "accepted": False
        }