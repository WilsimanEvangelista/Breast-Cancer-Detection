from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        a = request.data
        if a == 0:
            print("MERDA")
            return 0
        else:
            print(a)
            return "OK", 200

    except Exception as e:
        print("AAAAAAAAAAAAAA")
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)