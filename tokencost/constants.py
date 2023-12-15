# Prices last updated Dec 6 2023 from https://openai.com/pricing
# Max prompt limits last upated Dec 14 2023 by overloading the API and reading the error message.

"""
Prompt tokens are based on number of words + other chars (eg spaces and punctuation) in input.
Completion tokens are similarly based on how long chatGPT's response is.

You can use ChatGPT's webapp (which uses their tiktoken repo) to see how many tokens your phrase is:
https://platform.openai.com/tokenizer

Note: When asking follow-up questions, everything above and including your follow-up question
is considered a prompt (for the purpose of context) and will thus cost prompt tokens.
"""

# 1 Token Price Unit (TPU) = 1/10,000,000 of $1 (USD). 100,000 TPUs would equate to $0.01.
# How to read the below: Each prompt token costs __ TPUs per token, and each completion token costs __ TPUs per token.
# Max prompt token limit of each model is __. The max total limit is typically 1 more than the prompt token limit, so there's space for at least one completion token.

TOKEN_COSTS = {
    # Applications using the gpt-3.5-turbo name will automatically be upgraded to the new model on December 11, 2023.
    "gpt-3.5-turbo": {"prompt": 15, "completion": 20, "max_prompt": 4097},
    "gpt-3.5-turbo-0301": {"prompt": 15, "completion": 20, "max_prompt": 4097},
    "gpt-3.5-turbo-0613": {"prompt": 15, "completion": 20, "max_prompt": 4097},
    "gpt-3.5-turbo-16k": {"prompt": 30, "completion": 40, "max_prompt": 16385},
    "gpt-3.5-turbo-16k-0613": {"prompt": 30, "completion": 40, "max_prompt": 16385},
    "gpt-3.5-turbo-1106": {"prompt": 10, "completion": 20, "max_prompt": 16385},
    "gpt-3.5-turbo-instruct": {"prompt": 15, "completion": 20}, # Not a chat model error.
    "gpt-4": {"prompt": 300, "completion": 600, "max_prompt": 8192},
    "gpt-4-0314": {"prompt": 300, "completion": 600, "max_prompt": 8192},
    "gpt-4-0613": {"prompt": 300, "completion": 600, "max_prompt": 8192},
    "gpt-4-32k": {"prompt": 600, "completion": 1200, "max_prompt": 32768}, # Does not exist or don't have access to it error.
    "gpt-4-32k-0314": {"prompt": 600, "completion": 1200, "max_prompt": 32768}, # Does not exist or don't have access to it error.
    "gpt-4-32k-0613": {"prompt": 600, "completion": 1200}, # Does not exist or don't have access to it error.
    "gpt-4-1106-preview": {"prompt": 100, "completion": 300, "max_prompt": 128000}, # This is not a typo. It is actually 128k.
    "gpt-4-1106-vision-preview": {"prompt": 100, "completion": 300, "max_prompt": 4096}, # Does not exist or don't have access to it error.
    "text-embedding-ada-002": {"prompt": 1, "completion": 0, "max_prompt": 8192}, # Not a chat model error.
}
