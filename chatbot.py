import sqlite3
from embeddings import encode_chunks, encode_query, similarity
from chunking import extract_text_from_pdf, chunk_text,chunk_text_by_sentence,chunk_text_by_token
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load and chunk the paper
text = extract_text_from_pdf('llama2_paper.pdf')

# Load model and tokenizer
model_name = "facebook/opt-125m"  # Replace with a suitable model name
chunks = chunk_text_by_sentence(text)

model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Encode the chunks
chunk_embeddings = encode_chunks(chunks)

def get_response(query):
    # Check if the query has been stored in the database
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT response FROM responses WHERE query = ?", (query,))
        stored_response = c.fetchone()
        
        if stored_response:
            print(f"Stored response found for query: {query}")
            return stored_response[0]
        
    except Exception as e:
        print(f"Error retrieving stored response: {e}")
        return

    # Encode the query if no stored response found
    try:
        query_embedding = encode_query(query)
        print("Query encoded successfully.")
    except Exception as e:
        print(f"Error encoding query: {e}")
        return

    # Calculate similarity scores
    try:
        scores = [similarity(query_embedding, chunk_embedding) for chunk_embedding in chunk_embeddings]
        print("Similarity scores calculated successfully.")
    except Exception as e:
        print(f"Error calculating similarity scores: {e}")
        return

    # Check if any scores were computed
    if not scores:
        print("No similarity scores were computed.")
        return

    # Find the best chunk
    best_chunk = chunks[scores.index(max(scores))]
    print(f"Best chunk (index {scores.index(max(scores))}) selected with similarity score {max(scores)}:")
    
    # Generate response based on the best chunk
    response = generate_response_from_chunk(query, best_chunk)

    # Store the new response in the database
    try:
        c.execute("INSERT INTO responses (query, response) VALUES (?, ?)", (query, response))
        conn.commit()
        print(f"Response stored for query: {query}")
    except Exception as e:
        print(f"Error storing response: {e}")
    
    conn.close()

    return response



def generate_response_from_chunk(query, chunk):
    # Construct the prompt using the chunk and the query
    prompt = f"Chunk of text: {chunk}\n\nQuery: {query}\n\nResponse:"

    # Tokenize the prompt with truncation
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)

    # Ensure the input length does not exceed the model's maximum length
    input_length = inputs["input_ids"].shape[1]
    max_new_tokens = max(1, 2048 - input_length)

    # Generate a response using the model
    outputs = model.generate(
        inputs["input_ids"],
        max_new_tokens=max_new_tokens,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        num_beams=5,
    )

    # Decode the generated text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response