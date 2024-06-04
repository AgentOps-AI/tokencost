"""
Costs dictionary and utility tool for counting tokens
"""

import tiktoken
from typing import Union, List, Dict
from .constants import TOKEN_COSTS
from decimal import Decimal
import logging


# TODO: Add Claude support
# https://www-files.anthropic.com/production/images/model_pricing_july2023.pdf
# Note: cl100k is the openai base tokenizer. Nothing to do with Claude. Tiktoken doesn't have claude yet.
# https://github.com/anthropics/anthropic-tokenizer-typescript/blob/main/index.ts


def strip_ft_model_name(model: str) -> str:
    """
    Finetuned models format: ft:gpt-3.5-turbo:my-org:custom_suffix:id
    We only need the base model name to get cost info.
    """
    if model.startswith("ft:gpt-3.5-turbo"):
        model = "ft:gpt-3.5-turbo"
    return model


def count_message_tokens(messages: List[Dict[str, str]], model: str) -> int:
    """
    Return the total number of tokens in a prompt's messages.
    Args:
        messages (List[Dict[str, str]]): Message format for prompt requests. e.g.:
            [{ "role": "user", "content": "Hello world"},
             { "role": "assistant", "content": "How may I assist you today?"}]
        model (str): Name of LLM to choose encoding for.
    Returns:
        Total number of tokens in message.
    """
    model = model.lower()
    model = strip_ft_model_name(model)
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logging.warning("Model not found. Using cl100k_base encoding.")
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
        logging.warning(
            "gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return count_message_tokens(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        logging.warning(
            "gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return count_message_tokens(messages, model="gpt-4-0613")
    else:
        raise KeyError(
            f"""num_tokens_from_messages() is not implemented for model {model}.
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


def count_string_tokens(prompt: str, model: str) -> int:
    """
    Returns the number of tokens in a (prompt or completion) text string.

    Args:
        prompt (str): The text string
        model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
        int: The number of tokens in the text string.
    """
    model = model.lower()
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logging.warning("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(prompt))


def calculate_cost_by_tokens(num_tokens: int, model: str, token_type: str) -> Decimal:
    """
    Calculate the cost based on the number of tokens and the model.

    Args:
        num_tokens (int): The number of tokens.
        model (str): The model name.
        token_type (str): Type of token ('input' or 'output').

    Returns:
        Decimal: The calculated cost in USD.
    """
    model = model.lower()
    if model not in TOKEN_COSTS:
        raise KeyError(
            f"""Model {model} is not implemented.
            Double-check your spelling, or submit an issue/PR"""
        )

    cost_per_token_key = (
        "input_cost_per_token" if token_type == "input" else "output_cost_per_token"
    )
    cost_per_token = TOKEN_COSTS[model][cost_per_token_key]

    return Decimal(str(cost_per_token)) * Decimal(num_tokens)


def calculate_prompt_cost(prompt: Union[List[dict], str], model: str) -> Decimal:
    """
    Calculate the prompt's cost in USD.

    Args:
        prompt (Union[List[dict], str]): List of message objects or single string prompt.
        model (str): The model name.

    Returns:
        Decimal: The calculated cost in USD.

    e.g.:
    >>> prompt = [{ "role": "user", "content": "Hello world"},
                  { "role": "assistant", "content": "How may I assist you today?"}]
    >>>calculate_prompt_cost(prompt, "gpt-3.5-turbo")
    Decimal('0.0000300')
    # or
    >>> prompt = "Hello world"
    >>> calculate_prompt_cost(prompt, "gpt-3.5-turbo")
    Decimal('0.0000030')
    """
    model = model.lower()
    model = strip_ft_model_name(model)
    if model not in TOKEN_COSTS:
        raise KeyError(
            f"""Model {model} is not implemented.
            Double-check your spelling, or submit an issue/PR"""
        )
    if not isinstance(prompt, (list, str)):
        raise TypeError(
            f"""Prompt must be either a string or list of message objects.
            it is {type(prompt)} instead.
            """
        )
    prompt_tokens = (
        count_string_tokens(prompt, model)
        if isinstance(prompt, str)
        else count_message_tokens(prompt, model)
    )

    return calculate_cost_by_tokens(prompt_tokens, model, "input")


def calculate_completion_cost(completion: str, model: str) -> Decimal:
    """
    Calculate the prompt's cost in USD.

    Args:
        completion (str): Completion string.
        model (str): The model name.

    Returns:
        Decimal: The calculated cost in USD.

    e.g.:
    >>> completion = "How may I assist you today?"
    >>> calculate_completion_cost(completion, "gpt-3.5-turbo")
    Decimal('0.000014')
    """
    model = strip_ft_model_name(model)
    if model not in TOKEN_COSTS:
        raise KeyError(
            f"""Model {model} is not implemented.
            Double-check your spelling, or submit an issue/PR"""
        )
    completion_tokens = count_string_tokens(completion, model)

    return calculate_cost_by_tokens(completion_tokens, model, "output")


def calculate_all_costs_and_tokens(
    prompt: Union[List[dict], str], completion: str, model: str
) -> dict:
    """
    Calculate the prompt and completion costs and tokens in USD.

    Args:
        prompt (Union[List[dict], str]): List of message objects or single string prompt.
        completion (str): Completion string.
        model (str): The model name.

    Returns:
        dict: The calculated cost and tokens in USD.

    e.g.:
    >>> prompt = "Hello world"
    >>> completion = "How may I assist you today?"
    >>> calculate_all_costs_and_tokens(prompt, completion, "gpt-3.5-turbo")
    {'prompt_cost': Decimal('0.0000030'), 'prompt_tokens': 2, 'completion_cost': Decimal('0.000014'), 'completion_tokens': 7}
    """
    prompt_cost = calculate_prompt_cost(prompt, model)
    completion_cost = calculate_completion_cost(completion, model)
    prompt_tokens = (
        count_string_tokens(prompt, model)
        if isinstance(prompt, str)
        else count_message_tokens(prompt, model)
    )
    completion_tokens = count_string_tokens(completion, model)

    return {
        "prompt_cost": prompt_cost,
        "prompt_tokens": prompt_tokens,
        "completion_cost": completion_cost,
        "completion_tokens": completion_tokens,
    }
