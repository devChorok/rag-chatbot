from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer

def chunk_text_by_sentence(text, chunk_size=500):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= chunk_size:
            current_chunk += sentence + " "
            current_length += sentence_length
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            current_length = sentence_length

    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks


def chunk_text_by_token(text, model_name, chunk_size=500):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer(text)['input_ids']
    
    chunks = []
    for i in range(0, len(tokens), chunk_size):
        chunk_tokens = tokens[i:i+chunk_size]
        chunk = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk)
        
    return chunks

def sliding_window_chunking(text_tokens, window_size=512, overlap_size=256):
    """
    Performs sliding window chunking on a list of tokens.
    
    Args:
    - text_tokens (list): The list of tokens to chunk.
    - window_size (int): The number of tokens in each chunk.
    - overlap_size (int): The number of tokens to overlap between consecutive chunks.
    
    Returns:
    - List of token chunks.
    """
    # Ensure overlap is smaller than window size
    assert overlap_size < window_size, "Overlap size must be smaller than window size."

    chunks = []
    start = 0
    
    # Create chunks using sliding window approach
    while start < len(text_tokens):
        # Define the end of the window
        end = start + window_size
        chunk = text_tokens[start:end]
        chunks.append(chunk)
        
        # Slide the window by reducing overlap
        start += window_size - overlap_size
    
    return chunks

# Example usage
tokens = "This is a sample text that needs to be tokenized into chunks using the sliding window method.".split()
window_size = 10
overlap_size = 5

# Call the function
chunks = sliding_window_chunking(tokens, window_size=window_size, overlap_size=overlap_size)

# Print chunks
for idx, chunk in enumerate(chunks):
    print(f"Chunk {idx + 1}: {chunk}")


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500):
    chunks = []
    words = text.split()
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks
