# Prices last updated Dec 6 2023 from: https://openai.com/pricing
# Max prompt limits (aka context windows) last upated Dec 15 2023 from
# https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo


"""
Prompt (aka context) tokens are based on number of words + other chars (eg spaces and punctuation) in input.
Completion tokens are similarly based on how long chatGPT's response is.
Prompt tokens + completion tokens = total tokens.
The max total limit is typically 1 more than the prompt token limit, so there's space for at least one completion token.

You can use ChatGPT's webapp (which uses their tiktoken repo) to see how many tokens your phrase is:
https://platform.openai.com/tokenizer

Note: When asking follow-up questions, everything above and including your follow-up question
is considered a prompt (for the purpose of context) and will thus cost prompt tokens.

1 Token Price Unit (TPU) is defined as 1/10,000,000 of $1 (USD). 100,000 TPUs would equate to $0.01.
"""

USD_PER_TPU = float(10_000_000)

# How to read TOKEN_COSTS:
# Each prompt token costs __ TPUs per token.
# Each completion token costs __ TPUs per token.
# Max prompt limit of each model is __ tokens.
TOKEN_COSTS = {
    # Applications using the gpt-3.5-turbo name will automatically be upgraded to the new model on December 11, 2023.
    # Note: Documentation for some of the gpt-3.5s has a max_prompt/context window ?typo? that says 4096.
    # Can send 4097 prompt tokens (which returns 1 completion token, so total 4098)
    # and overloading API returns error message that states limit of 4097.

    "gpt-3.5-turbo": {"prompt": 15, "completion": 20, "max_prompt": 4097},
    "gpt-3.5-turbo-0301": {"prompt": 15, "completion": 20, "max_prompt": 4097},
    "gpt-3.5-turbo-0613": {"prompt": 15, "completion": 20, "max_prompt": 4097},
    "gpt-3.5-turbo-16k": {"prompt": 30, "completion": 40, "max_prompt": 16385},
    "gpt-3.5-turbo-16k-0613": {"prompt": 30, "completion": 40, "max_prompt": 16385},
    "gpt-3.5-turbo-1106": {"prompt": 10, "completion": 20, "max_prompt": 16385},
    "gpt-3.5-turbo-instruct": {"prompt": 15, "completion": 20, "max_prompt": 4096},
    "gpt-4": {"prompt": 300, "completion": 600, "max_prompt": 8192},
    "gpt-4-0314": {"prompt": 300, "completion": 600, "max_prompt": 8192},
    "gpt-4-0613": {"prompt": 300, "completion": 600, "max_prompt": 8192},
    "gpt-4-32k": {"prompt": 600, "completion": 1200, "max_prompt": 32768},
    "gpt-4-32k-0314": {"prompt": 600, "completion": 1200, "max_prompt": 32768},
    "gpt-4-32k-0613": {"prompt": 600, "completion": 1200, "max_prompt": 32768},
    "gpt-4-1106-preview": {"prompt": 100, "completion": 300, "max_prompt": 128000},  # Not a typo, actually 128k.
    "gpt-4-vision-preview": {"prompt": 100, "completion": 300, "max_prompt": 128000},
    "text-embedding-ada-002": {"prompt": 1, "completion": 0, "max_prompt": 8192},
}
