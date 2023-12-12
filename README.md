# TokenCost

## Overview

TokenCost is a specialized tool designed for calculating the token count and associated cost of strings and messages used in Large Language Models (LLMs). This utility is particularly useful for developers and researchers working with language models, enabling them to estimate the computational resources required for processing various inputs.

## Features

- **Token Counting**: Accurately counts the number of tokens in a given string or message.
- **Cost Calculation**: Computes the cost of processing based on the token count, considering the specific pricing model of the LLM in use.
- **Support for Multiple LLMs**: Compatible with various Large Language Models.
- **Easy Integration**: Simple API for integrating with existing projects or workflows.

## Installation

Tokencost can be installed either via PyPI or GitHub.


#### With [PyPI](https://pypi.org/project/tokencost/) (Python package):
```bash
pip install tokencost
```

#### With [GitHub](https://github.com/AgentOps-AI/tokencost):

```bash
git clone git@github.com:AgentOps-AI/tokencost.git
cd tokencost
pip install -e .
```

## Usage

To use TokenCost, follow these steps:

1. Import the module:

```python
from tokencost import TokenCalculator
```


3. Calculate tokens and cost:
```python
text = "Your sample text here"
token_count, cost = calculator.calculate(text)
print(f"Token Count: {token_count}, Cost: {cost}")
```

### Running tests
0. Install ```pytest``` if you don't have it already
```python
pip install pytest
```

1. Run the `tests/` folder while in the parent directory 
```python
pytest tests
```

## Contributing

Contributions to TokenCost are welcome! Please refer to our Contribution Guidelines for more details.

## License

TokenCost is released under the MIT License.
