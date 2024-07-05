from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        image_base64 = request.data.decode('utf-8')
        print(image)
        if not image_base64:
            return jsonify({"error": "No data found"}), 400

        # Imprime a string recebida
        print(f"Received data: {image_base64}")

        return "OK", 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)