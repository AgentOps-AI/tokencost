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


| Model Name | Prompt Cost (USD) | Completion Cost (USD) | Max Prompt Tokens |
| --- | --- | --- | --- |
| gpt-4 | $0.00003000 | $0.00006000 | 8192 |
| gpt-4-0314 | $0.00003000 | $0.00006000 | 8192 |
| gpt-4-0613 | $0.00003000 | $0.00006000 | 8192 |
| gpt-4-32k | $0.00006000 | $0.00012000 | 32768 |
| gpt-4-32k-0314 | $0.00006000 | $0.00012000 | 32768 |
| gpt-4-32k-0613 | $0.00006000 | $0.00012000 | 32768 |
| gpt-4-1106-preview | $0.00001000 | $0.00003000 | 128000 |
| gpt-4-0125-preview | $0.00001000 | $0.00003000 | 128000 |
| gpt-4-vision-preview | $0.00001000 | $0.00003000 | 128000 |
| gpt-3.5-turbo | $0.00000150 | $0.00000200 | 4097 |
| gpt-3.5-turbo-0301 | $0.00000150 | $0.00000200 | 4097 |
| gpt-3.5-turbo-0613 | $0.00000150 | $0.00000200 | 4097 |
| gpt-3.5-turbo-1106 | $0.00000050 | $0.00000150 | 16385 |
| gpt-3.5-turbo-0125 | $0.00000050 | $0.00000150 | 16385 |
| gpt-3.5-turbo-16k | $0.00000300 | $0.00000400 | 16385 |
| gpt-3.5-turbo-16k-0613 | $0.00000300 | $0.00000400 | 16385 |
| text-embedding-ada-002 | $0.00000010 | $0.00000000 | 8191 |
| text-embedding-3-small | $0.00000002 | $0.00000000 | 8191 |
| text-embedding-3-large | $0.00000013 | $0.00000000 | 8191 |
| azure/gpt-4-1106-preview | $0.00001000 | $0.00003000 | 128000 |
| azure/gpt-4-0613 | $0.00003000 | $0.00006000 | 8192 |
| azure/gpt-4-32k-0613 | $0.00006000 | $0.00012000 | 32768 |
| azure/gpt-4-32k | $0.00006000 | $0.00012000 | 32768 |
| azure/gpt-4 | $0.00003000 | $0.00006000 | 8192 |
| azure/gpt-35-turbo-16k-0613 | $0.00000300 | $0.00000400 | 16385 |
| azure/gpt-35-turbo-1106 | $0.00000150 | $0.00000200 | 16384 |
| azure/gpt-35-turbo-16k | $0.00000300 | $0.00000400 | 16385 |
| azure/gpt-35-turbo | $0.00000150 | $0.00000200 | 4097 |
| azure/text-embedding-ada-002 | $0.00000010 | $0.00000000 | 8191 |
| text-davinci-003 | $0.00000200 | $0.00000200 | 4097 |
| text-curie-001 | $0.00000200 | $0.00000200 | 2049 |
| text-babbage-001 | $0.00000040 | $0.00000040 | 2049 |
| text-ada-001 | $0.00000040 | $0.00000040 | 2049 |
| babbage-002 | $0.00000040 | $0.00000040 | 16384 |
| davinci-002 | $0.00000200 | $0.00000200 | 16384 |
| gpt-3.5-turbo-instruct | $0.00000150 | $0.00000200 | 8192 |
| claude-instant-1 | $0.00000160 | $0.00000550 | 100000 |
| mistral/mistral-tiny | $0.00000010 | $0.00000040 | 8192 |
| mistral/mistral-small | $0.00000060 | $0.00000190 | 8192 |
| mistral/mistral-medium | $0.00000270 | $0.00000820 | 8192 |
| claude-instant-1.2 | $0.00000010 | $0.00000050 | 100000 |
| claude-2 | $0.00000800 | $0.00002400 | 100000 |
| claude-2.1 | $0.00000800 | $0.00002400 | 200000 |
| text-bison | $0.00000010 | $0.00000010 | 8192 |
| text-bison@001 | $0.00000010 | $0.00000010 | 8192 |
| text-unicorn | $0.00001000 | $0.00002800 | 8192 |
| text-unicorn@001 | $0.00001000 | $0.00002800 | 8192 |
| chat-bison | $0.00000010 | $0.00000010 | 4096 |
| chat-bison@001 | $0.00000010 | $0.00000010 | 4096 |
| chat-bison@002 | $0.00000010 | $0.00000010 | 4096 |
| chat-bison-32k | $0.00000010 | $0.00000010 | 32000 |
| code-bison | $0.00000010 | $0.00000010 | 6144 |
| code-bison@001 | $0.00000010 | $0.00000010 | 6144 |
| code-gecko@001 | $0.00000010 | $0.00000010 | 2048 |
| code-gecko@002 | $0.00000010 | $0.00000010 | 2048 |
| code-gecko | $0.00000010 | $0.00000010 | 2048 |
| codechat-bison | $0.00000010 | $0.00000010 | 6144 |
| codechat-bison@001 | $0.00000010 | $0.00000010 | 6144 |
| codechat-bison-32k | $0.00000010 | $0.00000010 | 32000 |
| gemini-pro | $0.00000020 | $0.00000050 | 30720 |
| gemini-pro-vision | $0.00000020 | $0.00000050 | 30720 |
| palm/chat-bison | $0.00000010 | $0.00000010 | 4096 |
| palm/chat-bison-001 | $0.00000010 | $0.00000010 | 4096 |
| palm/text-bison | $0.00000010 | $0.00000010 | 8196 |
| palm/text-bison-001 | $0.00000010 | $0.00000010 | 8196 |
| palm/text-bison-safety-off | $0.00000010 | $0.00000010 | 8196 |
| palm/text-bison-safety-recitation-off | $0.00000010 | $0.00000010 | 8196 |
| command-nightly | $0.00001500 | $0.00001500 | 4096 |
| command | $0.00001500 | $0.00001500 | 4096 |
| command-light | $0.00001500 | $0.00001500 | 4096 |
| command-medium-beta | $0.00001500 | $0.00001500 | 4096 |
| command-xlarge-beta | $0.00001500 | $0.00001500 | 4096 |
| openrouter/openai/gpt-3.5-turbo | $0.00000150 | $0.00000200 | 4095 |
| openrouter/openai/gpt-3.5-turbo-16k | $0.00000300 | $0.00000400 | 16383 |
| openrouter/openai/gpt-4 | $0.00003000 | $0.00006000 | 8192 |
| openrouter/anthropic/claude-instant-v1 | $0.00000160 | $0.00000550 | 100000 |
| openrouter/anthropic/claude-2 | $0.00001100 | $0.00003260 | 100000 |
| openrouter/google/palm-2-chat-bison | $0.00000050 | $0.00000050 | 8000 |
| openrouter/google/palm-2-codechat-bison | $0.00000050 | $0.00000050 | 8000 |
| openrouter/meta-llama/llama-2-13b-chat | $0.00000020 | $0.00000020 | 4096 |
| openrouter/meta-llama/llama-2-70b-chat | $0.00000150 | $0.00000150 | 4096 |
| openrouter/meta-llama/codellama-34b-instruct | $0.00000050 | $0.00000050 | 8096 |
| openrouter/nousresearch/nous-hermes-llama2-13b | $0.00000020 | $0.00000020 | 4096 |
| openrouter/mancer/weaver | $0.00000560 | $0.00000560 | 8000 |
| openrouter/gryphe/mythomax-l2-13b | $0.00000180 | $0.00000180 | 8192 |
| openrouter/jondurbin/airoboros-l2-70b-2.1 | $0.00001380 | $0.00001380 | 4096 |
| openrouter/undi95/remm-slerp-l2-13b | $0.00000180 | $0.00000180 | 6144 |
| openrouter/pygmalionai/mythalion-13b | $0.00000180 | $0.00000180 | 4096 |
| openrouter/mistralai/mistral-7b-instruct | $0.00000000 | $0.00000000 | 4096 |
| j2-ultra | $0.00001500 | $0.00001500 | 8192 |
| j2-mid | $0.00001000 | $0.00001000 | 8192 |
| j2-light | $0.00000300 | $0.00000300 | 8192 |
| dolphin | $0.00002000 | $0.00002000 | 4096 |
| chatdolphin | $0.00002000 | $0.00002000 | 4096 |
| luminous-base | $0.00003000 | $0.00003300 | 2048 |
| luminous-base-control | $0.00003740 | $0.00004120 | 2048 |
| luminous-extended | $0.00004500 | $0.00004940 | 2048 |
| luminous-extended-control | $0.00005620 | $0.00006180 | 2048 |
| luminous-supreme | $0.00017500 | $0.00019250 | 2048 |
| luminous-supreme-control | $0.00021870 | $0.00024060 | 2048 |
| ai21.j2-mid-v1 | $0.00001250 | $0.00001250 | 8191 |
| ai21.j2-ultra-v1 | $0.00001880 | $0.00001880 | 8191 |
| amazon.titan-text-lite-v1 | $0.00000030 | $0.00000040 | 8000 |
| amazon.titan-text-express-v1 | $0.00000130 | $0.00000170 | 8000 |
| anthropic.claude-v1 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/us-east-1/anthropic.claude-v1 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/us-west-2/anthropic.claude-v1 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/ap-northeast-1/anthropic.claude-v1 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/eu-central-1/anthropic.claude-v1 | $0.00000800 | $0.00002400 | 100000 |
| anthropic.claude-v2 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/us-east-1/anthropic.claude-v2 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/us-west-2/anthropic.claude-v2 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/ap-northeast-1/anthropic.claude-v2 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/eu-central-1/anthropic.claude-v2 | $0.00000800 | $0.00002400 | 100000 |
| anthropic.claude-v2:1 | $0.00000800 | $0.00002400 | 200000 |
| bedrock/us-east-1/anthropic.claude-v2:1 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/us-west-2/anthropic.claude-v2:1 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/ap-northeast-1/anthropic.claude-v2:1 | $0.00000800 | $0.00002400 | 100000 |
| bedrock/eu-central-1/anthropic.claude-v2:1 | $0.00000800 | $0.00002400 | 100000 |
| anthropic.claude-instant-v1 | $0.00000160 | $0.00000550 | 100000 |
| bedrock/us-east-1/anthropic.claude-instant-v1 | $0.00000080 | $0.00000240 | 100000 |
| bedrock/us-west-2/anthropic.claude-instant-v1 | $0.00000080 | $0.00000240 | 100000 |
| bedrock/ap-northeast-1/anthropic.claude-instant-v1 | $0.00000220 | $0.00000750 | 100000 |
| bedrock/eu-central-1/anthropic.claude-instant-v1 | $0.00000240 | $0.00000830 | 100000 |
| cohere.command-text-v14 | $0.00000150 | $0.00000200 | 4096 |
| cohere.command-light-text-v14 | $0.00000030 | $0.00000060 | 4000 |
| cohere.embed-english-v3 | $0.00000010 | $0.00000000 | 512 |
| cohere.embed-multilingual-v3 | $0.00000010 | $0.00000000 | 512 |
| meta.llama2-13b-chat-v1 | $0.00000070 | $0.00000100 | 4096 |
| meta.llama2-70b-chat-v1 | $0.00000190 | $0.00000250 | 4096 |
| sagemaker/meta-textgeneration-llama-2-7b | $0.00000000 | $0.00000000 | 4096 |
| sagemaker/meta-textgeneration-llama-2-7b-f | $0.00000000 | $0.00000000 | 4096 |
| sagemaker/meta-textgeneration-llama-2-13b | $0.00000000 | $0.00000000 | 4096 |
| sagemaker/meta-textgeneration-llama-2-13b-f | $0.00000000 | $0.00000000 | 4096 |
| sagemaker/meta-textgeneration-llama-2-70b | $0.00000000 | $0.00000000 | 4096 |
| sagemaker/meta-textgeneration-llama-2-70b-b-f | $0.00000000 | $0.00000000 | 4096 |
| together-ai-7.1b-20b | $0.00000040 | $0.00000040 | 1000 |
| ollama/llama2 | $0.00000000 | $0.00000000 | 4096 |
| ollama/llama2:13b | $0.00000000 | $0.00000000 | 4096 |
| ollama/llama2:70b | $0.00000000 | $0.00000000 | 4096 |
| ollama/llama2-uncensored | $0.00000000 | $0.00000000 | 4096 |
| ollama/mistral | $0.00000000 | $0.00000000 | 8192 |
| ollama/codellama | $0.00000000 | $0.00000000 | 4096 |
| ollama/orca-mini | $0.00000000 | $0.00000000 | 4096 |
| ollama/vicuna | $0.00000000 | $0.00000000 | 2048 |
| deepinfra/meta-llama/Llama-2-70b-chat-hf | $0.00000070 | $0.00000090 | 4096 |
| deepinfra/codellama/CodeLlama-34b-Instruct-hf | $0.00000060 | $0.00000060 | 4096 |
| deepinfra/meta-llama/Llama-2-13b-chat-hf | $0.00000030 | $0.00000030 | 4096 |
| deepinfra/meta-llama/Llama-2-7b-chat-hf | $0.00000020 | $0.00000020 | 4096 |
| deepinfra/mistralai/Mistral-7B-Instruct-v0.1 | $0.00000020 | $0.00000020 | 4096 |
| deepinfra/jondurbin/airoboros-l2-70b-gpt4-1.4.1 | $0.00000070 | $0.00000090 | 4096 |
| perplexity/pplx-7b-chat | $0.00000000 | $0.00000000 | 8192 |
| perplexity/pplx-70b-chat | $0.00000000 | $0.00000000 | 4096 |
| perplexity/pplx-7b-online | $0.00000000 | $0.00050000 | 4096 |
| perplexity/pplx-70b-online | $0.00000000 | $0.00050000 | 4096 |
| perplexity/llama-2-13b-chat | $0.00000000 | $0.00000000 | 4096 |
| perplexity/llama-2-70b-chat | $0.00000000 | $0.00000000 | 4096 |
| perplexity/mistral-7b-instruct | $0.00000000 | $0.00000000 | 4096 |
| perplexity/replit-code-v1.5-3b | $0.00000000 | $0.00000000 | 4096 |
| anyscale/mistralai/Mistral-7B-Instruct-v0.1 | $0.00000010 | $0.00000010 | 16384 |
| anyscale/HuggingFaceH4/zephyr-7b-beta | $0.00000010 | $0.00000010 | 16384 |
| anyscale/meta-llama/Llama-2-7b-chat-hf | $0.00000010 | $0.00000010 | 4096 |
| anyscale/meta-llama/Llama-2-13b-chat-hf | $0.00000020 | $0.00000020 | 4096 |
| anyscale/meta-llama/Llama-2-70b-chat-hf | $0.00000100 | $0.00000100 | 4096 |
| anyscale/codellama/CodeLlama-34b-Instruct-hf | $0.00000100 | $0.00000100 | 16384 |
| cloudflare/@cf/meta/llama-2-7b-chat-fp16 | $0.00000190 | $0.00000190 | 3072 |
| cloudflare/@cf/meta/llama-2-7b-chat-int8 | $0.00000190 | $0.00000190 | 2048 |
| cloudflare/@cf/mistral/mistral-7b-instruct-v0.1 | $0.00000190 | $0.00000190 | 8192 |
| cloudflare/@hf/thebloke/codellama-7b-instruct-awq | $0.00000190 | $0.00000190 | 4096 |
| voyage/voyage-01 | $0.00000010 | $0.00000000 | 4096 |
| voyage/voyage-lite-01 | $0.00000010 | $0.00000000 | 4096 |

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
