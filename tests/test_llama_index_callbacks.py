# test_llama_index.py
import pytest
from tokencost.callbacks import llama_index
from llama_index.callbacks.schema import CBEventType, EventPayload
from unittest.mock import MagicMock

# Mock the calculate_prompt_cost and calculate_completion_cost functions
# and the USD_PER_TPU constant

STRING = "Hello, world!"


@pytest.fixture
def mock_tokencost(monkeypatch):
    monkeypatch.setattr('tokencost.calculate_prompt_cost', MagicMock(return_value=100))
    monkeypatch.setattr('tokencost.calculate_completion_cost', MagicMock(return_value=200))
    monkeypatch.setattr('tokencost.USD_PER_TPU', 10)

# Mock the ChatMessage class


@pytest.fixture
def mock_chat_message(monkeypatch):
    class MockChatMessage:
        def __init__(self, text):
            self.text = text

        def __str__(self):
            return self.text

    monkeypatch.setattr('llama_index.llms.ChatMessage', MockChatMessage)
    return MockChatMessage

# Test the _calc_llm_event_cost method for prompt and completion


def test_calc_llm_event_cost_prompt_completion(mock_tokencost, capsys):
    handler = llama_index.TokenCostHandler(model='gpt-3.5-turbo')
    payload = {
        EventPayload.PROMPT: STRING,
        EventPayload.COMPLETION: STRING
    }
    handler._calc_llm_event_cost(payload)
    captured = capsys.readouterr()
    assert "# Prompt cost: 6e-06" in captured.out
    assert "# Completion: 8e-06" in captured.out

# Test the _calc_llm_event_cost method for messages and response


def test_calc_llm_event_cost_messages_response(mock_tokencost, mock_chat_message, capsys):
    handler = llama_index.TokenCostHandler(model='gpt-3.5-turbo')
    payload = {
        EventPayload.MESSAGES: [mock_chat_message("message 1"), mock_chat_message("message 2")],
        EventPayload.RESPONSE: "test response"
    }
    handler._calc_llm_event_cost(payload)
    captured = capsys.readouterr()
    assert "# Prompt cost: 1.05e-05" in captured.out
    assert "# Completion: 4e-06" in captured.out

# Additional tests can be written for start_trace, end_trace, on_event_start, and on_event_end
# depending on the specific logic and requirements of those methods.
