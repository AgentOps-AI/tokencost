import openai
from tokencost import TOKEN_COSTS

models = (
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-instruct",
    "gpt-4-0314",
    "gpt-4",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-4-0613",
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "text-embedding-ada-002",
)

STRING = "Hello, world!"

MESSAGES = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
]
client = openai.Client()
# for model in models:
#     print(model)
#     d = {"model": model}
#     completion = client.chat.completions.create(messages=MESSAGES, model=model)
#     d["prompt_tokens"] = completion.usage.prompt_tokens
#     d["cost"] = d["prompt_tokens"] * TOKEN_COSTS[model]["prompt"]
#     print(d)
#     print("-" * 100)

for model in models:
    print(model, TOKEN_COSTS[model]["completion"] * 4)
    print("-" * 100)


# print(client.embeddings.create(input=STRING, model="text-embedding-ada-002"))
