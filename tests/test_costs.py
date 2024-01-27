#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tokencost.costs import (
    count_message_tokens,
    count_string_tokens,
    calculate_prompt_cost,
    calculate_completion_cost,
)

# 15 tokens
MESSAGES = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
]

MESSAGES_WITH_NAME = [
    {"role": "user", "content": "Hello", "name": "John"},
    {"role": "assistant", "content": "Hi there!"},
]

# 4 tokens
STRING = "Hello, world!"


# Chat models only, no embeddings (such as ada) since embeddings only does strings, not messages
@pytest.mark.parametrize(
    "model,expected_output",
    [
        ("gpt-3.5-turbo", 150),
        ("gpt-3.5-turbo-0301", 170),
        ("gpt-3.5-turbo-0613", 150),
        ("gpt-3.5-turbo-16k", 150),
        ("gpt-3.5-turbo-16k-0613", 150),
        ("gpt-3.5-turbo-1106", 150),
        ("gpt-3.5-turbo-instruct", 150),
        ("gpt-4", 150),
        ("gpt-4-0314", 150),
        ("gpt-4-0613", 150),
        ("gpt-4-32k", 150),
        ("gpt-4-32k-0314", 150),
        ("gpt-4-1106-preview", 150),
        ("gpt-4-vision-preview", 150),
    ],
)
def test_count_message_tokens(model, expected_output):
    print(model)
    assert count_message_tokens(MESSAGES, model) == expected_output


# Chat models only, no embeddings
@pytest.mark.parametrize(
    "model,expected_output",
    [
        ("gpt-3.5-turbo", 17),
        ("gpt-3.5-turbo-0301", 17),
        ("gpt-3.5-turbo-0613", 17),
        ("gpt-3.5-turbo-1106", 17),
        ("gpt-3.5-turbo-instruct", 17),
        ("gpt-3.5-turbo-16k", 17),
        ("gpt-3.5-turbo-16k-0613", 17),
        ("gpt-4", 17),
        ("gpt-4-0314", 17),
        ("gpt-4-0613", 17),
        ("gpt-4-32k", 17),
        ("gpt-4-32k-0314", 17),
        ("gpt-4-1106-preview", 17),
        ("gpt-4-vision-preview", 17),
    ],
)
def test_count_message_tokens_with_name(model, expected_output):
    """Notice: name 'John' appears"""

    assert count_message_tokens(MESSAGES_WITH_NAME, model) == expected_output


def test_count_message_tokens_empty_input():
    """Empty input should raise a KeyError"""
    with pytest.raises(KeyError):
        count_message_tokens("", "")


def test_count_message_tokens_invalid_model():
    """Invalid model should raise a KeyError"""

    with pytest.raises(KeyError):
        count_message_tokens(MESSAGES, model="invalid_model")


@pytest.mark.parametrize(
    "model,expected_output",
    [
        ("gpt-3.5-turbo", 40),
        ("gpt-3.5-turbo-0301", 40),
        ("gpt-3.5-turbo-0613", 40),
        ("gpt-3.5-turbo-16k", 40),
        ("gpt-3.5-turbo-16k-0613", 40),
        ("gpt-3.5-turbo-1106", 40),
        ("gpt-3.5-turbo-instruct", 40),
        ("gpt-4-0314", 40),
        ("gpt-4", 40),
        ("gpt-4-32k", 40),
        ("gpt-4-32k-0314", 40),
        ("gpt-4-0613", 40),
        ("gpt-4-1106-preview", 40),
        ("gpt-4-vision-preview", 40),
        ("text-embedding-ada-002", 40),
    ],
)
def test_count_string_tokens(model, expected_output):
    """Test that the string tokens are counted correctly."""

    # 4 tokens
    assert count_string_tokens(STRING, model=model) == expected_output

    # empty string
    assert count_string_tokens("", model=model) == 0


def test_count_string_invalid_model():
    """Test that the string tokens are counted correctly."""

    assert count_string_tokens(STRING, model="invalid model") == 4


# Costs from https://openai.com/pricing
# https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
@pytest.mark.parametrize(
    "prompt,model,expected_output",
    [
        (MESSAGES, "gpt-3.5-turbo", 2250),
        (MESSAGES, "gpt-3.5-turbo-0301", 2550),
        (MESSAGES, "gpt-3.5-turbo-0613", 2250),
        (MESSAGES, "gpt-3.5-turbo-16k", 4500),
        (MESSAGES, "gpt-3.5-turbo-16k-0613", 4500),
        (MESSAGES, "gpt-3.5-turbo-1106", 1500),
        (MESSAGES, "gpt-3.5-turbo-instruct", 2250),
        (MESSAGES, "gpt-4", 45000),
        (MESSAGES, "gpt-4-0314", 45000),
        (MESSAGES, "gpt-4-32k", 90000),
        (MESSAGES, "gpt-4-32k-0314", 90000),
        (MESSAGES, "gpt-4-0613", 45000),
        (MESSAGES, "gpt-4-1106-preview", 15000),
        (MESSAGES, "gpt-4-vision-preview", 15000),
        (STRING, "text-embedding-ada-002", 40),
    ],
)
def test_calculate_prompt_cost(prompt, model, expected_output):
    """Test that the cost calculation is correct."""

    cost = calculate_prompt_cost(prompt, model)
    assert cost == expected_output


def test_invalid_prompt_format():
    with pytest.raises(TypeError):
        calculate_prompt_cost(
            {"role": "user", "content": "invalid message type"}, model="gpt-3.5-turbo"
        )


@pytest.mark.parametrize(
    "prompt,model,expected_output",
    [
        (STRING, "gpt-3.5-turbo", 800),
        (STRING, "gpt-3.5-turbo-0301", 800),
        (STRING, "gpt-3.5-turbo-0613", 800),
        (STRING, "gpt-3.5-turbo-16k", 1600),
        (STRING, "gpt-3.5-turbo-16k-0613", 1600),
        (STRING, "gpt-3.5-turbo-1106", 800),
        (STRING, "gpt-3.5-turbo-instruct", 800),
        (STRING, "gpt-4", 24000),
        (STRING, "gpt-4-0314", 24000),
        (STRING, "gpt-4-32k", 48000),
        (STRING, "gpt-4-32k-0314", 48000),
        (STRING, "gpt-4-0613", 24000),
        (STRING, "gpt-4-1106-preview", 12000),
        (STRING, "gpt-4-vision-preview", 12000),
        (STRING, "text-embedding-ada-002", 0),
    ],
)
def test_calculate_completion_cost(prompt, model, expected_output):
    """Test that the completion cost calculation is correct."""

    cost = calculate_completion_cost(prompt, model)
    assert cost == expected_output


def test_calculate_cost_invalid_model():
    """Invalid model should raise a KeyError"""

    with pytest.raises(KeyError):
        calculate_prompt_cost(STRING, model="invalid_model")


def test_calculate_invalid_input_types():
    """Invalid input type should raise a KeyError"""

    with pytest.raises(KeyError):
        calculate_prompt_cost(STRING, model="invalid_model")

    with pytest.raises(KeyError):
        calculate_completion_cost(STRING, model="invalid_model")

    with pytest.raises(KeyError):
        # Message objects not allowed, must be list of message objects.
        calculate_prompt_cost(MESSAGES[0], model="invalid_model")
