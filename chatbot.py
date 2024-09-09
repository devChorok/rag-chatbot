from embeddings import encode_chunks, encode_query, similarity
from chunking import extract_text_from_pdf, chunk_text
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load and chunk the paper
text = extract_text_from_pdf('llama2_paper.pdf')
chunks = chunk_text(text)

# Load model and tokenizer
model_name = "facebook/opt-125m"  # Replace with a suitable model name
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Encode the chunks
chunk_embeddings = encode_chunks(chunks)

def get_response(query):
    # Encode the query
    query_embedding = encode_query(query)
    
    # Find the most similar chunk
    scores = [similarity(query_embedding, chunk_embedding) for chunk_embedding in chunk_embeddings]
    best_chunk = chunks[scores.index(max(scores))]
    
    # Generate response based on the best chunk
    response = generate_response_from_chunk(query, best_chunk)
    
    return response

def generate_response_from_chunk(query, chunk):
    # Construct the prompt using the chunk and the query
    prompt = f"Chunk of text: {chunk}\n\nQuery: {query}\n\nResponse:"

    # Tokenize the prompt with truncation
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)

    # Ensure the input length does not exceed the model's maximum length
    input_length = inputs["input_ids"].shape[1]
    max_new_tokens = 2048 - input_length

    # Generate a response using the model
    outputs = model.generate(
        inputs["input_ids"],
        max_new_tokens=max_new_tokens,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    # Decode the generated text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response