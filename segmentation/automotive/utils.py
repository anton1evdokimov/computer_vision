import torch
import numpy as np
from PIL import Image
from torchvision import transforms

def load_transformed_image(path: str):
    image = Image.open(path)
    image = image.convert('RGB')
    transform = transforms.Compose([
                                    transforms.ToTensor(),
                                    transforms.Resize((720, 1080)),
                                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                                    ])  
    image = transform(image)
    return image