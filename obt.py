from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    return jsonify({"error": "No valid files"}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)