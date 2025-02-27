from openai import OpenAI
client = OpenAI(api_key='sk-proj-...')

completion = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "How many tokens did I just use?"}]
)

print(f"Prompt tokens: {completion.usage.prompt_tokens}")
print(f"Competion tokens: {completion.usage.completion_tokens}")
