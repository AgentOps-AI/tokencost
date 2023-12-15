#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tokencost.costs import count_message_tokens, count_string_tokens, calculate_cost

MESSAGES = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
]

MESSAGES_WITH_NAME = [
    {"role": "user", "content": "Hello", "name": "John"},
    {"role": "assistant", "content": "Hi there!"},
]

STRING = "Hello, world!"

# Chat models only, no embeddings (such as ada) since embeddings only does strings, not messages
@pytest.mark.parametrize("model,expected_output", [
    ("gpt-3.5-turbo", 15),
    ("gpt-3.5-turbo-0301", 17),
    ("gpt-3.5-turbo-0613", 15),
    ("gpt-3.5-turbo-16k", 15),
    ("gpt-3.5-turbo-16k-0613", 15),
    ("gpt-3.5-turbo-1106", 15),
    ("gpt-3.5-turbo-instruct", 15),
    ("gpt-4", 15),
    ("gpt-4-0314", 15),
    ("gpt-4-0613", 15),
    ("gpt-4-32k", 15),
    ("gpt-4-32k-0314", 15),
    ("gpt-4-1106-preview", 15),
    ("gpt-4-vision-preview", 15),
])
def test_count_message_tokens(model, expected_output):
    print(model)
    assert count_message_tokens(MESSAGES, model) == expected_output


# Chat models only, no embeddings
@pytest.mark.parametrize("model,expected_output", [
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
])
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


@pytest.mark.parametrize("model,expected_output", [
    ("gpt-3.5-turbo", 4),
    ("gpt-3.5-turbo-0301", 4),
    ("gpt-3.5-turbo-0613", 4),
    ("gpt-3.5-turbo-16k", 4),
    ("gpt-3.5-turbo-16k-0613", 4),
    ("gpt-3.5-turbo-1106", 4),
    ("gpt-3.5-turbo-instruct", 4),
    ("gpt-4-0314", 4),
    ("gpt-4", 4),
    ("gpt-4-32k", 4),
    ("gpt-4-32k-0314", 4),
    ("gpt-4-0613", 4),
    ("gpt-4-1106-preview", 4),
    ("gpt-4-vision-preview", 4),
    ("text-embedding-ada-002", 4),
])
def test_count_string_tokens(model, expected_output):
    """Test that the string tokens are counted correctly."""

    string = "Hello, world!"
    assert count_string_tokens(string, model=model) == expected_output

    string = ""
    assert count_string_tokens(string, model=model) == 0


def test_count_string_tokens_invalid_model():
    """Invalid model should raise a KeyError"""

    with pytest.raises(KeyError):
        count_string_tokens(MESSAGES, model="invalid_model")


# Costs from https://openai.com/pricing
# https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
@pytest.mark.parametrize("prompt,completion,model,expected_output", [
    (STRING, MESSAGES, "gpt-3.5-turbo", 360),
    (STRING, STRING, "gpt-3.5-turbo", 140),
    (MESSAGES, STRING, "gpt-3.5-turbo", 305),
    (MESSAGES, MESSAGES, "gpt-3.5-turbo", 525),
    ([MESSAGES[0]], "", "gpt-3.5-turbo", 120),
    (STRING, STRING, "gpt-3.5-turbo-0301", 140),
    (STRING, STRING, "gpt-3.5-turbo-0613", 140),
    (STRING, STRING, "gpt-3.5-turbo-16k", 280),
    (STRING, STRING, "gpt-3.5-turbo-16k-0613", 280),
    (STRING, STRING, "gpt-3.5-turbo-1106", 120),
    (STRING, STRING, "gpt-3.5-turbo-instruct", 140),
    (STRING, STRING, "gpt-4", 3600),
    (STRING, STRING, "gpt-4-0314", 3600),
    (STRING, STRING, "gpt-4-32k", 7200),
    (STRING, STRING, "gpt-4-32k-0314", 7200),
    (STRING, STRING, "gpt-4-0613", 3600),
    (STRING, STRING, "gpt-4-1106-preview", 1600),
    (STRING, STRING, "gpt-4-vision-preview", 1600),
    (STRING, STRING, "text-embedding-ada-002", 4),
])
def test_calculate_cost(prompt, completion, model, expected_output):
    """Test that the cost calculation is correct."""

    cost = calculate_cost(prompt,
                          completion,
                          model)
    assert cost == expected_output


def test_calculate_cost_invalid_model():
    """Invalid model should raise a KeyError"""

    with pytest.raises(KeyError):
        calculate_cost(STRING, STRING, model="invalid_model")

def test_calculate_cost_invalid_input_types():
    """Invalid input type should raise a KeyError"""

    with pytest.raises(KeyError):
        calculate_cost(5, STRING, model="invalid_model")

    with pytest.raises(KeyError):
        calculate_cost(STRING, 5, model="invalid_model")

    with pytest.raises(KeyError):
        calculate_cost(MESSAGES[0], 5, model="invalid_model") # Message objects not allowed, must be list of message objects.
