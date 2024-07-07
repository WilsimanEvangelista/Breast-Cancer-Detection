from flask import Flask, request, jsonify
from download_images import authenticate, download_specific_photos

'''def main(file_names: list) -> None: #file_names is a list that must contain 4 images 
    folder_id = '1tY0nf5JzeScSieaa4DX8GDjAQ_i59xms'
    local_folder = 'downloads'
    
    service = authenticate()
    download_specific_photos(service, folder_id, file_names, local_folder)
    print("Downloads concluídos!")

'''
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
            return c, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


