import os
import json
import aiohttp
import asyncio
import logging
from decimal import Decimal
from typing import Dict
from forex_python.converter import CurrencyRates

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
    timeout = aiohttp.ClientTimeout(total=10)  # 10 seconds timeout
    async with aiohttp.ClientSession(trust_env=True, timeout=timeout) as session:
        async with session.get(PRICES_URL) as response:
            if response.status == 200:
                return await response.json(content_type=None)
            else:
                raise Exception(
                    f"Failed to fetch token costs, status code: {response.status}"
                )


async def update_token_costs():
    """Update the TOKEN_COSTS dictionary with the latest costs from the LiteLLM cost tracker asynchronously."""
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


class CurrencyConverter:
    """Handles currency conversion with caching for exchange rates."""

    def __init__(self):
        self._rate_cache: Dict[str, Decimal] = {}
        self._converter = CurrencyRates(force_decimal=True)
        self.supported_currencies = ["USD", "EUR"]

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Decimal:
        """
        Get exchange rate from one currency to another with caching.

        Args:
            from_currency (str): Source currency code (e.g., "USD")
            to_currency (str): Target currency code (e.g., "EUR")

        Returns:
            Decimal: Exchange rate as a decimal

        Raises:
            ValueError: If currency is not supported
        """
        if from_currency == to_currency:
            return Decimal("1.0")

        if from_currency not in self.supported_currencies:
            raise ValueError(f"Unsupported source currency: {from_currency}")
        if to_currency not in self.supported_currencies:
            raise ValueError(f"Unsupported target currency: {to_currency}")

        cache_key = f"{from_currency}_{to_currency}"

        if cache_key in self._rate_cache:
            return self._rate_cache[cache_key]

        try:
            rate = self._converter.get_rate(from_currency, to_currency)
            if rate is None:
                raise ValueError("Exchange rate not available")

            rate_decimal = Decimal(str(rate))
            self._rate_cache[cache_key] = rate_decimal
            return rate_decimal

        except Exception as e:
            logger.error(f"Failed to get exchange rate from {from_currency} to {to_currency}: {e}")
            if to_currency == "USD":
                return Decimal("1.0")
            raise ValueError(f"Currency conversion failed: {e}")

    def convert_amount(self, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        """
        Convert an amount from one currency to another.

        Args:
            amount (Decimal): Amount to convert
            from_currency (str): Source currency code
            to_currency (str): Target currency code

        Returns:
            Decimal: Converted amount
        """
        if from_currency == to_currency:
            return amount

        rate = self.get_exchange_rate(from_currency, to_currency)
        return amount * rate

    def clear_cache(self):
        """Clear the exchange rate cache."""
        self._rate_cache.clear()


# Global currency converter instance
_currency_converter = CurrencyConverter()


def convert_usd_to_currency(usd_amount: Decimal, target_currency: str) -> Decimal:
    """
    Convert USD amount to target currency.

    Args:
        usd_amount (Decimal): Amount in USD
        target_currency (str): Target currency code (e.g., "EUR")

    Returns:
        Decimal: Converted amount in target currency
    """
    return _currency_converter.convert_amount(usd_amount, "USD", target_currency)


def get_supported_currencies() -> list:
    """Get list of supported currencies for cost calculations."""
    return _currency_converter.supported_currencies.copy()


# Only run in a non-async context
if __name__ == "__main__":
    try:
        asyncio.run(update_token_costs())
        print("Token costs updated successfully")
    except Exception:
        logger.error("Failed to update token costs. Using static costs.")
