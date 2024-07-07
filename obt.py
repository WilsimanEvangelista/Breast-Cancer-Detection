from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print(request.headers)
        print(request.files)
        uploaded_file = request.files  # Assuming the file is uploaded with the key 'file'
        if uploaded_file.filename != '':
            file_content = uploaded_file.read().decode('utf-8')
            print("Conteúdo do arquivo:")
            print(file_content)
            return "Conteúdo do arquivo impresso no console.", 200
        else:
            return "Nenhum arquivo foi enviado.", 400

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)