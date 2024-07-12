'''
from flask import Flask, request, jsonify
from download_images import start_download_images
from upload_images import start_upload_images_to_drive
import json
from run_h5file import run_h5
from gradCam import generate_cam

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
            
            img = 'downloads/tem.png'
            run_h5(img)

            
            # PROCESSA IMAGEM
            cancer = 0
            pred_cancer = 0
            n_cancer = 0
            pred_n_cancer = 0
            list_img_process = []
            
            for i in list_new_name_images:
                print(f'downloads/{i}')
                img = f'downloads/{i}'
                run_h5(img)
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                #list_img_process.append(img_process)
                
                if diag == "Tumor Maligno":
                    cancer += 1
                    pred_cancer += pred
                    os.remove(i)
                else:
                    n_cancer += 1
                    pred_n_cancer += pred
                    os.remove(i)
                
            
            if n_cancer > cancer:
                diag_final = f'Tumor Benigno com {pred_n_cancer/n_cancer*100} de certeza.'
            else:
                diag_final = f'Tumor Maligno com {pred_cancer/cancer*100} de certeza.'
            
            #start_upload_images_to_drive(list_img_process) # Faz upload das imagens processadas para o drive

            return 'ok',200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)'''

from flask import Flask, request, jsonify
from download_images import start_download_images
import tensorflow as tf
from run_h5file import *
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
            model_path = "model/model.h5"
            loaded_model = tf.keras.models.load_model(model_path)
            
            new_list_images = []

            cancer = 0
            pred_cancer = 0
            n_cancer = 0
            pred_n_cancer = 0
            list_img_process = []

            combinedMultiDict_To_Lists = list(a.lists())
            list_Images = combinedMultiDict_To_Lists[0][0]

            for i in json.loads(list_Images):
                new_list_images.append(i.replace("\"","\'"))
            
            
            list_new_name_images = start_download_images(file_names=new_list_images)

            for i in list_new_name_images:
                name_final = f'downloads/{i}'
                pred, diag = run_h5(name_final, loaded_model)
                
                if diag == "Tumor Maligno":
                    cancer += 1
                    pred_cancer += pred
                    os.remove(name_final)
                else:
                    n_cancer += 1
                    pred_n_cancer += pred
                    os.remove(name_final)

            if n_cancer > cancer:
                d = (pred_n_cancer/n_cancer*100)[0][0]
                diag_final = f'Tumor Benigno com {d:.2f} de certeza.'
            else:
                d = (pred_cancer/cancer*100)[0][0]
                diag_final = f'Tumor Maligno com {d:.2f} de certeza.'
            
            print(diag_final)
            return diag_final, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)