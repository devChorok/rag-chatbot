from embeddings import encode_chunks, encode_query, similarity
from chunking import extract_text_from_pdf, chunk_text
import json

# Load and chunk the paper
text = extract_text_from_pdf('llama2_paper.pdf')
chunks = chunk_text(text)

# Encode the chunks
chunk_embeddings = encode_chunks(chunks)

def get_response(query):
    # Encode the query
    query_embedding = encode_query(query)
    
    # Find the most similar chunk
    scores = [similarity(query_embedding, chunk_embedding) for chunk_embedding in chunk_embeddings]
    best_chunk = chunks[scores.index(max(scores))]
    
    # Generate response based on best chunk
    response = generate_response_from_chunk(query, best_chunk)
    
    return response

def generate_response_from_chunk(query, chunk):
    # Logic to generate response based on the chunk
    return f"Based on the paper, the most relevant information is: {chunk[:300]}..."
