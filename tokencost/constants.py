import os
import yaml
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

USD_PER_TPU = 10_000_000

# How to read TOKEN_COSTS:
# Each prompt token costs __ TPUs per token.
# Each completion token costs __ TPUs per token.
# Max prompt limit of each model is __ tokens.

with open(os.path.join(os.path.dirname(__file__), "model_prices.yaml"), "r") as f:
    TOKEN_COSTS = yaml.safe_load(f)
