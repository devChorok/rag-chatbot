from flask import Flask, request, jsonify
from chatbot import get_response
from database import store_response
import time

app = Flask(__name__)

# Function to log query, response, and latency to a text file
def log_interaction(query, response, latency):
    with open('chatbot_interactions.txt', 'a') as f:
        f.write(f"Question: {query}\n")
        f.write(f"Response: {response}\n")
        f.write(f"Latency: {latency:.2f} seconds\n")
        f.write(f"{'-'*40}\n")  # Separator between interactions

@app.route('/query', methods=['POST'])
def query():
    try:
        start_time = time.time()

        # Get the query from the request
        data = request.get_json()
        query = data['query']

        # Get the response from the chatbot
        response = get_response(query)

        # Measure latency
        latency = time.time() - start_time

        # Store the query, response, and latency in the database
        store_response(query, response, latency)

        # Log the interaction to a text file
        log_interaction(query, response, latency)

        # Return the response and latency as JSON
        return jsonify({
            'query': query,
            'response': response,
            'latency': latency
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
