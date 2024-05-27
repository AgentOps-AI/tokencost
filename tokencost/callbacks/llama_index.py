from typing import Any, Dict, List, Optional, cast
from llama_index.core.callbacks.base_handler import BaseCallbackHandler
from llama_index.core.callbacks.schema import CBEventType, EventPayload
from llama_index.core.llms import ChatMessage
from tokencost import calculate_prompt_cost, calculate_completion_cost


class TokenCostHandler(BaseCallbackHandler):
    """Callback handler for printing llms inputs/outputs."""

    def __init__(self, model) -> None:
        super().__init__(event_starts_to_ignore=[], event_ends_to_ignore=[])
        self.model = model
        self.prompt_cost = 0
        self.completion_cost = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        return

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        return

    def _calc_llm_event_cost(self, payload: dict) -> None:
        if EventPayload.PROMPT in payload:
            prompt = str(payload.get(EventPayload.PROMPT))
            completion = str(payload.get(EventPayload.COMPLETION))
            prompt_cost, prompt_tokens = calculate_prompt_cost(prompt, self.model)
            completion_cost, completion_tokens = calculate_completion_cost(
                completion, self.model
            )

        elif EventPayload.MESSAGES in payload:
            messages = cast(List[ChatMessage], payload.get(EventPayload.MESSAGES, []))
            messages_str = "\n".join([str(x) for x in messages])
            prompt_cost, prompt_tokens = calculate_prompt_cost(messages_str, self.model)
            response = str(payload.get(EventPayload.RESPONSE))
            completion_cost, completion_tokens = calculate_completion_cost(
                response, self.model
            )

        self.prompt_cost += prompt_cost
        self.completion_cost += completion_cost
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens

    def reset_counts(self) -> None:
        self.prompt_cost = 0
        self.completion_cost = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        """Count the LLM or Embedding tokens as needed."""
        if event_type == CBEventType.LLM and payload is not None:
            self._calc_llm_event_cost(payload)
