# TokenCost

## Overview

TokenCost is a specialized tool designed for calculating the token count and associated U.S. dollar cost of strings and messages used in Large Language Models (LLMs). This utility is particularly useful for developers and researchers working with language models, enabling them to estimate the computational resources required for processing various inputs and their returned outputs.

```python
from tokencost import calculate_cost

prompt = "Sample input"
response = "Sample response text"
model = "gpt-3.5-turbo"


cost = calculate_cost(string_prompt, response, model)
print(cost) # in units of TPU, which is 1/10,000,000th of a USD.

# Prints the below:
# prompt_cost=15
# completion_cost=20
# 120
```

## Features

- **Token Counting**: Accurately counts the number of tokens in a given string or message.
- **Cost Calculation**: Computes the cost of processing based on the token count, considering the specific pricing model of the LLM in use.
- **Support for Multiple LLMs**: Compatible with various Large Language Models.
- **Easy Integration**: Simple API for integrating with existing projects or workflows.

## Installation

Tokencost can be installed either via PyPI or GitHub.

#### Recommended: with [PyPI](https://pypi.org/project/tokencost/) (Python package):

```bash
pip install tokencost
```

#### OR: with [GitHub](https://github.com/AgentOps-AI/tokencost):

```bash
git clone git@github.com:AgentOps-AI/tokencost.git
cd tokencost
pip install -e .
```

## Usage

To use TokenCost, follow these steps:

1. Import the module:

- Recommended: If you want to call the functions as `function_name` directly:

```python
from tokencost import count_message_tokens, count_string_tokens, calculate_cost
```

- OR if you want to call the functions as `tokencost.function_name`:

```python
import tokencost
```

2. Calculate tokens and cost (using `from tokencost import count_message_tokens, count_string_tokens, calculate_cost`):

```python

# First example using string input.
string_prompt = "Your sample text here"
response = "Sample response text"
model= "gpt-3.5-turbo"

cost = calculate_cost(string_prompt, response, model)

prompt_string_token_count = count_string_tokens(string_prompt, model)

print(f"{prompt_string_token_count=}, {completion_string_token_count=}")
print(f"Cost: ${string_cost/USD_PER_TPU} ({cost/CENTS_PER_TPU} cents)")

# Prints the below:
# prompt_cost=15
# completion_cost=20
# prompt_string_token_count=4, completion_string_token_count=3
# Cost: $1.2e-05 (0.0012 cents)

# Second example using list of message objects instead of string input.
messages =[
    {
        "role": "user",
        "content": "Hey how is your day",
    },
    {
        "role": 'assistant',
        "content": "As an LLM model I do not have days"
    },
    {
        "role": "user",
        "content": "Err sure okay fine"
    }
]
response = "Sample response text"
model= "gpt-3.5-turbo"

cost = calculate_cost(messages, response, model)

prompt_message_token_count = count_message_tokens(messages, model)
completion_string_token_count = count_string_tokens(response, model)

print(f"{prompt_message_token_count=}, {completion_string_token_count=}")
print(f"Cost: ${message_cost/USD_PER_TPU} ({cost/CENTS_PER_TPU} cents)")

# Prints the below:
# Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.
# prompt_cost=15
# completion_cost=20
# Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.
# prompt_message_token_count=34, completion_string_token_count=3
# Cost: $5.7e-05 (0.0057 cents)
```

## Running tests

0. Install `pytest` if you don't have it already

```python
pip install pytest
```

1. Run the `tests/` folder while in the parent directory

```python
pytest tests
```

## Contributing

Contributions to TokenCost are welcome! Feel free to create an [issue](https://github.com/AgentOps-AI/tokencost/issues) for any bug reports, complaints, or feature suggestions.

## License

TokenCost is released under the MIT License.
