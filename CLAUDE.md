# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TokenCost is a Python package that calculates USD costs for Large Language Model (LLM) API usage by estimating token counts and applying current pricing. It's designed for AI developers building agents and applications that need to track LLM costs across providers like OpenAI and Anthropic.

## Development Commands

### Installation and Setup
```bash
pip install -e .[dev]  # Install in development mode with dev dependencies
```

### Testing
```bash
# Run tests with coverage
python -m pytest tests/
coverage run --source tokencost -m pytest
coverage report -m

# Using tox (recommended)
tox  # Run tests and linting across environments
```

### Code Quality
```bash
# Linting
flake8 tokencost/
tox -e flake8

# Dependency validation
tach check  # Validate module dependencies according to tach.yml
```

### Price Updates
```bash
python update_prices.py  # Update model pricing data from LiteLLM
```

## Architecture

### Core Modules

- **`tokencost/costs.py`** - Main cost calculation and token counting logic
- **`tokencost/constants.py`** - Price data management and fetching utilities  
- **`tokencost/model_prices.json`** - Static pricing data for all supported models

### Key APIs

The main package exports these functions from `tokencost/__init__.py`:
- `count_message_tokens()` - Count tokens in ChatML message format
- `count_string_tokens()` - Count tokens in raw strings
- `calculate_prompt_cost()` - Calculate cost for input prompts
- `calculate_completion_cost()` - Calculate cost for model completions
- `calculate_all_costs_and_tokens()` - Comprehensive cost and token analysis

### Token Counting Strategy

- **OpenAI models**: Uses tiktoken (official tokenizer)
- **Anthropic models v3+**: Uses Anthropic's beta token counting API
- **Older Anthropic models**: Approximates with tiktoken cl100k_base encoding

### Module Dependencies

Following the `tach.yml` configuration:
- `tokencost` depends on `tokencost.constants` and `tokencost.costs`
- `tokencost.costs` depends on `tokencost.constants`
- `update_prices` depends on `tokencost`

## Development Notes

### Price Data Management
- Pricing data is automatically updated daily via GitHub Actions
- Updates pull from LiteLLM's cost tracker at `https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json`
- Manual updates can be triggered with `python update_prices.py`

### Testing
- Tests are in `tests/test_costs.py`
- Focus on cost calculation accuracy and token counting precision
- Coverage reporting is enabled and should be maintained

### Code Standards
- Maximum line length: 120 characters (flake8 configuration)
- Python 3.10+ required
- Import organization follows flake8 rules with F401 exceptions in `__init__.py`

### Package Distribution
- Uses modern `pyproject.toml` configuration
- `model_prices.json` is included in distribution via `MANIFEST.in`
- Published to PyPI as `tokencost`