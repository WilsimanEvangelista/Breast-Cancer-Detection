from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.headers)
    print(request.max_content_length)
    print(request.get_data())
    print(request.content_encoding)
    try:
        a = request.values
        if a == 0:
            print("AAAAAAAAAAA")
            return 0
        else:
            print(a)
            c = list(a.lists())
            print(c)
            print(c[0][0])
            return c[0][0], 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)