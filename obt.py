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
            new_list_images = []


            combinedMultiDict_To_Lists = list(a.lists())
            print(combinedMultiDict_To_Lists)

            list_Images = combinedMultiDict_To_Lists[0][0]
            print(list_Images)
            
            for i in list_Images:
                new_list_images.append(i.replace("\"","\'"))
            print(new_list_images)

            images_Download = main(file_names=new_list_images)
            print(images_Download)
            
            return list_Images,images_Download, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

