import os
import numpy as np
# import torch
from PIL import Image
import matplotlib.pyplot as plt

from segmentation.satellite.utils import load_image, load_mask  
# from torchvision import transforms

class SatelliteDataset():
    def __init__(self, img_dir = 'dataset'):

        self.img_dir = os.path.join(img_dir, "images/train")
        self.mask_dir = os.path.join(img_dir, "mask/train")
    
        self.img_pathes = []
        self.masks_pathes = []

        for file_path in os.walk(self.img_dir):
            self.img_pathes.extend(file_path[-1])

        for file_path in os.walk(self.mask_dir):
            self.masks_pathes.extend(file_path[-1])

        self.img_pathes.sort()
        self.masks_pathes.sort()
        
    def __getitem__(self, index):
        mask_path = self.masks_pathes[index]
        img_path = self.img_pathes[index]

        mask = load_mask(mask_path)
        img = load_image(img_path)

        return mask, img

    def __len__(self):
        return len(self.pathes)


if __name__ == "__main__":
    mask = load_mask("dataset/mask/train/img_resize_1002_mask.png")
    print(mask.shape)
    # plt.show()
    # print(np.unique(np.array(Image.open("dataset/mask/train/img_resize_1002_mask.png"))[:,:,2]))