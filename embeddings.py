from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def encode_chunks(chunks):
    return model.encode(chunks)

def encode_query(query):
    return model.encode([query])[0]

def similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
