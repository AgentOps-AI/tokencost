# TokenCost
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![PyPI - Version](https://img.shields.io/pypi/v/tokencost)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/AgentOpsAI)](https://x.com/agentopsai)

Clientside token counting + price estimation for LLM apps and AI agents. Tokencost helps calculate the USD cost of using major Large Language Model (LLMs) APIs by calculating the estimated cost of prompts and completions.

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
# 135 + 140 = 275 ($0.0000275)
# Priced in TPUs (token price units), which is 1/10,000,000th of a USD.
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
# 180 + 100 = 280 ($0.0000280)

from tokencost import USD_PER_TPU
print(f"Cost USD: ${(prompt_cost + completion_cost)/USD_PER_TPU}")
# $2.8e-05
```

**Calculating cost using string prompts instead of messages:**
```python
from tokencost import calculate_prompt_cost, USD_PER_TPU

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

message_prompt = [{ "role": "user", "content": "Hello world"}]
# Counting tokens in prompts formatted as message lists
print(count_message_tokens(message_prompt, model="gpt-3.5-turbo"))
# 9

# Alternatively, counting tokens in string prompts
print(count_string_tokens(prompt="Hello world", model="gpt-3.5-turbo"))
# 2

```

## Cost table
Units denominated in TPUs (Token Price Units = 1/10,000,000 USD). All prices can be located in `model_prices.yaml`.

| Model Name | Prompt Cost | Completion Cost | Max Prompt Tokens | 
| --- | --- | --- | --- |
| gpt-3.5-turbo | 15 | 20 | 4097 |
| gpt-3.5-turbo-instruct | 15 | 20 | 8192 |
| gpt-3.5-turbo-0301 | 15 | 20 | 4097 |
| gpt-3.5-turbo-0613 | 15 | 20 | 4097 |
| gpt-3.5-turbo-1106 | 10 | 20 | 16385 |
| gpt-3.5-turbo-16k | 30 | 40 | 16385 |
| gpt-3.5-turbo-16k-0613 | 30 | 40 | 16385 |
| gpt-4 | 300 | 600 | 8192 |
| gpt-4-0314 | 300 | 600 | 8192 |
| gpt-4-0613 | 300 | 600 | 8192 |
| gpt-4-32k | 600 | 1200 | 32768 |
| gpt-4-32k-0314 | 600 | 1200 | 32768 |
| gpt-4-32k-0613 | 600 | 1200 | 32768 |
| gpt-4-1106-preview | 100 | 300 | 128000 |
| gpt-4-vision-preview | 100 | 300 | 128000 |
| text-davinci-003 | 20 | 20 | 4097 |
| text-curie-001 | 20 | 20 | 2049 |
| text-babbage-001 | 4 | 4 | 2049 |
| text-ada-001 | 4 | 4 | 2049 |
| babbage-002 | 4 | 4 | 16384 |
| davinci-002 | 20 | 20 | 16384 |
| text-embedding-ada-002 | 1 | 0 | 8191 |
| azure/gpt-4-1106-preview | 100 | 300 | 128000 |
| azure/gpt-4-0613 | 300 | 600 | 8192 |
| azure/gpt-4-32k-0613 | 600 | 1200 | 32768 |
| azure/gpt-4-32k | 600 | 1200 | 32768 |
| azure/gpt-4 | 300 | 600 | 8192 |
| azure/gpt-35-turbo-16k-0613 | 30 | 40 | 16385 |
| azure/gpt-35-turbo-1106 | 15 | 20 | 16384 |
| azure/gpt-35-turbo-16k | 30 | 40 | 16385 |
| azure/gpt-35-turbo | 15 | 20 | 4097 |
| azure/text-embedding-ada-002 | 1 | 0 | 8191 |
| claude-instant-1 | 16 | 55 | 100000 |
| mistral/mistral-tiny | 1 | 4 | 8192 |
| mistral/mistral-small | 6 | 19 | 8192 |
| mistral/mistral-medium | 27 | 82 | 8192 |
| claude-instant-1.2 | 1 | 5 | 100000 |
| claude-2 | 80 | 240 | 100000 |
| claude-2.1 | 80 | 240 | 200000 |
| text-bison | 1 | 1 | 8192 |
| text-bison@001 | 1 | 1 | 8192 |
| text-unicorn | 100 | 280 | 8192 |
| text-unicorn@001 | 100 | 280 | 8192 |
| chat-bison | 1 | 1 | 4096 |
| chat-bison@001 | 1 | 1 | 4096 |
| chat-bison@002 | 1 | 1 | 4096 |
| chat-bison-32k | 1 | 1 | 32000 |
| code-bison | 1 | 1 | 6144 |
| code-bison@001 | 1 | 1 | 6144 |
| code-gecko@001 | 1 | 1 | 2048 |
| code-gecko@002 | 1 | 1 | 2048 |
| code-gecko | 1 | 1 | 2048 |
| codechat-bison | 1 | 1 | 6144 |
| codechat-bison@001 | 1 | 1 | 6144 |
| codechat-bison-32k | 1 | 1 | 32000 |
| gemini-pro | 2 | 5 | 30720 |
| gemini-pro-vision | 2 | 5 | 30720 |
| palm/chat-bison | 1 | 1 | 4096 |
| palm/chat-bison-001 | 1 | 1 | 4096 |
| palm/text-bison | 1 | 1 | 8196 |
| palm/text-bison-001 | 1 | 1 | 8196 |
| palm/text-bison-safety-off | 1 | 1 | 8196 |
| palm/text-bison-safety-recitation-off | 1 | 1 | 8196 |
| command-nightly | 150 | 150 | 4096 |
| command | 150 | 150 | 4096 |
| command-light | 150 | 150 | 4096 |
| command-medium-beta | 150 | 150 | 4096 |
| command-xlarge-beta | 150 | 150 | 4096 |
| openrouter/openai/gpt-3.5-turbo | 15 | 20 | 4095 |
| openrouter/openai/gpt-3.5-turbo-16k | 30 | 40 | 16383 |
| openrouter/openai/gpt-4 | 300 | 600 | 8192 |
| openrouter/anthropic/claude-instant-v1 | 16 | 55 | 100000 |
| openrouter/anthropic/claude-2 | 110 | 326 | 100000 |
| openrouter/google/palm-2-chat-bison | 5 | 5 | 8000 |
| openrouter/google/palm-2-codechat-bison | 5 | 5 | 8000 |
| openrouter/meta-llama/llama-2-13b-chat | 2 | 2 | 4096 |
| openrouter/meta-llama/llama-2-70b-chat | 15 | 15 | 4096 |
| openrouter/meta-llama/codellama-34b-instruct | 5 | 5 | 8096 |
| openrouter/nousresearch/nous-hermes-llama2-13b | 2 | 2 | 4096 |
| openrouter/mancer/weaver | 56 | 56 | 8000 |
| openrouter/gryphe/mythomax-l2-13b | 18 | 18 | 8192 |
| openrouter/jondurbin/airoboros-l2-70b-2.1 | 138 | 138 | 4096 |
| openrouter/undi95/remm-slerp-l2-13b | 18 | 18 | 6144 |
| openrouter/pygmalionai/mythalion-13b | 18 | 18 | 4096 |
| openrouter/mistralai/mistral-7b-instruct | 0 | 0 | 4096 |
| j2-ultra | 150 | 150 | 8192 |
| j2-mid | 100 | 100 | 8192 |
| j2-light | 30 | 30 | 8192 |
| dolphin | 200 | 200 | 4096 |
| chatdolphin | 200 | 200 | 4096 |
| luminous-base | 300 | 330 | 2048 |
| luminous-base-control | 374 | 412 | 2048 |
| luminous-extended | 450 | 494 | 2048 |
| luminous-extended-control | 562 | 618 | 2048 |
| luminous-supreme | 1750 | 1925 | 2048 |
| luminous-supreme-control | 2187 | 2406 | 2048 |
| ai21.j2-mid-v1 | 125 | 125 | 8191 |
| ai21.j2-ultra-v1 | 188 | 188 | 8191 |
| amazon.titan-text-lite-v1 | 3 | 4 | 8000 |
| amazon.titan-text-express-v1 | 13 | 17 | 8000 |
| anthropic.claude-v1 | 80 | 240 | 100000 |
| bedrock/us-east-1/anthropic.claude-v1 | 80 | 240 | 100000 |
| bedrock/us-west-2/anthropic.claude-v1 | 80 | 240 | 100000 |
| bedrock/ap-northeast-1/anthropic.claude-v1 | 80 | 240 | 100000 |
| bedrock/eu-central-1/anthropic.claude-v1 | 80 | 240 | 100000 |
| anthropic.claude-v2 | 80 | 240 | 100000 |
| bedrock/us-east-1/anthropic.claude-v2 | 80 | 240 | 100000 |
| bedrock/us-west-2/anthropic.claude-v2 | 80 | 240 | 100000 |
| bedrock/ap-northeast-1/anthropic.claude-v2 | 80 | 240 | 100000 |
| bedrock/eu-central-1/anthropic.claude-v2 | 80 | 240 | 100000 |
| anthropic.claude-v2:1 | 80 | 240 | 200000 |
| bedrock/us-east-1/anthropic.claude-v2:1 | 80 | 240 | 100000 |
| bedrock/us-west-2/anthropic.claude-v2:1 | 80 | 240 | 100000 |
| bedrock/ap-northeast-1/anthropic.claude-v2:1 | 80 | 240 | 100000 |
| bedrock/eu-central-1/anthropic.claude-v2:1 | 80 | 240 | 100000 |
| anthropic.claude-instant-v1 | 16 | 55 | 100000 |
| bedrock/us-east-1/anthropic.claude-instant-v1 | 8 | 24 | 100000 |
| bedrock/us-west-2/anthropic.claude-instant-v1 | 8 | 24 | 100000 |
| bedrock/ap-northeast-1/anthropic.claude-instant-v1 | 22 | 75 | 100000 |
| bedrock/eu-central-1/anthropic.claude-instant-v1 | 24 | 83 | 100000 |
| cohere.command-text-v14 | 15 | 20 | 4096 |
| cohere.command-light-text-v14 | 3 | 6 | 4000 |
| cohere.embed-english-v3 | 1 | 0 | 512 |
| cohere.embed-multilingual-v3 | 1 | 0 | 512 |
| meta.llama2-13b-chat-v1 | 7 | 10 | 4096 |
| meta.llama2-70b-chat-v1 | 19 | 25 | 4096 |
| sagemaker/meta-textgeneration-llama-2-7b | 0 | 0 | 4096 |
| sagemaker/meta-textgeneration-llama-2-7b-f | 0 | 0 | 4096 |
| sagemaker/meta-textgeneration-llama-2-13b | 0 | 0 | 4096 |
| sagemaker/meta-textgeneration-llama-2-13b-f | 0 | 0 | 4096 |
| sagemaker/meta-textgeneration-llama-2-70b | 0 | 0 | 4096 |
| sagemaker/meta-textgeneration-llama-2-70b-b-f | 0 | 0 | 4096 |
| together-ai-7.1b-20b | 4 | 4 | 1000 |
| ollama/llama2 | 0 | 0 | 4096 |
| ollama/llama2:13b | 0 | 0 | 4096 |
| ollama/llama2:70b | 0 | 0 | 4096 |
| ollama/llama2-uncensored | 0 | 0 | 4096 |
| ollama/mistral | 0 | 0 | 8192 |
| ollama/codellama | 0 | 0 | 4096 |
| ollama/orca-mini | 0 | 0 | 4096 |
| ollama/vicuna | 0 | 0 | 2048 |
| deepinfra/meta-llama/Llama-2-70b-chat-hf | 7 | 9 | 4096 |
| deepinfra/codellama/CodeLlama-34b-Instruct-hf | 6 | 6 | 4096 |
| deepinfra/meta-llama/Llama-2-13b-chat-hf | 3 | 3 | 4096 |
| deepinfra/meta-llama/Llama-2-7b-chat-hf | 2 | 2 | 4096 |
| deepinfra/mistralai/Mistral-7B-Instruct-v0.1 | 2 | 2 | 4096 |
| deepinfra/jondurbin/airoboros-l2-70b-gpt4-1.4.1 | 7 | 9 | 4096 |
| perplexity/pplx-7b-chat | 0 | 0 | 8192 |
| perplexity/pplx-70b-chat | 0 | 0 | 4096 |
| perplexity/pplx-7b-online | 0 | 5000 | 4096 |
| perplexity/pplx-70b-online | 0 | 5000 | 4096 |
| perplexity/llama-2-13b-chat | 0 | 0 | 4096 |
| perplexity/llama-2-70b-chat | 0 | 0 | 4096 |
| perplexity/mistral-7b-instruct | 0 | 0 | 4096 |
| perplexity/replit-code-v1.5-3b | 0 | 0 | 4096 |
| anyscale/mistralai/Mistral-7B-Instruct-v0.1 | 1 | 1 | 16384 |
| anyscale/HuggingFaceH4/zephyr-7b-beta | 1 | 1 | 16384 |
| anyscale/meta-llama/Llama-2-7b-chat-hf | 1 | 1 | 4096 |
| anyscale/meta-llama/Llama-2-13b-chat-hf | 2 | 2 | 4096 |
| anyscale/meta-llama/Llama-2-70b-chat-hf | 10 | 10 | 4096 |
| anyscale/codellama/CodeLlama-34b-Instruct-hf | 10 | 10 | 16384 |
| cloudflare/@cf/meta/llama-2-7b-chat-fp16 | 19 | 19 | 3072 |
| cloudflare/@cf/meta/llama-2-7b-chat-int8 | 19 | 19 | 2048 |
| cloudflare/@cf/mistral/mistral-7b-instruct-v0.1 | 19 | 19 | 8192 |
| cloudflare/@hf/thebloke/codellama-7b-instruct-awq | 19 | 19 | 4096 |
| voyage/voyage-01 | 1 | 0 | 4096 |
| voyage/voyage-lite-01 | 1 | 0 | 4096 |

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
