from flask import Flask, request, jsonify
from download_images import main

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        a = request.values
        if a == 0:
            print("AAAAAAAAAAA")
            return 0
        else:
            c = list(a.lists())
            return c[0][0], 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)