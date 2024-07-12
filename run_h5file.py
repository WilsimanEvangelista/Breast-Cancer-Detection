import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from PIL import Image
import numpy as np
import cv2

def run_h5(image_path: str, loaded_model) -> (float, str):
    print("--------------- INFERENCIA ---------------")
    print(image_path)

    image = cv2.imread(image_path)

    image_fromarray = Image.fromarray(image, 'RGB')
    resize_image = image_fromarray.resize((224, 224))
    expand_input = np.expand_dims(resize_image,axis=0)
    input_data = np.array(expand_input)
    input_data = input_data/255

    pred = loaded_model.predict(input_data)
    if pred >= 0.5:
        print(pred, "Tumor Maligno")
        return pred, "Tumor Maligno"
    else:
        print(pred, "Tumor Benigno")
        return pred, "Tumor Benigno"