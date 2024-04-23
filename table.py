import pandas as pd
import tokencost
df = pd.DataFrame(tokencost.TOKEN_COSTS).T
df[['input_cost_per_token', 'output_cost_per_token']] = df[[
    'input_cost_per_token', 'output_cost_per_token']].applymap(lambda x: '$'+f'{x:.8f}')

print(df[['max_tokens', 'max_input_tokens', 'input_cost_per_token', 'output_cost_per_token']].to_markdown())
