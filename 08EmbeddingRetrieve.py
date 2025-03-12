from openai import OpenAI
import psycopg2
import numpy as np
import re

DB_PARAMS = {
    "dbname": "rheldoc",
    "user": "postgres",
    "password": "xxx",
    "host": "localhost",
    "port": "5432"
}

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    return text

client = OpenAI(api_key='sk-proj-...')

def get_embedding2(text, model="text-embedding-3-small"):
    normalized_text = normalize_text(text)
    return client.embeddings.create(input=[normalized_text], model=model).data[0].embedding

def search_similar_chunks(query_text, top_n=3):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    query_embedding = get_embedding2(query_text)

    cur.execute("""
        SELECT id, page, chunk, 1 - (embedding <=> %s::vector) AS similarity
        FROM chunks
        ORDER BY embedding <=> %s::vector ASC
        LIMIT %s;
    """, (query_embedding, query_embedding,top_n))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return results

query = "How add existing user to existing group"
results = search_similar_chunks(query)

for row in results:
    print(row)
