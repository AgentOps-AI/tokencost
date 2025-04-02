from typing import TypedDict
from decimal import Decimal


class CostAndTokenInfo(TypedDict):
    """
    TypedDict representing the cost and token information for a prompt and completion.
    
    Attributes:
        prompt_cost (Decimal): The cost of the prompt in USD.
        prompt_tokens (int): The number of tokens in the prompt.
        completion_cost (Decimal): The cost of the completion in USD.
        completion_tokens (int): The number of tokens in the completion.
    """
    prompt_cost: Decimal
    prompt_tokens: int
    completion_cost: Decimal
    completion_tokens: int 