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

client = OpenAI(api_key='sk-proj-a....')
def get_embedding2(text, model="text-embedding-3-small"):
    normalized_text = normalize_text(text)
    return client.embeddings.create(input=[normalized_text], model=model).data[0].embedding

def update_embeddings():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    # Získání chunků bez embeddingu
    cur.execute("SELECT id, chunk FROM chunks WHERE embedding IS NULL;")
    rows = cur.fetchall()

    for chunk_id, chunk_text in rows:
        embedding = get_embedding2(chunk_text)
        embedding_str = np.array(embedding).tolist()  
        print(f"{chunk_id}")
        cur.execute("""
            UPDATE chunks SET embedding = %s WHERE id = %s;
        """, (embedding_str, chunk_id))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Saved {len(rows)} embeddingů to PostgreSQL")

update_embeddings()
