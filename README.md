# How to
install dependencies in requirements.txt
run server by running : python script/rest_server.py
ask queries by running : python script/request.py


# Findings on Chunking Methods and Latency

## Chunking Methods

### 1. **Chunk by Sentence**
- **Performance**: 
  - Relevant and coherent responses, with full sentences preserving context.
  - Clear and concise comparison of Llama model's performance with others, like ChatGPT and Falcon.
  - Example: "Llama 2-Chat 7B model outperforms MPT-7B on 60% of the prompts."
- **Latency**: 
  - Inconsistent latency, ranging from 3.31 seconds to 54.02 seconds depending on input.

### 2. **Chunk by Token**
- **Performance**: 
  - Less relevant responses due to the model receiving fragmented pieces of information.
  - Some irrelevant answers, such as unrelated medical advice, due to the broken token boundaries.
- **Latency**: 
  - Faster and more consistent latency, around 2.78 to 3.09 seconds.

### 3. **Sliding Window Chunking**
- **Performance**: 
  - This method gave some partially relevant responses but also exhibited issues with fragmented context.
  - Some repetitive or nonsensical output was seen in the responses.
- **Latency**: 
  - Higher latency, around 12.53 seconds due to additional processing involved in maintaining overlap between chunks.

### 4. **Chunking Without Overlap**
- **Performance**: 
  - When chunking without overlap, responses were less coherent and context was often lost.
  - The latency was faster but at the cost of relevance.
  
## Summary of Latency and Performance
- **Chunk by Sentence** provided the most relevant responses but had variability in latency.
- **Chunk by Token** produced the fastest latency but lacked relevance in its output.
- **Sliding Window Chunking** helped retain context across chunks but increased the latency significantly.
- **Chunking Without Overlap** resulted in quicker responses but with degraded performance in terms of context and relevance.

## Conclusion
For most applications, **Chunk by Sentence** offers the best tradeoff between relevance and latency, especially when full-context understanding is critical. **Chunk by Token** is suitable for scenarios where latency is prioritized over full sentence coherence, and **Sliding Window Chunking** should be used when context retention across chunk boundaries is crucial despite higher latency.
