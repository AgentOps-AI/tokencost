import pandas as pd
import tokencost
import json

# Update model_prices.json with the latest costs from the LiteLLM cost tracker

with open('tokencost/model_prices.json', 'r') as f:
    model_prices = json.load(f)
    if model_prices != tokencost.TOKEN_COSTS:
        print('Updating model_prices.json')

    json.dump(tokencost.TOKEN_COSTS, open('model_prices.json', 'w'))

# Load the data
df = pd.DataFrame(tokencost.TOKEN_COSTS).T
df['max_input_tokens'] = df['max_input_tokens'].apply(lambda x: '{:,.0f}'.format(x))
df['max_tokens'] = df['max_tokens'].apply(lambda x: '{:,.0f}'.format(x))


# Updated function to format the cost or handle NaN


def format_cost(x):
    if pd.isna(x):
        return '--'
    else:
        # Ensure the number is treated as a float and format it
        return '${:.8f}'.format(float(x))


# Apply the formatting function
df[['input_cost_per_token', 'output_cost_per_token']] = df[[
    'input_cost_per_token', 'output_cost_per_token']].applymap(format_cost)


column_mapping = {
    'input_cost_per_token': 'Prompt Cost (USD)',
    'output_cost_per_token': 'Completion Cost (USD)',
    'max_input_tokens': 'Max Prompt Tokens',
    'max_output_tokens': 'Max Output Tokens',
    'model_name': 'Model Name'
}

# Apply the column renaming
df.rename(columns=column_mapping, inplace=True)

# Write the DataFrame with the correct column names as markdown to a file
with open('pricing_table.md', 'w') as f:
    f.write(df[['Model Name', 'Prompt Cost (USD)', 'Completion Cost (USD)',
            'Max Prompt Tokens', 'Max Output Tokens']].to_markdown(index=False))
