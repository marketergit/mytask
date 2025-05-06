import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "model": "mixtral-8x7b-32768"
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        message = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": message})
    else:
        return jsonify({"response": "Failed to connect to Groq API."}), 500

if __name__ == '__main__':
    app.run(debug=True)
