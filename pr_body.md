## Model Price Updates for 06-12-2024

### Changes Summary
```diff
diff --git a/pricing_table.md b/pricing_table.md
index 29a3f98..8d09b3d 100644
--- a/pricing_table.md
+++ b/pricing_table.md
@@ -694,4 +694,12 @@
 | us.meta.llama3-1-70b-instruct-v1:0                                    | $0.99                             | $0.99                                 | 128,000             |                2048 |
 | us.meta.llama3-1-405b-instruct-v1:0                                   | $5.32                             | $16.00                                | 128,000             |                4096 |
 | stability.stable-image-ultra-v1:0                                     | --                                | --                                    | 77                  |                 nan |
-| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-32b-instruct     | $0.9                              | $0.9                                  | 4,096               |                4096 |
\ No newline at end of file
+| fireworks_ai/accounts/fireworks/models/qwen2p5-coder-32b-instruct     | $0.9                              | $0.9                                  | 4,096               |                4096 |
+| gemini/gemini-1.5-flash-8b                                            | $ 0.00                            | $ 0.00                                | 1,048,576           |                8192 |
+| rerank-v3.5                                                           | $ 0.00                            | $ 0.00                                | 4,096               |                4096 |
+| amazon.nova-micro-v1:0                                                | $0.035                            | $0.14                                 | 300,000             |                4096 |
+| amazon.nova-lite-v1:0                                                 | $0.06                             | $0.24                                 | 128,000             |                4096 |
+| amazon.nova-pro-v1:0                                                  | $0.8                              | $3.2                                  | 300,000             |                4096 |
+| together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo               | $0.18                             | $0.18                                 | nan                 |                 nan |
+| together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo              | $0.88                             | $0.88                                 | nan                 |                 nan |
+| together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo             | $3.5                              | $3.5                                  | nan                 |                 nan |
\ No newline at end of file
diff --git a/tokencost/model_prices.json b/tokencost/model_prices.json
index efeabdc..667f8d7 100644
--- a/tokencost/model_prices.json
+++ b/tokencost/model_prices.json
@@ -713,7 +713,8 @@
         "supports_function_calling": true,
         "supports_parallel_function_calling": true,
         "supports_response_schema": true,
-        "supports_vision": true
+        "supports_vision": true,
+        "supports_prompt_caching": true
     },
     "azure/gpt-4o-2024-05-13": {
         "max_tokens": 4096,
@@ -739,7 +740,8 @@
         "supports_function_calling": true,
         "supports_parallel_function_calling": true,
         "supports_response_schema": true,
-        "supports_vision": true
+        "supports_vision": true,
+        "supports_prompt_caching": true
     },
     "azure/global-standard/gpt-4o-mini": {
         "max_tokens": 16384,
@@ -1806,6 +1808,7 @@
         "supports_vision": true,
         "tool_use_system_prompt_tokens": 159,
         "supports_assistant_prefill": true,
+        "supports_pdf_input": true,
         "supports_prompt_caching": true,
         "supports_response_schema": true
     },
@@ -3025,6 +3028,8 @@
         "supports_vision": true,
         "supports_response_schema": true,
         "supports_prompt_caching": true,
+        "tpm": 4000000,
+        "rpm": 2000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-flash-001": {
@@ -3048,6 +3053,8 @@
         "supports_vision": true,
         "supports_response_schema": true,
         "supports_prompt_caching": true,
+        "tpm": 4000000,
+        "rpm": 2000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-flash": {
@@ -3070,6 +3077,8 @@
         "supports_function_calling": true,
         "supports_vision": true,
         "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 2000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-flash-latest": {
@@ -3092,6 +3101,8 @@
         "supports_function_calling": true,
         "supports_vision": true,
         "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 2000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-flash-8b-exp-0924": {
@@ -3114,6 +3125,8 @@
         "supports_function_calling": true,
         "supports_vision": true,
         "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 4000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-flash-exp-0827": {
@@ -3136,6 +3149,8 @@
         "supports_function_calling": true,
         "supports_vision": true,
         "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 2000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-flash-8b-exp-0827": {
@@ -3157,6 +3172,9 @@
         "supports_system_messages": true,
         "supports_function_calling": true,
         "supports_vision": true,
+        "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 4000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-pro": {
@@ -3170,7 +3188,10 @@
         "litellm_provider": "gemini",
         "mode": "chat",
         "supports_function_calling": true,
-        "source": "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models#foundation_models"
+        "rpd": 30000,
+        "tpm": 120000,
+        "rpm": 360,
+        "source": "https://ai.google.dev/gemini-api/docs/models/gemini"
     },
     "gemini/gemini-1.5-pro": {
         "max_tokens": 8192,
@@ -3187,6 +3208,8 @@
         "supports_vision": true,
         "supports_tool_choice": true,
         "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 1000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-pro-002": {
@@ -3205,6 +3228,8 @@
         "supports_tool_choice": true,
         "supports_response_schema": true,
         "supports_prompt_caching": true,
+        "tpm": 4000000,
+        "rpm": 1000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-pro-001": {
@@ -3223,6 +3248,8 @@
         "supports_tool_choice": true,
         "supports_response_schema": true,
         "supports_prompt_caching": true,
+        "tpm": 4000000,
+        "rpm": 1000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-pro-exp-0801": {
@@ -3240,6 +3267,8 @@
         "supports_vision": true,
         "supports_tool_choice": true,
         "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 1000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-pro-exp-0827": {
@@ -3257,6 +3286,8 @@
         "supports_vision": true,
         "supports_tool_choice": true,
         "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 1000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-1.5-pro-latest": {
@@ -3274,6 +3305,8 @@
         "supports_vision": true,
         "supports_tool_choice": true,
         "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 1000,
         "source": "https://ai.google.dev/pricing"
     },
     "gemini/gemini-pro-vision": {
@@ -3288,6 +3321,9 @@
         "mode": "chat",
         "supports_function_calling": true,
         "supports_vision": true,
+        "rpd": 30000,
+        "tpm": 120000,
+        "rpm": 360,
         "source": "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models#foundation_models"
     },
     "gemini/gemini-gemma-2-27b-it": {
@@ -4377,7 +4413,8 @@
         "mode": "chat",
         "supports_function_calling": true,
         "supports_vision": true,
-        "supports_assistant_prefill": true
+        "supports_assistant_prefill": true,
+        "supports_prompt_caching": true
     },
     "anthropic.claude-3-5-sonnet-latest-v2:0": {
         "max_tokens": 4096,
@@ -6892,7 +6929,6 @@
         "tool_use_system_prompt_tokens": 264,
         "supports_assistant_prefill": true,
         "supports_prompt_caching": true,
-        "supports_pdf_input": true,
         "supports_response_schema": true
     },
     "vertex_ai/claude-3-5-haiku@20241022": {
@@ -6934,7 +6970,8 @@
         "litellm_provider": "bedrock",
         "mode": "chat",
         "supports_assistant_prefill": true,
-        "supports_function_calling": true
+        "supports_function_calling": true,
+        "supports_prompt_caching": true
     },
     "us.anthropic.claude-3-5-haiku-20241022-v1:0": {
         "max_tokens": 4096,
@@ -7175,7 +7212,12 @@
         "supports_function_calling": true,
         "supports_vision": true,
         "supports_response_schema": true,
-        "source": "https://ai.google.dev/pricing"
+        "tpm": 4000000,
+        "rpm": 1000,
+        "source": "https://ai.google.dev/pricing",
+        "metadata": {
+            "notes": "Rate limits not documented for gemini-exp-1114. Assuming same as gemini-1.5-pro."
+        }
     },
     "openrouter/qwen/qwen-2.5-coder-32b-instruct": {
         "max_tokens": 33792,
@@ -7236,5 +7278,103 @@
         "mode": "chat",
         "supports_function_calling": true,
         "source": "https://fireworks.ai/pricing"
+    },
+    "gemini/gemini-1.5-flash-8b": {
+        "max_tokens": 8192,
+        "max_input_tokens": 1048576,
+        "max_output_tokens": 8192,
+        "max_images_per_prompt": 3000,
+        "max_videos_per_prompt": 10,
+        "max_video_length": 1,
+        "max_audio_length_hours": 8.4,
+        "max_audio_per_prompt": 1,
+        "max_pdf_size_mb": 30,
+        "input_cost_per_token": 0,
+        "input_cost_per_token_above_128k_tokens": 0,
+        "output_cost_per_token": 0,
+        "output_cost_per_token_above_128k_tokens": 0,
+        "litellm_provider": "gemini",
+        "mode": "chat",
+        "supports_system_messages": true,
+        "supports_function_calling": true,
+        "supports_vision": true,
+        "supports_response_schema": true,
+        "tpm": 4000000,
+        "rpm": 4000,
+        "source": "https://ai.google.dev/pricing"
+    },
+    "rerank-v3.5": {
+        "max_tokens": 4096,
+        "max_input_tokens": 4096,
+        "max_output_tokens": 4096,
+        "max_query_tokens": 2048,
+        "input_cost_per_token": 0.0,
+        "input_cost_per_query": 0.002,
+        "output_cost_per_token": 0.0,
+        "litellm_provider": "cohere",
+        "mode": "rerank"
+    },
+    "amazon.nova-micro-v1:0": {
+        "max_tokens": 4096,
+        "max_input_tokens": 300000,
+        "max_output_tokens": 4096,
+        "input_cost_per_token": 3.5e-08,
+        "output_cost_per_token": 1.4e-07,
+        "litellm_provider": "bedrock_converse",
+        "mode": "chat",
+        "supports_function_calling": true,
+        "supports_vision": true,
+        "supports_pdf_input": true,
+        "supports_prompt_caching": true
+    },
+    "amazon.nova-lite-v1:0": {
+        "max_tokens": 4096,
+        "max_input_tokens": 128000,
+        "max_output_tokens": 4096,
+        "input_cost_per_token": 6e-08,
+        "output_cost_per_token": 2.4e-07,
+        "litellm_provider": "bedrock_converse",
+        "mode": "chat",
+        "supports_function_calling": true,
+        "supports_vision": true,
+        "supports_pdf_input": true,
+        "supports_prompt_caching": true
+    },
+    "amazon.nova-pro-v1:0": {
+        "max_tokens": 4096,
+        "max_input_tokens": 300000,
+        "max_output_tokens": 4096,
+        "input_cost_per_token": 8e-07,
+        "output_cost_per_token": 3.2e-06,
+        "litellm_provider": "bedrock_converse",
+        "mode": "chat",
+        "supports_function_calling": true,
+        "supports_vision": true,
+        "supports_pdf_input": true,
+        "supports_prompt_caching": true
+    },
+    "together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": {
+        "input_cost_per_token": 1.8e-07,
+        "output_cost_per_token": 1.8e-07,
+        "litellm_provider": "together_ai",
+        "supports_function_calling": true,
+        "supports_parallel_function_calling": true,
+        "mode": "chat"
+    },
+    "together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": {
+        "input_cost_per_token": 8.8e-07,
+        "output_cost_per_token": 8.8e-07,
+        "litellm_provider": "together_ai",
+        "supports_function_calling": true,
+        "supports_parallel_function_calling": true,
+        "mode": "chat"
+    },
+    "together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": {
+        "input_cost_per_token": 3.5e-06,
+        "output_cost_per_token": 3.5e-06,
+        "litellm_provider": "together_ai",
+        "supports_function_calling": true,
+        "supports_parallel_function_calling": true,
+        "mode": "chat"
     }
 }
\ No newline at end of file
```
