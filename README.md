# TokenCost

## Overview

TokenCost is a specialized tool designed for calculating the token count and associated cost of strings and messages used in Large Language Models (LLMs). This utility is particularly useful for developers and researchers working with language models, enabling them to estimate the computational resources required for processing various inputs.

## Features

- **Token Counting**: Accurately counts the number of tokens in a given string or message.
- **Cost Calculation**: Computes the cost of processing based on the token count, considering the specific pricing model of the LLM in use.
- **Support for Multiple LLMs**: Compatible with various Large Language Models.
- **Easy Integration**: Simple API for integrating with existing projects or workflows.

## Installation

To install TokenCost, use the following command:

```bash
git clone https://github.com/yourusername/tokencost.git
cd tokencost
pip install -r requirements.txt
```


## Usage

To use TokenCost, follow these steps:

1. Import the module:

```python
from tokencost import TokenCalculator
```


3. Calculate tokens and cost:
```python
text = "Your sample text here"
token_count, cost = calculator.calculate(text)
print(f"Token Count: {token_count}, Cost: {cost}")
```

To run tests, follow the below steps:

	0. `pip install pytest` if you don't have pytest already

	1. `pytest tests` while in the `tokencost` folder to run the `tests` folder

## Contributing


Contributions to TokenCost are welcome! Please refer to our Contribution Guidelines for more details.

## License

TokenCost is released under the MIT License.
