"""
Costs dictionary and utility tool for counting tokens
"""

import tiktoken
from typing import List

# Calculated in TPU (token price units) aka (1/10,000,000 of $1)
TOKEN_COSTS = {
    # Applications using the gpt-3.5-turbo name will automatically be upgraded to the new model on December 11.
    "gpt-3.5-turbo": {"prompt": 15, "completion": 20},
    "gpt-3.5-turbo-0301": {"prompt": 15, "completion": 20},
    "gpt-3.5-turbo-0613": {"prompt": 15, "completion": 20},
    "gpt-3.5-turbo-1106": {"prompt": 10, "completion": 20},
    "gpt-3.5-turbo-instruct": {"prompt": 15, "completion": 20},
    "gpt-3.5-turbo-16k": {"prompt": 30, "completion": 40},
    "gpt-3.5-turbo-16k-0613": {"prompt": 30, "completion": 40},
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


# TODO: Add Claude support
# https://www-files.anthropic.com/production/images/model_pricing_july2023.pdf
# Note: cl100k is the openai base tokenizer. Nothing to do with Claude. Tiktoken doesn't have claude yet.
# https://github.com/anthropics/anthropic-tokenizer-typescript/blob/main/index.ts

TOKEN_MAX = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0301": 4096,
    "gpt-3.5-turbo-0613": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-3.5-turbo-16k-0613": 16384,
    "gpt-4-0314": 8192,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0314": 32768,
    "gpt-4-0613": 8192,
    "text-embedding-ada-002": 8192,
}


def count_message_tokens(messages, model):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 4
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return count_message_tokens(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return count_message_tokens(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def count_string_tokens(string: str, model_name: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The text string.
        model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
        int: The number of tokens in the text string.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(string))


def get_max_completion_tokens(messages: List[dict], model: str, default: int) -> int:
    """Calculate the maximum number of completion tokens for a given model and list of messages.

    Args:
        messages: A list of messages.
        model: The model name.

    Returns:
        The maximum number of completion tokens.
    """
    if model not in TOKEN_MAX:
        return default
    return TOKEN_MAX[model] - count_message_tokens(messages) - 1


def calculate_cost(prompt_tokens: int, completion_tokens: int, model: str) -> float:
    """
    Calculate the cost of tokens.

    Args:
        prompt (str): The prompt string.
        completion (str): The completion string.
        model (str): The model name.

    Returns:
        float: The calculated cost.
    """
    prompt_cost = TOKEN_COSTS[model]["prompt"]
    print(f"{prompt_cost=}")
    completion_cost = TOKEN_COSTS[model]["completion"]
    print(f"{completion_cost=}")

    cost = (prompt_tokens * prompt_cost + completion_tokens * completion_cost)
    return cost

