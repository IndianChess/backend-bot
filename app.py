from flask import Flask, request, jsonify
from gradio_client import Client

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    client = Client("Nymbo/Qwen2.5-Coder-32B-Instruct-Serverless")

    try:
        # Infinite timeout by setting it to None
        result = client.predict(
            message=data.get('message', ''),
            system_message=data.get('system_message', ''),
            max_tokens=data.get('max_tokens', 512),
            temperature=data.get('temperature', 0.7),
            top_p=data.get('top_p', 0.95),
            api_name="/chat",
            timeout=None  # Attempt to remove timeout
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
