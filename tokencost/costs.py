"""
Costs dictionary and utility tool for counting tokens
"""
import tiktoken
from typing import Union, List
from .constants import TOKEN_COSTS


# TODO: Add Claude support
# https://www-files.anthropic.com/production/images/model_pricing_july2023.pdf
# Note: cl100k is the openai base tokenizer. Nothing to do with Claude. Tiktoken doesn't have claude yet.
# https://github.com/anthropics/anthropic-tokenizer-typescript/blob/main/index.ts


def count_message_tokens(messages: List, model: str) -> int:
    """Return the total number of tokens in a list of (prompt or completion) messages."""
    if not messages:
        raise KeyError("Empty message list provided.")
    model = model.lower()
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
        raise KeyError(
            f"""num_tokens_from_messages() is not implemented for model {model}.
            Double check your spelling, or open an issue/PR:
            https://github.com/AgentOps-AI/tokencost/blob/main/tokencost/constants.py
            See https://github.com/openai/openai-python/blob/main/chatml.md for how messages are converted to tokens."""
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


def count_string_tokens(string: str, model: str) -> int:
    """
    Returns the number of tokens in a (prompt or completion) text string.

    Args:
        string (str): The text string.
        model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
        int: The number of tokens in the text string.
    """
    model = model.lower()
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(string))


def calculate_cost(prompt: Union[List[dict], str], completion: Union[List[dict], str], model: str) -> float:
    """
    Calculate the cost of tokens in TPUs.  1 TPU = 1/10,000,000 of $1 (USD), so 100,000 TPUs = $0.01.

    Args:
        prompt (Union[List[dict], str]): List of message objects or single string prompt.
        completion (Union[List[dict], str]): List of message objects or single string completion.
        model (str): The model name.

    Returns:
        float: The calculated cost in TPUs.
    """
    model = model.lower()
    if model not in TOKEN_COSTS:
        raise KeyError(
            f"""calculate_cost() is not implemented for model {model}.
            Double-check your spelling, or submit an issue/PR:
            https://github.com/AgentOps-AI/tokencost/blob/main/tokencost/constants.py
            """
        )
    if not isinstance(prompt, (list, str)) or not isinstance(completion, (list, str)):
        raise TypeError(
            f"""Prompt and completion each must be either a string or list of message objects.
            They are {type(prompt)} and {type(completion)}, respectively.
            """
        )
    prompt_tokens = count_string_tokens(prompt, model) if isinstance(
        prompt, str) else count_message_tokens(prompt, model)
    prompt_cost = TOKEN_COSTS[model]["prompt"]
    completion_tokens = count_string_tokens(completion, model) if isinstance(
        completion, str) else count_message_tokens(completion, model)
    completion_cost = TOKEN_COSTS[model]["completion"]

    cost = (prompt_tokens * prompt_cost + completion_tokens * completion_cost)
    return cost
