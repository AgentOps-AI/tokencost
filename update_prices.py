import pandas as pd
import tokencost
import json

# Update model_prices.json with the latest costs from the LiteLLM cost tracker


def diff_dicts(dict1, dict2):
    diff_keys = dict1.keys() ^ dict2.keys()
    differences = {k: (dict1.get(k), dict2.get(k)) for k in diff_keys}
    differences.update({k: (dict1[k], dict2[k]) for k in dict1 if k in dict2 and dict1[k] != dict2[k]})

    if differences:
        print("Differences found:")
        for key, (val1, val2) in differences.items():
            print(f"{key}: {val1} != {val2}")
    else:
        print("No differences found.")

    if differences:
        return True
    else:
        return False


with open('tokencost/model_prices.json', 'r') as f:
    model_prices = json.load(f)

if diff_dicts(model_prices, tokencost.TOKEN_COSTS):
    print('Updating model_prices.json')
    with open('tokencost/model_prices.json', 'w') as f:
        json.dump(tokencost.TOKEN_COSTS, f, indent=4)
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
        # Find the last non-zero digit
        str_x = str(float(x * 1_000_000))
        last_non_zero = len(str_x) - len(str_x.rstrip('0'))
        # Ensure at least 2 decimal places
        decimal_places = max(2, last_non_zero)
        return '${:,.{}f}'.format(float(x * 1_000_000), decimal_places)


# Apply the formatting function using DataFrame.apply and lambda
df[['input_cost_per_token', 'output_cost_per_token']] = df[[
    'input_cost_per_token', 'output_cost_per_token']].apply(lambda x: x.map(format_cost))


column_mapping = {
    'input_cost_per_token': 'Prompt Cost (USD) per 1M tokens',
    'output_cost_per_token': 'Completion Cost (USD) per 1M tokens',
    'max_input_tokens': 'Max Prompt Tokens',
    'max_output_tokens': 'Max Output Tokens',
    'model_name': 'Model Name'
}

# Assuming the keys of the JSON data represent the model names and have been set as the index
df['Model Name'] = df.index

# Apply the column renaming
df.rename(columns=column_mapping, inplace=True)

# Write the DataFrame with the correct column names as markdown to a file
with open('pricing_table.md', 'w') as f:
    f.write(df[['Model Name', 'Prompt Cost (USD) per 1M tokens', 'Completion Cost (USD) per 1M tokens',
            'Max Prompt Tokens', 'Max Output Tokens']].to_markdown(index=False))
