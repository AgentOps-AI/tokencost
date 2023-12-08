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

@pytest.mark.parametrize("model,expected_output", [
    ("gpt-3.5-turbo", 15),
    ("gpt-3.5-turbo-0301", 17),
    ("gpt-3.5-turbo-0613", 15),
    ("gpt-3.5-turbo-16k", 15),
    ("gpt-3.5-turbo-16k-0613", 15),
    ("gpt-4-0314", 15),
    ("gpt-4", 15),
    ("gpt-4-32k", 15),
    ("gpt-4-32k-0314", 15),
    ("gpt-4-0613", 15),
    # ("text-embedding-ada-002", 27),
])
def test_count_message_tokens(model, expected_output):
    print(model)
    assert count_message_tokens(MESSAGES, model) == expected_output


# Chat models only, no embeddings
@pytest.mark.parametrize("model,expected_output", [
    ("gpt-3.5-turbo", 17),
    ("gpt-3.5-turbo-0301", 17),
    ("gpt-3.5-turbo-0613", 17),
    ("gpt-3.5-turbo-16k", 17),
    ("gpt-3.5-turbo-16k-0613", 17),
    ("gpt-4-0314", 17),
    ("gpt-4", 17),
    ("gpt-4-32k", 17),
    ("gpt-4-32k-0314", 17),
    ("gpt-4-0613", 17)
])
def test_count_message_tokens_with_name(model, expected_output):
    """Notice: name 'John' appears"""

    assert count_message_tokens(MESSAGES_WITH_NAME, model) == expected_output


def test_count_message_tokens_empty_input():
    """Empty input should raise a NotImplementedError"""
    with pytest.raises(NotImplementedError):
        count_message_tokens("", "")


def test_count_message_tokens_invalid_model():
    """Invalid model should raise a KeyError"""

    with pytest.raises(NotImplementedError):
        count_message_tokens(MESSAGES, model="invalid_model")


@pytest.mark.parametrize("model,expected_output", [
    ("gpt-3.5-turbo", 4),
    ("gpt-3.5-turbo-0301", 4),
    ("gpt-3.5-turbo-0613", 4),
    ("gpt-3.5-turbo-16k", 4),
    ("gpt-3.5-turbo-16k-0613", 4),
    ("gpt-4-0314", 4),
    ("gpt-4", 4),
    ("gpt-4-32k", 4),
    ("gpt-4-32k-0314", 4),
    ("gpt-4-0613", 4),
])
def test_count_string_tokens(model, expected_output):
    """Test that the string tokens are counted correctly."""

    string = "Hello, world!"
    assert count_string_tokens(string, model_name=model) == expected_output


def test_count_string_tokens_empty_input():
    """Test that the string tokens are counted correctly."""

    assert count_string_tokens("", model_name="gpt-3.5-turbo-0301") == 0


@pytest.mark.parametrize("model,expected_output", [
    ("gpt-3.5-turbo", 4),
    ("gpt-3.5-turbo-0301", 4),
    ("gpt-3.5-turbo-0613", 4),
    ("gpt-3.5-turbo-16k", 4),
    ("gpt-3.5-turbo-16k-0613", 4),
    ("gpt-4-0314", 4),
    ("gpt-4", 4),
    ("gpt-4-32k", 4),
    ("gpt-4-32k-0314", 4),
    ("gpt-4-0613", 4),
    ("text-embedding-ada-002", 4),
])
def test_count_string_tokens_gpt_4(model, expected_output):
    """Test that the string tokens are counted correctly."""

    string = "Hello, world!"
    assert count_string_tokens(string, model_name=model) == expected_output


# Costs from https://openai.com/pricing
# https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
@pytest.mark.parametrize("model,expected_output", [
    ("gpt-3.5-turbo", 7500),
    ("gpt-3.5-turbo-0301", 7500),
    ("gpt-3.5-turbo-0613", 7500),
    ("gpt-3.5-turbo-16k", 15000),
    ("gpt-3.5-turbo-16k-0613", 15000),
    ("gpt-4-0314", 180000),
    ("gpt-4", 180000),
    ("gpt-4-32k", 360000),
    ("gpt-4-32k-0314", 360000),
    ("gpt-4-0613", 180000),
    ("text-embedding-ada-002", 300),
])
def test_calculate_cost(model, expected_output):
    """Test that the cost calculation is correct."""

    prompt_tokens = count_string_tokens('hello world!'*100,  # 300 tokens
                                        model)
    assert prompt_tokens == 300
    completion_tokens = count_string_tokens('hello world!'*50,  # 150 tokens
                                            model)

    assert completion_tokens == 150

    cost = calculate_cost(prompt_tokens,
                          completion_tokens,
                          model)
    assert cost == expected_output

    assert calculate_cost(900, 754, 'gpt-4') == 722400
