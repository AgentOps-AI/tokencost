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
<a href="https://discord.com/invite/FagdcwwXRR">📢 Discord</a>
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

## How tokens are counted

Under the hood, strings and ChatML messages are tokenized using [Tiktoken](https://github.com/openai/tiktoken), OpenAI's official tokenizer. Tiktoken splits text into tokens (which can be parts of words or individual characters) and handles both raw strings and message formats with additional tokens for message formatting and roles.

For Anthropic models above version 3 (i.e. Sonnet 3.5, Haiku 3.5, and Opus 3), we use the [Anthropic beta token counting API](https://docs.anthropic.com/claude/docs/beta-api-for-counting-tokens) to ensure accurate token counts. For older Claude models, we approximate using Tiktoken with the cl100k_base encoding.


## Cost table
Units denominated in USD. All prices can be located in `model_prices.json`.


* Prices last updated Jan 30, 2024 from [LiteLLM's cost dictionary](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)

| Model Name                                                            | Prompt Cost (USD) per 1M tokens   | Completion Cost (USD) per 1M tokens   | Max Prompt Tokens   |   Max Output Tokens |
|:----------------------------------------------------------------------|:----------------------------------|:--------------------------------------|:--------------------|--------------------:|
| gpt-4                                                                 | $30                               | $60                                   | 8192                |            4096     |
| gpt-4o                                                                | $2.5                              | $10                                   | 128,000             |           16384     |
| gpt-4o-audio-preview                                                  | $2.5                              | $10                                   | 128,000             |           16384     |
| gpt-4o-audio-preview-2024-10-01                                       | $2.5                              | $10                                   | 128,000             |           16384     |
| gpt-4o-mini                                                           | $0.15                             | $0.6                                  | 128,000             |           16384     |
| gpt-4o-mini-2024-07-18                                                | $0.15                             | $0.6                                  | 128,000             |           16384     |
| o1-mini                                                               | $1.1                              | $4.4                                  | 128,000             |           65536     |
| o1-mini-2024-09-12                                                    | $3                                | $12                                   | 128,000             |           65536     |
| o1-preview                                                            | $15                               | $60                                   | 128,000             |           32768     |
| o1-preview-2024-09-12                                                 | $15                               | $60                                   | 128,000             |           32768     |
| chatgpt-4o-latest                                                     | $5                                | $15                                   | 128,000             |            4096     |
| gpt-4o-2024-05-13                                                     | $5                                | $15                                   | 128,000             |            4096     |
| gpt-4o-2024-08-06                                                     | $2.5                              | $10                                   | 128,000             |           16384     |
| gpt-4-turbo-preview                                                   | $10                               | $30                                   | 128,000             |            4096     |
| gpt-4-0314                                                            | $30                               | $60                                   | 8,192               |            4096     |
| gpt-4-0613                                                            | $30                               | $60                                   | 8,192               |            4096     |
| gpt-4-32k                                                             | $60                               | $120                                  | 32,768              |            4096     |
| gpt-4-32k-0314                                                        | $60                               | $120                                  | 32,768              |            4096     |
| gpt-4-32k-0613                                                        | $60                               | $120                                  | 32,768              |            4096     |
| gpt-4-turbo                                                           | $10                               | $30                                   | 128,000             |            4096     |
| gpt-4-turbo-2024-04-09                                                | $10                               | $30                                   | 128,000             |            4096     |
| gpt-4-1106-preview                                                    | $10                               | $30                                   | 128,000             |            4096     |
| gpt-4-0125-preview                                                    | $10                               | $30                                   | 128,000             |            4096     |
| gpt-4-vision-preview                                                  | $10                               | $30                                   | 128,000             |            4096     |
| gpt-4-1106-vision-preview                                             | $10                               | $30                                   | 128,000             |            4096     |
| gpt-3.5-turbo                                                         | $1.5                              | $2                                    | 16,385              |            4096     |
| gpt-3.5-turbo-0301                                                    | $1.5                              | $2                                    | 4,097               |            4096     |
| gpt-3.5-turbo-0613                                                    | $1.5                              | $2                                    | 4,097               |            4096     |
| gpt-3.5-turbo-1106                                                    | $1                                | $2                                    | 16,385              |            4096     |
| gpt-3.5-turbo-0125                                                    | $0.5                              | $1.5                                  | 16,385              |            4096     |
| gpt-3.5-turbo-16k                                                     | $3                                | $4                                    | 16,385              |            4096     |
| gpt-3.5-turbo-16k-0613                                                | $3                                | $4                                    | 16,385              |            4096     |
| ft:gpt-3.5-turbo                                                      | $3                                | $6                                    | 16,385              |            4096     |
| ft:gpt-3.5-turbo-0125                                                 | $3                                | $6                                    | 16,385              |            4096     |
| ft:gpt-3.5-turbo-1106                                                 | $3                                | $6                                    | 16,385              |            4096     |
| ft:gpt-3.5-turbo-0613                                                 | $3                                | $6                                    | 4,096               |            4096     |
| ft:gpt-4-0613                                                         | $30                               | $60                                   | 8,192               |            4096     |
| ft:gpt-4o-2024-08-06                                                  | $3.75                             | $15                                   | 128,000             |           16384     |
| ft:gpt-4o-mini-2024-07-18                                             | $0.3                              | $1.2                                  | 128,000             |           16384     |
| ft:davinci-002                                                        | $2                                | $2                                    | 16,384              |            4096     |
| ft:babbage-002                                                        | $0.4                              | $0.4                                  | 16,384              |            4096     |
| text-embedding-3-large                                                | $0.13                             | $0                                    | 8,191               |             nan     |
| text-embedding-3-small                                                | $0.02                             | $0                                    | 8,191               |             nan     |
| text-embedding-ada-002                                                | $0.1                              | $0                                    | 8,191               |             nan     |
| text-embedding-ada-002-v2                                             | $0.1                              | $0                                    | 8,191               |             nan     |
| text-moderation-stable                                                | $0                                | $0                                    | 32,768              |               0     |
| text-moderation-007                                                   | $0                                | $0                                    | 32,768              |               0     |
| text-moderation-latest                                                | $0                                | $0                                    | 32,768              |               0     |
| 256-x-256/dall-e-2                                                    | --                                | --                                    | nan                 |             nan     |
| 512-x-512/dall-e-2                                                    | --                                | --                                    | nan                 |             nan     |
| 1024-x-1024/dall-e-2                                                  | --                                | --                                    | nan                 |             nan     |
| hd/1024-x-1792/dall-e-3                                               | --                                | --                                    | nan                 |             nan     |
| hd/1792-x-1024/dall-e-3                                               | --                                | --                                    | nan                 |             nan     |
| hd/1024-x-1024/dall-e-3                                               | --                                | --                                    | nan                 |             nan     |
| standard/1024-x-1792/dall-e-3                                         | --                                | --                                    | nan                 |             nan     |
| standard/1792-x-1024/dall-e-3                                         | --                                | --                                    | nan                 |             nan     |
| standard/1024-x-1024/dall-e-3                                         | --                                | --                                    | nan                 |             nan     |
| whisper-1                                                             | --                                | --                                    | nan                 |             nan     |
| tts-1                                                                 | --                                | --                                    | nan                 |             nan     |
| tts-1-hd                                                              | --                                | --                                    | nan                 |             nan     |
| azure/tts-1                                                           | --                                | --                                    | nan                 |             nan     |
| azure/tts-1-hd                                                        | --                                | --                                    | nan                 |             nan     |
| azure/whisper-1                                                       | --                                | --                                    | nan                 |             nan     |
| azure/o1-mini                                                         | $1.21                             | $4.84                                 | 128,000             |           65536     |
| azure/o1-mini-2024-09-12                                              | $1.1                              | $4.4                                  | 128,000             |           65536     |
| azure/o1-preview                                                      | $15                               | $60                                   | 128,000             |           32768     |
| azure/o1-preview-2024-09-12                                           | $15                               | $60                                   | 128,000             |           32768     |
| azure/gpt-4o                                                          | $2.5                              | $10                                   | 128,000             |           16384     |
| azure/gpt-4o-2024-08-06                                               | $2.5                              | $10                                   | 128,000             |           16384     |
| azure/gpt-4o-2024-05-13                                               | $5                                | $15                                   | 128,000             |            4096     |
| azure/global-standard/gpt-4o-2024-08-06                               | $2.5                              | $10                                   | 128,000             |           16384     |
| azure/global-standard/gpt-4o-mini                                     | $0.15                             | $0.6                                  | 128,000             |           16384     |
| azure/gpt-4o-mini                                                     | $0.16                             | $0.66                                 | 128,000             |           16384     |
| azure/gpt-4-turbo-2024-04-09                                          | $10                               | $30                                   | 128,000             |            4096     |
| azure/gpt-4-0125-preview                                              | $10                               | $30                                   | 128,000             |            4096     |
| azure/gpt-4-1106-preview                                              | $10                               | $30                                   | 128,000             |            4096     |
| azure/gpt-4-0613                                                      | $30                               | $60                                   | 8,192               |            4096     |
| azure/gpt-4-32k-0613                                                  | $60                               | $120                                  | 32,768              |            4096     |
| azure/gpt-4-32k                                                       | $60                               | $120                                  | 32,768              |            4096     |
| azure/gpt-4                                                           | $30                               | $60                                   | 8,192               |            4096     |
| azure/gpt-4-turbo                                                     | $10                               | $30                                   | 128,000             |            4096     |
| azure/gpt-4-turbo-vision-preview                                      | $10                               | $30                                   | 128,000             |            4096     |
| azure/gpt-35-turbo-16k-0613                                           | $3                                | $4                                    | 16,385              |            4096     |
| azure/gpt-35-turbo-1106                                               | $1                                | $2                                    | 16,384              |            4096     |
| azure/gpt-35-turbo-0613                                               | $1.5                              | $2                                    | 4,097               |            4096     |
| azure/gpt-35-turbo-0301                                               | $0.2                              | $2                                    | 4,097               |            4096     |
| azure/gpt-35-turbo-0125                                               | $0.5                              | $1.5                                  | 16,384              |            4096     |
| azure/gpt-35-turbo-16k                                                | $3                                | $4                                    | 16,385              |            4096     |
| azure/gpt-35-turbo                                                    | $0.5                              | $1.5                                  | 4,097               |            4096     |
| azure/gpt-3.5-turbo-instruct-0914                                     | $1.5                              | $2                                    | 4,097               |             nan     |
| azure/gpt-35-turbo-instruct                                           | $1.5                              | $2                                    | 4,097               |             nan     |
| azure/gpt-35-turbo-instruct-0914                                      | $1.5                              | $2                                    | 4,097               |             nan     |
| azure/mistral-large-latest                                            | $8                                | $24                                   | 32,000              |             nan     |
| azure/mistral-large-2402                                              | $8                                | $24                                   | 32,000              |             nan     |
| azure/command-r-plus                                                  | $3                                | $15                                   | 128,000             |            4096     |
| azure/ada                                                             | $0.1                              | $0                                    | 8,191               |             nan     |
| azure/text-embedding-ada-002                                          | $0.1                              | $0                                    | 8,191               |             nan     |
| azure/text-embedding-3-large                                          | $0.13                             | $0                                    | 8,191               |             nan     |
| azure/text-embedding-3-small                                          | $0.02                             | $0                                    | 8,191               |             nan     |
| azure/standard/1024-x-1024/dall-e-3                                   | --                                | $0                                    | nan                 |             nan     |
| azure/hd/1024-x-1024/dall-e-3                                         | --                                | $0                                    | nan                 |             nan     |
| azure/standard/1024-x-1792/dall-e-3                                   | --                                | $0                                    | nan                 |             nan     |
| azure/standard/1792-x-1024/dall-e-3                                   | --                                | $0                                    | nan                 |             nan     |
| azure/hd/1024-x-1792/dall-e-3                                         | --                                | $0                                    | nan                 |             nan     |
| azure/hd/1792-x-1024/dall-e-3                                         | --                                | $0                                    | nan                 |             nan     |
| azure/standard/1024-x-1024/dall-e-2                                   | --                                | $0                                    | nan                 |             nan     |
| azure_ai/jamba-instruct                                               | $0.5                              | $0.7                                  | 70,000              |            4096     |
| azure_ai/mistral-large                                                | $4                                | $12                                   | 32,000              |            8191     |
| azure_ai/mistral-small                                                | $1                                | $3                                    | 32,000              |            8191     |
| azure_ai/Meta-Llama-3-70B-Instruct                                    | $1.1                              | $0.37                                 | 8,192               |            2048     |
| azure_ai/Meta-Llama-3.1-8B-Instruct                                   | $0.3                              | $0.61                                 | 128,000             |            2048     |
| azure_ai/Meta-Llama-3.1-70B-Instruct                                  | $2.68                             | $3.54                                 | 128,000             |            2048     |
| azure_ai/Meta-Llama-3.1-405B-Instruct                                 | $5.33                             | $16                                   | 128,000             |            2048     |
| azure_ai/cohere-rerank-v3-multilingual                                | $0                                | $0                                    | 4,096               |            4096     |
| azure_ai/cohere-rerank-v3-english                                     | $0                                | $0                                    | 4,096               |            4096     |
| azure_ai/Cohere-embed-v3-english                                      | $0.1                              | $0                                    | 512                 |             nan     |
| azure_ai/Cohere-embed-v3-multilingual                                 | $0.1                              | $0                                    | 512                 |             nan     |
| babbage-002                                                           | $0.4                              | $0.4                                  | 16,384              |            4096     |
| davinci-002                                                           | $2                                | $2                                    | 16,384              |            4096     |
| gpt-3.5-turbo-instruct                                                | $1.5                              | $2                                    | 8,192               |            4096     |
| gpt-3.5-turbo-instruct-0914                                           | $1.5                              | $2                                    | 8,192               |            4097     |
| claude-instant-1                                                      | $1.63                             | $5.51                                 | 100,000             |            8191     |
| mistral/mistral-tiny                                                  | $0.25                             | $0.25                                 | 32,000              |            8191     |
| mistral/mistral-small                                                 | $0.1                              | $0.3                                  | 32,000              |            8191     |
| mistral/mistral-small-latest                                          | $0.1                              | $0.3                                  | 32,000              |            8191     |
| mistral/mistral-medium                                                | $2.7                              | $8.1                                  | 32,000              |            8191     |
| mistral/mistral-medium-latest                                         | $2.7                              | $8.1                                  | 32,000              |            8191     |
| mistral/mistral-medium-2312                                           | $2.7                              | $8.1                                  | 32,000              |            8191     |
| mistral/mistral-large-latest                                          | $2                                | $6                                    | 128,000             |          128000     |
| mistral/mistral-large-2402                                            | $4                                | $12                                   | 32,000              |            8191     |
| mistral/mistral-large-2407                                            | $3                                | $9                                    | 128,000             |          128000     |
| mistral/pixtral-12b-2409                                              | $0.15                             | $0.15                                 | 128,000             |          128000     |
| mistral/open-mistral-7b                                               | $0.25                             | $0.25                                 | 32,000              |            8191     |
| mistral/open-mixtral-8x7b                                             | $0.7                              | $0.7                                  | 32,000              |            8191     |
| mistral/open-mixtral-8x22b                                            | $2                                | $6                                    | 65,336              |            8191     |
| mistral/codestral-latest                                              | $1                                | $3                                    | 32,000              |            8191     |
| mistral/codestral-2405                                                | $1                                | $3                                    | 32,000              |            8191     |
| mistral/open-mistral-nemo                                             | $0.3                              | $0.3                                  | 128,000             |          128000     |
| mistral/open-mistral-nemo-2407                                        | $0.3                              | $0.3                                  | 128,000             |          128000     |
| mistral/open-codestral-mamba                                          | $0.25                             | $0.25                                 | 256,000             |          256000     |
| mistral/codestral-mamba-latest                                        | $0.25                             | $0.25                                 | 256,000             |          256000     |
| mistral/mistral-embed                                                 | $0.1                              | --                                    | 8,192               |             nan     |
| deepseek-chat                                                         | $0.14                             | $0.28                                 | 128,000             |            4096     |
| codestral/codestral-latest                                            | $0                                | $0                                    | 32,000              |            8191     |
| codestral/codestral-2405                                              | $0                                | $0                                    | 32,000              |            8191     |
| text-completion-codestral/codestral-latest                            | $0                                | $0                                    | 32,000              |            8191     |
| text-completion-codestral/codestral-2405                              | $0                                | $0                                    | 32,000              |            8191     |
| deepseek-coder                                                        | $0.14                             | $0.28                                 | 128,000             |            4096     |
| groq/llama2-70b-4096                                                  | $0.7                              | $0.8                                  | 4,096               |            4096     |
| groq/llama3-8b-8192                                                   | $0.05                             | $0.08                                 | 8,192               |            8192     |
| groq/llama3-70b-8192                                                  | $0.59                             | $0.79                                 | 8,192               |            8192     |
| groq/llama-3.1-8b-instant                                             | $0.05                             | $0.08                                 | 8,192               |            8192     |
| groq/llama-3.1-70b-versatile                                          | $0.59                             | $0.79                                 | 8,192               |            8192     |
| groq/llama-3.1-405b-reasoning                                         | $0.59                             | $0.79                                 | 8,192               |            8192     |
| groq/mixtral-8x7b-32768                                               | $0.24                             | $0.24                                 | 32,768              |           32768     |
| groq/gemma-7b-it                                                      | $0.07                             | $0.07                                 | 8,192               |            8192     |
| groq/gemma2-9b-it                                                     | $0.2                              | $0.2                                  | 8,192               |            8192     |
| groq/llama3-groq-70b-8192-tool-use-preview                            | $0.89                             | $0.89                                 | 8,192               |            8192     |
| groq/llama3-groq-8b-8192-tool-use-preview                             | $0.19                             | $0.19                                 | 8,192               |            8192     |
| cerebras/llama3.1-8b                                                  | $0.1                              | $0.1                                  | 128,000             |          128000     |
| cerebras/llama3.1-70b                                                 | $0.6                              | $0.6                                  | 128,000             |          128000     |
| friendliai/mixtral-8x7b-instruct-v0-1                                 | $0.4                              | $0.4                                  | 32,768              |           32768     |
| friendliai/meta-llama-3-8b-instruct                                   | $0.1                              | $0.1                                  | 8,192               |            8192     |
| friendliai/meta-llama-3-70b-instruct                                  | $0.8                              | $0.8                                  | 8,192               |            8192     |
| claude-instant-1.2                                                    | $0.16                             | $0.55                                 | 100,000             |            8191     |
| claude-2                                                              | $8                                | $24                                   | 100,000             |            8191     |
| claude-2.1                                                            | $8                                | $24                                   | 200,000             |            8191     |
| claude-3-haiku-20240307                                               | $0.25                             | $1.25                                 | 200,000             |            4096     |
| claude-3-haiku-latest                                                 | $0.25                             | $1.25                                 | 200,000             |            4096     |
| claude-3-opus-20240229                                                | $15                               | $75                                   | 200,000             |            4096     |
| claude-3-opus-latest                                                  | $15                               | $75                                   | 200,000             |            4096     |
| claude-3-sonnet-20240229                                              | $3                                | $15                                   | 200,000             |            4096     |
| claude-3-5-sonnet-20240620                                            | $3                                | $15                                   | 200,000             |            8192     |
| claude-3-5-sonnet-20241022                                            | $3                                | $15                                   | 200,000             |            8192     |
| claude-3-5-sonnet-latest                                              | $3                                | $15                                   | 200,000             |            8192     |
| text-bison                                                            | --                                | --                                    | 8,192               |            2048     |
| text-bison@001                                                        | --                                | --                                    | 8,192               |            1024     |
| text-bison@002                                                        | --                                | --                                    | 8,192               |            1024     |
| text-bison32k                                                         | $0.12                             | $0.12                                 | 8,192               |            1024     |
| text-bison32k@002                                                     | $0.12                             | $0.12                                 | 8,192               |            1024     |
| text-unicorn                                                          | $10                               | $28                                   | 8,192               |            1024     |
| text-unicorn@001                                                      | $10                               | $28                                   | 8,192               |            1024     |
| chat-bison                                                            | $0.12                             | $0.12                                 | 8,192               |            4096     |
| chat-bison@001                                                        | $0.12                             | $0.12                                 | 8,192               |            4096     |
| chat-bison@002                                                        | $0.12                             | $0.12                                 | 8,192               |            4096     |
| chat-bison-32k                                                        | $0.12                             | $0.12                                 | 32,000              |            8192     |
| chat-bison-32k@002                                                    | $0.12                             | $0.12                                 | 32,000              |            8192     |
| code-bison                                                            | $0.12                             | $0.12                                 | 6,144               |            1024     |
| code-bison@001                                                        | $0.12                             | $0.12                                 | 6,144               |            1024     |
| code-bison@002                                                        | $0.12                             | $0.12                                 | 6,144               |            1024     |
| code-bison32k                                                         | $0.12                             | $0.12                                 | 6,144               |            1024     |
| code-bison-32k@002                                                    | $0.12                             | $0.12                                 | 6,144               |            1024     |
| code-gecko@001                                                        | $0.12                             | $0.12                                 | 2,048               |              64     |
| code-gecko@002                                                        | $0.12                             | $0.12                                 | 2,048               |              64     |
| code-gecko                                                            | $0.12                             | $0.12                                 | 2,048               |              64     |
| code-gecko-latest                                                     | $0.12                             | $0.12                                 | 2,048               |              64     |
| codechat-bison@latest                                                 | $0.12                             | $0.12                                 | 6,144               |            1024     |
| codechat-bison                                                        | $0.12                             | $0.12                                 | 6,144               |            1024     |
| codechat-bison@001                                                    | $0.12                             | $0.12                                 | 6,144               |            1024     |
| codechat-bison@002                                                    | $0.12                             | $0.12                                 | 6,144               |            1024     |
| codechat-bison-32k                                                    | $0.12                             | $0.12                                 | 32,000              |            8192     |
| codechat-bison-32k@002                                                | $0.12                             | $0.12                                 | 32,000              |            8192     |
| gemini-pro                                                            | $0.5                              | $1.5                                  | 32,760              |            8192     |
| gemini-1.0-pro                                                        | $0.5                              | $1.5                                  | 32,760              |            8192     |
| gemini-1.0-pro-001                                                    | $0.5                              | $1.5                                  | 32,760              |            8192     |
| gemini-1.0-ultra                                                      | $0.5                              | $1.5                                  | 8,192               |            2048     |
| gemini-1.0-ultra-001                                                  | $0.5                              | $1.5                                  | 8,192               |            2048     |
| gemini-1.0-pro-002                                                    | $0.5                              | $1.5                                  | 32,760              |            8192     |
| gemini-1.5-pro                                                        | $1.25                             | $5                                    | 2,097,152           |            8192     |
| gemini-1.5-pro-002                                                    | $1.25                             | $5                                    | 2,097,152           |            8192     |
| gemini-1.5-pro-001                                                    | $1.25                             | $5                                    | 1,000,000           |            8192     |
| gemini-1.5-pro-preview-0514                                           | $0.08                             | $0.31                                 | 1,000,000           |            8192     |
| gemini-1.5-pro-preview-0215                                           | $0.08                             | $0.31                                 | 1,000,000           |            8192     |
| gemini-1.5-pro-preview-0409                                           | $0.08                             | $0.31                                 | 1,000,000           |            8192     |
| gemini-1.5-flash                                                      | $0.08                             | $0.3                                  | 1,000,000           |            8192     |
| gemini-1.5-flash-exp-0827                                             | $0                                | $0                                    | 1,000,000           |            8192     |
| gemini-1.5-flash-002                                                  | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini-1.5-flash-001                                                  | $0.08                             | $0.3                                  | 1,000,000           |            8192     |
| gemini-1.5-flash-preview-0514                                         | $0.08                             | $0                                    | 1,000,000           |            8192     |
| gemini-pro-experimental                                               | $0                                | $0                                    | 1,000,000           |            8192     |
| gemini-flash-experimental                                             | $0                                | $0                                    | 1,000,000           |            8192     |
| gemini-pro-vision                                                     | $0.5                              | $1.5                                  | 16,384              |            2048     |
| gemini-1.0-pro-vision                                                 | $0.5                              | $1.5                                  | 16,384              |            2048     |
| gemini-1.0-pro-vision-001                                             | $0.5                              | $1.5                                  | 16,384              |            2048     |
| medlm-medium                                                          | --                                | --                                    | 32,768              |            8192     |
| medlm-large                                                           | --                                | --                                    | 8,192               |            1024     |
| vertex_ai/claude-3-sonnet@20240229                                    | $3                                | $15                                   | 200,000             |            4096     |
| vertex_ai/claude-3-5-sonnet@20240620                                  | $3                                | $15                                   | 200,000             |            8192     |
| vertex_ai/claude-3-5-sonnet-v2@20241022                               | $3                                | $15                                   | 200,000             |            8192     |
| vertex_ai/claude-3-haiku@20240307                                     | $0.25                             | $1.25                                 | 200,000             |            4096     |
| vertex_ai/claude-3-opus@20240229                                      | $15                               | $75                                   | 200,000             |            4096     |
| vertex_ai/meta/llama3-405b-instruct-maas                              | $0                                | $0                                    | 32,000              |           32000     |
| vertex_ai/meta/llama3-70b-instruct-maas                               | $0                                | $0                                    | 32,000              |           32000     |
| vertex_ai/meta/llama3-8b-instruct-maas                                | $0                                | $0                                    | 32,000              |           32000     |
| vertex_ai/meta/llama-3.2-90b-vision-instruct-maas                     | $0                                | $0                                    | 128,000             |            2048     |
| vertex_ai/mistral-large@latest                                        | $2                                | $6                                    | 128,000             |            8191     |
| vertex_ai/mistral-large@2407                                          | $2                                | $6                                    | 128,000             |            8191     |
| vertex_ai/mistral-nemo@latest                                         | $0.15                             | $0.15                                 | 128,000             |          128000     |
| vertex_ai/jamba-1.5-mini@001                                          | $0.2                              | $0.4                                  | 256,000             |          256000     |
| vertex_ai/jamba-1.5-large@001                                         | $2                                | $8                                    | 256,000             |          256000     |
| vertex_ai/jamba-1.5                                                   | $0.2                              | $0.4                                  | 256,000             |          256000     |
| vertex_ai/jamba-1.5-mini                                              | $0.2                              | $0.4                                  | 256,000             |          256000     |
| vertex_ai/jamba-1.5-large                                             | $2                                | $8                                    | 256,000             |          256000     |
| vertex_ai/mistral-nemo@2407                                           | $3                                | $3                                    | 128,000             |          128000     |
| vertex_ai/codestral@latest                                            | $0.2                              | $0.6                                  | 128,000             |          128000     |
| vertex_ai/codestral@2405                                              | $0.2                              | $0.6                                  | 128,000             |          128000     |
| vertex_ai/imagegeneration@006                                         | --                                | --                                    | nan                 |             nan     |
| vertex_ai/imagen-3.0-generate-001                                     | --                                | --                                    | nan                 |             nan     |
| vertex_ai/imagen-3.0-fast-generate-001                                | --                                | --                                    | nan                 |             nan     |
| text-embedding-004                                                    | $0.1                              | $0                                    | 2,048               |             nan     |
| text-multilingual-embedding-002                                       | $0.1                              | $0                                    | 2,048               |             nan     |
| textembedding-gecko                                                   | $0.1                              | $0                                    | 3,072               |             nan     |
| textembedding-gecko-multilingual                                      | $0.1                              | $0                                    | 3,072               |             nan     |
| textembedding-gecko-multilingual@001                                  | $0.1                              | $0                                    | 3,072               |             nan     |
| textembedding-gecko@001                                               | $0.1                              | $0                                    | 3,072               |             nan     |
| textembedding-gecko@003                                               | $0.1                              | $0                                    | 3,072               |             nan     |
| text-embedding-preview-0409                                           | $0.01                             | $0                                    | 3,072               |             nan     |
| text-multilingual-embedding-preview-0409                              | $0.01                             | $0                                    | 3,072               |             nan     |
| palm/chat-bison                                                       | $0.12                             | $0.12                                 | 8,192               |            4096     |
| palm/chat-bison-001                                                   | $0.12                             | $0.12                                 | 8,192               |            4096     |
| palm/text-bison                                                       | $0.12                             | $0.12                                 | 8,192               |            1024     |
| palm/text-bison-001                                                   | $0.12                             | $0.12                                 | 8,192               |            1024     |
| palm/text-bison-safety-off                                            | $0.12                             | $0.12                                 | 8,192               |            1024     |
| palm/text-bison-safety-recitation-off                                 | $0.12                             | $0.12                                 | 8,192               |            1024     |
| gemini/gemini-1.5-flash-002                                           | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini/gemini-1.5-flash-001                                           | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini/gemini-1.5-flash                                               | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini/gemini-1.5-flash-latest                                        | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini/gemini-1.5-flash-8b-exp-0924                                   | $0                                | $0                                    | 1,048,576           |            8192     |
| gemini/gemini-1.5-flash-exp-0827                                      | $0                                | $0                                    | 1,048,576           |            8192     |
| gemini/gemini-1.5-flash-8b-exp-0827                                   | $0                                | $0                                    | 1,000,000           |            8192     |
| gemini/gemini-pro                                                     | $0.35                             | $1.05                                 | 32,760              |            8192     |
| gemini/gemini-1.5-pro                                                 | $3.5                              | $10.5                                 | 2,097,152           |            8192     |
| gemini/gemini-1.5-pro-002                                             | $3.5                              | $10.5                                 | 2,097,152           |            8192     |
| gemini/gemini-1.5-pro-001                                             | $3.5                              | $10.5                                 | 2,097,152           |            8192     |
| gemini/gemini-1.5-pro-exp-0801                                        | $3.5                              | $10.5                                 | 2,097,152           |            8192     |
| gemini/gemini-1.5-pro-exp-0827                                        | $0                                | $0                                    | 2,097,152           |            8192     |
| gemini/gemini-1.5-pro-latest                                          | $3.5                              | $1.05                                 | 1,048,576           |            8192     |
| gemini/gemini-pro-vision                                              | $0.35                             | $1.05                                 | 30,720              |            2048     |
| gemini/gemini-gemma-2-27b-it                                          | $0.35                             | $1.05                                 | nan                 |            8192     |
| gemini/gemini-gemma-2-9b-it                                           | $0.35                             | $1.05                                 | nan                 |            8192     |
| command-r                                                             | $0.15                             | $0.6                                  | 128,000             |            4096     |
| command-r-08-2024                                                     | $0.15                             | $0.6                                  | 128,000             |            4096     |
| command-light                                                         | $0.3                              | $0.6                                  | 4,096               |            4096     |
| command-r-plus                                                        | $2.5                              | $10                                   | 128,000             |            4096     |
| command-r-plus-08-2024                                                | $2.5                              | $10                                   | 128,000             |            4096     |
| command-nightly                                                       | $1                                | $2                                    | 4,096               |            4096     |
| command                                                               | $1                                | $2                                    | 4,096               |            4096     |
| rerank-english-v3.0                                                   | $0                                | $0                                    | 4,096               |            4096     |
| rerank-multilingual-v3.0                                              | $0                                | $0                                    | 4,096               |            4096     |
| rerank-english-v2.0                                                   | $0                                | $0                                    | 4,096               |            4096     |
| rerank-multilingual-v2.0                                              | $0                                | $0                                    | 4,096               |            4096     |
| embed-english-v3.0                                                    | $0.1                              | $0                                    | 1,024               |             nan     |
| embed-english-light-v3.0                                              | $0.1                              | $0                                    | 1,024               |             nan     |
| embed-multilingual-v3.0                                               | $0.1                              | $0                                    | 1,024               |             nan     |
| embed-english-v2.0                                                    | $0.1                              | $0                                    | 4,096               |             nan     |
| embed-english-light-v2.0                                              | $0.1                              | $0                                    | 1,024               |             nan     |
| embed-multilingual-v2.0                                               | $0.1                              | $0                                    | 768                 |             nan     |
| replicate/meta/llama-2-13b                                            | $0.1                              | $0.5                                  | 4,096               |            4096     |
| replicate/meta/llama-2-13b-chat                                       | $0.1                              | $0.5                                  | 4,096               |            4096     |
| replicate/meta/llama-2-70b                                            | $0.65                             | $2.75                                 | 4,096               |            4096     |
| replicate/meta/llama-2-70b-chat                                       | $0.65                             | $2.75                                 | 4,096               |            4096     |
| replicate/meta/llama-2-7b                                             | $0.05                             | $0.25                                 | 4,096               |            4096     |
| replicate/meta/llama-2-7b-chat                                        | $0.05                             | $0.25                                 | 4,096               |            4096     |
| replicate/meta/llama-3-70b                                            | $0.65                             | $2.75                                 | 8,192               |            8192     |
| replicate/meta/llama-3-70b-instruct                                   | $0.65                             | $2.75                                 | 8,192               |            8192     |
| replicate/meta/llama-3-8b                                             | $0.05                             | $0.25                                 | 8,086               |            8086     |
| replicate/meta/llama-3-8b-instruct                                    | $0.05                             | $0.25                                 | 8,086               |            8086     |
| replicate/mistralai/mistral-7b-v0.1                                   | $0.05                             | $0.25                                 | 4,096               |            4096     |
| replicate/mistralai/mistral-7b-instruct-v0.2                          | $0.05                             | $0.25                                 | 4,096               |            4096     |
| replicate/mistralai/mixtral-8x7b-instruct-v0.1                        | $0.3                              | $1                                    | 4,096               |            4096     |
| openrouter/deepseek/deepseek-coder                                    | $0.14                             | $0.28                                 | 66,000              |            4096     |
| openrouter/microsoft/wizardlm-2-8x22b:nitro                           | $1                                | $1                                    | nan                 |             nan     |
| openrouter/google/gemini-pro-1.5                                      | $2.5                              | $7.5                                  | 1,000,000           |            8192     |
| openrouter/mistralai/mixtral-8x22b-instruct                           | $0.65                             | $0.65                                 | nan                 |             nan     |
| openrouter/cohere/command-r-plus                                      | $3                                | $15                                   | nan                 |             nan     |
| openrouter/databricks/dbrx-instruct                                   | $0.6                              | $0.6                                  | nan                 |             nan     |
| openrouter/anthropic/claude-3-haiku                                   | $0.25                             | $1.25                                 | nan                 |             nan     |
| openrouter/anthropic/claude-3-haiku-20240307                          | $0.25                             | $1.25                                 | 200,000             |            4096     |
| anthropic/claude-3-5-sonnet-20241022                                  | $3                                | $15                                   | 200,000             |            8192     |
| anthropic/claude-3-5-sonnet-latest                                    | $3                                | $15                                   | 200,000             |            8192     |
| openrouter/anthropic/claude-3.5-sonnet                                | $3                                | $15                                   | 200,000             |            8192     |
| openrouter/anthropic/claude-3.5-sonnet:beta                           | $3                                | $15                                   | 200,000             |            8192     |
| openrouter/anthropic/claude-3-sonnet                                  | $3                                | $15                                   | nan                 |             nan     |
| openrouter/mistralai/mistral-large                                    | $8                                | $24                                   | nan                 |             nan     |
| openrouter/cognitivecomputations/dolphin-mixtral-8x7b                 | $0.5                              | $0.5                                  | nan                 |             nan     |
| openrouter/google/gemini-pro-vision                                   | $0.12                             | $0.38                                 | nan                 |             nan     |
| openrouter/fireworks/firellava-13b                                    | $0.2                              | $0.2                                  | nan                 |             nan     |
| openrouter/meta-llama/llama-3-8b-instruct:free                        | $0                                | $0                                    | nan                 |             nan     |
| openrouter/meta-llama/llama-3-8b-instruct:extended                    | $0.22                             | $2.25                                 | nan                 |             nan     |
| openrouter/meta-llama/llama-3-70b-instruct:nitro                      | $0.9                              | $0.9                                  | nan                 |             nan     |
| openrouter/meta-llama/llama-3-70b-instruct                            | $0.59                             | $0.79                                 | nan                 |             nan     |
| openrouter/openai/o1-mini                                             | $3                                | $12                                   | 128,000             |           65536     |
| openrouter/openai/o1-mini-2024-09-12                                  | $3                                | $12                                   | 128,000             |           65536     |
| openrouter/openai/o1-preview                                          | $15                               | $60                                   | 128,000             |           32768     |
| openrouter/openai/o1-preview-2024-09-12                               | $15                               | $60                                   | 128,000             |           32768     |
| openrouter/openai/gpt-4o                                              | $2.5                              | $10                                   | 128,000             |            4096     |
| openrouter/openai/gpt-4o-2024-05-13                                   | $5                                | $15                                   | 128,000             |            4096     |
| openrouter/openai/gpt-4-vision-preview                                | $10                               | $30                                   | nan                 |             nan     |
| openrouter/openai/gpt-3.5-turbo                                       | $1.5                              | $2                                    | nan                 |             nan     |
| openrouter/openai/gpt-3.5-turbo-16k                                   | $3                                | $4                                    | nan                 |             nan     |
| openrouter/openai/gpt-4                                               | $30                               | $60                                   | nan                 |             nan     |
| openrouter/anthropic/claude-instant-v1                                | $1.63                             | $5.51                                 | nan                 |            8191     |
| openrouter/anthropic/claude-2                                         | $11.02                            | $32.68                                | nan                 |            8191     |
| openrouter/anthropic/claude-3-opus                                    | $15                               | $75                                   | 200,000             |            4096     |
| openrouter/google/palm-2-chat-bison                                   | $0.5                              | $0.5                                  | nan                 |             nan     |
| openrouter/google/palm-2-codechat-bison                               | $0.5                              | $0.5                                  | nan                 |             nan     |
| openrouter/meta-llama/llama-2-13b-chat                                | $0.2                              | $0.2                                  | nan                 |             nan     |
| openrouter/meta-llama/llama-2-70b-chat                                | $1.5                              | $1.5                                  | nan                 |             nan     |
| openrouter/meta-llama/codellama-34b-instruct                          | $0.5                              | $0.5                                  | nan                 |             nan     |
| openrouter/nousresearch/nous-hermes-llama2-13b                        | $0.2                              | $0.2                                  | nan                 |             nan     |
| openrouter/mancer/weaver                                              | $5.62                             | $5.62                                 | nan                 |             nan     |
| openrouter/gryphe/mythomax-l2-13b                                     | $1.88                             | $1.88                                 | nan                 |             nan     |
| openrouter/jondurbin/airoboros-l2-70b-2.1                             | $13.88                            | $13.88                                | nan                 |             nan     |
| openrouter/undi95/remm-slerp-l2-13b                                   | $1.88                             | $1.88                                 | nan                 |             nan     |
| openrouter/pygmalionai/mythalion-13b                                  | $1.88                             | $1.88                                 | nan                 |             nan     |
| openrouter/mistralai/mistral-7b-instruct                              | $0.13                             | $0.13                                 | nan                 |             nan     |
| openrouter/mistralai/mistral-7b-instruct:free                         | $0                                | $0                                    | nan                 |             nan     |
| j2-ultra                                                              | $15                               | $15                                   | 8,192               |            8192     |
| jamba-1.5-mini@001                                                    | $0.2                              | $0.4                                  | 256,000             |          256000     |
| jamba-1.5-large@001                                                   | $2                                | $8                                    | 256,000             |          256000     |
| jamba-1.5                                                             | $0.2                              | $0.4                                  | 256,000             |          256000     |
| jamba-1.5-mini                                                        | $0.2                              | $0.4                                  | 256,000             |          256000     |
| jamba-1.5-large                                                       | $2                                | $8                                    | 256,000             |          256000     |
| j2-mid                                                                | $10                               | $10                                   | 8,192               |            8192     |
| j2-light                                                              | $3                                | $3                                    | 8,192               |            8192     |
| dolphin                                                               | $0.5                              | $0.5                                  | 16,384              |           16384     |
| chatdolphin                                                           | $0.5                              | $0.5                                  | 16,384              |           16384     |
| luminous-base                                                         | $30                               | $33                                   | nan                 |             nan     |
| luminous-base-control                                                 | $37.5                             | $41.25                                | nan                 |             nan     |
| luminous-extended                                                     | $45                               | $49.5                                 | nan                 |             nan     |
| luminous-extended-control                                             | $56.25                            | $61.88                                | nan                 |             nan     |
| luminous-supreme                                                      | $175                              | $192.5                                | nan                 |             nan     |
| luminous-supreme-control                                              | $218.75                           | $240.62                               | nan                 |             nan     |
| ai21.j2-mid-v1                                                        | $12.5                             | $12.5                                 | 8,191               |            8191     |
| ai21.j2-ultra-v1                                                      | $18.8                             | $18.8                                 | 8,191               |            8191     |
| ai21.jamba-instruct-v1:0                                              | $0.5                              | $0.7                                  | 70,000              |            4096     |
| amazon.titan-text-lite-v1                                             | $0.3                              | $0.4                                  | 42,000              |            4000     |
| amazon.titan-text-express-v1                                          | $1.3                              | $1.7                                  | 42,000              |            8000     |
| amazon.titan-text-premier-v1:0                                        | $0.5                              | $1.5                                  | 42,000              |           32000     |
| amazon.titan-embed-text-v1                                            | $0.1                              | $0                                    | 8,192               |             nan     |
| amazon.titan-embed-text-v2:0                                          | $0.2                              | $0                                    | 8,192               |             nan     |
| mistral.mistral-7b-instruct-v0:2                                      | $0.15                             | $0.2                                  | 32,000              |            8191     |
| mistral.mixtral-8x7b-instruct-v0:1                                    | $0.45                             | $0.7                                  | 32,000              |            8191     |
| mistral.mistral-large-2402-v1:0                                       | $8                                | $24                                   | 32,000              |            8191     |
| mistral.mistral-large-2407-v1:0                                       | $3                                | $9                                    | 128,000             |            8191     |
| mistral.mistral-small-2402-v1:0                                       | $1                                | $3                                    | 32,000              |            8191     |
| bedrock/us-west-2/mistral.mixtral-8x7b-instruct-v0:1                  | $0.45                             | $0.7                                  | 32,000              |            8191     |
| bedrock/us-east-1/mistral.mixtral-8x7b-instruct-v0:1                  | $0.45                             | $0.7                                  | 32,000              |            8191     |
| bedrock/eu-west-3/mistral.mixtral-8x7b-instruct-v0:1                  | $0.59                             | $0.91                                 | 32,000              |            8191     |
| bedrock/us-west-2/mistral.mistral-7b-instruct-v0:2                    | $0.15                             | $0.2                                  | 32,000              |            8191     |
| bedrock/us-east-1/mistral.mistral-7b-instruct-v0:2                    | $0.15                             | $0.2                                  | 32,000              |            8191     |
| bedrock/eu-west-3/mistral.mistral-7b-instruct-v0:2                    | $0.2                              | $0.26                                 | 32,000              |            8191     |
| bedrock/us-east-1/mistral.mistral-large-2402-v1:0                     | $8                                | $24                                   | 32,000              |            8191     |
| bedrock/us-west-2/mistral.mistral-large-2402-v1:0                     | $8                                | $24                                   | 32,000              |            8191     |
| bedrock/eu-west-3/mistral.mistral-large-2402-v1:0                     | $10.4                             | $31.2                                 | 32,000              |            8191     |
| anthropic.claude-3-sonnet-20240229-v1:0                               | $3                                | $15                                   | 200,000             |            4096     |
| anthropic.claude-3-5-sonnet-20240620-v1:0                             | $3                                | $15                                   | 200,000             |            4096     |
| anthropic.claude-3-5-sonnet-20241022-v2:0                             | $3                                | $15                                   | 200,000             |            8192     |
| anthropic.claude-3-5-sonnet-latest-v2:0                               | $3                                | $15                                   | 200,000             |            4096     |
| anthropic.claude-3-haiku-20240307-v1:0                                | $0.25                             | $1.25                                 | 200,000             |            4096     |
| anthropic.claude-3-opus-20240229-v1:0                                 | $15                               | $75                                   | 200,000             |            4096     |
| us.anthropic.claude-3-sonnet-20240229-v1:0                            | $3                                | $15                                   | 200,000             |            4096     |
| us.anthropic.claude-3-5-sonnet-20240620-v1:0                          | $3                                | $15                                   | 200,000             |            4096     |
| us.anthropic.claude-3-5-sonnet-20241022-v2:0                          | $3                                | $15                                   | 200,000             |            8192     |
| us.anthropic.claude-3-haiku-20240307-v1:0                             | $0.25                             | $1.25                                 | 200,000             |            4096     |
| us.anthropic.claude-3-opus-20240229-v1:0                              | $15                               | $75                                   | 200,000             |            4096     |
| eu.anthropic.claude-3-sonnet-20240229-v1:0                            | $3                                | $15                                   | 200,000             |            4096     |
| eu.anthropic.claude-3-5-sonnet-20240620-v1:0                          | $3                                | $15                                   | 200,000             |            4096     |
| eu.anthropic.claude-3-5-sonnet-20241022-v2:0                          | $3                                | $15                                   | 200,000             |            8192     |
| eu.anthropic.claude-3-haiku-20240307-v1:0                             | $0.25                             | $1.25                                 | 200,000             |            4096     |
| eu.anthropic.claude-3-opus-20240229-v1:0                              | $15                               | $75                                   | 200,000             |            4096     |
| anthropic.claude-v1                                                   | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/us-east-1/anthropic.claude-v1                                 | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/us-west-2/anthropic.claude-v1                                 | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/ap-northeast-1/anthropic.claude-v1                            | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v1         | --                                | --                                    | 100,000             |            8191     |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v1         | --                                | --                                    | 100,000             |            8191     |
| bedrock/eu-central-1/anthropic.claude-v1                              | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v1           | --                                | --                                    | 100,000             |            8191     |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v1           | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v1              | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v1              | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v1              | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v1              | --                                | --                                    | 100,000             |            8191     |
| anthropic.claude-v2                                                   | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/us-east-1/anthropic.claude-v2                                 | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/us-west-2/anthropic.claude-v2                                 | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/ap-northeast-1/anthropic.claude-v2                            | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v2         | --                                | --                                    | 100,000             |            8191     |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v2         | --                                | --                                    | 100,000             |            8191     |
| bedrock/eu-central-1/anthropic.claude-v2                              | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v2           | --                                | --                                    | 100,000             |            8191     |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v2           | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v2              | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v2              | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v2              | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v2              | --                                | --                                    | 100,000             |            8191     |
| anthropic.claude-v2:1                                                 | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/us-east-1/anthropic.claude-v2:1                               | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/us-west-2/anthropic.claude-v2:1                               | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/ap-northeast-1/anthropic.claude-v2:1                          | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v2:1       | --                                | --                                    | 100,000             |            8191     |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v2:1       | --                                | --                                    | 100,000             |            8191     |
| bedrock/eu-central-1/anthropic.claude-v2:1                            | $8                                | $24                                   | 100,000             |            8191     |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v2:1         | --                                | --                                    | 100,000             |            8191     |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v2:1         | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v2:1            | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v2:1            | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v2:1            | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v2:1            | --                                | --                                    | 100,000             |            8191     |
| anthropic.claude-instant-v1                                           | $0.8                              | $2.4                                  | 100,000             |            8191     |
| bedrock/us-east-1/anthropic.claude-instant-v1                         | $0.8                              | $2.4                                  | 100,000             |            8191     |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-instant-v1      | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-instant-v1      | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-instant-v1      | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-instant-v1      | --                                | --                                    | 100,000             |            8191     |
| bedrock/us-west-2/anthropic.claude-instant-v1                         | $0.8                              | $2.4                                  | 100,000             |            8191     |
| bedrock/ap-northeast-1/anthropic.claude-instant-v1                    | $2.23                             | $7.55                                 | 100,000             |            8191     |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-instant-v1 | --                                | --                                    | 100,000             |            8191     |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-instant-v1 | --                                | --                                    | 100,000             |            8191     |
| bedrock/eu-central-1/anthropic.claude-instant-v1                      | $2.48                             | $8.38                                 | 100,000             |            8191     |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-instant-v1   | --                                | --                                    | 100,000             |            8191     |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-instant-v1   | --                                | --                                    | 100,000             |            8191     |
| cohere.command-text-v14                                               | $1.5                              | $2                                    | 4,096               |            4096     |
| bedrock/*/1-month-commitment/cohere.command-text-v14                  | --                                | --                                    | 4,096               |            4096     |
| bedrock/*/6-month-commitment/cohere.command-text-v14                  | --                                | --                                    | 4,096               |            4096     |
| cohere.command-light-text-v14                                         | $0.3                              | $0.6                                  | 4,096               |            4096     |
| bedrock/*/1-month-commitment/cohere.command-light-text-v14            | --                                | --                                    | 4,096               |            4096     |
| bedrock/*/6-month-commitment/cohere.command-light-text-v14            | --                                | --                                    | 4,096               |            4096     |
| cohere.command-r-plus-v1:0                                            | $3                                | $15                                   | 128,000             |            4096     |
| cohere.command-r-v1:0                                                 | $0.5                              | $1.5                                  | 128,000             |            4096     |
| cohere.embed-english-v3                                               | $0.1                              | $0                                    | 512                 |             nan     |
| cohere.embed-multilingual-v3                                          | $0.1                              | $0                                    | 512                 |             nan     |
| meta.llama2-13b-chat-v1                                               | $0.75                             | $1                                    | 4,096               |            4096     |
| meta.llama2-70b-chat-v1                                               | $1.95                             | $2.56                                 | 4,096               |            4096     |
| meta.llama3-8b-instruct-v1:0                                          | $0.3                              | $0.6                                  | 8,192               |            8192     |
| bedrock/us-east-1/meta.llama3-8b-instruct-v1:0                        | $0.3                              | $0.6                                  | 8,192               |            8192     |
| bedrock/us-west-1/meta.llama3-8b-instruct-v1:0                        | $0.3                              | $0.6                                  | 8,192               |            8192     |
| bedrock/ap-south-1/meta.llama3-8b-instruct-v1:0                       | $0.36                             | $0.72                                 | 8,192               |            8192     |
| bedrock/ca-central-1/meta.llama3-8b-instruct-v1:0                     | $0.35                             | $0.69                                 | 8,192               |            8192     |
| bedrock/eu-west-1/meta.llama3-8b-instruct-v1:0                        | $0.32                             | $0.65                                 | 8,192               |            8192     |
| bedrock/eu-west-2/meta.llama3-8b-instruct-v1:0                        | $0.39                             | $0.78                                 | 8,192               |            8192     |
| bedrock/sa-east-1/meta.llama3-8b-instruct-v1:0                        | $0.5                              | $1.01                                 | 8,192               |            8192     |
| meta.llama3-70b-instruct-v1:0                                         | $2.65                             | $3.5                                  | 8,192               |            8192     |
| bedrock/us-east-1/meta.llama3-70b-instruct-v1:0                       | $2.65                             | $3.5                                  | 8,192               |            8192     |
| bedrock/us-west-1/meta.llama3-70b-instruct-v1:0                       | $2.65                             | $3.5                                  | 8,192               |            8192     |
| bedrock/ap-south-1/meta.llama3-70b-instruct-v1:0                      | $3.18                             | $4.2                                  | 8,192               |            8192     |
| bedrock/ca-central-1/meta.llama3-70b-instruct-v1:0                    | $3.05                             | $4.03                                 | 8,192               |            8192     |
| bedrock/eu-west-1/meta.llama3-70b-instruct-v1:0                       | $2.86                             | $3.78                                 | 8,192               |            8192     |
| bedrock/eu-west-2/meta.llama3-70b-instruct-v1:0                       | $3.45                             | $4.55                                 | 8,192               |            8192     |
| bedrock/sa-east-1/meta.llama3-70b-instruct-v1:0                       | $4.45                             | $5.88                                 | 8,192               |            8192     |
| meta.llama3-1-8b-instruct-v1:0                                        | $0.22                             | $0.22                                 | 128,000             |            2048     |
| meta.llama3-1-70b-instruct-v1:0                                       | $0.99                             | $0.99                                 | 128,000             |            2048     |
| meta.llama3-1-405b-instruct-v1:0                                      | $5.32                             | $16                                   | 128,000             |            4096     |
| meta.llama3-2-1b-instruct-v1:0                                        | $0.1                              | $0.1                                  | 128,000             |            4096     |
| us.meta.llama3-2-1b-instruct-v1:0                                     | $0.1                              | $0.1                                  | 128,000             |            4096     |
| eu.meta.llama3-2-1b-instruct-v1:0                                     | $0.13                             | $0.13                                 | 128,000             |            4096     |
| meta.llama3-2-3b-instruct-v1:0                                        | $0.15                             | $0.15                                 | 128,000             |            4096     |
| us.meta.llama3-2-3b-instruct-v1:0                                     | $0.15                             | $0.15                                 | 128,000             |            4096     |
| eu.meta.llama3-2-3b-instruct-v1:0                                     | $0.19                             | $0.19                                 | 128,000             |            4096     |
| meta.llama3-2-11b-instruct-v1:0                                       | $0.35                             | $0.35                                 | 128,000             |            4096     |
| us.meta.llama3-2-11b-instruct-v1:0                                    | $0.35                             | $0.35                                 | 128,000             |            4096     |
| meta.llama3-2-90b-instruct-v1:0                                       | $2                                | $2                                    | 128,000             |            4096     |
| us.meta.llama3-2-90b-instruct-v1:0                                    | $2                                | $2                                    | 128,000             |            4096     |
| 512-x-512/50-steps/stability.stable-diffusion-xl-v0                   | --                                | --                                    | 77                  |             nan     |
| 512-x-512/max-steps/stability.stable-diffusion-xl-v0                  | --                                | --                                    | 77                  |             nan     |
| max-x-max/50-steps/stability.stable-diffusion-xl-v0                   | --                                | --                                    | 77                  |             nan     |
| max-x-max/max-steps/stability.stable-diffusion-xl-v0                  | --                                | --                                    | 77                  |             nan     |
| 1024-x-1024/50-steps/stability.stable-diffusion-xl-v1                 | --                                | --                                    | 77                  |             nan     |
| 1024-x-1024/max-steps/stability.stable-diffusion-xl-v1                | --                                | --                                    | 77                  |             nan     |
| sagemaker/meta-textgeneration-llama-2-7b                              | $0                                | $0                                    | 4,096               |            4096     |
| sagemaker/meta-textgeneration-llama-2-7b-f                            | $0                                | $0                                    | 4,096               |            4096     |
| sagemaker/meta-textgeneration-llama-2-13b                             | $0                                | $0                                    | 4,096               |            4096     |
| sagemaker/meta-textgeneration-llama-2-13b-f                           | $0                                | $0                                    | 4,096               |            4096     |
| sagemaker/meta-textgeneration-llama-2-70b                             | $0                                | $0                                    | 4,096               |            4096     |
| sagemaker/meta-textgeneration-llama-2-70b-b-f                         | $0                                | $0                                    | 4,096               |            4096     |
| together-ai-up-to-4b                                                  | $0.1                              | $0.1                                  | nan                 |             nan     |
| together-ai-4.1b-8b                                                   | $0.2                              | $0.2                                  | nan                 |             nan     |
| together-ai-8.1b-21b                                                  | $0.3                              | $0.3                                  | nan                 |             nan     |
| together-ai-21.1b-41b                                                 | $0.8                              | $0.8                                  | nan                 |             nan     |
| together-ai-41.1b-80b                                                 | $0.9                              | $0.9                                  | nan                 |             nan     |
| together-ai-81.1b-110b                                                | $1.8                              | $1.8                                  | nan                 |             nan     |
| together-ai-embedding-up-to-150m                                      | $0.01                             | $0                                    | nan                 |             nan     |
| together-ai-embedding-151m-to-350m                                    | $0.02                             | $0                                    | nan                 |             nan     |
| together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1                      | $0.6                              | $0.6                                  | nan                 |             nan     |
| together_ai/mistralai/Mistral-7B-Instruct-v0.1                        | --                                | --                                    | nan                 |             nan     |
| together_ai/togethercomputer/CodeLlama-34b-Instruct                   | --                                | --                                    | nan                 |             nan     |
| ollama/codegemma                                                      | $0                                | $0                                    | 8,192               |            8192     |
| ollama/codegeex4                                                      | $0                                | $0                                    | 32,768              |            8192     |
| ollama/deepseek-coder-v2-instruct                                     | $0                                | $0                                    | 32,768              |            8192     |
| ollama/deepseek-coder-v2-base                                         | $0                                | $0                                    | 8,192               |            8192     |
| ollama/deepseek-coder-v2-lite-instruct                                | $0                                | $0                                    | 32,768              |            8192     |
| ollama/deepseek-coder-v2-lite-base                                    | $0                                | $0                                    | 8,192               |            8192     |
| ollama/internlm2_5-20b-chat                                           | $0                                | $0                                    | 32,768              |            8192     |
| ollama/llama2                                                         | $0                                | $0                                    | 4,096               |            4096     |
| ollama/llama2:7b                                                      | $0                                | $0                                    | 4,096               |            4096     |
| ollama/llama2:13b                                                     | $0                                | $0                                    | 4,096               |            4096     |
| ollama/llama2:70b                                                     | $0                                | $0                                    | 4,096               |            4096     |
| ollama/llama2-uncensored                                              | $0                                | $0                                    | 4,096               |            4096     |
| ollama/llama3                                                         | $0                                | $0                                    | 8,192               |            8192     |
| ollama/llama3:8b                                                      | $0                                | $0                                    | 8,192               |            8192     |
| ollama/llama3:70b                                                     | $0                                | $0                                    | 8,192               |            8192     |
| ollama/llama3.1                                                       | $0                                | $0                                    | 8,192               |            8192     |
| ollama/mistral-large-instruct-2407                                    | $0                                | $0                                    | 65,536              |            8192     |
| ollama/mistral                                                        | $0                                | $0                                    | 8,192               |            8192     |
| ollama/mistral-7B-Instruct-v0.1                                       | $0                                | $0                                    | 8,192               |            8192     |
| ollama/mistral-7B-Instruct-v0.2                                       | $0                                | $0                                    | 32,768              |           32768     |
| ollama/mixtral-8x7B-Instruct-v0.1                                     | $0                                | $0                                    | 32,768              |           32768     |
| ollama/mixtral-8x22B-Instruct-v0.1                                    | $0                                | $0                                    | 65,536              |           65536     |
| ollama/codellama                                                      | $0                                | $0                                    | 4,096               |            4096     |
| ollama/orca-mini                                                      | $0                                | $0                                    | 4,096               |            4096     |
| ollama/vicuna                                                         | $0                                | $0                                    | 2,048               |            2048     |
| deepinfra/lizpreciatior/lzlv_70b_fp16_hf                              | $0.7                              | $0.9                                  | 4,096               |            4096     |
| deepinfra/Gryphe/MythoMax-L2-13b                                      | $0.22                             | $0.22                                 | 4,096               |            4096     |
| deepinfra/mistralai/Mistral-7B-Instruct-v0.1                          | $0.13                             | $0.13                                 | 32,768              |            8191     |
| deepinfra/meta-llama/Llama-2-70b-chat-hf                              | $0.7                              | $0.9                                  | 4,096               |            4096     |
| deepinfra/cognitivecomputations/dolphin-2.6-mixtral-8x7b              | $0.27                             | $0.27                                 | 32,768              |            8191     |
| deepinfra/codellama/CodeLlama-34b-Instruct-hf                         | $0.6                              | $0.6                                  | 4,096               |            4096     |
| deepinfra/deepinfra/mixtral                                           | $0.27                             | $0.27                                 | 32,000              |            4096     |
| deepinfra/Phind/Phind-CodeLlama-34B-v2                                | $0.6                              | $0.6                                  | 16,384              |            4096     |
| deepinfra/mistralai/Mixtral-8x7B-Instruct-v0.1                        | $0.27                             | $0.27                                 | 32,768              |            8191     |
| deepinfra/deepinfra/airoboros-70b                                     | $0.7                              | $0.9                                  | 4,096               |            4096     |
| deepinfra/01-ai/Yi-34B-Chat                                           | $0.6                              | $0.6                                  | 4,096               |            4096     |
| deepinfra/01-ai/Yi-6B-200K                                            | $0.13                             | $0.13                                 | 200,000             |            4096     |
| deepinfra/jondurbin/airoboros-l2-70b-gpt4-1.4.1                       | $0.7                              | $0.9                                  | 4,096               |            4096     |
| deepinfra/meta-llama/Llama-2-13b-chat-hf                              | $0.22                             | $0.22                                 | 4,096               |            4096     |
| deepinfra/amazon/MistralLite                                          | $0.2                              | $0.2                                  | 32,768              |            8191     |
| deepinfra/meta-llama/Llama-2-7b-chat-hf                               | $0.13                             | $0.13                                 | 4,096               |            4096     |
| deepinfra/meta-llama/Meta-Llama-3-8B-Instruct                         | $0.08                             | $0.08                                 | 8,191               |            4096     |
| deepinfra/meta-llama/Meta-Llama-3-70B-Instruct                        | $0.59                             | $0.79                                 | 8,191               |            4096     |
| deepinfra/01-ai/Yi-34B-200K                                           | $0.6                              | $0.6                                  | 200,000             |            4096     |
| deepinfra/openchat/openchat_3.5                                       | $0.13                             | $0.13                                 | 4,096               |            4096     |
| perplexity/codellama-34b-instruct                                     | $0.35                             | $1.4                                  | 16,384              |           16384     |
| perplexity/codellama-70b-instruct                                     | $0.7                              | $2.8                                  | 16,384              |           16384     |
| perplexity/llama-3.1-70b-instruct                                     | $1                                | $1                                    | 131,072             |          131072     |
| perplexity/llama-3.1-8b-instruct                                      | $0.2                              | $0.2                                  | 131,072             |          131072     |
| perplexity/llama-3.1-sonar-huge-128k-online                           | $5                                | $5                                    | 127,072             |          127072     |
| perplexity/llama-3.1-sonar-large-128k-online                          | $1                                | $1                                    | 127,072             |          127072     |
| perplexity/llama-3.1-sonar-large-128k-chat                            | $1                                | $1                                    | 131,072             |          131072     |
| perplexity/llama-3.1-sonar-small-128k-chat                            | $0.2                              | $0.2                                  | 131,072             |          131072     |
| perplexity/llama-3.1-sonar-small-128k-online                          | $0.2                              | $0.2                                  | 127,072             |          127072     |
| perplexity/pplx-7b-chat                                               | $0.07                             | $0.28                                 | 8,192               |            8192     |
| perplexity/pplx-70b-chat                                              | $0.7                              | $2.8                                  | 4,096               |            4096     |
| perplexity/pplx-7b-online                                             | $0                                | $0.28                                 | 4,096               |            4096     |
| perplexity/pplx-70b-online                                            | $0                                | $2.8                                  | 4,096               |            4096     |
| perplexity/llama-2-70b-chat                                           | $0.7                              | $2.8                                  | 4,096               |            4096     |
| perplexity/mistral-7b-instruct                                        | $0.07                             | $0.28                                 | 4,096               |            4096     |
| perplexity/mixtral-8x7b-instruct                                      | $0.07                             | $0.28                                 | 4,096               |            4096     |
| perplexity/sonar-small-chat                                           | $0.07                             | $0.28                                 | 16,384              |           16384     |
| perplexity/sonar-small-online                                         | $0                                | $0.28                                 | 12,000              |           12000     |
| perplexity/sonar-medium-chat                                          | $0.6                              | $1.8                                  | 16,384              |           16384     |
| perplexity/sonar-medium-online                                        | $0                                | $1.8                                  | 12,000              |           12000     |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-1b-instruct         | $0.1                              | $0.1                                  | 16,384              |           16384     |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-3b-instruct         | $0.1                              | $0.1                                  | 16,384              |           16384     |
| fireworks_ai/accounts/fireworks/models/llama-v3p2-11b-vision-instruct | $0.2                              | $0.2                                  | 16,384              |           16384     |
| accounts/fireworks/models/llama-v3p2-90b-vision-instruct              | $0.9                              | $0.9                                  | 16,384              |           16384     |
| fireworks_ai/accounts/fireworks/models/firefunction-v2                | $0.9                              | $0.9                                  | 8,192               |            8192     |
| fireworks_ai/accounts/fireworks/models/mixtral-8x22b-instruct-hf      | $1.2                              | $1.2                                  | 65,536              |           65536     |
| fireworks_ai/accounts/fireworks/models/qwen2-72b-instruct             | $0.9                              | $0.9                                  | 32,768              |           32768     |
| fireworks_ai/accounts/fireworks/models/yi-large                       | $3                                | $3                                    | 32,768              |           32768     |
| fireworks_ai/accounts/fireworks/models/deepseek-coder-v2-instruct     | $1.2                              | $1.2                                  | 65,536              |           65536     |
| fireworks_ai/nomic-ai/nomic-embed-text-v1.5                           | $0.01                             | $0                                    | 8,192               |             nan     |
| fireworks_ai/nomic-ai/nomic-embed-text-v1                             | $0.01                             | $0                                    | 8,192               |             nan     |
| fireworks_ai/WhereIsAI/UAE-Large-V1                                   | $0.02                             | $0                                    | 512                 |             nan     |
| fireworks_ai/thenlper/gte-large                                       | $0.02                             | $0                                    | 512                 |             nan     |
| fireworks_ai/thenlper/gte-base                                        | $0.01                             | $0                                    | 512                 |             nan     |
| fireworks-ai-up-to-16b                                                | $0.2                              | $0.2                                  | nan                 |             nan     |
| fireworks-ai-16.1b-to-80b                                             | $0.9                              | $0.9                                  | nan                 |             nan     |
| fireworks-ai-moe-up-to-56b                                            | $0.5                              | $0.5                                  | nan                 |             nan     |
| fireworks-ai-56b-to-176b                                              | $1.2                              | $1.2                                  | nan                 |             nan     |
| fireworks-ai-default                                                  | $0                                | $0                                    | nan                 |             nan     |
| fireworks-ai-embedding-up-to-150m                                     | $0.01                             | $0                                    | nan                 |             nan     |
| fireworks-ai-embedding-150m-to-350m                                   | $0.02                             | $0                                    | nan                 |             nan     |
| anyscale/mistralai/Mistral-7B-Instruct-v0.1                           | $0.15                             | $0.15                                 | 16,384              |           16384     |
| anyscale/mistralai/Mixtral-8x7B-Instruct-v0.1                         | $0.15                             | $0.15                                 | 16,384              |           16384     |
| anyscale/mistralai/Mixtral-8x22B-Instruct-v0.1                        | $0.9                              | $0.9                                  | 65,536              |           65536     |
| anyscale/HuggingFaceH4/zephyr-7b-beta                                 | $0.15                             | $0.15                                 | 16,384              |           16384     |
| anyscale/google/gemma-7b-it                                           | $0.15                             | $0.15                                 | 8,192               |            8192     |
| anyscale/meta-llama/Llama-2-7b-chat-hf                                | $0.15                             | $0.15                                 | 4,096               |            4096     |
| anyscale/meta-llama/Llama-2-13b-chat-hf                               | $0.25                             | $0.25                                 | 4,096               |            4096     |
| anyscale/meta-llama/Llama-2-70b-chat-hf                               | $1                                | $1                                    | 4,096               |            4096     |
| anyscale/codellama/CodeLlama-34b-Instruct-hf                          | $1                                | $1                                    | 4,096               |            4096     |
| anyscale/codellama/CodeLlama-70b-Instruct-hf                          | $1                                | $1                                    | 4,096               |            4096     |
| anyscale/meta-llama/Meta-Llama-3-8B-Instruct                          | $0.15                             | $0.15                                 | 8,192               |            8192     |
| anyscale/meta-llama/Meta-Llama-3-70B-Instruct                         | $1                                | $1                                    | 8,192               |            8192     |
| cloudflare/@cf/meta/llama-2-7b-chat-fp16                              | $1.92                             | $1.92                                 | 3,072               |            3072     |
| cloudflare/@cf/meta/llama-2-7b-chat-int8                              | $1.92                             | $1.92                                 | 2,048               |            2048     |
| cloudflare/@cf/mistral/mistral-7b-instruct-v0.1                       | $1.92                             | $1.92                                 | 8,192               |            8192     |
| cloudflare/@hf/thebloke/codellama-7b-instruct-awq                     | $1.92                             | $1.92                                 | 4,096               |            4096     |
| voyage/voyage-01                                                      | $0.1                              | $0                                    | 4,096               |             nan     |
| voyage/voyage-lite-01                                                 | $0.1                              | $0                                    | 4,096               |             nan     |
| voyage/voyage-large-2                                                 | $0.12                             | $0                                    | 16,000              |             nan     |
| voyage/voyage-law-2                                                   | $0.12                             | $0                                    | 16,000              |             nan     |
| voyage/voyage-code-2                                                  | $0.12                             | $0                                    | 16,000              |             nan     |
| voyage/voyage-2                                                       | $0.1                              | $0                                    | 4,000               |             nan     |
| voyage/voyage-lite-02-instruct                                        | $0.1                              | $0                                    | 4,000               |             nan     |
| voyage/voyage-finance-2                                               | $0.12                             | $0                                    | 32,000              |             nan     |
| databricks/databricks-meta-llama-3-1-405b-instruct                    | $5                                | $15                                   | 128,000             |          128000     |
| databricks/databricks-meta-llama-3-1-70b-instruct                     | $1                                | $3                                    | 128,000             |          128000     |
| databricks/databricks-dbrx-instruct                                   | $0.75                             | $2.25                                 | 32,768              |           32768     |
| databricks/databricks-meta-llama-3-70b-instruct                       | $1                                | $3                                    | 128,000             |          128000     |
| databricks/databricks-llama-2-70b-chat                                | $0.5                              | $1.5                                  | 4,096               |            4096     |
| databricks/databricks-mixtral-8x7b-instruct                           | $0.5                              | $1                                    | 4,096               |            4096     |
| databricks/databricks-mpt-30b-instruct                                | $1                                | $1                                    | 8,192               |            8192     |
| databricks/databricks-mpt-7b-instruct                                 | $0.5                              | $0                                    | 8,192               |            8192     |
| databricks/databricks-bge-large-en                                    | $0.1                              | $0                                    | 512                 |             nan     |
| databricks/databricks-gte-large-en                                    | $0.13                             | $0                                    | 8,192               |             nan     |
| azure/gpt-4o-mini-2024-07-18                                          | $0.16                             | $0.66                                 | 128,000             |           16384     |
| amazon.titan-embed-image-v1                                           | $0.8                              | $0                                    | 128                 |             nan     |
| azure_ai/mistral-large-2407                                           | $2                                | $6                                    | 128,000             |            4096     |
| azure_ai/ministral-3b                                                 | $0.04                             | $0.04                                 | 128,000             |            4096     |
| azure_ai/Llama-3.2-11B-Vision-Instruct                                | $0.37                             | $0.37                                 | 128,000             |            2048     |
| azure_ai/Llama-3.2-90B-Vision-Instruct                                | $2.04                             | $2.04                                 | 128,000             |            2048     |
| azure_ai/Phi-3.5-mini-instruct                                        | $0.13                             | $0.52                                 | 128,000             |            4096     |
| azure_ai/Phi-3.5-vision-instruct                                      | $0.13                             | $0.52                                 | 128,000             |            4096     |
| azure_ai/Phi-3.5-MoE-instruct                                         | $0.16                             | $0.64                                 | 128,000             |            4096     |
| azure_ai/Phi-3-mini-4k-instruct                                       | $0.13                             | $0.52                                 | 4,096               |            4096     |
| azure_ai/Phi-3-mini-128k-instruct                                     | $0.13                             | $0.52                                 | 128,000             |            4096     |
| azure_ai/Phi-3-small-8k-instruct                                      | $0.15                             | $0.6                                  | 8,192               |            4096     |
| azure_ai/Phi-3-small-128k-instruct                                    | $0.15                             | $0.6                                  | 128,000             |            4096     |
| azure_ai/Phi-3-medium-4k-instruct                                     | $0.17                             | $0.68                                 | 4,096               |            4096     |
| azure_ai/Phi-3-medium-128k-instruct                                   | $0.17                             | $0.68                                 | 128,000             |            4096     |
| xai/grok-beta                                                         | $5                                | $15                                   | 131,072             |          131072     |
| claude-3-5-haiku-20241022                                             | $0.8                              | $4                                    | 200,000             |            8192     |
| vertex_ai/claude-3-5-haiku@20241022                                   | $1                                | $5                                    | 200,000             |            8192     |
| openrouter/anthropic/claude-3-5-haiku                                 | $1                                | $5                                    | nan                 |             nan     |
| openrouter/anthropic/claude-3-5-haiku-20241022                        | $1                                | $5                                    | 200,000             |            8192     |
| anthropic.claude-3-5-haiku-20241022-v1:0                              | $0.8                              | $4                                    | 200,000             |            8192     |
| us.anthropic.claude-3-5-haiku-20241022-v1:0                           | $0.8                              | $4                                    | 200,000             |            8192     |
| eu.anthropic.claude-3-5-haiku-20241022-v1:0                           | $0.25                             | $1.25                                 | 200,000             |            8192     |
| stability.sd3-large-v1:0                                              | --                                | --                                    | 77                  |             nan     |
| gpt-4o-2024-11-20                                                     | $2.5                              | $10                                   | 128,000             |           16384     |
| ft:gpt-4o-2024-11-20                                                  | $3.75                             | $15                                   | 128,000             |           16384     |
| azure/gpt-4o-2024-11-20                                               | $2.75                             | $11                                   | 128,000             |           16384     |
| azure/global-standard/gpt-4o-2024-11-20                               | $2.5                              | $10                                   | 128,000             |           16384     |
| groq/llama-3.2-1b-preview                                             | $0.04                             | $0.04                                 | 8,192               |            8192     |
| groq/llama-3.2-3b-preview                                             | $0.06                             | $0.06                                 | 8,192               |            8192     |
| groq/llama-3.2-11b-text-preview                                       | $0.18                             | $0.18                                 | 8,192               |            8192     |
| groq/llama-3.2-11b-vision-preview                                     | $0.18                             | $0.18                                 | 8,192               |            8192     |
| groq/llama-3.2-90b-text-preview                                       | $0.9                              | $0.9                                  | 8,192               |            8192     |
| groq/llama-3.2-90b-vision-preview                                     | $0.9                              | $0.9                                  | 8,192               |            8192     |
| vertex_ai/claude-3-sonnet                                             | $3                                | $15                                   | 200,000             |            4096     |
| vertex_ai/claude-3-5-sonnet                                           | $3                                | $15                                   | 200,000             |            8192     |
| vertex_ai/claude-3-5-sonnet-v2                                        | $3                                | $15                                   | 200,000             |            8192     |
| vertex_ai/claude-3-haiku                                              | $0.25                             | $1.25                                 | 200,000             |            4096     |
| vertex_ai/claude-3-5-haiku                                            | $1                                | $5                                    | 200,000             |            8192     |
| vertex_ai/claude-3-opus                                               | $15                               | $75                                   | 200,000             |            4096     |
| gemini/gemini-exp-1114                                                | $0                                | $0                                    | 1,048,576           |            8192     |
| openrouter/qwen/qwen-2.5-coder-32b-instruct                           | $0.18                             | $0.18                                 | 33,792              |           33792     |
| us.meta.llama3-1-8b-instruct-v1:0                                     | $0.22                             | $0.22                                 | 128,000             |            2048     |
| us.meta.llama3-1-70b-instruct-v1:0                                    | $0.99                             | $0.99                                 | 128,000             |            2048     |
| us.meta.llama3-1-405b-instruct-v1:0                                   | $5.32                             | $16                                   | 128,000             |            4096     |
| stability.stable-image-ultra-v1:0                                     | --                                | --                                    | 77                  |             nan     |
| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-32b-instruct     | $0.9                              | $0.9                                  | 4,096               |            4096     |
| omni-moderation-latest                                                | $0                                | $0                                    | 32,768              |               0     |
| omni-moderation-latest-intents                                        | $0                                | $0                                    | 32,768              |               0     |
| omni-moderation-2024-09-26                                            | $0                                | $0                                    | 32,768              |               0     |
| gpt-4o-audio-preview-2024-12-17                                       | $2.5                              | $10                                   | 128,000             |           16384     |
| gpt-4o-mini-audio-preview-2024-12-17                                  | $0.15                             | $0.6                                  | 128,000             |           16384     |
| o1                                                                    | $15                               | $60                                   | 200,000             |          100000     |
| o1-2024-12-17                                                         | $15                               | $60                                   | 200,000             |          100000     |
| gpt-4o-realtime-preview-2024-10-01                                    | $5                                | $20                                   | 128,000             |            4096     |
| gpt-4o-realtime-preview                                               | $5                                | $20                                   | 128,000             |            4096     |
| gpt-4o-realtime-preview-2024-12-17                                    | $5                                | $20                                   | 128,000             |            4096     |
| gpt-4o-mini-realtime-preview                                          | $0.6                              | $2.4                                  | 128,000             |            4096     |
| gpt-4o-mini-realtime-preview-2024-12-17                               | $0.6                              | $2.4                                  | 128,000             |            4096     |
| azure/o1                                                              | $15                               | $60                                   | 200,000             |          100000     |
| azure_ai/Llama-3.3-70B-Instruct                                       | $0.71                             | $0.71                                 | 128,000             |            2048     |
| mistral/mistral-large-2411                                            | $2                                | $6                                    | 128,000             |          128000     |
| mistral/pixtral-large-latest                                          | $2                                | $6                                    | 128,000             |          128000     |
| mistral/pixtral-large-2411                                            | $2                                | $6                                    | 128,000             |          128000     |
| deepseek/deepseek-chat                                                | $0.27                             | $1.1                                  | 65,536              |            8192     |
| deepseek/deepseek-coder                                               | $0.14                             | $0.28                                 | 128,000             |            4096     |
| groq/llama-3.3-70b-versatile                                          | $0.59                             | $0.79                                 | 128,000             |            8192     |
| groq/llama-3.3-70b-specdec                                            | $0.59                             | $0.99                                 | 8,192               |            8192     |
| friendliai/meta-llama-3.1-8b-instruct                                 | $0.1                              | $0.1                                  | 8,192               |            8192     |
| friendliai/meta-llama-3.1-70b-instruct                                | $0.6                              | $0.6                                  | 8,192               |            8192     |
| gemini-2.0-flash-exp                                                  | $0.15                             | $0.6                                  | 1,048,576           |            8192     |
| gemini/gemini-2.0-flash-exp                                           | $0                                | $0                                    | 1,048,576           |            8192     |
| vertex_ai/mistral-large@2411-001                                      | $2                                | $6                                    | 128,000             |            8191     |
| vertex_ai/mistral-large-2411                                          | $2                                | $6                                    | 128,000             |            8191     |
| text-embedding-005                                                    | $0.1                              | $0                                    | 2,048               |             nan     |
| gemini/gemini-1.5-flash-8b                                            | $0                                | $0                                    | 1,048,576           |            8192     |
| gemini/gemini-exp-1206                                                | $0                                | $0                                    | 2,097,152           |            8192     |
| command-r7b-12-2024                                                   | $0.15                             | $0.04                                 | 128,000             |            4096     |
| rerank-v3.5                                                           | $0                                | $0                                    | 4,096               |            4096     |
| openrouter/deepseek/deepseek-chat                                     | $0.14                             | $0.28                                 | 65,536              |            8192     |
| openrouter/openai/o1                                                  | $15                               | $60                                   | 200,000             |          100000     |
| amazon.nova-micro-v1:0                                                | $0.04                             | $0.14                                 | 300,000             |            4096     |
| amazon.nova-lite-v1:0                                                 | $0.06                             | $0.24                                 | 128,000             |            4096     |
| amazon.nova-pro-v1:0                                                  | $0.8                              | $3.2                                  | 300,000             |            4096     |
| meta.llama3-3-70b-instruct-v1:0                                       | $0.72                             | $0.72                                 | 128,000             |            4096     |
| together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo               | $0.18                             | $0.18                                 | nan                 |             nan     |
| together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo              | $0.88                             | $0.88                                 | nan                 |             nan     |
| together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo             | $3.5                              | $3.5                                  | nan                 |             nan     |
| deepinfra/meta-llama/Meta-Llama-3.1-405B-Instruct                     | $0.9                              | $0.9                                  | 32,768              |           32768     |
| fireworks_ai/accounts/fireworks/models/deepseek-v3                    | $0.9                              | $0.9                                  | 128,000             |            8192     |
| voyage/voyage-3-large                                                 | $0.18                             | $0                                    | 32,000              |             nan     |
| voyage/voyage-3                                                       | $0.06                             | $0                                    | 32,000              |             nan     |
| voyage/voyage-3-lite                                                  | $0.02                             | $0                                    | 32,000              |             nan     |
| voyage/voyage-code-3                                                  | $0.18                             | $0                                    | 32,000              |             nan     |
| voyage/voyage-multimodal-3                                            | $0.12                             | $0                                    | 32,000              |             nan     |
| voyage/rerank-2                                                       | $0.05                             | $0                                    | 16,000              |           16000     |
| voyage/rerank-2-lite                                                  | $0.02                             | $0                                    | 8,000               |            8000     |
| databricks/meta-llama-3.3-70b-instruct                                | $1                                | $3                                    | 128,000             |          128000     |
| sambanova/Meta-Llama-3.1-8B-Instruct                                  | $0.1                              | $0.2                                  | 16,000              |           16000     |
| sambanova/Meta-Llama-3.1-70B-Instruct                                 | $0.6                              | $1.2                                  | 128,000             |          128000     |
| sambanova/Meta-Llama-3.1-405B-Instruct                                | $5                                | $10                                   | 16,000              |           16000     |
| sambanova/Meta-Llama-3.2-1B-Instruct                                  | $0.4                              | $0.8                                  | 16,000              |           16000     |
| sambanova/Meta-Llama-3.2-3B-Instruct                                  | $0.8                              | $1.6                                  | 4,000               |            4000     |
| sambanova/Meta-Llama-3.3-70B-Instruct                                 | $0.6                              | $1.2                                  | 128,000             |          128000     |
| sambanova/Qwen2.5-Coder-32B-Instruct                                  | $1.5                              | $3                                    | 8,000               |            8000     |
| sambanova/Qwen2.5-72B-Instruct                                        | $2                                | $4                                    | 8,000               |            8000     |
| o3-mini                                                               | $1.1                              | $4.4                                  | 200,000             |          100000     |
| o3-mini-2025-01-31                                                    | $1.1                              | $4.4                                  | 200,000             |          100000     |
| azure/o3-mini-2025-01-31                                              | $1.1                              | $4.4                                  | 200,000             |          100000     |
| azure/o3-mini                                                         | $1.1                              | $4.4                                  | 200,000             |          100000     |
| azure/o1-2024-12-17                                                   | $15                               | $60                                   | 200,000             |          100000     |
| azure_ai/deepseek-r1                                                  | $1.35                             | $5.4                                  | 128,000             |            8192     |
| deepseek/deepseek-reasoner                                            | $0.55                             | $2.19                                 | 65,536              |            8192     |
| xai/grok-2-vision-1212                                                | $2                                | $10                                   | 32,768              |           32768     |
| xai/grok-2-vision-latest                                              | $2                                | $10                                   | 32,768              |           32768     |
| xai/grok-2-vision                                                     | $2                                | $10                                   | 32,768              |           32768     |
| xai/grok-vision-beta                                                  | $5                                | $15                                   | 8,192               |            8192     |
| xai/grok-2-1212                                                       | $2                                | $10                                   | 131,072             |          131072     |
| xai/grok-2                                                            | $2                                | $10                                   | 131,072             |          131072     |
| xai/grok-2-latest                                                     | $2                                | $10                                   | 131,072             |          131072     |
| groq/deepseek-r1-distill-llama-70b                                    | $0.75                             | $0.99                                 | 131,072             |          131072     |
| gemini/gemini-2.0-flash                                               | $0.1                              | $0.4                                  | 1,048,576           |            8192     |
| gemini-2.0-flash-001                                                  | $0.15                             | $0.6                                  | 1,048,576           |            8192     |
| gemini-2.0-flash-thinking-exp                                         | $0                                | $0                                    | 1,048,576           |            8192     |
| gemini-2.0-flash-thinking-exp-01-21                                   | $0                                | $0                                    | 1,048,576           |           65536     |
| gemini/gemini-2.0-flash-001                                           | $0.1                              | $0.4                                  | 1,048,576           |            8192     |
| gemini/gemini-2.0-flash-lite-preview-02-05                            | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini/gemini-2.0-flash-thinking-exp                                  | $0                                | $0                                    | 1,048,576           |           65536     |
| vertex_ai/codestral-2501                                              | $0.2                              | $0.6                                  | 128,000             |          128000     |
| openrouter/deepseek/deepseek-r1                                       | $0.55                             | $2.19                                 | 65,336              |            8192     |
| ai21.jamba-1-5-large-v1:0                                             | $2                                | $8                                    | 256,000             |          256000     |
| ai21.jamba-1-5-mini-v1:0                                              | $0.2                              | $0.4                                  | 256,000             |          256000     |
| us.amazon.nova-micro-v1:0                                             | $0.04                             | $0.14                                 | 300,000             |            4096     |
| us.amazon.nova-lite-v1:0                                              | $0.06                             | $0.24                                 | 128,000             |            4096     |
| us.amazon.nova-pro-v1:0                                               | $0.8                              | $3.2                                  | 300,000             |            4096     |
| stability.sd3-5-large-v1:0                                            | --                                | --                                    | 77                  |             nan     |
| stability.stable-image-core-v1:0                                      | --                                | --                                    | 77                  |             nan     |
| stability.stable-image-core-v1:1                                      | --                                | --                                    | 77                  |             nan     |
| stability.stable-image-ultra-v1:1                                     | --                                | --                                    | 77                  |             nan     |
| together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo                   | $0.88                             | $0.88                                 | nan                 |             nan     |
| together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo-Free              | $0                                | $0                                    | nan                 |             nan     |
| fireworks_ai/accounts/fireworks/models/llama-v3p1-8b-instruct         | $0.1                              | $0.1                                  | 16,384              |           16384     |
| assemblyai/nano                                                       | --                                | --                                    | nan                 |             nan     |
| assemblyai/best                                                       | --                                | --                                    | nan                 |             nan     |
| azure/gpt-3.5-turbo-0125                                              | $0.5                              | $1.5                                  | 16,384              |            4096     |
| azure/gpt-3.5-turbo                                                   | $0.5                              | $1.5                                  | 4,097               |            4096     |
| gemini-2.0-pro-exp-02-05                                              | $1.25                             | $10                                   | 2,097,152           |            8192     |
| us.meta.llama3-3-70b-instruct-v1:0                                    | $0.72                             | $0.72                                 | 128,000             |            4096     |
| perplexity/sonar                                                      | $1                                | $1                                    | 128,000             |             nan     |
| perplexity/sonar-pro                                                  | $3                                | $15                                   | 200,000             |            8000     |
| openrouter/google/gemini-2.0-flash-001                                | $0.1                              | $0.4                                  | 1,048,576           |            8192     |
| gpt-4.5-preview                                                       | $75                               | $150                                  | 128,000             |           16384     |
| gpt-4.5-preview-2025-02-27                                            | $75                               | $150                                  | 128,000             |           16384     |
| azure_ai/Phi-4                                                        | $0.12                             | $0.5                                  | 16,384              |           16384     |
| cerebras/llama3.3-70b                                                 | $0.85                             | $1.2                                  | 128,000             |          128000     |
| claude-3-5-haiku-latest                                               | $1                                | $5                                    | 200,000             |            8192     |
| claude-3-7-sonnet-latest                                              | $3                                | $15                                   | 200,000             |          128000     |
| claude-3-7-sonnet-20250219                                            | $3                                | $15                                   | 200,000             |          128000     |
| vertex_ai/claude-3-7-sonnet@20250219                                  | $3                                | $15                                   | 200,000             |            8192     |
| openrouter/anthropic/claude-3.7-sonnet                                | $3                                | $15                                   | 200,000             |            8192     |
| openrouter/anthropic/claude-3.7-sonnet:beta                           | $3                                | $15                                   | 200,000             |            8192     |
| amazon.rerank-v1:0                                                    | $0                                | $0                                    | 32,000              |           32000     |
| anthropic.claude-3-7-sonnet-20250219-v1:0                             | $3                                | $15                                   | 200,000             |            8192     |
| us.anthropic.claude-3-7-sonnet-20250219-v1:0                          | $3                                | $15                                   | 200,000             |            8192     |
| cohere.rerank-v3-5:0                                                  | $0                                | $0                                    | 32,000              |           32000     |
| jina-reranker-v2-base-multilingual                                    | $0.02                             | $0.02                                 | 1,024               |            1024     |
| bedrock/invoke/anthropic.claude-3-5-sonnet-20240620-v1:0              | $3                                | $15                                   | 200,000             |            4096     |
| azure/gpt-4o-mini-realtime-preview-2024-12-17                         | $0.6                              | $2.4                                  | 128,000             |            4096     |
| azure/eu/gpt-4o-mini-realtime-preview-2024-12-17                      | $0.66                             | $2.64                                 | 128,000             |            4096     |
| azure/us/gpt-4o-mini-realtime-preview-2024-12-17                      | $0.66                             | $2.64                                 | 128,000             |            4096     |
| azure/gpt-4o-realtime-preview-2024-10-01                              | $5                                | $20                                   | 128,000             |            4096     |
| azure/us/gpt-4o-realtime-preview-2024-10-01                           | $5.5                              | $22                                   | 128,000             |            4096     |
| azure/eu/gpt-4o-realtime-preview-2024-10-01                           | $5.5                              | $22                                   | 128,000             |            4096     |
| azure/us/o3-mini-2025-01-31                                           | $1.21                             | $4.84                                 | 200,000             |          100000     |
| azure/eu/o3-mini-2025-01-31                                           | $1.21                             | $4.84                                 | 200,000             |          100000     |
| azure/us/o1-mini-2024-09-12                                           | $1.21                             | $4.84                                 | 128,000             |           65536     |
| azure/eu/o1-mini-2024-09-12                                           | $1.21                             | $4.84                                 | 128,000             |           65536     |
| azure/us/o1-2024-12-17                                                | $16.5                             | $66                                   | 200,000             |          100000     |
| azure/eu/o1-2024-12-17                                                | $16.5                             | $66                                   | 200,000             |          100000     |
| azure/us/o1-preview-2024-09-12                                        | $16.5                             | $66                                   | 128,000             |           32768     |
| azure/eu/o1-preview-2024-09-12                                        | $16.5                             | $66                                   | 128,000             |           32768     |
| azure/us/gpt-4o-2024-11-20                                            | $2.75                             | $11                                   | 128,000             |           16384     |
| azure/eu/gpt-4o-2024-11-20                                            | $2.75                             | $11                                   | 128,000             |           16384     |
| azure/us/gpt-4o-2024-08-06                                            | $2.75                             | $11                                   | 128,000             |           16384     |
| azure/eu/gpt-4o-2024-08-06                                            | $2.75                             | $11                                   | 128,000             |           16384     |
| azure/us/gpt-4o-mini-2024-07-18                                       | $0.16                             | $0.66                                 | 128,000             |           16384     |
| azure/eu/gpt-4o-mini-2024-07-18                                       | $0.16                             | $0.66                                 | 128,000             |           16384     |
| azure_ai/deepseek-v3                                                  | $1.14                             | $4.56                                 | 128,000             |            8192     |
| azure_ai/mistral-nemo                                                 | $0.15                             | $0.15                                 | 131,072             |            4096     |
| azure_ai/Phi-4-mini-instruct                                          | $0.08                             | $0.3                                  | 131,072             |            4096     |
| azure_ai/Phi-4-multimodal-instruct                                    | $0.08                             | $0.32                                 | 131,072             |            4096     |
| gemini/gemini-2.0-pro-exp-02-05                                       | $0                                | $0                                    | 2,097,152           |            8192     |
| gemini/gemini-2.0-flash-thinking-exp-01-21                            | $0                                | $0                                    | 1,048,576           |           65536     |
| gemini/gemma-3-27b-it                                                 | $0                                | $0                                    | 131,072             |            8192     |
| gemini/learnlm-1.5-pro-experimental                                   | $0                                | $0                                    | 32,767              |            8192     |
| vertex_ai/imagen-3.0-generate-002                                     | --                                | --                                    | nan                 |             nan     |
| jamba-large-1.6                                                       | $2                                | $8                                    | 256,000             |          256000     |
| jamba-mini-1.6                                                        | $0.2                              | $0.4                                  | 256,000             |          256000     |
| eu.amazon.nova-micro-v1:0                                             | $0.05                             | $0.18                                 | 300,000             |            4096     |
| eu.amazon.nova-lite-v1:0                                              | $0.08                             | $0.31                                 | 128,000             |            4096     |
| 1024-x-1024/50-steps/bedrock/amazon.nova-canvas-v1:0                  | --                                | --                                    | 2,600               |             nan     |
| eu.amazon.nova-pro-v1:0                                               | $1.05                             | $4.2                                  | 300,000             |            4096     |
| us.deepseek.r1-v1:0                                                   | $1.35                             | $5.4                                  | 128,000             |            4096     |
| snowflake/deepseek-r1                                                 | --                                | --                                    | 32,768              |            8192     |
| snowflake/snowflake-arctic                                            | --                                | --                                    | 4,096               |            8192     |
| snowflake/claude-3-5-sonnet                                           | --                                | --                                    | 18,000              |            8192     |
| snowflake/mistral-large                                               | --                                | --                                    | 32,000              |            8192     |
| snowflake/mistral-large2                                              | --                                | --                                    | 128,000             |            8192     |
| snowflake/reka-flash                                                  | --                                | --                                    | 100,000             |            8192     |
| snowflake/reka-core                                                   | --                                | --                                    | 32,000              |            8192     |
| snowflake/jamba-instruct                                              | --                                | --                                    | 256,000             |            8192     |
| snowflake/jamba-1.5-mini                                              | --                                | --                                    | 256,000             |            8192     |
| snowflake/jamba-1.5-large                                             | --                                | --                                    | 256,000             |            8192     |
| snowflake/mixtral-8x7b                                                | --                                | --                                    | 32,000              |            8192     |
| snowflake/llama2-70b-chat                                             | --                                | --                                    | 4,096               |            8192     |
| snowflake/llama3-8b                                                   | --                                | --                                    | 8,000               |            8192     |
| snowflake/llama3-70b                                                  | --                                | --                                    | 8,000               |            8192     |
| snowflake/llama3.1-8b                                                 | --                                | --                                    | 128,000             |            8192     |
| snowflake/llama3.1-70b                                                | --                                | --                                    | 128,000             |            8192     |
| snowflake/llama3.3-70b                                                | --                                | --                                    | 128,000             |            8192     |
| snowflake/snowflake-llama-3.3-70b                                     | --                                | --                                    | 8,000               |            8192     |
| snowflake/llama3.1-405b                                               | --                                | --                                    | 128,000             |            8192     |
| snowflake/snowflake-llama-3.1-405b                                    | --                                | --                                    | 8,000               |            8192     |
| snowflake/llama3.2-1b                                                 | --                                | --                                    | 128,000             |            8192     |
| snowflake/llama3.2-3b                                                 | --                                | --                                    | 128,000             |            8192     |
| snowflake/mistral-7b                                                  | --                                | --                                    | 32,000              |            8192     |
| snowflake/gemma-7b                                                    | --                                | --                                    | 8,000               |            8192     |
| azure/global/gpt-4o-2024-11-20                                        | $2.5                              | $10                                   | 128,000             |           16384     |
| azure/global/gpt-4o-2024-08-06                                        | $2.5                              | $10                                   | 128,000             |           16384     |
| o1-pro                                                                | $150                              | $600                                  | 200,000             |          100000     |
| o1-pro-2025-03-19                                                     | $150                              | $600                                  | 200,000             |          100000     |
| gpt-4o-search-preview-2025-03-11                                      | $2.5                              | $10                                   | 128,000             |           16384     |
| gpt-4o-search-preview                                                 | $2.5                              | $10                                   | 128,000             |           16384     |
| gpt-4o-mini-search-preview-2025-03-11                                 | $0.15                             | $0.6                                  | 128,000             |           16384     |
| gpt-4o-mini-search-preview                                            | $0.15                             | $0.6                                  | 128,000             |           16384     |
| azure/gpt-4.5-preview                                                 | $75                               | $150                                  | 128,000             |           16384     |
| azure_ai/mistral-small-2503                                           | $1                                | $3                                    | 128,000             |          128000     |
| text-embedding-large-exp-03-07                                        | $0.1                              | $0                                    | 8,192               |             nan     |
| gpt-4.1                                                               | $2                                | $8                                    | 1,047,576           |           32768     |
| gpt-4.1-2025-04-14                                                    | $2                                | $8                                    | 1,047,576           |           32768     |
| gpt-4.1-mini                                                          | $0.4                              | $1.6                                  | 1,047,576           |           32768     |
| gpt-4.1-mini-2025-04-14                                               | $0.4                              | $1.6                                  | 1,047,576           |           32768     |
| gpt-4.1-nano                                                          | $0.1                              | $0.4                                  | 1,047,576           |           32768     |
| gpt-4.1-nano-2025-04-14                                               | $0.1                              | $0.4                                  | 1,047,576           |           32768     |
| watsonx/ibm/granite-3-8b-instruct                                     | $200                              | $200                                  | 8,192               |            1024     |
| computer-use-preview                                                  | $3                                | $12                                   | 8,192               |            1024     |
| o3                                                                    | $10                               | $40                                   | 200,000             |          100000     |
| o3-2025-04-16                                                         | $10                               | $40                                   | 200,000             |          100000     |
| o4-mini                                                               | $1.1                              | $4.4                                  | 200,000             |          100000     |
| o4-mini-2025-04-16                                                    | $1.1                              | $4.4                                  | 200,000             |          100000     |
| gpt-image-1                                                           | --                                | --                                    | nan                 |             nan     |
| low/1024-x-1024/gpt-image-1                                           | --                                | --                                    | nan                 |             nan     |
| medium/1024-x-1024/gpt-image-1                                        | --                                | --                                    | nan                 |             nan     |
| high/1024-x-1024/gpt-image-1                                          | --                                | --                                    | nan                 |             nan     |
| low/1024-x-1536/gpt-image-1                                           | --                                | --                                    | nan                 |             nan     |
| medium/1024-x-1536/gpt-image-1                                        | --                                | --                                    | nan                 |             nan     |
| high/1024-x-1536/gpt-image-1                                          | --                                | --                                    | nan                 |             nan     |
| low/1536-x-1024/gpt-image-1                                           | --                                | --                                    | nan                 |             nan     |
| medium/1536-x-1024/gpt-image-1                                        | --                                | --                                    | nan                 |             nan     |
| high/1536-x-1024/gpt-image-1                                          | --                                | --                                    | nan                 |             nan     |
| gpt-4o-transcribe                                                     | $2.5                              | $10                                   | 16,000              |            2000     |
| gpt-4o-mini-transcribe                                                | $1.25                             | $5                                    | 16,000              |            2000     |
| gpt-4o-mini-tts                                                       | $2.5                              | $10                                   | nan                 |             nan     |
| azure/computer-use-preview                                            | $3                                | $12                                   | 8,192               |            1024     |
| azure/gpt-4o-audio-preview-2024-12-17                                 | $2.5                              | $10                                   | 128,000             |           16384     |
| azure/gpt-4o-mini-audio-preview-2024-12-17                            | $2.5                              | $10                                   | 128,000             |           16384     |
| azure/gpt-4.1                                                         | $2                                | $8                                    | 1,047,576           |           32768     |
| azure/gpt-4.1-2025-04-14                                              | $2                                | $8                                    | 1,047,576           |           32768     |
| azure/gpt-4.1-mini                                                    | $0.4                              | $1.6                                  | 1,047,576           |           32768     |
| azure/gpt-4.1-mini-2025-04-14                                         | $0.4                              | $1.6                                  | 1,047,576           |           32768     |
| azure/gpt-4.1-nano                                                    | $0.1                              | $0.4                                  | 1,047,576           |           32768     |
| azure/gpt-4.1-nano-2025-04-14                                         | $0.1                              | $0.4                                  | 1,047,576           |           32768     |
| azure/o3                                                              | $10                               | $40                                   | 200,000             |          100000     |
| azure/o3-2025-04-16                                                   | $10                               | $40                                   | 200,000             |          100000     |
| azure/o4-mini                                                         | $1.1                              | $4.4                                  | 200,000             |          100000     |
| azure/gpt-4o-realtime-preview-2024-12-17                              | $5                                | $20                                   | 128,000             |            4096     |
| azure/us/gpt-4o-realtime-preview-2024-12-17                           | $5.5                              | $22                                   | 128,000             |            4096     |
| azure/eu/gpt-4o-realtime-preview-2024-12-17                           | $5.5                              | $22                                   | 128,000             |            4096     |
| azure/o4-mini-2025-04-16                                              | $1.1                              | $4.4                                  | 200,000             |          100000     |
| azure/gpt-image-1                                                     | --                                | --                                    | nan                 |             nan     |
| azure/low/1024-x-1024/gpt-image-1                                     | --                                | --                                    | nan                 |             nan     |
| azure/medium/1024-x-1024/gpt-image-1                                  | --                                | --                                    | nan                 |             nan     |
| azure/high/1024-x-1024/gpt-image-1                                    | --                                | --                                    | nan                 |             nan     |
| azure/low/1024-x-1536/gpt-image-1                                     | --                                | --                                    | nan                 |             nan     |
| azure/medium/1024-x-1536/gpt-image-1                                  | --                                | --                                    | nan                 |             nan     |
| azure/high/1024-x-1536/gpt-image-1                                    | --                                | --                                    | nan                 |             nan     |
| azure/low/1536-x-1024/gpt-image-1                                     | --                                | --                                    | nan                 |             nan     |
| azure/medium/1536-x-1024/gpt-image-1                                  | --                                | --                                    | nan                 |             nan     |
| azure/high/1536-x-1024/gpt-image-1                                    | --                                | --                                    | nan                 |             nan     |
| azure_ai/mistral-large-latest                                         | $2                                | $6                                    | 128,000             |            4096     |
| xai/grok-3-beta                                                       | $3                                | $15                                   | 131,072             |          131072     |
| xai/grok-3-fast-beta                                                  | $5                                | $25                                   | 131,072             |          131072     |
| xai/grok-3-fast-latest                                                | $5                                | $25                                   | 131,072             |          131072     |
| xai/grok-3-mini-beta                                                  | $0.3                              | $0.5                                  | 131,072             |          131072     |
| xai/grok-3-mini-fast-beta                                             | $0.6                              | $4                                    | 131,072             |          131072     |
| xai/grok-3-mini-fast-latest                                           | $0.6                              | $4                                    | 131,072             |          131072     |
| groq/whisper-large-v3                                                 | --                                | --                                    | nan                 |             nan     |
| groq/whisper-large-v3-turbo                                           | --                                | --                                    | nan                 |             nan     |
| groq/distil-whisper-large-v3-en                                       | --                                | --                                    | nan                 |             nan     |
| meta_llama/Llama-4-Scout-17B-16E-Instruct-FP8                         | --                                | --                                    | 10,000,000          |            4028     |
| meta_llama/Llama-4-Maverick-17B-128E-Instruct-FP8                     | --                                | --                                    | 1,000,000           |            4028     |
| meta_llama/Llama-3.3-70B-Instruct                                     | --                                | --                                    | 128,000             |            4028     |
| meta_llama/Llama-3.3-8B-Instruct                                      | --                                | --                                    | 128,000             |            4028     |
| gemini-2.5-pro-exp-03-25                                              | $1.25                             | $10                                   | 1,048,576           |           65535     |
| gemini/gemini-2.5-pro-exp-03-25                                       | $0                                | $0                                    | 1,048,576           |           65535     |
| gemini/gemini-2.5-flash-preview-04-17                                 | $0.15                             | $0.6                                  | 1,048,576           |           65535     |
| gemini-2.5-flash-preview-04-17                                        | $0.15                             | $0.6                                  | 1,048,576           |           65535     |
| gemini-2.0-flash                                                      | $0.1                              | $0.4                                  | 1,048,576           |            8192     |
| gemini-2.0-flash-lite                                                 | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini-2.0-flash-lite-001                                             | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini-2.5-pro-preview-05-06                                          | $1.25                             | $10                                   | 1,048,576           |           65535     |
| gemini-2.5-pro-preview-03-25                                          | $1.25                             | $10                                   | 1,048,576           |           65535     |
| gemini/gemini-2.0-flash-lite                                          | $0.08                             | $0.3                                  | 1,048,576           |            8192     |
| gemini/gemini-2.5-pro-preview-05-06                                   | $1.25                             | $10                                   | 1,048,576           |           65535     |
| gemini/gemini-2.5-pro-preview-03-25                                   | $1.25                             | $10                                   | 1,048,576           |           65535     |
| vertex_ai/meta/llama-4-scout-17b-16e-instruct-maas                    | $0.25                             | $0.7                                  | 10,000,000          |               1e+07 |
| vertex_ai/meta/llama-4-scout-17b-128e-instruct-maas                   | $0.25                             | $0.7                                  | 10,000,000          |               1e+07 |
| vertex_ai/meta/llama-4-maverick-17b-128e-instruct-maas                | $0.35                             | $1.15                                 | 1,000,000           |               1e+06 |
| vertex_ai/meta/llama-4-maverick-17b-16e-instruct-maas                 | $0.35                             | $1.15                                 | 1,000,000           |               1e+06 |
| vertex_ai/mistral-small-2503@001                                      | $1                                | $3                                    | 32,000              |            8191     |
| vertex_ai/mistral-small-2503                                          | $1                                | $3                                    | 128,000             |          128000     |
| multimodalembedding                                                   | $0.8                              | $0                                    | 2,048               |             nan     |
| multimodalembedding@001                                               | $0.8                              | $0                                    | 2,048               |             nan     |
| command-a-03-2025                                                     | $2.5                              | $10                                   | 256,000             |            8000     |
| mistralai/mistral-small-3.1-24b-instruct                              | $0.1                              | $0.3                                  | nan                 |             nan     |
| openrouter/openai/o3-mini                                             | $1.1                              | $4.4                                  | 128,000             |           65536     |
| openrouter/openai/o3-mini-high                                        | $1.1                              | $4.4                                  | 128,000             |           65536     |
| us.amazon.nova-premier-v1:0                                           | $2.5                              | $12.5                                 | 1,000,000           |            4096     |
| meta.llama4-maverick-17b-instruct-v1:0                                | $0.24                             | $0.97                                 | 128,000             |            4096     |
| us.meta.llama4-maverick-17b-instruct-v1:0                             | $0.24                             | $0.97                                 | 128,000             |            4096     |
| meta.llama4-scout-17b-instruct-v1:0                                   | $0.17                             | $0.66                                 | 128,000             |            4096     |
| us.meta.llama4-scout-17b-instruct-v1:0                                | $0.17                             | $0.66                                 | 128,000             |            4096     |
| together_ai/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8         | --                                | --                                    | nan                 |             nan     |
| together_ai/meta-llama/Llama-4-Scout-17B-16E-Instruct                 | --                                | --                                    | nan                 |             nan     |
| together_ai/meta-llama/Llama-3.2-3B-Instruct-Turbo                    | --                                | --                                    | nan                 |             nan     |
| together_ai/Qwen/Qwen2.5-7B-Instruct-Turbo                            | --                                | --                                    | nan                 |             nan     |
| together_ai/Qwen/Qwen2.5-72B-Instruct-Turbo                           | --                                | --                                    | nan                 |             nan     |
| together_ai/deepseek-ai/DeepSeek-V3                                   | --                                | --                                    | nan                 |             nan     |
| together_ai/mistralai/Mistral-Small-24B-Instruct-2501                 | --                                | --                                    | nan                 |             nan     |
| perplexity/sonar-deep-research                                        | $2                                | $8                                    | 128,000             |             nan     |
| fireworks_ai/accounts/fireworks/models/deepseek-r1                    | $3                                | $8                                    | 128,000             |           20480     |
| fireworks_ai/accounts/fireworks/models/deepseek-r1-basic              | $0.55                             | $2.19                                 | 128,000             |           20480     |
| fireworks_ai/accounts/fireworks/models/llama-v3p1-405b-instruct       | $3                                | $3                                    | 128,000             |           16384     |
| fireworks_ai/accounts/fireworks/models/llama4-maverick-instruct-basic | $0.22                             | $0.88                                 | 131,072             |          131072     |
| fireworks_ai/accounts/fireworks/models/llama4-scout-instruct-basic    | $0.15                             | $0.6                                  | 131,072             |          131072     |
| fireworks-ai-up-to-4b                                                 | $0.2                              | $0.2                                  | nan                 |             nan     |
| fireworks-ai-4.1b-to-16b                                              | $0.2                              | $0.2                                  | nan                 |             nan     |
| fireworks-ai-above-16b                                                | $0.9                              | $0.9                                  | nan                 |             nan     |
| databricks/databricks-claude-3-7-sonnet                               | $2.5                              | $178.57                               | 200,000             |          128000     |
| databricks/databricks-meta-llama-3-3-70b-instruct                     | $1                                | $3                                    | 128,000             |          128000     |
| azure_ai/deepseek-v3-0324                                             | $1.14                             | $4.56                                 | 128,000             |            8192     |
| azure_ai/Llama-4-Scout-17B-16E-Instruct                               | $0.2                              | $0.78                                 | 10,000,000          |           16384     |
| azure_ai/Llama-4-Maverick-17B-128E-Instruct-FP8                       | $1.41                             | $0.35                                 | 1,000,000           |           16384     |
| cerebras/llama-3.3-70b                                                | $0.85                             | $1.2                                  | 128,000             |          128000     |
| perplexity/sonar-reasoning                                            | $1                                | $5                                    | 128,000             |             nan     |
| perplexity/sonar-reasoning-pro                                        | $2                                | $8                                    | 128,000             |             nan     |
| nscale/meta-llama/Llama-4-Scout-17B-16E-Instruct                      | $0.09                             | $0.29                                 | nan                 |             nan     |
| nscale/Qwen/Qwen2.5-Coder-3B-Instruct                                 | $0.01                             | $0.03                                 | nan                 |             nan     |
| nscale/Qwen/Qwen2.5-Coder-7B-Instruct                                 | $0.01                             | $0.03                                 | nan                 |             nan     |
| nscale/Qwen/Qwen2.5-Coder-32B-Instruct                                | $0.06                             | $0.2                                  | nan                 |             nan     |
| nscale/Qwen/QwQ-32B                                                   | $0.18                             | $0.2                                  | nan                 |             nan     |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Llama-70B                      | $0.38                             | $0.38                                 | nan                 |             nan     |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Llama-8B                       | $0.02                             | $0.02                                 | nan                 |             nan     |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B                      | $0.09                             | $0.09                                 | nan                 |             nan     |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B                        | $0.2                              | $0.2                                  | nan                 |             nan     |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B                       | $0.07                             | $0.07                                 | nan                 |             nan     |
| nscale/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B                       | $0.15                             | $0.15                                 | nan                 |             nan     |
| nscale/mistralai/mixtral-8x22b-instruct-v0.1                          | $0.6                              | $0.6                                  | nan                 |             nan     |
| nscale/meta-llama/Llama-3.1-8B-Instruct                               | $0.03                             | $0.03                                 | nan                 |             nan     |
| nscale/meta-llama/Llama-3.3-70B-Instruct                              | $0.2                              | $0.2                                  | nan                 |             nan     |
| nscale/black-forest-labs/FLUX.1-schnell                               | --                                | --                                    | nan                 |             nan     |
| nscale/stabilityai/stable-diffusion-xl-base-1.0                       | --                                | --                                    | nan                 |             nan     |## Contributing

Contributions to TokenCost are welcome! Feel free to create an [issue](https://github.com/AgentOps-AI/tokencost/issues) for any bug reports, complaints, or feature suggestions.

## License

TokenCost is released under the MIT License.
