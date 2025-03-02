from openai import OpenAI
import re


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    return text

client = OpenAI(api_key='sk-proj-...')
def get_embedding2(text, model="text-embedding-3-small"):
    normalized_text = normalize_text(text)
    return client.embeddings.create(input=[normalized_text], model=model).data[0].embedding

emb = get_embedding2("Some text")
print(emb)
