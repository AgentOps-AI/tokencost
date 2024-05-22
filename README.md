<p align="center">
  <img src="https://github.com/AgentOps-AI/tokencost/blob/c6c29613ec1131e72a27525de3aa5af8966fb6af/tokencost.png" height="300" alt="Tokencost" />
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


* Prices last updated Jan 30, 2024 from: https://openai.com/pricing and https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json

| Model Name                                                                                  | Prompt Cost (USD)   | Completion Cost (USD)   | Max Prompt Tokens   |   Max Output Tokens |
|:--------------------------------------------------------------------------------------------|:--------------------|:------------------------|:--------------------|--------------------:|
| gpt-4                                                                                       | $0.00003000         | $0.00006000             | 8,192               |                4096 |
| gpt-4o                                                                                      | $0.00000500         | $0.00001500             | 128,000             |                4096 |
| gpt-4o-2024-05-13                                                                           | $0.00000500         | $0.00001500             | 128,000             |                4096 |
| gpt-4-turbo-preview                                                                         | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| gpt-4-0314                                                                                  | $0.00003000         | $0.00006000             | 8,192               |                4096 |
| gpt-4-0613                                                                                  | $0.00003000         | $0.00006000             | 8,192               |                4096 |
| gpt-4-32k                                                                                   | $0.00006000         | $0.00012000             | 32,768              |                4096 |
| gpt-4-32k-0314                                                                              | $0.00006000         | $0.00012000             | 32,768              |                4096 |
| gpt-4-32k-0613                                                                              | $0.00006000         | $0.00012000             | 32,768              |                4096 |
| gpt-4-turbo                                                                                 | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| gpt-4-turbo-2024-04-09                                                                      | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| gpt-4-1106-preview                                                                          | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| gpt-4-0125-preview                                                                          | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| gpt-4-vision-preview                                                                        | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| gpt-4-1106-vision-preview                                                                   | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| gpt-3.5-turbo                                                                               | $0.00000150         | $0.00000200             | 16,385              |                4096 |
| gpt-3.5-turbo-0301                                                                          | $0.00000150         | $0.00000200             | 4,097               |                4096 |
| gpt-3.5-turbo-0613                                                                          | $0.00000150         | $0.00000200             | 4,097               |                4096 |
| gpt-3.5-turbo-1106                                                                          | $0.00000100         | $0.00000200             | 16,385              |                4096 |
| gpt-3.5-turbo-0125                                                                          | $0.00000050         | $0.00000150             | 16,385              |                4096 |
| gpt-3.5-turbo-16k                                                                           | $0.00000300         | $0.00000400             | 16,385              |                4096 |
| gpt-3.5-turbo-16k-0613                                                                      | $0.00000300         | $0.00000400             | 16,385              |                4096 |
| ft:gpt-3.5-turbo                                                                            | $0.00000300         | $0.00000600             | 4,097               |                4096 |
| text-embedding-3-large                                                                      | $0.00000013         | $0.00000000             | 8,191               |                 nan |
| text-embedding-3-small                                                                      | $0.00000002         | $0.00000000             | 8,191               |                 nan |
| text-embedding-ada-002                                                                      | $0.00000010         | $0.00000000             | 8,191               |                 nan |
| text-embedding-ada-002-v2                                                                   | $0.00000010         | $0.00000000             | 8,191               |                 nan |
| text-moderation-stable                                                                      | $0.00000000         | $0.00000000             | 32,768              |                   0 |
| text-moderation-007                                                                         | $0.00000000         | $0.00000000             | 32,768              |                   0 |
| text-moderation-latest                                                                      | $0.00000000         | $0.00000000             | 32,768              |                   0 |
| 256-x-256/dall-e-2                                                                          | --                  | --                      | nan                 |                 nan |
| 512-x-512/dall-e-2                                                                          | --                  | --                      | nan                 |                 nan |
| 1024-x-1024/dall-e-2                                                                        | --                  | --                      | nan                 |                 nan |
| hd/1024-x-1792/dall-e-3                                                                     | --                  | --                      | nan                 |                 nan |
| hd/1792-x-1024/dall-e-3                                                                     | --                  | --                      | nan                 |                 nan |
| hd/1024-x-1024/dall-e-3                                                                     | --                  | --                      | nan                 |                 nan |
| standard/1024-x-1792/dall-e-3                                                               | --                  | --                      | nan                 |                 nan |
| standard/1792-x-1024/dall-e-3                                                               | --                  | --                      | nan                 |                 nan |
| standard/1024-x-1024/dall-e-3                                                               | --                  | --                      | nan                 |                 nan |
| whisper-1                                                                                   | --                  | --                      | nan                 |                 nan |
| azure/whisper-1                                                                             | --                  | --                      | nan                 |                 nan |
| azure/gpt-4-turbo-2024-04-09                                                                | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| azure/gpt-4-0125-preview                                                                    | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| azure/gpt-4-1106-preview                                                                    | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| azure/gpt-4-0613                                                                            | $0.00003000         | $0.00006000             | 8,192               |                4096 |
| azure/gpt-4-32k-0613                                                                        | $0.00006000         | $0.00012000             | 32,768              |                4096 |
| azure/gpt-4-32k                                                                             | $0.00006000         | $0.00012000             | 32,768              |                4096 |
| azure/gpt-4                                                                                 | $0.00003000         | $0.00006000             | 8,192               |                4096 |
| azure/gpt-4-turbo                                                                           | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| azure/gpt-4-turbo-vision-preview                                                            | $0.00001000         | $0.00003000             | 128,000             |                4096 |
| azure/gpt-35-turbo-16k-0613                                                                 | $0.00000300         | $0.00000400             | 16,385              |                4096 |
| azure/gpt-35-turbo-1106                                                                     | $0.00000150         | $0.00000200             | 16,384              |                4096 |
| azure/gpt-35-turbo-0125                                                                     | $0.00000050         | $0.00000150             | 16,384              |                4096 |
| azure/gpt-35-turbo-16k                                                                      | $0.00000300         | $0.00000400             | 16,385              |                4096 |
| azure/gpt-35-turbo                                                                          | $0.00000150         | $0.00000200             | 4,097               |                4096 |
| azure/gpt-3.5-turbo-instruct-0914                                                           | $0.00000150         | $0.00000200             | 4,097               |                 nan |
| azure/gpt-35-turbo-instruct                                                                 | $0.00000150         | $0.00000200             | 4,097               |                 nan |
| azure/mistral-large-latest                                                                  | $0.00000800         | $0.00002400             | 32,000              |                 nan |
| azure/mistral-large-2402                                                                    | $0.00000800         | $0.00002400             | 32,000              |                 nan |
| azure/command-r-plus                                                                        | $0.00000300         | $0.00001500             | 128,000             |                4096 |
| azure/ada                                                                                   | $0.00000010         | $0.00000000             | 8,191               |                 nan |
| azure/text-embedding-ada-002                                                                | $0.00000010         | $0.00000000             | 8,191               |                 nan |
| azure/text-embedding-3-large                                                                | $0.00000013         | $0.00000000             | 8,191               |                 nan |
| azure/text-embedding-3-small                                                                | $0.00000002         | $0.00000000             | 8,191               |                 nan |
| azure/standard/1024-x-1024/dall-e-3                                                         | --                  | $0.00000000             | nan                 |                 nan |
| azure/hd/1024-x-1024/dall-e-3                                                               | --                  | $0.00000000             | nan                 |                 nan |
| azure/standard/1024-x-1792/dall-e-3                                                         | --                  | $0.00000000             | nan                 |                 nan |
| azure/standard/1792-x-1024/dall-e-3                                                         | --                  | $0.00000000             | nan                 |                 nan |
| azure/hd/1024-x-1792/dall-e-3                                                               | --                  | $0.00000000             | nan                 |                 nan |
| azure/hd/1792-x-1024/dall-e-3                                                               | --                  | $0.00000000             | nan                 |                 nan |
| azure/standard/1024-x-1024/dall-e-2                                                         | --                  | $0.00000000             | nan                 |                 nan |
| babbage-002                                                                                 | $0.00000040         | $0.00000040             | 16,384              |                4096 |
| davinci-002                                                                                 | $0.00000200         | $0.00000200             | 16,384              |                4096 |
| gpt-3.5-turbo-instruct                                                                      | $0.00000150         | $0.00000200             | 8,192               |                4096 |
| gpt-3.5-turbo-instruct-0914                                                                 | $0.00000150         | $0.00000200             | 8,192               |                4097 |
| claude-instant-1                                                                            | $0.00000163         | $0.00000551             | 100,000             |                8191 |
| mistral/mistral-tiny                                                                        | $0.00000015         | $0.00000046             | 32,000              |                8191 |
| mistral/mistral-small                                                                       | $0.00000200         | $0.00000600             | 32,000              |                8191 |
| mistral/mistral-small-latest                                                                | $0.00000200         | $0.00000600             | 32,000              |                8191 |
| mistral/mistral-medium                                                                      | $0.00000270         | $0.00000810             | 32,000              |                8191 |
| mistral/mistral-medium-latest                                                               | $0.00000270         | $0.00000810             | 32,000              |                8191 |
| mistral/mistral-medium-2312                                                                 | $0.00000270         | $0.00000810             | 32,000              |                8191 |
| mistral/mistral-large-latest                                                                | $0.00000800         | $0.00002400             | 32,000              |                8191 |
| mistral/mistral-large-2402                                                                  | $0.00000800         | $0.00002400             | 32,000              |                8191 |
| mistral/open-mixtral-8x7b                                                                   | $0.00000200         | $0.00000600             | 32,000              |                8191 |
| mistral/mistral-embed                                                                       | $0.00000011         | --                      | 8,192               |                 nan |
| deepseek-chat                                                                               | $0.00000014         | $0.00000028             | 32,000              |                4096 |
| deepseek-coder                                                                              | $0.00000014         | $0.00000028             | 16,000              |                4096 |
| groq/llama2-70b-4096                                                                        | $0.00000070         | $0.00000080             | 4,096               |                4096 |
| groq/llama3-8b-8192                                                                         | $0.00000010         | $0.00000010             | 8,192               |                8192 |
| groq/llama3-70b-8192                                                                        | $0.00000064         | $0.00000080             | 8,192               |                8192 |
| groq/mixtral-8x7b-32768                                                                     | $0.00000027         | $0.00000027             | 32,768              |               32768 |
| groq/gemma-7b-it                                                                            | $0.00000010         | $0.00000010             | 8,192               |                8192 |
| claude-instant-1.2                                                                          | $0.00000016         | $0.00000055             | 100,000             |                8191 |
| claude-2                                                                                    | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| claude-2.1                                                                                  | $0.00000800         | $0.00002400             | 200,000             |                8191 |
| claude-3-haiku-20240307                                                                     | $0.00000025         | $0.00000125             | 200,000             |                4096 |
| claude-3-opus-20240229                                                                      | $0.00001500         | $0.00007500             | 200,000             |                4096 |
| claude-3-sonnet-20240229                                                                    | $0.00000300         | $0.00001500             | 200,000             |                4096 |
| text-bison                                                                                  | $0.00000012         | $0.00000012             | 8,192               |                1024 |
| text-bison@001                                                                              | $0.00000012         | $0.00000012             | 8,192               |                1024 |
| text-unicorn                                                                                | $0.00001000         | $0.00002800             | 8,192               |                1024 |
| text-unicorn@001                                                                            | $0.00001000         | $0.00002800             | 8,192               |                1024 |
| chat-bison                                                                                  | $0.00000012         | $0.00000012             | 8,192               |                4096 |
| chat-bison@001                                                                              | $0.00000012         | $0.00000012             | 8,192               |                4096 |
| chat-bison@002                                                                              | $0.00000012         | $0.00000012             | 8,192               |                4096 |
| chat-bison-32k                                                                              | $0.00000012         | $0.00000012             | 32,000              |                8192 |
| code-bison                                                                                  | $0.00000012         | $0.00000012             | 6,144               |                1024 |
| code-bison@001                                                                              | $0.00000012         | $0.00000012             | 6,144               |                1024 |
| code-gecko@001                                                                              | $0.00000012         | $0.00000012             | 2,048               |                  64 |
| code-gecko@002                                                                              | $0.00000012         | $0.00000012             | 2,048               |                  64 |
| code-gecko                                                                                  | $0.00000012         | $0.00000012             | 2,048               |                  64 |
| codechat-bison                                                                              | $0.00000012         | $0.00000012             | 6,144               |                1024 |
| codechat-bison@001                                                                          | $0.00000012         | $0.00000012             | 6,144               |                1024 |
| codechat-bison-32k                                                                          | $0.00000012         | $0.00000012             | 32,000              |                8192 |
| gemini-pro                                                                                  | $0.00000025         | $0.00000050             | 32,760              |                8192 |
| gemini-1.0-pro                                                                              | $0.00000025         | $0.00000050             | 32,760              |                8192 |
| gemini-1.0-pro-001                                                                          | $0.00000025         | $0.00000050             | 32,760              |                8192 |
| gemini-1.0-pro-002                                                                          | $0.00000025         | $0.00000050             | 32,760              |                8192 |
| gemini-1.5-pro                                                                              | $0.00000063         | $0.00000188             | 1,000,000           |                8192 |
| gemini-1.5-pro-preview-0215                                                                 | $0.00000063         | $0.00000188             | 1,000,000           |                8192 |
| gemini-1.5-pro-preview-0409                                                                 | $0.00000063         | $0.00000188             | 1,000,000           |                8192 |
| gemini-experimental                                                                         | $0.00000000         | $0.00000000             | 1,000,000           |                8192 |
| gemini-pro-vision                                                                           | $0.00000025         | $0.00000050             | 16,384              |                2048 |
| gemini-1.0-pro-vision                                                                       | $0.00000025         | $0.00000050             | 16,384              |                2048 |
| gemini-1.0-pro-vision-001                                                                   | $0.00000025         | $0.00000050             | 16,384              |                2048 |
| vertex_ai/claude-3-sonnet@20240229                                                          | $0.00000300         | $0.00001500             | 200,000             |                4096 |
| vertex_ai/claude-3-haiku@20240307                                                           | $0.00000025         | $0.00000125             | 200,000             |                4096 |
| vertex_ai/claude-3-opus@20240229                                                            | $0.00000150         | $0.00000750             | 200,000             |                4096 |
| textembedding-gecko                                                                         | $0.00000001         | $0.00000000             | 3,072               |                 nan |
| textembedding-gecko-multilingual                                                            | $0.00000001         | $0.00000000             | 3,072               |                 nan |
| textembedding-gecko-multilingual@001                                                        | $0.00000001         | $0.00000000             | 3,072               |                 nan |
| textembedding-gecko@001                                                                     | $0.00000001         | $0.00000000             | 3,072               |                 nan |
| textembedding-gecko@003                                                                     | $0.00000001         | $0.00000000             | 3,072               |                 nan |
| text-embedding-preview-0409                                                                 | $0.00000001         | $0.00000000             | 3,072               |                 nan |
| text-multilingual-embedding-preview-0409                                                    | $0.00000001         | $0.00000000             | 3,072               |                 nan |
| palm/chat-bison                                                                             | $0.00000012         | $0.00000012             | 8,192               |                4096 |
| palm/chat-bison-001                                                                         | $0.00000012         | $0.00000012             | 8,192               |                4096 |
| palm/text-bison                                                                             | $0.00000012         | $0.00000012             | 8,192               |                1024 |
| palm/text-bison-001                                                                         | $0.00000012         | $0.00000012             | 8,192               |                1024 |
| palm/text-bison-safety-off                                                                  | $0.00000012         | $0.00000012             | 8,192               |                1024 |
| palm/text-bison-safety-recitation-off                                                       | $0.00000012         | $0.00000012             | 8,192               |                1024 |
| gemini/gemini-pro                                                                           | $0.00000000         | $0.00000000             | 32,760              |                8192 |
| gemini/gemini-1.5-pro                                                                       | $0.00000000         | $0.00000000             | 1,000,000           |                8192 |
| gemini/gemini-1.5-pro-latest                                                                | $0.00000000         | $0.00000000             | 1,048,576           |                8192 |
| gemini/gemini-pro-vision                                                                    | $0.00000000         | $0.00000000             | 30,720              |                2048 |
| command-r                                                                                   | $0.00000050         | $0.00000150             | 128,000             |                4096 |
| command-light                                                                               | $0.00001500         | $0.00001500             | 4,096               |                4096 |
| command-r-plus                                                                              | $0.00000300         | $0.00001500             | 128,000             |                4096 |
| command-nightly                                                                             | $0.00001500         | $0.00001500             | 4,096               |                4096 |
| command                                                                                     | $0.00001500         | $0.00001500             | 4,096               |                4096 |
| command-medium-beta                                                                         | $0.00001500         | $0.00001500             | 4,096               |                4096 |
| command-xlarge-beta                                                                         | $0.00001500         | $0.00001500             | 4,096               |                4096 |
| replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1 | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| replicate/meta/llama-2-13b                                                                  | $0.00000010         | $0.00000050             | 4,096               |                4096 |
| replicate/meta/llama-2-13b-chat                                                             | $0.00000010         | $0.00000050             | 4,096               |                4096 |
| replicate/meta/llama-2-70b                                                                  | $0.00000065         | $0.00000275             | 4,096               |                4096 |
| replicate/meta/llama-2-70b-chat                                                             | $0.00000065         | $0.00000275             | 4,096               |                4096 |
| replicate/meta/llama-2-7b                                                                   | $0.00000005         | $0.00000025             | 4,096               |                4096 |
| replicate/meta/llama-2-7b-chat                                                              | $0.00000005         | $0.00000025             | 4,096               |                4096 |
| replicate/meta/llama-3-70b                                                                  | $0.00000065         | $0.00000275             | 4,096               |                4096 |
| replicate/meta/llama-3-70b-instruct                                                         | $0.00000065         | $0.00000275             | 4,096               |                4096 |
| replicate/meta/llama-3-8b                                                                   | $0.00000005         | $0.00000025             | 4,096               |                4096 |
| replicate/meta/llama-3-8b-instruct                                                          | $0.00000005         | $0.00000025             | 4,096               |                4096 |
| replicate/mistralai/mistral-7b-v0.1                                                         | $0.00000005         | $0.00000025             | 4,096               |                4096 |
| replicate/mistralai/mistral-7b-instruct-v0.2                                                | $0.00000005         | $0.00000025             | 4,096               |                4096 |
| replicate/mistralai/mixtral-8x7b-instruct-v0.1                                              | $0.00000030         | $0.00000100             | 4,096               |                4096 |
| openrouter/microsoft/wizardlm-2-8x22b:nitro                                                 | $0.00000100         | $0.00000100             | nan                 |                 nan |
| openrouter/google/gemini-pro-1.5                                                            | $0.00000250         | $0.00000750             | 1,000,000           |                8192 |
| openrouter/mistralai/mixtral-8x22b-instruct                                                 | $0.00000065         | $0.00000065             | nan                 |                 nan |
| openrouter/cohere/command-r-plus                                                            | $0.00000300         | $0.00001500             | nan                 |                 nan |
| openrouter/databricks/dbrx-instruct                                                         | $0.00000060         | $0.00000060             | nan                 |                 nan |
| openrouter/anthropic/claude-3-haiku                                                         | $0.00000025         | $0.00000125             | nan                 |                 nan |
| openrouter/anthropic/claude-3-sonnet                                                        | $0.00000300         | $0.00001500             | nan                 |                 nan |
| openrouter/mistralai/mistral-large                                                          | $0.00000800         | $0.00002400             | nan                 |                 nan |
| openrouter/cognitivecomputations/dolphin-mixtral-8x7b                                       | $0.00000050         | $0.00000050             | nan                 |                 nan |
| openrouter/google/gemini-pro-vision                                                         | $0.00000012         | $0.00000038             | nan                 |                 nan |
| openrouter/fireworks/firellava-13b                                                          | $0.00000020         | $0.00000020             | nan                 |                 nan |
| openrouter/meta-llama/llama-3-8b-instruct:free                                              | $0.00000000         | $0.00000000             | nan                 |                 nan |
| openrouter/meta-llama/llama-3-8b-instruct:extended                                          | $0.00000022         | $0.00000225             | nan                 |                 nan |
| openrouter/meta-llama/llama-3-70b-instruct:nitro                                            | $0.00000090         | $0.00000090             | nan                 |                 nan |
| openrouter/meta-llama/llama-3-70b-instruct                                                  | $0.00000059         | $0.00000079             | nan                 |                 nan |
| openrouter/openai/gpt-4-vision-preview                                                      | $0.00001000         | $0.00003000             | nan                 |                 nan |
| openrouter/openai/gpt-3.5-turbo                                                             | $0.00000150         | $0.00000200             | nan                 |                 nan |
| openrouter/openai/gpt-3.5-turbo-16k                                                         | $0.00000300         | $0.00000400             | nan                 |                 nan |
| openrouter/openai/gpt-4                                                                     | $0.00003000         | $0.00006000             | nan                 |                 nan |
| openrouter/anthropic/claude-instant-v1                                                      | $0.00000163         | $0.00000551             | nan                 |                8191 |
| openrouter/anthropic/claude-2                                                               | $0.00001102         | $0.00003268             | nan                 |                8191 |
| openrouter/anthropic/claude-3-opus                                                          | $0.00001500         | $0.00007500             | 200,000             |                4096 |
| openrouter/google/palm-2-chat-bison                                                         | $0.00000050         | $0.00000050             | nan                 |                 nan |
| openrouter/google/palm-2-codechat-bison                                                     | $0.00000050         | $0.00000050             | nan                 |                 nan |
| openrouter/meta-llama/llama-2-13b-chat                                                      | $0.00000020         | $0.00000020             | nan                 |                 nan |
| openrouter/meta-llama/llama-2-70b-chat                                                      | $0.00000150         | $0.00000150             | nan                 |                 nan |
| openrouter/meta-llama/codellama-34b-instruct                                                | $0.00000050         | $0.00000050             | nan                 |                 nan |
| openrouter/nousresearch/nous-hermes-llama2-13b                                              | $0.00000020         | $0.00000020             | nan                 |                 nan |
| openrouter/mancer/weaver                                                                    | $0.00000563         | $0.00000563             | nan                 |                 nan |
| openrouter/gryphe/mythomax-l2-13b                                                           | $0.00000188         | $0.00000188             | nan                 |                 nan |
| openrouter/jondurbin/airoboros-l2-70b-2.1                                                   | $0.00001388         | $0.00001388             | nan                 |                 nan |
| openrouter/undi95/remm-slerp-l2-13b                                                         | $0.00000188         | $0.00000188             | nan                 |                 nan |
| openrouter/pygmalionai/mythalion-13b                                                        | $0.00000188         | $0.00000188             | nan                 |                 nan |
| openrouter/mistralai/mistral-7b-instruct                                                    | $0.00000013         | $0.00000013             | nan                 |                 nan |
| openrouter/mistralai/mistral-7b-instruct:free                                               | $0.00000000         | $0.00000000             | nan                 |                 nan |
| j2-ultra                                                                                    | $0.00001500         | $0.00001500             | 8,192               |                8192 |
| j2-mid                                                                                      | $0.00001000         | $0.00001000             | 8,192               |                8192 |
| j2-light                                                                                    | $0.00000300         | $0.00000300             | 8,192               |                8192 |
| dolphin                                                                                     | $0.00000050         | $0.00000050             | 16,384              |               16384 |
| chatdolphin                                                                                 | $0.00000050         | $0.00000050             | 16,384              |               16384 |
| luminous-base                                                                               | $0.00003000         | $0.00003300             | nan                 |                 nan |
| luminous-base-control                                                                       | $0.00003750         | $0.00004125             | nan                 |                 nan |
| luminous-extended                                                                           | $0.00004500         | $0.00004950             | nan                 |                 nan |
| luminous-extended-control                                                                   | $0.00005625         | $0.00006187             | nan                 |                 nan |
| luminous-supreme                                                                            | $0.00017500         | $0.00019250             | nan                 |                 nan |
| luminous-supreme-control                                                                    | $0.00021875         | $0.00024063             | nan                 |                 nan |
| ai21.j2-mid-v1                                                                              | $0.00001250         | $0.00001250             | 8,191               |                8191 |
| ai21.j2-ultra-v1                                                                            | $0.00001880         | $0.00001880             | 8,191               |                8191 |
| amazon.titan-text-lite-v1                                                                   | $0.00000030         | $0.00000040             | 42,000              |                4000 |
| amazon.titan-text-express-v1                                                                | $0.00000130         | $0.00000170             | 42,000              |                8000 |
| amazon.titan-embed-text-v1                                                                  | $0.00000010         | $0.00000000             | 8,192               |                 nan |
| amazon.titan-embed-text-v2:0                                                                | $0.00000020         | $0.00000000             | 8,192               |                 nan |
| mistral.mistral-7b-instruct-v0:2                                                            | $0.00000015         | $0.00000020             | 32,000              |                8191 |
| mistral.mixtral-8x7b-instruct-v0:1                                                          | $0.00000045         | $0.00000070             | 32,000              |                8191 |
| mistral.mistral-large-2402-v1:0                                                             | $0.00000800         | $0.00002400             | 32,000              |                8191 |
| bedrock/us-west-2/mistral.mixtral-8x7b-instruct-v0:1                                        | $0.00000045         | $0.00000070             | 32,000              |                8191 |
| bedrock/us-east-1/mistral.mixtral-8x7b-instruct-v0:1                                        | $0.00000045         | $0.00000070             | 32,000              |                8191 |
| bedrock/eu-west-3/mistral.mixtral-8x7b-instruct-v0:1                                        | $0.00000059         | $0.00000091             | 32,000              |                8191 |
| bedrock/us-west-2/mistral.mistral-7b-instruct-v0:2                                          | $0.00000015         | $0.00000020             | 32,000              |                8191 |
| bedrock/us-east-1/mistral.mistral-7b-instruct-v0:2                                          | $0.00000015         | $0.00000020             | 32,000              |                8191 |
| bedrock/eu-west-3/mistral.mistral-7b-instruct-v0:2                                          | $0.00000020         | $0.00000026             | 32,000              |                8191 |
| bedrock/us-east-1/mistral.mistral-large-2402-v1:0                                           | $0.00000800         | $0.00002400             | 32,000              |                8191 |
| bedrock/us-west-2/mistral.mistral-large-2402-v1:0                                           | $0.00000800         | $0.00002400             | 32,000              |                8191 |
| bedrock/eu-west-3/mistral.mistral-large-2402-v1:0                                           | $0.00001040         | $0.00003120             | 32,000              |                8191 |
| anthropic.claude-3-sonnet-20240229-v1:0                                                     | $0.00000300         | $0.00001500             | 200,000             |                4096 |
| anthropic.claude-3-haiku-20240307-v1:0                                                      | $0.00000025         | $0.00000125             | 200,000             |                4096 |
| anthropic.claude-3-opus-20240229-v1:0                                                       | $0.00001500         | $0.00007500             | 200,000             |                4096 |
| anthropic.claude-v1                                                                         | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/us-east-1/anthropic.claude-v1                                                       | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/us-west-2/anthropic.claude-v1                                                       | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/ap-northeast-1/anthropic.claude-v1                                                  | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v1                               | --                  | --                      | 100,000             |                8191 |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v1                               | --                  | --                      | 100,000             |                8191 |
| bedrock/eu-central-1/anthropic.claude-v1                                                    | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v1                                 | --                  | --                      | 100,000             |                8191 |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v1                                 | --                  | --                      | 100,000             |                8191 |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v1                                    | --                  | --                      | 100,000             |                8191 |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v1                                    | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v1                                    | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v1                                    | --                  | --                      | 100,000             |                8191 |
| anthropic.claude-v2                                                                         | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/us-east-1/anthropic.claude-v2                                                       | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/us-west-2/anthropic.claude-v2                                                       | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/ap-northeast-1/anthropic.claude-v2                                                  | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v2                               | --                  | --                      | 100,000             |                8191 |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v2                               | --                  | --                      | 100,000             |                8191 |
| bedrock/eu-central-1/anthropic.claude-v2                                                    | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v2                                 | --                  | --                      | 100,000             |                8191 |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v2                                 | --                  | --                      | 100,000             |                8191 |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v2                                    | --                  | --                      | 100,000             |                8191 |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v2                                    | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v2                                    | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v2                                    | --                  | --                      | 100,000             |                8191 |
| anthropic.claude-v2:1                                                                       | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/us-east-1/anthropic.claude-v2:1                                                     | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/us-west-2/anthropic.claude-v2:1                                                     | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/ap-northeast-1/anthropic.claude-v2:1                                                | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-v2:1                             | --                  | --                      | 100,000             |                8191 |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-v2:1                             | --                  | --                      | 100,000             |                8191 |
| bedrock/eu-central-1/anthropic.claude-v2:1                                                  | $0.00000800         | $0.00002400             | 100,000             |                8191 |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-v2:1                               | --                  | --                      | 100,000             |                8191 |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-v2:1                               | --                  | --                      | 100,000             |                8191 |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-v2:1                                  | --                  | --                      | 100,000             |                8191 |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-v2:1                                  | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-v2:1                                  | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-v2:1                                  | --                  | --                      | 100,000             |                8191 |
| anthropic.claude-instant-v1                                                                 | $0.00000163         | $0.00000551             | 100,000             |                8191 |
| bedrock/us-east-1/anthropic.claude-instant-v1                                               | $0.00000080         | $0.00000240             | 100,000             |                8191 |
| bedrock/us-east-1/1-month-commitment/anthropic.claude-instant-v1                            | --                  | --                      | 100,000             |                8191 |
| bedrock/us-east-1/6-month-commitment/anthropic.claude-instant-v1                            | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/1-month-commitment/anthropic.claude-instant-v1                            | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/6-month-commitment/anthropic.claude-instant-v1                            | --                  | --                      | 100,000             |                8191 |
| bedrock/us-west-2/anthropic.claude-instant-v1                                               | $0.00000080         | $0.00000240             | 100,000             |                8191 |
| bedrock/ap-northeast-1/anthropic.claude-instant-v1                                          | $0.00000223         | $0.00000755             | 100,000             |                8191 |
| bedrock/ap-northeast-1/1-month-commitment/anthropic.claude-instant-v1                       | --                  | --                      | 100,000             |                8191 |
| bedrock/ap-northeast-1/6-month-commitment/anthropic.claude-instant-v1                       | --                  | --                      | 100,000             |                8191 |
| bedrock/eu-central-1/anthropic.claude-instant-v1                                            | $0.00000248         | $0.00000838             | 100,000             |                8191 |
| bedrock/eu-central-1/1-month-commitment/anthropic.claude-instant-v1                         | --                  | --                      | 100,000             |                8191 |
| bedrock/eu-central-1/6-month-commitment/anthropic.claude-instant-v1                         | --                  | --                      | 100,000             |                8191 |
| cohere.command-text-v14                                                                     | $0.00000150         | $0.00000200             | 4,096               |                4096 |
| bedrock/*/1-month-commitment/cohere.command-text-v14                                        | --                  | --                      | 4,096               |                4096 |
| bedrock/*/6-month-commitment/cohere.command-text-v14                                        | --                  | --                      | 4,096               |                4096 |
| cohere.command-light-text-v14                                                               | $0.00000030         | $0.00000060             | 4,096               |                4096 |
| bedrock/*/1-month-commitment/cohere.command-light-text-v14                                  | --                  | --                      | 4,096               |                4096 |
| bedrock/*/6-month-commitment/cohere.command-light-text-v14                                  | --                  | --                      | 4,096               |                4096 |
| cohere.command-r-plus-v1:0                                                                  | $0.00000300         | $0.00001500             | 128,000             |                4096 |
| cohere.command-r-v1:0                                                                       | $0.00000050         | $0.00000150             | 128,000             |                4096 |
| cohere.embed-english-v3                                                                     | $0.00000010         | $0.00000000             | 512                 |                 nan |
| cohere.embed-multilingual-v3                                                                | $0.00000010         | $0.00000000             | 512                 |                 nan |
| meta.llama2-13b-chat-v1                                                                     | $0.00000075         | $0.00000100             | 4,096               |                4096 |
| meta.llama2-70b-chat-v1                                                                     | $0.00000195         | $0.00000256             | 4,096               |                4096 |
| meta.llama3-8b-instruct-v1:0                                                                | $0.00000040         | $0.00000060             | 8,192               |                8192 |
| meta.llama3-70b-instruct-v1:0                                                               | $0.00000265         | $0.00000350             | 8,192               |                8192 |
| 512-x-512/50-steps/stability.stable-diffusion-xl-v0                                         | --                  | --                      | 77                  |                 nan |
| 512-x-512/max-steps/stability.stable-diffusion-xl-v0                                        | --                  | --                      | 77                  |                 nan |
| max-x-max/50-steps/stability.stable-diffusion-xl-v0                                         | --                  | --                      | 77                  |                 nan |
| max-x-max/max-steps/stability.stable-diffusion-xl-v0                                        | --                  | --                      | 77                  |                 nan |
| 1024-x-1024/50-steps/stability.stable-diffusion-xl-v1                                       | --                  | --                      | 77                  |                 nan |
| 1024-x-1024/max-steps/stability.stable-diffusion-xl-v1                                      | --                  | --                      | 77                  |                 nan |
| sagemaker/meta-textgeneration-llama-2-7b                                                    | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-7b-f                                                  | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-13b                                                   | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-13b-f                                                 | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-70b                                                   | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| sagemaker/meta-textgeneration-llama-2-70b-b-f                                               | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| together-ai-up-to-3b                                                                        | $0.00000010         | $0.00000010             | nan                 |                 nan |
| together-ai-3.1b-7b                                                                         | $0.00000020         | $0.00000020             | nan                 |                 nan |
| together-ai-7.1b-20b                                                                        | $0.00000040         | $0.00000040             | nan                 |                 nan |
| together-ai-20.1b-40b                                                                       | $0.00000080         | $0.00000080             | nan                 |                 nan |
| together-ai-40.1b-70b                                                                       | $0.00000090         | $0.00000090             | nan                 |                 nan |
| together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1                                            | $0.00000060         | $0.00000060             | nan                 |                 nan |
| together_ai/mistralai/Mistral-7B-Instruct-v0.1                                              | --                  | --                      | nan                 |                 nan |
| together_ai/togethercomputer/CodeLlama-34b-Instruct                                         | --                  | --                      | nan                 |                 nan |
| ollama/llama2                                                                               | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| ollama/llama2:13b                                                                           | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| ollama/llama2:70b                                                                           | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| ollama/llama2-uncensored                                                                    | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| ollama/mistral                                                                              | $0.00000000         | $0.00000000             | 8,192               |                8192 |
| ollama/codellama                                                                            | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| ollama/orca-mini                                                                            | $0.00000000         | $0.00000000             | 4,096               |                4096 |
| ollama/vicuna                                                                               | $0.00000000         | $0.00000000             | 2,048               |                2048 |
| deepinfra/lizpreciatior/lzlv_70b_fp16_hf                                                    | $0.00000070         | $0.00000090             | 4,096               |                4096 |
| deepinfra/Gryphe/MythoMax-L2-13b                                                            | $0.00000022         | $0.00000022             | 4,096               |                4096 |
| deepinfra/mistralai/Mistral-7B-Instruct-v0.1                                                | $0.00000013         | $0.00000013             | 32,768              |                8191 |
| deepinfra/meta-llama/Llama-2-70b-chat-hf                                                    | $0.00000070         | $0.00000090             | 4,096               |                4096 |
| deepinfra/cognitivecomputations/dolphin-2.6-mixtral-8x7b                                    | $0.00000027         | $0.00000027             | 32,768              |                8191 |
| deepinfra/codellama/CodeLlama-34b-Instruct-hf                                               | $0.00000060         | $0.00000060             | 4,096               |                4096 |
| deepinfra/deepinfra/mixtral                                                                 | $0.00000027         | $0.00000027             | 32,000              |                4096 |
| deepinfra/Phind/Phind-CodeLlama-34B-v2                                                      | $0.00000060         | $0.00000060             | 16,384              |                4096 |
| deepinfra/mistralai/Mixtral-8x7B-Instruct-v0.1                                              | $0.00000027         | $0.00000027             | 32,768              |                8191 |
| deepinfra/deepinfra/airoboros-70b                                                           | $0.00000070         | $0.00000090             | 4,096               |                4096 |
| deepinfra/01-ai/Yi-34B-Chat                                                                 | $0.00000060         | $0.00000060             | 4,096               |                4096 |
| deepinfra/01-ai/Yi-6B-200K                                                                  | $0.00000013         | $0.00000013             | 200,000             |                4096 |
| deepinfra/jondurbin/airoboros-l2-70b-gpt4-1.4.1                                             | $0.00000070         | $0.00000090             | 4,096               |                4096 |
| deepinfra/meta-llama/Llama-2-13b-chat-hf                                                    | $0.00000022         | $0.00000022             | 4,096               |                4096 |
| deepinfra/amazon/MistralLite                                                                | $0.00000020         | $0.00000020             | 32,768              |                8191 |
| deepinfra/meta-llama/Llama-2-7b-chat-hf                                                     | $0.00000013         | $0.00000013             | 4,096               |                4096 |
| deepinfra/01-ai/Yi-34B-200K                                                                 | $0.00000060         | $0.00000060             | 200,000             |                4096 |
| deepinfra/openchat/openchat_3.5                                                             | $0.00000013         | $0.00000013             | 4,096               |                4096 |
| perplexity/codellama-34b-instruct                                                           | $0.00000035         | $0.00000140             | 16,384              |               16384 |
| perplexity/codellama-70b-instruct                                                           | $0.00000070         | $0.00000280             | 16,384              |               16384 |
| perplexity/pplx-7b-chat                                                                     | $0.00000007         | $0.00000028             | 8,192               |                8192 |
| perplexity/pplx-70b-chat                                                                    | $0.00000070         | $0.00000280             | 4,096               |                4096 |
| perplexity/pplx-7b-online                                                                   | $0.00000000         | $0.00000028             | 4,096               |                4096 |
| perplexity/pplx-70b-online                                                                  | $0.00000000         | $0.00000280             | 4,096               |                4096 |
| perplexity/llama-2-70b-chat                                                                 | $0.00000070         | $0.00000280             | 4,096               |                4096 |
| perplexity/mistral-7b-instruct                                                              | $0.00000007         | $0.00000028             | 4,096               |                4096 |
| perplexity/mixtral-8x7b-instruct                                                            | $0.00000007         | $0.00000028             | 4,096               |                4096 |
| perplexity/sonar-small-chat                                                                 | $0.00000007         | $0.00000028             | 16,384              |               16384 |
| perplexity/sonar-small-online                                                               | $0.00000000         | $0.00000028             | 12,000              |               12000 |
| perplexity/sonar-medium-chat                                                                | $0.00000060         | $0.00000180             | 16,384              |               16384 |
| perplexity/sonar-medium-online                                                              | $0.00000000         | $0.00000180             | 12,000              |               12000 |
| anyscale/mistralai/Mistral-7B-Instruct-v0.1                                                 | $0.00000015         | $0.00000015             | 16,384              |               16384 |
| anyscale/Mixtral-8x7B-Instruct-v0.1                                                         | $0.00000015         | $0.00000015             | 16,384              |               16384 |
| anyscale/HuggingFaceH4/zephyr-7b-beta                                                       | $0.00000015         | $0.00000015             | 16,384              |               16384 |
| anyscale/meta-llama/Llama-2-7b-chat-hf                                                      | $0.00000015         | $0.00000015             | 4,096               |                4096 |
| anyscale/meta-llama/Llama-2-13b-chat-hf                                                     | $0.00000025         | $0.00000025             | 4,096               |                4096 |
| anyscale/meta-llama/Llama-2-70b-chat-hf                                                     | $0.00000100         | $0.00000100             | 4,096               |                4096 |
| anyscale/codellama/CodeLlama-34b-Instruct-hf                                                | $0.00000100         | $0.00000100             | 4,096               |                4096 |
| cloudflare/@cf/meta/llama-2-7b-chat-fp16                                                    | $0.00000192         | $0.00000192             | 3,072               |                3072 |
| cloudflare/@cf/meta/llama-2-7b-chat-int8                                                    | $0.00000192         | $0.00000192             | 2,048               |                2048 |
| cloudflare/@cf/mistral/mistral-7b-instruct-v0.1                                             | $0.00000192         | $0.00000192             | 8,192               |                8192 |
| cloudflare/@hf/thebloke/codellama-7b-instruct-awq                                           | $0.00000192         | $0.00000192             | 4,096               |                4096 |
| voyage/voyage-01                                                                            | $0.00000010         | $0.00000000             | 4,096               |                 nan |
| voyage/voyage-lite-01                                                                       | $0.00000010         | $0.00000000             | 4,096               |                 nan |
| voyage/voyage-large-2                                                                       | $0.00000012         | $0.00000000             | 16,000              |                 nan |
| voyage/voyage-law-2                                                                         | $0.00000012         | $0.00000000             | 16,000              |                 nan |
| voyage/voyage-code-2                                                                        | $0.00000012         | $0.00000000             | 16,000              |                 nan |
| voyage/voyage-2                                                                             | $0.00000010         | $0.00000000             | 4,000               |                 nan |
| voyage/voyage-lite-02-instruct                                                              | $0.00000010         | $0.00000000             | 4,000               |                 nan |

### Callback handlers
You may also calculate token costs in LLM wrapper/framework libraries using callbacks. 
#### LlamaIndex
```sh
pip install `'tokencost[llama-index]'`
```
To use the base callback handler, you may import it:

```python
from tokencost.callbacks.llama_index import BaseCallbackHandler
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
