# TokenCost

## Overview

TokenCost is a specialized tool designed for calculating the USD cost of using major Large Language Models (LLMs) APIs. 

### Features
* **LLM Price Tracking** Major LLM providers frequently add new models and update pricing. This repo helps track the latest price changes
* **Token counting** Accurately count prompt tokens before sending OpenAI requests
* **Easy integration** Get the cost of a prompt or completion with a single function

### Example usage:

```python
from tokencost import calculate_prompt_cost, calculate_completion_cost

model = "gpt-3.5-turbo"
prompt = "Hello world"
completion = "How may I assist you today?"

prompt_cost = calculate_prompt_cost(prompt, model)
completion_cost = calculate_completion_cost(completion, model)
print(f"{prompt_cost} + {completion_cost} = {prompt_cost + completion_cost}")
# 30 + 140 = 170
# In TPUs (token price units), which is 1/10,000,000th of a USD.
```

## Installation

#### Recommended: [PyPI](https://pypi.org/project/tokencost/):

```bash
pip install tokencost
```

## Usage

### Counting tokens

```python
from tokencost import count_message_tokens, count_string_tokens

message_prompt = [{ "role": "user", "content": "Hello world"}]
# Counting tokens in prompts formatted as message lists
print(count_message_tokens(message_prompt, model="gpt-3.5-turbo"))
# 9

# Alternatively, counting tokens in string prompts
print(count_string_tokens(prompt="Hello world", model="gpt-3.5-turbo"))
# 2

```

### Cost estimates
Calculating the cost of prompts and completions from OpenAI requests
```python
from openai import OpenAI

client = OpenAI()
model = "gpt-3.5-turbo"
prompt = [{ "role": "user", "content": "Say this is a test"}]

chat_completion = client.chat.completions.create(
    messages=prompt, model=model
)

completion = chat_completion.choices[0].message.content
# "This is a test."

prompt_cost = calculate_prompt_cost(prompt, model)
completion_cost = calculate_completion_cost(completion, model)
print(f"{prompt_cost} + {completion_cost} = {prompt_cost + completion_cost}")
# 180 + 100 = 280

from tokencost import USD_PER_TPU
print(f"Cost USD: ${(prompt_cost + completion_cost)/USD_PER_TPU}")
# $2.8e-05
```

**Calculating cost using string prompts instead of messages:**
```python
prompt_string = "Hello world" 
response = "How may I assist you today?"
model= "gpt-3.5-turbo"

prompt_cost = calculate_prompt_cost(prompt_string, model)
print(f"Cost: ${prompt_cost/USD_PER_TPU}")
# Cost: $3e-06
```

**Counting tokens**
```python
from tokencost import count_message_tokens, count_string_tokens
prompt = [{ "role": "user", "content": "Say this is a test"}]
prompt_message_token_count = count_message_tokens(prompt, model)
print(f"{prompt_message_token_count=}")
# prompt_message_token_count=12

completion_string_token_count = count_string_tokens(response, model)
print(f"{completion_string_token_count=}")
# completion_string_token_count=7
```

## Cost table
Units denominated in TPUs (Token Price Units = 1/10,000,000 USD)

| Model Name                | Prompt Cost | Completion Cost | Max Prompt Tokens |
|---------------------------|-------------|-----------------|-------------------|
| gpt-3.5-turbo             | 15          | 20              | 4097              |
| gpt-3.5-turbo-0301        | 15          | 20              | 4097              |
| gpt-3.5-turbo-0613        | 15          | 20              | 4097              |
| gpt-3.5-turbo-16k         | 30          | 40              | 16385             |
| gpt-3.5-turbo-16k-0613    | 30          | 40              | 16385             |
| gpt-3.5-turbo-1106        | 10          | 20              | 16385             |
| gpt-3.5-turbo-instruct    | 15          | 20              | 4096              |
| gpt-4                     | 300         | 600             | 8192              |
| gpt-4-0314                | 300         | 600             | 8192              |
| gpt-4-0613                | 300         | 600             | 8192              |
| gpt-4-32k                 | 600         | 1200            | 32768             |
| gpt-4-32k-0314            | 600         | 1200            | 32768             |
| gpt-4-32k-0613            | 600         | 1200            | 32768             |
| gpt-4-1106-preview        | 100         | 300             | 128000            |
| gpt-4-vision-preview      | 100         | 300             | 128000            |
| text-embedding-ada-002    | 1           | N/A             | 8192              |




### Running locally

#### Installation via [GitHub](https://github.com/AgentOps-AI/tokencost):

```bash
git clone git@github.com:AgentOps-AI/tokencost.git
cd tokencost
pip install -e .
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

This repo also supports `tox`, simply run `python -m tox`.

## Contributing

Contributions to TokenCost are welcome! Feel free to create an [issue](https://github.com/AgentOps-AI/tokencost/issues) for any bug reports, complaints, or feature suggestions.

## License

TokenCost is released under the MIT License.
