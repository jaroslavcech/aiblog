import fitz
import re
import tiktoken
import psycopg2

DB_PARAMS = {
    "dbname": "rheldoc",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}


def chunk_text_with_overlap(text, max_tokens=512, overlap=50, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + max_tokens
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += max_tokens - overlap
        if start >= len(words):
            break

    return chunks

def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    return {page.number + 1: page.get_text("text") for page in doc}


def generate_page_chunks(pdf_path, max_tokens=512, overlap_chars=50):
    pages_text = extract_text_by_page(pdf_path)
    structured_chunks = []

    for page, text in pages_text.items(): 
        text_chunks = chunk_text_with_overlap(text, max_tokens=max_tokens, overlap=overlap_chars)
        for chunk in text_chunks:
            structured_chunks.append({
                "page": page,
                "chunk": chunk
            })

    return structured_chunks


def save_chunks_to_db(chunks):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    for entry in chunks:
        cur.execute("""
            INSERT INTO chunks (page, chunk) VALUES (%s, %s, %s);
        """, (entry["page"], entry["chunk"]))

    conn.commit()
    cur.close()
    conn.close()


pdf_path = "Data/Red_Hat_Enterprise_Linux-7-System_Administrators_Guide-en-US.pdf"
page_chunks = generate_page_chunks(pdf_path, max_tokens=256, overlap_chars=26)

for entry in page_chunks[:5]:
    print(entry)
save_chunks_to_db(page_chunks)
