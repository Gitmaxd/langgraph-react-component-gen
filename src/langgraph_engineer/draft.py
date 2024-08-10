from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState

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

prompt = """You are an expert Next.js and React developer tasked with drafting high-quality, performant components. 
Your goal is to create a component based on the provided requirements, adhering to Next.js and React best practices.

Here are some example tests for React components. This should contain relevant information on how to create and test high-quality React components:

<react_test_examples>
{file}
</react_test_examples>

Based on the information above and the user's requirements, draft a Next.js React component. Follow these guidelines:

1. Generate only one code block, combining all necessary code.
2. Use modern React patterns with functional components and hooks.
3. Implement Next.js-specific features where appropriate (e.g., Image component, Link component).
4. Include helpful comments to explain your implementation choices.
5. Prioritize simplicity and readability - avoid unnecessary complexity.
6. Ensure proper typing for props and state (use TypeScript if specified in requirements).
7. Implement basic error handling and prop validation.
8. Consider server-side rendering (SSR) and static site generation (SSG) implications.
9. Use appropriate file naming conventions for Next.js (e.g., [id].js for dynamic routes).

Generate your code using markdown javascript syntax, like this:

```javascript
// Your component code here
```

Remember to produce only one code block containing the entire component!"""

def draft_answer(state: AgentState, config):
    file_contents = """
    [Your multi-line string with React test examples will go here]
    """
    messages = [
        {"role": "system", "content": prompt.format(file=file_contents)},
        {"role": "user", "content": state.get('requirements')}
    ] + state['messages']
    model = _get_model(config, "anthropic", "draft_model")
    response = model.invoke(messages)
    return {"messages": [response]}