import tensorflow as tf
from PIL import Image
import numpy as np
import cv2

def main():
    model_path = "model/model.h5"
    loaded_model = tf.keras.models.load_model(model_path)

    image = cv2.imread("tem.png")

    image_fromarray = Image.fromarray(image, 'RGB')
    resize_image = image_fromarray.resize((224, 224))
    expand_input = np.expand_dims(resize_image,axis=0)
    input_data = np.array(expand_input)
    input_data = input_data/255

    pred = loaded_model.predict(input_data)
    if pred >= 0.5:
        print("Yes")
    else:
        print("No")
        
if __name__ == "__main__":
    main()