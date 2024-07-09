from flask import Flask, request, jsonify
from download_images import start_download_images
from upload_images import start_upload_images_to_drive
import json


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        a = request.values
        if a == 0:
            print("AAAAAAAAAAA")
            return 0
        else:
            new_list_images = []

            combinedMultiDict_To_Lists = list(a.lists())
            list_Images = combinedMultiDict_To_Lists[0][0]

            for i in json.loads(list_Images):
                new_list_images.append(i.replace("\"","\'"))
            
            list_new_name_images = start_download_images(file_names=new_list_images) # Faz download das imagens e retorna o nome das imagens de forma sanitizada

            # PROCESSA IMAGEM

            start_upload_images_to_drive(list_new_name_images) # Faz upload das imagens processadas para o drive


            return "Ok", 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

