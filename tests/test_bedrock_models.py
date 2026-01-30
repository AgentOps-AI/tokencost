"""
Test AWS Bedrock model support in tokencost
"""

import pytest
from decimal import Decimal
from tokencost import calculate_cost_by_tokens, calculate_prompt_cost, calculate_completion_cost


class TestBedrockModels:
    """Test that AWS Bedrock model names are properly handled."""
    
    def test_bedrock_claude_35_sonnet_v1_cost_calculation(self):
        """Test cost calculation for bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"""
        model = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        # Test input token cost: $3.00 per 1M tokens = 3e-06 per token
        input_cost = calculate_cost_by_tokens(1000, model, "input")
        assert input_cost == Decimal("0.003")
        
        # Test output token cost: $15.00 per 1M tokens = 1.5e-05 per token
        output_cost = calculate_cost_by_tokens(1000, model, "output")
        assert output_cost == Decimal("0.015")
    
    def test_bedrock_claude_35_sonnet_v2_cost_calculation(self):
        """Test cost calculation for bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"""
        model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
        
        # Test input token cost
        input_cost = calculate_cost_by_tokens(1000, model, "input")
        assert input_cost == Decimal("0.003")
        
        # Test output token cost
        output_cost = calculate_cost_by_tokens(1000, model, "output")
        assert output_cost == Decimal("0.015")
    
    def test_bedrock_model_without_prefix(self):
        """Test that models without bedrock/ prefix still work"""
        model = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        # Should work the same way
        input_cost = calculate_cost_by_tokens(1000, model, "input")
        assert input_cost == Decimal("0.003")
        
        output_cost = calculate_cost_by_tokens(1000, model, "output")
        assert output_cost == Decimal("0.015")
    
    def test_bedrock_model_case_insensitive(self):
        """Test that model names are case-insensitive"""
        model_upper = "BEDROCK/ANTHROPIC.CLAUDE-3-5-SONNET-20240620-V1:0"
        model_mixed = "Bedrock/Anthropic.Claude-3-5-Sonnet-20240620-v1:0"
        
        # Both should work
        input_cost_upper = calculate_cost_by_tokens(1000, model_upper, "input")
        input_cost_mixed = calculate_cost_by_tokens(1000, model_mixed, "input")
        
        assert input_cost_upper == Decimal("0.003")
        assert input_cost_mixed == Decimal("0.003")
    
    def test_bedrock_prompt_cost_calculation(self):
        """Test calculate_prompt_cost with Bedrock model"""
        model = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        # Note: For Claude models, this will require anthropic API key
        # So we test with a simple prompt that would work with tiktoken fallback
        # The actual token counting for Claude requires the anthropic library
        try:
            # This might fail without proper Anthropic API key
            prompt = "Hello, world!"
            cost = calculate_prompt_cost(prompt, model)
            # Just verify it returns a Decimal, actual value depends on tokenization
            assert isinstance(cost, Decimal)
        except Exception as e:
            # Expected if Anthropic API key is not set
            if "ANTHROPIC_API_KEY" in str(e) or "API" in str(e):
                pytest.skip("Anthropic API key not available for testing")
            else:
                raise
    
    def test_bedrock_completion_cost_calculation(self):
        """Test calculate_completion_cost with Bedrock model"""
        model = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        try:
            completion = "This is a test completion."
            cost = calculate_completion_cost(completion, model)
            # Just verify it returns a Decimal
            assert isinstance(cost, Decimal)
        except Exception as e:
            # Expected if Anthropic API key is not set
            if "ANTHROPIC_API_KEY" in str(e) or "API" in str(e):
                pytest.skip("Anthropic API key not available for testing")
            else:
                raise
    
    def test_bedrock_cached_token_cost(self):
        """Test cached token cost calculation for Bedrock Claude 3.5 Sonnet v2"""
        model = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"
        
        # Test cached input token cost: 3e-07 per token
        cached_cost = calculate_cost_by_tokens(1000, model, "cached")
        assert cached_cost == Decimal("0.0003")
    
    def test_invalid_bedrock_model(self):
        """Test that invalid Bedrock model names raise appropriate errors"""
        model = "bedrock/invalid-model-name"
        
        with pytest.raises(KeyError) as exc_info:
            calculate_cost_by_tokens(1000, model, "input")
        
        assert "not implemented" in str(exc_info.value).lower()