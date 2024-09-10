import requests

# Define the URL of your Flask server endpoint
url = 'http://127.0.0.1:5000/query'

# Define the query you want to send
data = {
    'query': 'What is the main contribution of the Llama model?'
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response from the server
print(response.json())
