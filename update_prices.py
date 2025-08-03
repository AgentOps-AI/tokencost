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

# Update the README.md with the pricing table
def update_readme_pricing_table():
    """Update the pricing table in README.md with the latest data"""
    # Read the current README
    with open("README.md", "r") as f:
        readme_content = f.read()
    
    # Create a summary table with key models for the README
    # Filter for the most important models to keep the README table manageable
    important_models = [
        'gpt-4', 'gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0125',
        'o1-mini', 'o1-preview', 'text-embedding-3-large', 'text-embedding-3-small', 
        'text-embedding-ada-002'
    ]
    
    # Filter the dataframe for important models
    summary_df = df[df.index.isin(important_models)]
    
    # Generate the summary table
    summary_table_md = summary_df[
        [
            "Model Name",
            "Prompt Cost (USD) per 1M tokens",
            "Completion Cost (USD) per 1M tokens",
            "Max Prompt Tokens",
            "Max Output Tokens",
        ]
    ].to_markdown(index=False)
    
    # Create the new pricing table section
    new_pricing_section = f"""## Cost table
Units denominated in USD. All prices can be located [here](pricing_table.md).

<details>
<summary>📊 View Full Pricing Table</summary>

{summary_table_md}

*For the complete pricing table with all models, see [pricing_table.md](pricing_table.md)*

</details>"""
    
    # Find and replace the existing pricing table section
    import re
    pattern = r'## Cost table\nUnits denominated in USD\. All prices can be located \[here\]\(pricing_table\.md\)\.\n\n<details>\n<summary>📊 View Full Pricing Table</summary>\n\n.*?\n\n\*For the complete pricing table with all models, see \[pricing_table\.md\]\(pricing_table\.md\)\*\n\n</details>'
    
    if re.search(pattern, readme_content, re.DOTALL):
        # Replace existing section
        updated_readme = re.sub(pattern, new_pricing_section, readme_content, flags=re.DOTALL)
    else:
        # If no existing section found, add it before the end of the file
        # Find the last section and add before it
        lines = readme_content.split('\n')
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith('## '):
                lines.insert(i, new_pricing_section)
                break
        updated_readme = '\n'.join(lines)
    
    # Write the updated README
    with open("README.md", "w") as f:
        f.write(updated_readme)
    
    print("Pricing table updated in README.md")

# Update the README
update_readme_pricing_table()
