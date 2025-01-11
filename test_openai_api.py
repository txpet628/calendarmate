from openai import OpenAI

def update_token_usage(tokens: str) -> None:
    fname = "tokens_used.txt"
    with open(fname, '+a') as fh:
        fh.write(f"{tokens}\n")


fname = "/Users/diana/my_api_secrets/openai_api_key"
with open(fname, "r") as fh:
    api_key = fh.read().strip()

client = OpenAI(
  api_key=api_key
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

response_msg = completion.choices[0].message.content
tokens_used = completion.usage.total_tokens
print(f"Response: {response_msg}")
print(f"Tokens used {tokens_used}")
update_token_usage(tokens_used)