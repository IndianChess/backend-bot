from flask import Flask, request, jsonify
from gradio_client import Client
import time

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    client = Client("Nymbo/Qwen2.5-Coder-32B-Instruct-Serverless")

    # Implementing manual retry mechanism to wait indefinitely
    while True:
        try:
            result = client.predict(
                message=data.get('message', ''),
                system_message=data.get('system_message', ''),
                max_tokens=data.get('max_tokens', 512),
                temperature=data.get('temperature', 0.7),
                top_p=data.get('top_p', 0.95),
                api_name="/chat"
            )
            return jsonify(result)

        except Exception as e:
            print(f"Request failed: {e}. Retrying in 10 seconds...")
            time.sleep(10)  # Wait and retry indefinitely

if __name__ == '__main__':
    app.run(debug=True)
