# main.py
from gradio_client import Client
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = Client("vilarin/Llama-3.1-8B-Instruct")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get("message")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        result = client.predict(
            message=message,
            system_prompt="You are a compassionate and empathetic therapist. You listen carefully and provide thoughtful, supportive responses.",
            temperature=0.8,
            max_new_tokens=1024,
            top_p=1,
            top_k=20,
            penalty=1.2,
            api_name="/chat"
        )
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
