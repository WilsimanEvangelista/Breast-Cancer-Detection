from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Request Method:", request.method)
    print("Request Headers:", request.headers)
    print("Request Form:", request.form)
    print("Request Files:", request.files)
    
    if not request.files:
        return jsonify({"error": "No files part"}), 400

    for file in request.files.values():
        if file.filename == '':
            continue
        if allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "No valid files"}), 400
