import tiktoken

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

prompt = "How many tokens does this text have?"
response = "The answer to your question is..."

prompt_tokens = count_tokens(prompt, model="gpt-4")
response_tokens = count_tokens(response, model="gpt-4")

print(f"Input tokens: {prompt_tokens}")
print(f"Output tokens: {response_tokens}")
