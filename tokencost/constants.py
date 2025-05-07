import os
import json
import aiohttp
import asyncio
import logging

logger = logging.getLogger(__name__)

"""
Prompt (aka context) tokens are based on number of words + other chars (eg spaces and punctuation) in input.
Completion tokens are similarly based on how long chatGPT's response is.
Prompt tokens + completion tokens = total tokens.
The max total limit is typically 1 more than the prompt token limit, so there's space for at least one completion token.

You can use ChatGPT's webapp (which uses their tiktoken repo) to see how many tokens your phrase is:
https://platform.openai.com/tokenizer

Note: When asking follow-up questions, everything above and including your follow-up question
is considered a prompt (for the purpose of context) and will thus cost prompt tokens.
"""

# How to read TOKEN_COSTS:
# Each prompt token costs __ USD per token.
# Each completion token costs __ USD per token.
# Max prompt limit of each model is __ tokens.

PRICES_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"


async def fetch_costs():
    """Fetch the latest token costs from the LiteLLM cost tracker asynchronously.
    Returns:
        dict: The token costs for each model.
    Raises:
        Exception: If the request fails.
    """
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(PRICES_URL) as response:
            if response.status == 200:
                return await response.json(content_type=None)
            else:
                raise Exception(
                    f"Failed to fetch token costs, status code: {response.status}"
                )


async def update_token_costs():
    """Update the TOKEN_COSTS dictionary with the latest costs from the LiteLLM cost tracker asynchronously."""
    global TOKEN_COSTS
    try:
        fetched_costs = await fetch_costs()
        # Safely remove 'sample_spec' if it exists
        TOKEN_COSTS.update(fetched_costs)
        TOKEN_COSTS.pop("sample_spec", None)
        return TOKEN_COSTS
    except Exception as e:
        logger.error(f"Failed to update TOKEN_COSTS: {e}")
        raise


def refresh_prices(write_file=True):
    """Synchronous wrapper for update_token_costs that optionally writes to model_prices.json."""
    try:
        # Run the async function in a new event loop
        updated_costs = asyncio.run(update_token_costs())
        
        # Write to file if requested
        if write_file:
            file_path = os.path.join(os.path.dirname(__file__), "model_prices.json")
            with open(file_path, "w") as f:
                json.dump(TOKEN_COSTS, f, indent=4)
            logger.info(f"Updated prices written to {file_path}")
            
        return updated_costs
    except Exception as e:
        logger.error(f"Failed to refresh prices: {e}")
        # Return the static prices as fallback
        return TOKEN_COSTS


with open(os.path.join(os.path.dirname(__file__), "model_prices.json"), "r") as f:
    TOKEN_COSTS_STATIC = json.load(f)


# Set initial TOKEN_COSTS to the static values
TOKEN_COSTS = TOKEN_COSTS_STATIC.copy()

# Only run in a non-async context
if __name__ == "__main__":
    try:
        asyncio.run(update_token_costs())
        print("Token costs updated successfully")
    except Exception:
        logger.error("Failed to update token costs. Using static costs.")
