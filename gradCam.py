import os
import cv2
import numpy as np
import torch
from torchvision import models
from pytorch_grad_cam import (
    GradCAM, HiResCAM, ScoreCAM, GradCAMPlusPlus,
    AblationCAM, XGradCAM, EigenCAM, EigenGradCAM,
    LayerCAM, FullGrad, GradCAMElementWise
)
from pytorch_grad_cam import GuidedBackpropReLUModel
from pytorch_grad_cam.utils.image import (
    show_cam_on_image, deprocess_image, preprocess_image
)
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget


def generate_cam(image_path, method='gradcam', device='cpu', aug_smooth=False, eigen_smooth=False, output_dir='uploads'):
    methods = {
        "gradcam": GradCAM,
        "hirescam": HiResCAM,
        "scorecam": ScoreCAM,
        "gradcam++": GradCAMPlusPlus,
        "ablationcam": AblationCAM,
        "xgradcam": XGradCAM,
        "eigencam": EigenCAM,
        "eigengradcam": EigenGradCAM,
        "layercam": LayerCAM,
        "fullgrad": FullGrad,
        "gradcamelementwise": GradCAMElementWise
    }

    model = models.resnet50(pretrained=True).to(torch.device(device)).eval()

    # Choose the target layer you want to compute the visualization for.
    target_layers = [model.layer4]

    rgb_img = cv2.imread(image_path, 1)[:, :, ::-1]
    rgb_img = np.float32(rgb_img) / 255
    input_tensor = preprocess_image(rgb_img,
                                    mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225]).to(device)

    targets = None

    cam_algorithm = methods[method]
    with cam_algorithm(model=model,
                       target_layers=target_layers) as cam:

        cam.batch_size = 32
        grayscale_cam = cam(input_tensor=input_tensor,
                            targets=targets,
                            aug_smooth=aug_smooth,
                            eigen_smooth=eigen_smooth)

        grayscale_cam = grayscale_cam[0, :]

        cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        cam_image = cv2.cvtColor(cam_image, cv2.COLOR_RGB2BGR)

    gb_model = GuidedBackpropReLUModel(model=model, device=device)
    gb = gb_model(input_tensor, target_category=None)

    cam_mask = cv2.merge([grayscale_cam, grayscale_cam, grayscale_cam])
    cam_gb = deprocess_image(cam_mask * gb)
    gb = deprocess_image(gb)

    os.makedirs(output_dir, exist_ok=True)
    final_name = (image_path.split('.'))[0]
    image_final_name = f'{final_name}_cam.jpg'
    cam_output_path = os.path.join(output_dir, image_final_name)
    
    image_final_path = f'{output_dir}/{final_name}_cam.jpg'

    cv2.imwrite(cam_output_path, cam_image)
    #cv2.imwrite(gb_output_path, gb)
    #cv2.imwrite(cam_gb_output_path, cam_gb)
    
    return image_final_path