import pandas as pd
import tokencost
from decimal import Decimal
import json
import re

# Update model_prices.json with the latest costs from the LiteLLM cost tracker
print("Fetching latest prices...")
tokencost.refresh_prices(write_file=False)


def diff_dicts(dict1, dict2):
    # Filter out keys from dict1 that start with 'openai/'
    dict1_filtered = {k: v for k, v in dict1.items() if not k.startswith('openai/')}
    
    diff_keys_initial = dict1_filtered.keys() ^ dict2.keys()
    diff_keys = {k for k in diff_keys_initial if not k.startswith('openai/')}
    differences = {k: (dict1_filtered.get(k), dict2.get(k)) for k in diff_keys}
    differences.update(
        {k: (dict1_filtered[k], dict2[k]) for k in dict1_filtered if k in dict2 and dict1_filtered[k] != dict2[k]}
    )

    if differences:
        print("Differences found:")
        for key, (val1, val2) in differences.items():
            print(f"{key}: {val1} != {val2}")
    else:
        print("No differences found.")

    return bool(differences)


# Load the current file for comparison
with open("tokencost/model_prices.json", "r") as f:
    model_prices = json.load(f)

# Compare the refreshed TOKEN_COSTS with the file, ignoring "openai/" keys
if diff_dicts(model_prices, tokencost.TOKEN_COSTS):
    print("Updating model_prices.json")
    with open("tokencost/model_prices.json", "w") as f:
        json.dump(tokencost.TOKEN_COSTS, f, indent=4)
    print("File updated successfully")
    # Reload the prices after updating
    with open("tokencost/model_prices.json", "r") as f:
        model_prices = json.load(f)
else:
    print("File is already up to date")

# Add/overwrite the "openai/" keys from the unprefixed keys in the final price list
openai_models = {key: value for key, value in model_prices.items() if value.get("litellm_provider") == "openai"}

for key, value in openai_models.items():
    if not key.startswith('openai/'):
        new_key = f"openai/{key}"
        model_prices[new_key] = value

# Write the final, consistent data back to the file
print("Adding 'openai/' pre-fixed models to model_prices.json")
with open("tokencost/model_prices.json", "w") as f:
    json.dump(model_prices, f, indent=4)

# Load the data
df = pd.DataFrame(model_prices).T
df.loc[df.index[1:], "max_input_tokens"] = (
    df["max_input_tokens"].iloc[1:].apply(lambda x: "{:,.0f}".format(x))
)
df.loc[df.index[1:], "max_tokens"] = (
    df["max_tokens"].iloc[1:].apply(lambda x: "{:,.0f}".format(x))
)


# Updated function to format the cost or handle NaN
def format_cost(x):
    if pd.isna(x):
        return "--"
    else:
        price_per_million = Decimal(str(x)) * Decimal(str(1_000_000))
        normalized = price_per_million.normalize()
        formatted_price = "{:.2f}".format(normalized)

        formatted_price = (
            formatted_price.rstrip("0").rstrip(".")
            if "." in formatted_price
            else formatted_price + ".00"
        )

        return f"${formatted_price}"


# Apply the formatting function using DataFrame.apply and lambda
df[["input_cost_per_token", "output_cost_per_token"]] = df[
    ["input_cost_per_token", "output_cost_per_token"]
].apply(lambda x: x.map(format_cost))


column_mapping = {
    "input_cost_per_token": "Prompt Cost (USD) per 1M tokens",
    "output_cost_per_token": "Completion Cost (USD) per 1M tokens",
    "max_input_tokens": "Max Prompt Tokens",
    "max_output_tokens": "Max Output Tokens",
    "model_name": "Model Name",
}

# Assuming the keys of the JSON data represent the model names and have been set as the index
df["Model Name"] = df.index

# Apply the column renaming
df.rename(columns=column_mapping, inplace=True)

# Generate the markdown table
table_md = df[
    [
        "Model Name",
        "Prompt Cost (USD) per 1M tokens",
        "Completion Cost (USD) per 1M tokens",
        "Max Prompt Tokens",
        "Max Output Tokens",
    ]
].to_markdown(index=False)

# Write the markdown table to pricing_table.md for reference
with open("pricing_table.md", "w") as f:
    f.write(table_md)

print("Pricing table updated in pricing_table.md")

# Read the README.md file
with open("README.md", "r") as f:
    readme_content = f.read()

# Find and replace just the table in the README, preserving the header text
# The regex pattern matches a markdown table starting with the "Model Name" header
# and ending before the "Note:" line
table_pattern = r"(?s)\| Model Name.*?(?=\n\n\*\*Note:\*\*)"

# Get a subset of the table (first 10 rows) for the README
table_lines = table_md.split('\n')
subset_table = '\n'.join(table_lines[:12])  # Header + separator + first 10 data rows

table_replacement = subset_table

updated_readme = re.sub(table_pattern, table_replacement, readme_content, flags=re.DOTALL)

# Write the updated README
with open("README.md", "w") as f:
    f.write(updated_readme)

print("README.md updated with the latest pricing table")
