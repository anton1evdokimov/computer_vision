import os
import numpy as np
from PIL import Image

def load_mask(path: str):
    mask = Image.open(path)
    mask = np.array(mask)/255
    mask = mask.transpose((2,0,1))
    new_channel = np.where(np.sum(mask,axis=0) == 0, 1, 0)
    mask = np.concatenate([mask, new_channel[None,:,:]])

    return mask

def load_image(path: str):
    img = Image.open(path)
    img = np.array(img)/255
    return img