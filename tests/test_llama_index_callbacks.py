# test_llama_index.py
import pytest
from tokencost.callbacks import llama_index
from llama_index.core.callbacks.schema import CBEventType, EventPayload
from unittest.mock import MagicMock

# Mock the calculate_prompt_cost and calculate_completion_cost functions

# 4 tokens
STRING = "Hello, world!"


# Mock the ChatMessage class in LlamaIndex
@pytest.fixture
def mock_chat_message(monkeypatch):
    class MockChatMessage:
        def __init__(self, text):
            self.text = text

        def __str__(self):
            return self.text

    monkeypatch.setattr("llama_index.core.llms.ChatMessage", MockChatMessage)
    return MockChatMessage


# Test the _calc_llm_event_cost method for prompt and completion


def test_calc_llm_event_cost_prompt_completion(capsys):
    handler = llama_index.TokenCostHandler(model="gpt-3.5-turbo")
    payload = {EventPayload.PROMPT: STRING, EventPayload.COMPLETION: STRING}
    handler._calc_llm_event_cost(payload)
    captured = capsys.readouterr()
    assert "# Prompt cost: 0.0000060" in captured.out
    assert "# Completion: 0.000008" in captured.out


# Test the _calc_llm_event_cost method for messages and response


def test_calc_llm_event_cost_messages_response(mock_chat_message, capsys):
    handler = llama_index.TokenCostHandler(model="gpt-3.5-turbo")
    payload = {
        EventPayload.MESSAGES: [
            mock_chat_message("message 1"),
            mock_chat_message("message 2"),
        ],
        EventPayload.RESPONSE: "test response",
    }
    handler._calc_llm_event_cost(payload)
    captured = capsys.readouterr()
    assert "# Prompt cost: 0.0000105" in captured.out
    assert "# Completion: 0.000004" in captured.out


# Additional tests can be written for start_trace, end_trace, on_event_start, and on_event_end
# depending on the specific logic and requirements of those methods.
