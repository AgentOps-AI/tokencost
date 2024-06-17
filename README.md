<p align="center">
  <img src="https://raw.githubusercontent.com/AgentOps-AI/tokencost/main/tokencost.png" height="300" alt="Tokencost" />
</p>

<p align="center">
  <em>Clientside token counting + price estimation for LLM apps and AI agents.</em>
</p>
<p align="center">
    <a href="https://pypi.org/project/tokencost/" target="_blank">
        <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
        <img alt="Version" src="https://img.shields.io/pypi/v/tokencost?style=for-the-badge&color=3670A0">
    </a>
</p>
<p align="center">
<a href="https://twitter.com/agentopsai/">🐦 Twitter</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://discord.gg/JHPt4C7r">📢 Discord</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://agentops.ai/?tokencost">🖇️ AgentOps</a>
</p>


# TokenCost
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![PyPI - Version](https://img.shields.io/pypi/v/tokencost)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/AgentOpsAI)](https://x.com/agentopsai)

Tokencost helps calculate the USD cost of using major Large Language Model (LLMs) APIs by calculating the estimated cost of prompts and completions.

Building AI agents? Check out [AgentOps](https://agentops.ai/?tokencost)


### Features
* **LLM Price Tracking** Major LLM providers frequently add new models and update pricing. This repo helps track the latest price changes
* **Token counting** Accurately count prompt tokens before sending OpenAI requests
* **Easy integration** Get the cost of a prompt or completion with a single function

### Example usage:

```python
from tokencost import calculate_prompt_cost, calculate_completion_cost

model = "gpt-3.5-turbo"
prompt = [{ "role": "user", "content": "Hello world"}]
completion = "How may I assist you today?"

prompt_cost = calculate_prompt_cost(prompt, model)
completion_cost = calculate_completion_cost(completion, model)

print(f"{prompt_cost} + {completion_cost} = {prompt_cost + completion_cost}")
# 0.0000135 + 0.000014 = 0.0000275
```

## Installation

#### Recommended: [PyPI](https://pypi.org/project/tokencost/):

```bash
pip install tokencost
```

## Usage

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
# 0.0000180 + 0.000010 = 0.0000280
```

**Calculating cost using string prompts instead of messages:**
```python
from tokencost import calculate_prompt_cost

prompt_string = "Hello world" 
response = "How may I assist you today?"
model= "gpt-3.5-turbo"

prompt_cost = calculate_prompt_cost(prompt_string, model)
print(f"Cost: ${prompt_cost}")
# Cost: $3e-06
```

**Counting tokens**

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

## Cost table
Units denominated in USD. All prices can be located in `model_prices.json`.


* Prices last updated Jan 30, 2024 from [LiteLLM's cost dictionary](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)

| Model Name                                                                                  | Prompt Cost (USD) per 1M tokens   | Completion Cost (USD) per 1M tokens   | Max Prompt Tokens   |   Max Output Tokens |
|:--------------------------------------------------------------------------------------------|:----------------------------------|:--------------------------------------|:--------------------|--------------------:|
| gpt-4                                                                                       | $30.00                            | $60.00                                | 8,192               |                4096 |
| gpt-4o                                                                                      | $5.00                             | $15.00                                | 128,000             |                4096 |
| gpt-4o-2024-05-13                                                                           | $5.00                             | $15.00                                | 128,000             |                4096 |
| gpt-4-turbo-preview                                                                         | $10.00                            | $30.00                                | 128,000             |                4096 |
| gpt-4-0314                                                                                  | $30.00                            | $60.00                                | 8,192               |                4096 |
| gpt-4-0613                                                                                  | $30.00                            | $60.00                                | 8,192               |                4096 |
| gpt-4-32k                                                                                   | $60.00                            | $120.00                               | 32,768              |                4096 |
| gpt-4-32k-0314                                                                              | $60.00                            | $120.00                               | 32,768              |                4096 |
| gpt-4-32k-0613                                                                              | $60.00                            | $120.00                               | 32,768              |                4096 |
| gpt-4-turbo                                                                                 | $10.00                            | $30.00                                | 128,000             |                4096 |
| gpt-4-turbo-2024-04-09                                                                      | $10.00                            | $30.00                                | 128,000             |                4096 |
| gpt-4-1106-preview                                                                          | $10.00                            | $30.00                                | 128,000             |                4096 |
| gpt-4-0125-preview                                                                          | $10.00                            | $30.00                                | 128,000             |                4096 |
| gpt-4-vision-preview                                                                        | $10.00                            | $30.00                                | 128,000             |                4096 |
| gpt-4-1106-vision-preview                                                                   | $10.00                            | $30.00                                | 128,000             |                4096 |
| gpt-3.5-turbo                                                                               | $1.5                              | $2.00                                 | 16,385              |                4096 |
| gpt-3.5-turbo-0301                                                                          | $1.5                              | $2.00                                 | 4,097               |                4096 |
| gpt-3.5-turbo-0613                                                                          | $1.5                              | $2.00                                 | 4,097               |                4096 |
| gpt-3.5-turbo-1106                                                                          | $1.00                             | $2.00                                 | 16,385              |                4096 |
| gpt-3.5-turbo-0125                                                                          | $0.5                              | $1.5                                  | 16,385              |                4096 |
| gpt-3.5-turbo-16k                                                                           | $3.00                             | $4.00                                 | 16,385              |                4096 |
| gpt-3.5-turbo-16k-0613                                                                      | $3.00                             | $4.00                                 | 16,385              |                4096 |
| ft:gpt-3.5-turbo                                                                            | $3.00                             | $6.00                                 | 4,097               |                4096 |
| ft:davinci-002                                                                              | $2.00                             | $2.00                                 | 16,384              |                4096 |
| ft:babbage-002                                                                              | $0.4                              | $0.4                                  | 16,384              |                4096 |
| text-embedding-3-large                                                                      | $0.13                             | $0.00                                 | 8,191               |                 nan |
| text-embedding-3-small                                                                      | $0.02                             | $0.00                                 | 8,191               |                 nan |
| text-embedding-ada-002                                                                      | $0.1                              | $0.00                                 | 8,191               |                 nan |
| text-embedding-ada-002-v2                                                                   | $0.1                              | $0.00                                 | 8,191               |                 nan |
| text-moderation-stable                                                                      | $0.00                             | $0.00                                 | 32,768              |                   0 |
| text-moderation-007                                                                         | $0.00                             | $0.00                                 | 32,768              |                   0 |
| text-moderation-latest                                                                      | $0.00                             | $0.00                                 | 32,768              |                   0 |
| 256-x-256/dall-e-2                                                                          | --                                | --                                    | nan                 |                 nan |
| 512-x-512/dall-e-2                                                                          | --                                | --                                    | nan                 |                 nan |
| 1024-x-1024/dall-e-2                                                                        | --                                | --                                    | nan                 |                 nan |
| hd/1024-x-1792/dall-e-3                                                                     | --                                | --                                    | nan                 |                 nan |
| hd/1792-x-1024/dall-e-3                                                                     | --                                | --                                    | nan                 |                 nan |
| hd/1024-x-1024/dall-e-3                                                                     | --                                | --                                    | nan                 |                 nan |
| standard/1024-x-1792/dall-e-3                                                               | --                                | --                                    | nan                 |                 nan |
| standard/1792-x-1024/dall-e-3                                                               | --                                | --                                    | nan                 |                 nan |
| standard/1024-x-1024/dall-e-3                                                               | --                                | --                                    | nan                 |                 nan |
| whisper-1                                                                                   | --                                | --                                    | nan                 |                 nan |
| azure/whisper-1                                                                             | --                                | --                                    | nan                 |                 nan |
| azure/gpt-4o                                                                                | $5.00                             | $15.00                                | 128,000             |                4096 |
| azure/gpt-4-turbo-2024-04-09                                                                | $10.00                            | $30.00                                | 128,000             |                4096 |
| azure/gpt-4-0125-preview                                                                    | $10.00                            | $30.00                                | 128,000             |                4096 |
| azure/gpt-4-1106-preview                                                                    | $10.00                            | $30.00                                | 128,000             |                4096 |
| azure/gpt-4-0613                                                                            | $30.00                            | $60.00                                | 8,192               |                4096 |
| azure/gpt-4-32k-0613                                                                        | $60.00                            | $120.00                               | 32,768              |                4096 |
| azure/gpt-4-32k                                                                             | $60.00                            | $120.00                               | 32,768              |                4096 |
| azure/gpt-4                                                                                 | $30.00                            | $60.00                                | 8,192               |                4096 |
| azure/gpt-4-turbo                                                                           | $10.00                            | $30.00                                | 128,000             |                4096 |
| azure/gpt-4-turbo-vision-preview                                                            | $10.00                            | $30.00                                | 128,000             |                4096 |
| azure/gpt-35-turbo-16k-0613                                                                 | $3.00                             | $4.00                                 | 16,385              |                4096 |
| azure/gpt-35-turbo-1106                                                                     | $1.5                              | $2.00                                 | 16,384              |                4096 |
| azure/gpt-35-turbo-0125                                                                     | $0.5                              | $1.5                                  | 16,384              |                4096 |
| azure/gpt-35-turbo-16k                                                                      | $3.00                             | $4.00                                 | 16,385              |                4096 |
| azure/gpt-35-turbo                                                                          | $0.5                              | $1.5                                  | 4,097               |                4096 |
| azure/gpt-3.5-turbo-instruct-0914                                                           | $1.5                              | $2.00                                 | 4,097               |                 nan |
| azure/gpt-35-turbo-instruct                                                                 | $1.5                              | $2.00                                 | 4,097               |                 nan |
| azure/mistral-large-latest                                                                  | $8.00                             | $24.00                                | 32,000              |                 nan |
| azure/mistral-large-2402                                                                    | $8.00                             | $24.00                                | 32,000              |                 nan |
| azure/command-r-plus                                                                        | $3.00                             | $15.00                                | 128,000             |                4096 |
| azure/ada                                                                                   | $0.1                              | $0.00                                 | 8,191               |                 nan |
| azure/text-embedding-ada-002                                                                | $0.1                              | $0.00                                 | 8,191               |                 nan |
| azure/text-embedding-3-large                                                                | $0.13                             | $0.00                                 | 8,191               |                 nan |
| azure/text-embedding-3-small                                                                | $0.02                             | $0.00                                 | 8,191               |                 nan |
| azure/standard/1024-x-1024/dall-e-3                                                         | --                                | $0.00                                 | nan                 |                 nan |
| azure/hd/1024-x-1024/dall-e-3                                                               | --                                | $0.00                                 | nan                 |                 nan |
| azure/standard/1024-x-1792/dall-e-3                                                         | --                                | $0.00                                 | nan                 |                 nan |
| azure/standard/1792-x-1024/dall-e-3                                                         | --                                | $0.00                                 | nan                 |                 nan |
| azure/hd/1024-x-1792/dall-e-3                                                               | --                                | $0.00                                 | nan                 |                 nan |
| azure/hd/1792-x-1024/dall-e-3                                                               | --                                | $0.00                                 | nan                 |                 nan |
| azure/standard/1024-x-1024/dall-e-2                                                         | --                                | $0.00                                 | nan                 |                 nan |
| babbage-002                                                                                 | $0.4                              | $0.4                                  | 16,384              |                4096 |
| davinci-002                                                                                 | $2.00                             | $2.00                                 | 16,384              |                4096 |
| gpt-3.5-turbo-instruct                                                                      | $1.5                              | $2.00                                 | 8,192               |                4096 |
| gpt-3.5-turbo-instruct-0914                                                                 | $1.5                              | $2.00                                 | 8,192               |                4097 |
| claude-instant-1                                                                            | $1.63                             | $5.51                                 | 100,000             |                8191 |
| mistral/mistral-tiny                                                                        | $0.25                             | $0.25                                 | 32,000              |                8191 |
| mistral/mistral-small                                                                       | $1.00                             | $3.00                                 | 32,000              |                8191 |
| mistral/mistral-small-latest                                                                | $1.00                             | $3.00                                 | 32,000              |                8191 |
| mistral/mistral-medium                                                                      | $2.7                              | $8.1                                  | 32,000              |                8191 |
| mistral/mistral-medium-latest                                                               | $2.7                              | $8.1                                  | 32,000              |                8191 |
| mistral/mistral-medium-2312                                                                 | $2.7                              | $8.1                                  | 32,000              |                8191 |
| mistral/mistral-large-latest                                                                | $4.00                             | $12.00                                | 32,000              |                8191 |
| mistral/mistral-large-2402                                                                  | $4.00                             | $12.00                                | 32,000              |                8191 |
| mistral/open-mistral-7b                                                                     | $0.25                             | $0.25                                 | 32,000              |                8191 |
| mistral/open-mixtral-8x7b                                                                   | $0.7                              | $0.7                                  | 32,000              |                8191 |
| mistral/open-mixtral-8x22b                                                                  | $2.00                             | $6.00                                 | 64,000              |                8191 |
| mistral/codestral-latest                                                                    | $1.00                             | $3.00                                 | 32,000              |                8191 |
| mistral/codestral-2405                                                                      | $1.00                             | $3.00                                 | 32,000              |                8191 |
| mistral/mistral-embed                                                                       | $0.1                              | --                                    | 8,192               |                 nan |
| deepseek-chat                                                                               | $0.14                             | $0.28                                 | 32,000              |                4096 |
| deepseek-coder                                                                              | $0.14                             | $0.28                                 | 16,000              |                4096 |
| groq/llama2-70b-4096                                                                        | $0.7                              | $0.8                                  | 4,096               |                4096 |
| groq/llama3-8b-8192                                                                         | $0.1                              | $0.1                                  | 8,192               |                8192 |
| groq/llama3-70b-8192                                                                        | $0.64                             | $0.8                                  | 8,192               |                8192 |
| groq/mixtral-8x7b-32768                                                                     | $0.27                             | $0.27                                 | 32,768              |               32768 |
| groq/gemma-7b-it                                                                            | $0.1                              | $0.1                                  | 8,192               |                8192 |
| claude-instant-1.2                                                                          | $0.163                            | $0.551                                | 100,000             |                8191 |
| claude-2                                                                                    | $8.00                             | $24.00                                | 100,000             |                8191 |
| claude-2.1                                                                                  | $8.00                             | $24.00                                | 200,000             |                8191 |
| claude-3-haiku-20240307                                                                     | $0.25                             | $1.25                                 | 200,000             |                4096 |
| claude-3-opus-20240229                                                                      | $15.00                            | $75.00                                | 200,000             |                4096 |
| claude-3-sonnet-20240229                                                                    | $3.00                             | $15.00                                | 200,000             |                4096 |
| text-bison                                                                                  | $0.125                            | $0.125                                | 8,192               |                1024 |
| text-bison@001                                                                              | $0.125                            | $0.125                                | 8,192               |                1024 |
| text-unicorn                                                                                | $10.00                            | $28.00                                | 8,192               |                1024 |
| text-unicorn@001                                                                            | $10.00                            | $28.00                                | 8,192               |                1024 |
| chat-bison                                                                                  | $0.125                            | $0.125                                | 8,192               |                4096 |
| chat-bison@001                                                                              | $0.125                            | $0.125                                | 8,192               |                4096 |
| chat-bison@002                                                                              | $0.125                            | $0.125                                | 8,192               |                4096 |
| chat-bison-32k                                                                              | $0.125                            | $0.125                                | 32,000              |                8192 |
| code-bison                                                                                  | $0.125                            | $0.125                                | 6,144               |                1024 |
| code-bison@001                                                                              | $0.125                            | $0.125                                | 6,144               |                1024 |
| code-gecko@001                                                                              | $0.125                            | $0.125                                | 2,048               |                  64 |
| code-gecko@002                                                                              | $0.125                            | $0.125                                | 2,048               |                  64 |
| code-gecko                                                                                  | $0.125                            | $0.125                                | 2,048               |                  64 |
| codechat-bison                                                                              | $0.125                            | $0.125                                | 6,144               |                1024 |
| codechat-bison@001                                                                          | $0.125                            | $0.125                                | 6,144               |                1024 |
| codechat-bison-32k                                                                          | $0.125                            | $0.125                                | 32,000              |                8192 |
| gemini-pro                                                                                  | $0.03125                          | $0.09375                              | 32,760              |                8192 |
| gemini-1.0-pro                                                                              | $0.03125                          | $0.09375                              | 32,760              |                8192 |
| gemini-1.0-pro-001                                                                          | $0.03125                          | $0.09375                              | 32,760              |                8192 |
| gemini-1.0-pro-002                                                                          | $0.03125                          | $0.09375                              | 32,760              |                8192 |
| gemini-1.5-pro                                                                              | $0.3125                           | $0.9375                               | 1,000,000           |                8192 |
| gemini-1.5-flash-001                                                                        | $0.03125                          | $0.09375                              | 1,000,000           |                8192 |
| gemini-1.5-flash-preview-0514                                                               | $0.03125                          | $0.09375                              | 1,000,000           |                8192 |
| gemini-1.5-pro-001                                                                          | $0.3125                           | $0.9375                               | 1,000,000           |                8192 |
| gemini-1.5-pro-preview-0514                                                                 | $0.3125                           | $0.9375                               | 1,000,000           |                8192 |
| gemini-1.5-pro-preview-0215                                                                 | $0.3125                           | $0.9375                               | 1,000,000           |                8192 |
| gemini-1.5-pro-preview-0409                                                                 | $0.3125                           | $0.9375                               | 1,000,000           |                8192 |
| gemini-experimental                                                                         | $0.00                             | $0.00                                 | 1,000,000           |                8192 |
| gemini-pro-vision                                                                           | $0.25                             | $0.5                                  | 16,384              |                2048 |
| gemini-1.0-pro-vision                                                                       | $0.25                             | $0.5                                  | 16,384              |                2048 |
| gemini-1.0-pro-vision-001                                                                   | $0.25                             | $0.5                                  | 16,384              |                2048 |
| vertex_ai/claude-3-sonnet@20240229                                                          | $3.00                             | $15.00                                | 200,000             |                4096 |
| vertex_ai/claude-3-haiku@20240307                                                           | $0.25                             | $1.25                                 | 200,000             |                4096 |
| vertex_ai/claude-3-opus@20240229                                                            | $15.00                            | $75.00                                | 200,000             |                4096 |
| vertex_ai/imagegeneration@006                                                               | --                                | --                                    | nan                 |                 nan |
| text-embedding-004                                                                          | $0.00625                          | $0.00                                 | 3,072               |                 nan |
| text-multilingual-embedding-002                                                             | $0.00625                          | $0.00                                 | 2,048               |                 nan |
| textembedding-gecko                                                                         | $0.00625                          | $0.00                                 | 3,072               |                 nan |
| textembedding-gecko-multilingual                                                            | $0.00625                          | $0.00                                 | 3,072               |                 nan |
| textembedding-gecko-multilingual@001                                                        | $0.00625                          | $0.00                                 | 3,072               |                 nan |
| textembedding-gecko@001                                                                     | $0.00625                          | $0.00                                 | 3,072               |                 nan |
| textembedding-gecko@003                                                                     | $0.00625                          | $0.00                                 | 3,072               |                 nan |
| text-embedding-preview-0409                                                                 | $0.00625                          | $0.00                                 | 3,072               |                 nan |
| text-multilingual-embedding-preview-0409                                                    | $0.00625                          | $0.00                                 | 3,072               |                 nan |
| palm/chat-bison                                                                             | $0.125                            | $0.125                                | 8,192               |                4096 |
| palm/chat-bison-001                                                                         | $0.125                            | $0.125                                | 8,192               |                4096 |
| palm/text-bison                                                                             | $0.125                            | $0.125                                | 8,192               |                1024 |
| palm/text-bison-001                                                                         | $0.125                            | $0.125                                | 8,192               |                1024 |
| palm/text-bison-safety-off                                                                  | $0.125                            | $0.125                                | 8,192               |                1024 |
| palm/text-bison-safety-recitation-off                                                       | $0.125                            | $0.125                                | 8,192               |                1024 |
| gemini/gemini-1.5-flash-latest                                                              | $0.35                             | $1.05                                 | 1,000,000           |                8192 |
| gemini/gemini-pro                                                                           | $0.35                             | $1.05                                 | 32,760              |                8192 |
| gemini/gemini-1.5-pro                                                                       | $0.35                             | $1.05                                 | 1,000,000           |                8192 |
| gemini/gemini-1.5-pro-latest                                                                | $0.35                             | $1.05                                 | 1,048,576           |                8192 |
| gemini/gemini-pro-vision                                                                    | $0.35                             | $1.05                                 | 30,720              |                2048 |
| command-r                                                                                   | $0.5                              | $1.5                                  | 128,000             |                4096 |
| command-light                                                                               | $15.00                            | $15.00                                | 4,096               |                4096 |
| command-r-plus                                                                              | $3.00                             | $15.00                                | 128,000             |                4096 |
| command-nightly                                                                             | $15.00                            | $15.00                                | 4,096               |                4096 |
| command                                                                                     | $15.00                            | $15.00                                | 4,096               |                4096 |
| command-medium-beta                                                                         | $15.00                            | $15.00                                | 4,096               |                4096 |
| command-xlarge-beta                                                                         | $15.00                            | $15.00                                | 4,096               |                4096 |
| replicate/meta/llama-2-13b                                                                  | $0.1                              | $0.5                                  | 4,096               |                4096 |
| replicate/meta/llama-2-13b-chat                                                             | $0.1                              | $0.5                                  | 4,096               |                4096 |
| replicate/meta/llama-2-70b                                                                  | $0.65                             | $2.75                                 | 4,096               |                4096 |
| replicate/meta/llama-2-70b-chat                                                             | $0.65                             | $2.75                                 | 4,096               |                4096 |
| replicate/meta/llama-2-7b                                                                   | $0.05                             | $0.25                                 | 4,096               |                4096 |
| replicate/meta/llama-2-7b-chat                                                              | $0.05                             | $0.25                                 | 4,096               |                4096 |
| replicate/meta/llama-3-70b                                                                  | $0.65                             | $2.75                                 | 8,192               |                8192 |
| replicate/meta/llama-3-70b-instruct                                                         | $0.65                             | $2.75                                 | 8,192               |                8192 |
| replicate/meta/llama-3-8b                                                                   | $0.05                             | $0.25                                 | 8,086               |                8086 |
| replicate/meta/llama-3-8b-instruct                                                          | $0.05                             | $0.25                                 | 8,086               |                8086 |
| replicate/mistralai/mistral-7b-v0.1                                                         | $0.05                             | $0.25                                 | 4,096               |                4096 |
| replicate/mistralai/mistral-7b-instruct-v0.2                                                | $0.05                             | $0.25                                 | 4,096               |                4096 |
| replicate/mistralai/mixtral-8x7b-instruct-v0.1                                              | $0.3                              | $1.00                                 | 4,096               |                4096 |
| openrouter/microsoft/wizardlm-2-8x22b:nitro                                                 | $1.00                             | $1.00                                 | nan                 |                 nan |
| openrouter/google/gemini-pro-1.5                                                            | $2.5                              | $7.5                                  | 1,000,000           |                8192 |
| openrouter/mistralai/mixtral-8x22b-instruct                                                 | $0.65                             | $0.65                                 | nan                 |                 nan |
| openrouter/cohere/command-r-plus                                                            | $3.00                             | $15.00                                | nan                 |                 nan |
| openrouter/databricks/dbrx-instruct                                                         | $0.6                              | $0.6                                  | nan                 |                 nan |
| openrouter/anthropic/claude-3-haiku                                                         | $0.25                             | $1.25                                 | nan                 |                 nan |
| openrouter/anthropic/claude-3-sonnet                                                        | $3.00                             | $15.00                                | nan                 |                 nan |
| openrouter/mistralai/mistral-large                                                          | $8.00                             | $24.00                                | nan                 |                 nan |
| openrouter/cognitivecomputations/dolphin-mixtral-8x7b                                       | $0.5                              | $0.5                                  | nan                 |                 nan |
| openrouter/google/gemini-pro-vision                                                         | $0.125                            | $0.375                                | nan                 |                 nan |
| openrouter/fireworks/firellava-13b                                                          | $0.2                              | $0.2                                  | nan                 |                 nan |
| openrouter/meta-llama/llama-3-8b-instruct:free                                              | $0.00                             | $0.00                                 | nan                 |                 nan |
| openrouter/meta-llama/llama-3-8b-instruct:extended                                          | $0.225                            | $2.25                                 | nan                 |                 nan |
| openrouter/meta-llama/llama-3-70b-instruct:nitro                                            | $0.9                              | $0.9                                  | nan                 |                 nan |
| openrouter/meta-llama/llama-3-70b-instruct                                                  | $0.59                             | $0.79                                 | nan                 |                 nan |
| openrouter/openai/gpt-4o                                                                    | $5.00                             | $15.00                                | 128,000             |                4096 |
| openrouter/openai/gpt-4o-2024-05-13                                                         | $5.00                             | $15.00                                | 128,000             |                4096 |
| openrouter/openai/gpt-4-vision-preview                                                      | $10.00                            | $30.00                                | nan                 |                 nan |
| openrouter/openai/gpt-3.5-turbo                                                             | $1.5                              | $2.00                                 | nan                 |                 nan |
| openrouter/openai/gpt-3.5-turbo-16k                                                         | $3.00                             | $4.00                                 | nan                 |                 nan |
| openrouter/openai/gpt-4                                                                     | $30.00                            | $60.00                                | nan                 |                 nan |
| openrouter/anthropic/claude-instant-v1                                                      | $1.63                             | $5.51                                 | nan                 |                8191 |
| openrouter/anthropic/claude-2                                                               | $11.02                            | $32.68                                | nan                 |                8191 |
| openrouter/anthropic/claude-3-opus                                                          | $15.00                            | $75.00                                | 200,000             |                4096 |
| openrouter/google/palm-2-chat-bison                                                         | $0.5                              | $0.5                                  | nan                 |                 nan |
| openrouter/google/palm-2-codechat-bison                                                     | $0.5                              | $0.5                                  | nan                 |                 nan |
| openrouter/meta-llama/llama-2-13b-chat                                                      | $0.2                              | $0.2                                  | nan                 |                 nan |
| openrouter/meta-llama/llama-2-70b-chat                                                      | $1.5                              | $1.5                                  | nan                 |                 nan |
| openrouter/meta-llama/codellama-34b-instruct                                                | $0.5                              | $0.5                                  | nan                 |                 nan |
| openrouter/nousresearch/nous-hermes-llama2-13b                                              | $0.2                              | $0.2                                  | nan                 |                 nan |
| openrouter/mancer/weaver                                                                    | $5.625                            | $5.625                                | nan                 |                 nan |
| openrouter/gryphe/mythomax-l2-13b                                                           | $1.875                            | $1.875                                | nan                 |                 nan |
| openrouter/jondurbin/airoboros-l2-70b-2.1                                                   | $13.875                           | $13.875                               | nan                 |                 nan |
| openrouter/undi95/remm-slerp-l2-13b                                                         | $1.875                            | $1.875                                | nan                 |                 nan |
| openrouter/pygmalionai/mythalion-13b                                                        | $1.875                            | $1.875                                | nan                 |                 nan |
| openrouter/mistralai/mistral-7b-instruct                                                    | $0.13                             | $0.13                                 | nan                 |                 nan |
| openrouter/mistralai/mistral-7b-instruct:free                                               | $0.00                             | $0.00                                 | nan                 |                 nan |
| j2-ultra                                                                                    | $15.00                            | $15.00                                | 8,192               |                8192 |
| j2-mid                                                                                      | $10.00                            | $10.00                                | 8,192               |                8192 |
| j2-light                                                                                    | $3.00                             | $3.00                                 | 8,192               |                8192 |
| dolphin                                                                                     | $0.5                              | $0.5                                  | 16,384              |               16384 |
| chatdolphin                                                                                 | $0.5                              | $0.5                                  | 16,384              |               16384 |
| luminous-base                                                                               | $30.00                            | $33.00                                | nan                 |                 nan |
| luminous-base-control                                                                       | $37.5                             | $41.25                                | nan                 |                 nan |
| luminous-extended                                                                           | $45.00                            | $49.5                                 | nan                 |                 nan |
| luminous-extended-control                                                                   | $56.25                            | $61.875                               | nan                 |                 nan |
| luminous-supreme                                                                            | $175.00                           | $192.5                                | nan                 |                 nan |
| luminous-supreme-control                                                                    | $218.75                           | $240.625                              | nan                 |                 nan |
| ai21.j2-mid-v1                                                                              | $12.5                             | $12.5                                 | 8,191               |                8191 |
| ai21.j2-ultra-v1                                                                            | $18.8                             | $18.8                                 | 8,191               |                8191 |
| amazon.titan-text-lite-v1                                                                   | $0.3                              | $0.4                                  | 42,000              |                4000 |
| amazon.titan-text-express-v1                                                                | $1.3                              | $1.7                                  | 42,000              |                8000 |
| amazon.titan-embed-text-v1                                                                  | $0.1                              | $0.00                                 | 8,192               |                 nan |
| amazon.titan-embed-text-v2:0                                                                | $0.2                              | $0.00                                 | 8,192               |                 nan |
| mistral.mistral-7b-instruct-v0:2                                                            | $0.15                             | $0.2                                  | 32,000              |                8191 |
| mistral.mixtral-8x7b-instruct-v0:1                                                          | $0.45                             | $0.7                                  | 32,000              |                8191 |
| mistral.mistral-large-2402-v1:0                                                             | $8.00                             | $24.00                                | 32,000              |                8191 |
| bedrock/us-west-2/mistral.mixtral-8x7b-instruct-v0:1                                        | $0.45                             | $0.7                                  | 32,000              |                8191 |
| bedrock/us-east-1/mistral.mixtral-8x7b-instruct-v0:1                                        | $0.45                             | $0.7                                  | 32,000              |                8191 |
| bedrock/eu-west-3/mistral.mixtral-8x7b-instruct-v0:1                                        | $0.59                             | $0.91                                 | 32,000              |                8191 |
| bedrock/us-west-2/mistral.mistral-7b-instruct-v0:2                                          | $0.15                             | $0.2                                  | 32,000              |                8191 |
| bedrock/us-east-1/mistral.mistral-7b-instruct-v0:2                                          | $0.15                             | $0.2                                  | 32,000              |                8191 |
| bedrock/eu-west-3/mistral.mistral-7b-instruct-v0:2                                          | $0.2                              | $0.26                                 | 32,000              |                8191 |
| bedrock/us-east-1/mistral.mistral-large-2402-v1:0                                           | $8.00                             | $24.00                                | 32,000              |                8191 |
| bedrock/us-west-2/mistral.mistral-large-2402-v1:0                                           | $8.00                             | $24.00                                | 32,000              |                8191 |
| bedrock/eu-west-3/mistral.mistral-large-2402-v1:0                                           | $10.4                             | $31.2                                 | 32,000              |                8191 |
| anthropic.claude-3-sonnet-20240229-v1:0                                                     | $3.00                             | $15.00                                | 200,000             |                4096 |
| anthropic.claude-3-haiku-20240307-v1:0                                                      | $0.25                             | $1.25                                 | 200,000             |                4096 |
| anthropic.claude-3-opus-20240229-v1:0                                                       | $15.00                            | $75.00                                | 200,000             |                4096 |
| anthropic.claude-v1                                                                         | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/us-east-1/anthropic.claude-v1                                                       | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/us-west-2/anthropic.claude-v1                                                       | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/ap-northeast-1/anthropic.claude-v1                                                  | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v1                               | --                                | --                                    | 100,000             |                8191 |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v1                               | --                                | --                                    | 100,000             |                8191 |
| bedrock/eu-central-1/anthropic.claude-v1                                                    | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v1                                 | --                                | --                                    | 100,000             |                8191 |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v1                                 | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v1                                    | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v1                                    | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v1                                    | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v1                                    | --                                | --                                    | 100,000             |                8191 |
| anthropic.claude-v2                                                                         | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/us-east-1/anthropic.claude-v2                                                       | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/us-west-2/anthropic.claude-v2                                                       | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/ap-northeast-1/anthropic.claude-v2                                                  | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v2                               | --                                | --                                    | 100,000             |                8191 |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v2                               | --                                | --                                    | 100,000             |                8191 |
| bedrock/eu-central-1/anthropic.claude-v2                                                    | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v2                                 | --                                | --                                    | 100,000             |                8191 |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v2                                 | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v2                                    | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v2                                    | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v2                                    | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v2                                    | --                                | --                                    | 100,000             |                8191 |
| anthropic.claude-v2:1                                                                       | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/us-east-1/anthropic.claude-v2:1                                                     | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/us-west-2/anthropic.claude-v2:1                                                     | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/ap-northeast-1/anthropic.claude-v2:1                                                | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v2:1                             | --                                | --                                    | 100,000             |                8191 |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v2:1                             | --                                | --                                    | 100,000             |                8191 |
| bedrock/eu-central-1/anthropic.claude-v2:1                                                  | $8.00                             | $24.00                                | 100,000             |                8191 |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v2:1                               | --                                | --                                    | 100,000             |                8191 |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v2:1                               | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v2:1                                  | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v2:1                                  | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v2:1                                  | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v2:1                                  | --                                | --                                    | 100,000             |                8191 |
| anthropic.claude-instant-v1                                                                 | $1.63                             | $5.51                                 | 100,000             |                8191 |
| bedrock/us-east-1/anthropic.claude-instant-v1                                               | $0.8                              | $2.4                                  | 100,000             |                8191 |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-instant-v1                            | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-instant-v1                            | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-instant-v1                            | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-instant-v1                            | --                                | --                                    | 100,000             |                8191 |
| bedrock/us-west-2/anthropic.claude-instant-v1                                               | $0.8                              | $2.4                                  | 100,000             |                8191 |
| bedrock/ap-northeast-1/anthropic.claude-instant-v1                                          | $2.23                             | $7.55                                 | 100,000             |                8191 |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-instant-v1                       | --                                | --                                    | 100,000             |                8191 |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-instant-v1                       | --                                | --                                    | 100,000             |                8191 |
| bedrock/eu-central-1/anthropic.claude-instant-v1                                            | $2.48                             | $8.38                                 | 100,000             |                8191 |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-instant-v1                         | --                                | --                                    | 100,000             |                8191 |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-instant-v1                         | --                                | --                                    | 100,000             |                8191 |
| cohere.command-text-v14                                                                     | $1.5                              | $2.00                                 | 4,096               |                4096 |
| bedrock/*/1-month-commitment/cohere.command-text-v14                                        | --                                | --                                    | 4,096               |                4096 |
| bedrock/*/6-month-commitment/cohere.command-text-v14                                        | --                                | --                                    | 4,096               |                4096 |
| cohere.command-light-text-v14                                                               | $0.3                              | $0.6                                  | 4,096               |                4096 |
| bedrock/*/1-month-commitment/cohere.command-light-text-v14                                  | --                                | --                                    | 4,096               |                4096 |
| bedrock/*/6-month-commitment/cohere.command-light-text-v14                                  | --                                | --                                    | 4,096               |                4096 |
| cohere.command-r-plus-v1:0                                                                  | $3.00                             | $15.00                                | 128,000             |                4096 |
| cohere.command-r-v1:0                                                                       | $0.5                              | $1.5                                  | 128,000             |                4096 |
| cohere.embed-english-v3                                                                     | $0.1                              | $0.00                                 | 512                 |                 nan |
| cohere.embed-multilingual-v3                                                                | $0.1                              | $0.00                                 | 512                 |                 nan |
| meta.llama2-13b-chat-v1                                                                     | $0.75                             | $1.00                                 | 4,096               |                4096 |
| meta.llama2-70b-chat-v1                                                                     | $1.95                             | $2.56                                 | 4,096               |                4096 |
| meta.llama3-8b-instruct-v1:0                                                                | $0.4                              | $0.6                                  | 8,192               |                8192 |
| meta.llama3-70b-instruct-v1:0                                                               | $2.65                             | $3.5                                  | 8,192               |                8192 |
| 512-x-512/50-steps/stability.stable-diffusion-xl-v0                                         | --                                | --                                    | 77                  |                 nan |
| 512-x-512/max-steps/stability.stable-diffusion-xl-v0                                        | --                                | --                                    | 77                  |                 nan |
| max-x-max/50-steps/stability.stable-diffusion-xl-v0                                         | --                                | --                                    | 77                  |                 nan |
| max-x-max/max-steps/stability.stable-diffusion-xl-v0                                        | --                                | --                                    | 77                  |                 nan |
| 1024-x-1024/50-steps/stability.stable-diffusion-xl-v1                                       | --                                | --                                    | 77                  |                 nan |
| 1024-x-1024/max-steps/stability.stable-diffusion-xl-v1                                      | --                                | --                                    | 77                  |                 nan |
| sagemaker/meta-textgeneration-llama-2-7b                                                    | $0.00                             | $0.00                                 | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-7b-f                                                  | $0.00                             | $0.00                                 | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-13b                                                   | $0.00                             | $0.00                                 | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-13b-f                                                 | $0.00                             | $0.00                                 | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-70b                                                   | $0.00                             | $0.00                                 | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-70b-b-f                                               | $0.00                             | $0.00                                 | 4,096               |                4096 |
| together-ai-up-to-4b                                                                        | $0.1                              | $0.1                                  | nan                 |                 nan |
| together-ai-4.1b-8b                                                                         | $0.2                              | $0.2                                  | nan                 |                 nan |
| together-ai-8.1b-21b                                                                        | $0.3                              | $0.3                                  | nan                 |                 nan |
| together-ai-21.1b-41b                                                                       | $0.8                              | $0.8                                  | nan                 |                 nan |
| together-ai-41.1b-80b                                                                       | $0.9                              | $0.9                                  | nan                 |                 nan |
| together-ai-81.1b-110b                                                                      | $1.8                              | $1.8                                  | nan                 |                 nan |
| together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1                                            | $0.6                              | $0.6                                  | nan                 |                 nan |
| together_ai/mistralai/Mistral-7B-Instruct-v0.1                                              | --                                | --                                    | nan                 |                 nan |
| together_ai/togethercomputer/CodeLlama-34b-Instruct                                         | --                                | --                                    | nan                 |                 nan |
| ollama/llama2                                                                               | $0.00                             | $0.00                                 | 4,096               |                4096 |
| ollama/llama2:13b                                                                           | $0.00                             | $0.00                                 | 4,096               |                4096 |
| ollama/llama2:70b                                                                           | $0.00                             | $0.00                                 | 4,096               |                4096 |
| ollama/llama2-uncensored                                                                    | $0.00                             | $0.00                                 | 4,096               |                4096 |
| ollama/llama3                                                                               | $0.00                             | $0.00                                 | 8,192               |                8192 |
| ollama/llama3:70b                                                                           | $0.00                             | $0.00                                 | 8,192               |                8192 |
| ollama/mistral                                                                              | $0.00                             | $0.00                                 | 8,192               |                8192 |
| ollama/mistral-7B-Instruct-v0.1                                                             | $0.00                             | $0.00                                 | 8,192               |                8192 |
| ollama/mistral-7B-Instruct-v0.2                                                             | $0.00                             | $0.00                                 | 32,768              |               32768 |
| ollama/mixtral-8x7B-Instruct-v0.1                                                           | $0.00                             | $0.00                                 | 32,768              |               32768 |
| ollama/mixtral-8x22B-Instruct-v0.1                                                          | $0.00                             | $0.00                                 | 65,536              |               65536 |
| ollama/codellama                                                                            | $0.00                             | $0.00                                 | 4,096               |                4096 |
| ollama/orca-mini                                                                            | $0.00                             | $0.00                                 | 4,096               |                4096 |
| ollama/vicuna                                                                               | $0.00                             | $0.00                                 | 2,048               |                2048 |
| deepinfra/lizpreciatior/lzlv_70b_fp16_hf                                                    | $0.7                              | $0.9                                  | 4,096               |                4096 |
| deepinfra/Gryphe/MythoMax-L2-13b                                                            | $0.22                             | $0.22                                 | 4,096               |                4096 |
| deepinfra/mistralai/Mistral-7B-Instruct-v0.1                                                | $0.13                             | $0.13                                 | 32,768              |                8191 |
| deepinfra/meta-llama/Llama-2-70b-chat-hf                                                    | $0.7                              | $0.9                                  | 4,096               |                4096 |
| deepinfra/cognitivecomputations/dolphin-2.6-mixtral-8x7b                                    | $0.27                             | $0.27                                 | 32,768              |                8191 |
| deepinfra/codellama/CodeLlama-34b-Instruct-hf                                               | $0.6                              | $0.6                                  | 4,096               |                4096 |
| deepinfra/deepinfra/mixtral                                                                 | $0.27                             | $0.27                                 | 32,000              |                4096 |
| deepinfra/Phind/Phind-CodeLlama-34B-v2                                                      | $0.6                              | $0.6                                  | 16,384              |                4096 |
| deepinfra/mistralai/Mixtral-8x7B-Instruct-v0.1                                              | $0.27                             | $0.27                                 | 32,768              |                8191 |
| deepinfra/deepinfra/airoboros-70b                                                           | $0.7                              | $0.9                                  | 4,096               |                4096 |
| deepinfra/01-ai/Yi-34B-Chat                                                                 | $0.6                              | $0.6                                  | 4,096               |                4096 |
| deepinfra/01-ai/Yi-6B-200K                                                                  | $0.13                             | $0.13                                 | 200,000             |                4096 |
| deepinfra/jondurbin/airoboros-l2-70b-gpt4-1.4.1                                             | $0.7                              | $0.9                                  | 4,096               |                4096 |
| deepinfra/meta-llama/Llama-2-13b-chat-hf                                                    | $0.22                             | $0.22                                 | 4,096               |                4096 |
| deepinfra/amazon/MistralLite                                                                | $0.2                              | $0.2                                  | 32,768              |                8191 |
| deepinfra/meta-llama/Llama-2-7b-chat-hf                                                     | $0.13                             | $0.13                                 | 4,096               |                4096 |
| deepinfra/meta-llama/Meta-Llama-3-8B-Instruct                                               | $0.08                             | $0.08                                 | 8,191               |                4096 |
| deepinfra/meta-llama/Meta-Llama-3-70B-Instruct                                              | $0.59                             | $0.79                                 | 8,191               |                4096 |
| deepinfra/01-ai/Yi-34B-200K                                                                 | $0.6                              | $0.6                                  | 200,000             |                4096 |
| deepinfra/openchat/openchat_3.5                                                             | $0.13                             | $0.13                                 | 4,096               |                4096 |
| perplexity/codellama-34b-instruct                                                           | $0.35                             | $1.4                                  | 16,384              |               16384 |
| perplexity/codellama-70b-instruct                                                           | $0.7                              | $2.8                                  | 16,384              |               16384 |
| perplexity/pplx-7b-chat                                                                     | $0.07                             | $0.28                                 | 8,192               |                8192 |
| perplexity/pplx-70b-chat                                                                    | $0.7                              | $2.8                                  | 4,096               |                4096 |
| perplexity/pplx-7b-online                                                                   | $0.00                             | $0.28                                 | 4,096               |                4096 |
| perplexity/pplx-70b-online                                                                  | $0.00                             | $2.8                                  | 4,096               |                4096 |
| perplexity/llama-2-70b-chat                                                                 | $0.7                              | $2.8                                  | 4,096               |                4096 |
| perplexity/mistral-7b-instruct                                                              | $0.07                             | $0.28                                 | 4,096               |                4096 |
| perplexity/mixtral-8x7b-instruct                                                            | $0.07                             | $0.28                                 | 4,096               |                4096 |
| perplexity/sonar-small-chat                                                                 | $0.07                             | $0.28                                 | 16,384              |               16384 |
| perplexity/sonar-small-online                                                               | $0.00                             | $0.28                                 | 12,000              |               12000 |
| perplexity/sonar-medium-chat                                                                | $0.6                              | $1.8                                  | 16,384              |               16384 |
| perplexity/sonar-medium-online                                                              | $0.00                             | $1.8                                  | 12,000              |               12000 |
| anyscale/mistralai/Mistral-7B-Instruct-v0.1                                                 | $0.15                             | $0.15                                 | 16,384              |               16384 |
| anyscale/mistralai/Mixtral-8x7B-Instruct-v0.1                                               | $0.15                             | $0.15                                 | 16,384              |               16384 |
| anyscale/mistralai/Mixtral-8x22B-Instruct-v0.1                                              | $0.9                              | $0.9                                  | 65,536              |               65536 |
| anyscale/HuggingFaceH4/zephyr-7b-beta                                                       | $0.15                             | $0.15                                 | 16,384              |               16384 |
| anyscale/google/gemma-7b-it                                                                 | $0.15                             | $0.15                                 | 8,192               |                8192 |
| anyscale/meta-llama/Llama-2-7b-chat-hf                                                      | $0.15                             | $0.15                                 | 4,096               |                4096 |
| anyscale/meta-llama/Llama-2-13b-chat-hf                                                     | $0.25                             | $0.25                                 | 4,096               |                4096 |
| anyscale/meta-llama/Llama-2-70b-chat-hf                                                     | $1.00                             | $1.00                                 | 4,096               |                4096 |
| anyscale/codellama/CodeLlama-34b-Instruct-hf                                                | $1.00                             | $1.00                                 | 4,096               |                4096 |
| anyscale/codellama/CodeLlama-70b-Instruct-hf                                                | $1.00                             | $1.00                                 | 4,096               |                4096 |
| anyscale/meta-llama/Meta-Llama-3-8B-Instruct                                                | $0.15                             | $0.15                                 | 8,192               |                8192 |
| anyscale/meta-llama/Meta-Llama-3-70B-Instruct                                               | $1.00                             | $1.00                                 | 8,192               |                8192 |
| cloudflare/@cf/meta/llama-2-7b-chat-fp16                                                    | $1.923                            | $1.923                                | 3,072               |                3072 |
| cloudflare/@cf/meta/llama-2-7b-chat-int8                                                    | $1.923                            | $1.923                                | 2,048               |                2048 |
| cloudflare/@cf/mistral/mistral-7b-instruct-v0.1                                             | $1.923                            | $1.923                                | 8,192               |                8192 |
| cloudflare/@hf/thebloke/codellama-7b-instruct-awq                                           | $1.923                            | $1.923                                | 4,096               |                4096 |
| voyage/voyage-01                                                                            | $0.1                              | $0.00                                 | 4,096               |                 nan |
| voyage/voyage-lite-01                                                                       | $0.1                              | $0.00                                 | 4,096               |                 nan |
| voyage/voyage-large-2                                                                       | $0.12                             | $0.00                                 | 16,000              |                 nan |
| voyage/voyage-law-2                                                                         | $0.12                             | $0.00                                 | 16,000              |                 nan |
| voyage/voyage-code-2                                                                        | $0.12                             | $0.00                                 | 16,000              |                 nan |
| voyage/voyage-2                                                                             | $0.1                              | $0.00                                 | 4,000               |                 nan |
| voyage/voyage-lite-02-instruct                                                              | $0.1                              | $0.00                                 | 4,000               |                 nan |
| databricks/databricks-dbrx-instruct                                                         | $0.75                             | $2.25                                 | 32,768              |               32768 |
| databricks/databricks-meta-llama-3-70b-instruct                                             | $1.00                             | $3.00                                 | 8,192               |                8192 |
| databricks/databricks-llama-2-70b-chat                                                      | $0.5                              | $1.5                                  | 4,096               |                4096 |
| databricks/databricks-mixtral-8x7b-instruct                                                 | $0.5                              | $1.00                                 | 4,096               |                4096 |
| databricks/databricks-mpt-30b-instruct                                                      | $1.00                             | $1.00                                 | 8,192               |                8192 |
| databricks/databricks-mpt-7b-instruct                                                       | $0.5                              | $0.5                                  | 8,192               |                8192 |
| databricks/databricks-bge-large-en                                                          | $0.1                              | $0.00                                 | 512                 |                 nan |

### Callback handlers
You may also calculate token costs in LLM wrapper/framework libraries using callbacks. 

#### LlamaIndex
```sh
pip install `'tokencost[llama-index]'`
```
To use the base callback handler, you may import it:

```python
from tokencost.callbacks.llama_index import TokenCostHandler
```

and pass to your framework callback handler.

#### Langchain
(Coming Soon)

### Running locally

#### Installation via [GitHub](https://github.com/AgentOps-AI/tokencost):

```bash
git clone git@github.com:AgentOps-AI/tokencost.git
cd tokencost
pip install -e .
```

## Running tests

0. Install `pytest` if you don't have it already

```shell
pip install pytest
```

1. Run the `tests/` folder while in the parent directory

```shell
pytest tests
```

This repo also supports `tox`, simply run `python -m tox`.

## Contributing

Contributions to TokenCost are welcome! Feel free to create an [issue](https://github.com/AgentOps-AI/tokencost/issues) for any bug reports, complaints, or feature suggestions.

## License

TokenCost is released under the MIT License.
