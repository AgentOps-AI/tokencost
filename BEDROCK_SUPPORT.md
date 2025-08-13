# AWS Bedrock Model Support for tokencost

## Problem Solved
Users integrating AgentOps with AWS Bedrock were unable to track costs for their LLM usage. The model identifier `bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0` was not recognized by the tokencost library, resulting in warnings like "Unable to calculate cost - This might be because you're using an unrecognized model."

## Solution Implemented

### 1. Added Model Name Normalization
Created a new function `normalize_bedrock_model_name()` in `/workspace/tokencost/costs.py` that:
- Strips the `bedrock/` prefix from model names
- Maps Bedrock model identifiers to their corresponding entries in the model prices dictionary

### 2. Updated Cost Calculation Functions
Modified the following functions to use the normalization:
- `calculate_cost_by_tokens()`
- `calculate_prompt_cost()`
- `calculate_completion_cost()`
- `count_message_tokens()`
- `count_string_tokens()`

### 3. Added Explicit Bedrock Model Entries
Added explicit entries in `/workspace/tokencost/model_prices.json` for:
- `bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0`
- `bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0`

These entries have the correct pricing:
- Input tokens: $3.00 per 1M tokens (3e-06 per token)
- Output tokens: $15.00 per 1M tokens (1.5e-05 per token)
- Cached input tokens (v2 only): $0.30 per 1M tokens (3e-07 per token)

### 4. Added Comprehensive Tests
Created test suite in `/workspace/tests/test_bedrock_models.py` that verifies:
- Cost calculation for Bedrock models with `bedrock/` prefix
- Cost calculation for models without the prefix
- Case-insensitive model name handling
- Cached token cost calculation
- Proper error handling for invalid models

## Supported Model Formats

The following AWS Bedrock model formats are now supported:

### Claude 3.5 Sonnet Models
- `bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0`
- `bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0`
- `anthropic.claude-3-5-sonnet-20240620-v1:0` (without prefix)
- `anthropic.claude-3-5-sonnet-20241022-v2:0` (without prefix)

### Other Bedrock Models
The normalization function will automatically handle any model with the `bedrock/` prefix by stripping it and looking up the base model name in the prices dictionary.

## Usage Example

```python
from tokencost import calculate_cost_by_tokens

# Works with bedrock/ prefix
model = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
input_cost = calculate_cost_by_tokens(1000, model, "input")  # Returns $0.003
output_cost = calculate_cost_by_tokens(1000, model, "output")  # Returns $0.015

# Also works without prefix
model = "anthropic.claude-3-5-sonnet-20240620-v1:0"
input_cost = calculate_cost_by_tokens(1000, model, "input")  # Returns $0.003
```

## Impact

This fix enables:
- Cost tracking for AWS Bedrock users in AgentOps
- Budget management for production deployments using AWS Bedrock
- Support for CrewAI applications using AWS Bedrock LLM integration
- Compatibility with any framework using Bedrock model identifiers

## Testing

Run the test suite to verify the implementation:

```bash
python3 -m pytest tests/test_bedrock_models.py -v
```

All tests should pass, confirming that AWS Bedrock models are now properly supported for cost calculation.