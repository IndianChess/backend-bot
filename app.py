import os
import logging
from gradio_client import Client
from flask import Flask, request, jsonify
from flask_cors import CORS

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Gradio Client
client = Client("Nymbo/Llama-3.1-8B-Instruct-Inference")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "No message provided"}), 400

        logging.info(f"Received message: {message}")

        # Call Gradio API
        result = client.predict(
            message=message,
            system_message="You are a compassionate and empathetic therapist. You listen carefully and provide thoughtful, supportive responses. Keep your responses simple and short.",
            temperature=0.8,
            max_tokens=218,
            top_p=1,
            api_name="/chat"
        )

        logging.info(f"AI Response: {result}")
        return jsonify({"response": result})

    except Exception as e:
        logging.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
