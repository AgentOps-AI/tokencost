import pandas as pd
import tokencost
from decimal import Decimal
import json

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
from tabulate import tabulate

table_data = df[
    [
        "Model Name",
        "Prompt Cost (USD) per 1M tokens",
        "Completion Cost (USD) per 1M tokens",
        "Max Prompt Tokens",
        "Max Output Tokens",
    ]
].values.tolist()

headers = [
    "Model Name",
    "Prompt Cost (USD) per 1M tokens",
    "Completion Cost (USD) per 1M tokens",
    "Max Prompt Tokens",
    "Max Output Tokens",
]

table_md = tabulate(table_data, headers=headers, tablefmt='pipe')

# Write the markdown table to pricing_table.md for reference
with open("pricing_table.md", "w") as f:
    f.write(table_md)

print("Pricing table updated in pricing_table.md")

# Now update the README.md file with the pricing table
def update_readme_with_pricing_table(table_md):
    """Update README.md by inserting the pricing table after the 'Cost table' section."""
    with open("README.md", "r") as f:
        readme_content = f.read()
    
    # Find the "Cost table" section
    cost_table_marker = "## Cost table"
    cost_table_index = readme_content.find(cost_table_marker)
    
    if cost_table_index == -1:
        print("Warning: Could not find '## Cost table' section in README.md")
        return
    
    # Find the end of the current cost table section (next ## heading or end of file)
    lines = readme_content.split('\n')
    cost_table_line = None
    
    for i, line in enumerate(lines):
        if line.strip() == cost_table_marker:
            cost_table_line = i
            break
    
    if cost_table_line is None:
        print("Warning: Could not locate cost table line in README.md")
        return
    
    # Find the next section (line starting with ##) or end of file
    next_section_line = len(lines)
    for i in range(cost_table_line + 1, len(lines)):
        if lines[i].strip().startswith("## ") and lines[i].strip() != cost_table_marker:
            next_section_line = i
            break
    
    # Build the new README content
    new_lines = []
    
    # Add everything up to and including the cost table header
    new_lines.extend(lines[:cost_table_line + 1])
    
    # Add the description line
    new_lines.append("Units denominated in USD. All prices can be located [here](pricing_table.md).")
    new_lines.append("")  # Empty line
    
    # Add the pricing table
    new_lines.extend(table_md.split('\n'))
    
    # Add everything after the old cost table section
    if next_section_line < len(lines):
        new_lines.append("")  # Empty line before next section
        new_lines.extend(lines[next_section_line:])
    
    # Write the updated README
    with open("README.md", "w") as f:
        f.write('\n'.join(new_lines))
    
    print("README.md updated with pricing table")

# Update the README with the pricing table
update_readme_with_pricing_table(table_md)
