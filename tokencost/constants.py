import os
import json
from urllib.request import urlopen

"""
Prompt (aka context) tokens are based on number of words + other chars (eg spaces and punctuation) in input.
Completion tokens are similarly based on how long chatGPT's response is.
Prompt tokens + completion tokens = total tokens.
The max total limit is typically 1 more than the prompt token limit, so there's space for at least one completion token.

You can use ChatGPT's webapp (which uses their tiktoken repo) to see how many tokens your phrase is:
https://platform.openai.com/tokenizer

Note: When asking follow-up questions, everything above and including your follow-up question
is considered a prompt (for the purpose of context) and will thus cost prompt tokens.
"""

# How to read TOKEN_COSTS:
# Each prompt token costs __ USD per token.
# Each completion token costs __ USD per token.
# Max prompt limit of each model is __ tokens.

# Fetch the latest prices using urllib.request
PRICES_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"


def fetch_costs():
    try:
        with urlopen(PRICES_URL) as response:
            if response.status == 200:
                return json.loads(response.read())
            else:
                raise Exception("Failed to fetch token costs, status code: {}".format(response.status))
    except Exception:
        # If fetching fails, use the local model_prices.json as a fallback
        print('Unable to fetch token costs, using local model_prices.json as fallback. Prices may have changed since the last update.')
        with open(os.path.join(os.path.dirname(__file__), "model_prices.json"), "r") as f:
            return json.load(f)


TOKEN_COSTS = fetch_costs()
