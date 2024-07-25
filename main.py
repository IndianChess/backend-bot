# main.py
from gradio_client import Client
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for simplicity, restrict in production

client = Client("ysharma/Chat_with_Meta_llama3_8b")

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
