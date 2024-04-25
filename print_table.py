import pandas as pd
import tokencost

# Load the data
df = pd.DataFrame(tokencost.TOKEN_COSTS).T
df['max_input_tokens'] = df['max_input_tokens'].apply(lambda x: '{:,.0f}'.format(x))

# Updated function to format the cost or handle NaN


def format_cost(x):
    if pd.isna(x):
        return 'NaN'
    else:
        # Ensure the number is treated as a float and format it
        return '${:.8f}'.format(float(x))


# Apply the formatting function
df[['input_cost_per_token', 'output_cost_per_token']] = df[[
    'input_cost_per_token', 'output_cost_per_token']].applymap(format_cost)

# Print the DataFrame as markdown
print(df[['max_tokens', 'max_input_tokens', 'input_cost_per_token', 'output_cost_per_token']].to_markdown())
