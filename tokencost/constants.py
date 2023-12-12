# Last updated Dec 6 2023 from https://openai.com/pricing

"""
Prompt tokens are based on number of words + other chars (eg spaces and punctuation) in input.
Completion tokens are similarly based on how long chatGPT's response is.

You can use ChatGPT's webapp (which uses their tiktoken repo) to see how many tokens your phrase is:
https://platform.openai.com/tokenizer

However, when asking follow-up questions and to maintain context, everything above and
including your follow-up question is considered a prompt and will cost prompt tokens.
"""

# How to read the below: Each prompt token costs __ TPUs per token, and each completion token costs __ TPUs per token.
# Calculated in TPUs (token price unit), where 1 TPU = 1/10,000,000 of $1 (USD). 100,000 TPUs would equate to $0.01.
TOKEN_COSTS = {
    # Applications using the gpt-3.5-turbo name will automatically be upgraded to the new model on December 11, 2023.
    "gpt-3.5-turbo": {"prompt": 15, "completion": 20},
    "gpt-3.5-turbo-0301": {"prompt": 15, "completion": 20},
    "gpt-3.5-turbo-0613": {"prompt": 15, "completion": 20},
    "gpt-3.5-turbo-16k": {"prompt": 30, "completion": 40},
    "gpt-3.5-turbo-16k-0613": {"prompt": 30, "completion": 40},
    "gpt-3.5-turbo-1106": {"prompt": 10, "completion": 20},
    "gpt-3.5-turbo-instruct": {"prompt": 15, "completion": 20},
    "gpt-4": {"prompt": 300, "completion": 600},
    "gpt-4-0314": {"prompt": 300, "completion": 600},
    "gpt-4-0613": {"prompt": 300, "completion": 600},
    "gpt-4-32k": {"prompt": 600, "completion": 1200},
    "gpt-4-32k-0314": {"prompt": 600, "completion": 1200},
    "gpt-4-32k-0613": {"prompt": 600, "completion": 1200},
    "gpt-4-1106-preview": {"prompt": 100, "completion": 300},
    "gpt-4-1106-vision-preview": {"prompt": 100, "completion": 300},
    "text-embedding-ada-002": {"prompt": 1, "completion": 0, },
}

# Token max is the combined prompt/completion limit.
TOKEN_MAX = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0301": 4096,
    "gpt-3.5-turbo-0613": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-3.5-turbo-16k-0613": 16384,
    "gpt-4": 8192,
    "gpt-4-0314": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0314": 32768,
    "gpt-4-0613": 8192,
    "gpt-4-1106-vision-preview": 4096,
    "text-embedding-ada-002": 8192,
}
