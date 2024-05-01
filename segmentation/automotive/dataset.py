import os
import utils
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from pycocotools.coco import COCO

class RoadSignDataset():
    def __init__(self, coco_annotation_path: str, img_dir = 'sign_dataset/train',
                 pad_shape = (4,4,8,8)):
        self.coco_dataset = COCO(coco_annotation_path)
        self.img_dir = img_dir
        self.cat_ids = self.coco_dataset.getCatIds()
        self.pad_shape = pad_shape

    def __getitem__(self, index):
        img = self.coco_dataset.imgs[index]
        image = utils.load_transformed_image(os.path.join(self.img_dir, img['file_name']))
        mask_one_class = self.__load_mask__(index, image_shape = image.shape[1:])
        pad_transorm = torch.nn.ZeroPad2d(self.pad_shape)
        return pad_transorm(image), pad_transorm(mask_one_class)

    def __len__(self):
        return len(self.coco_dataset.getImgIds())
    
    def __load_mask__(self, index: int, image_shape: tuple):
        img = self.coco_dataset.imgs[index]
        anns_ids = self.coco_dataset.getAnnIds(imgIds=img['id'], catIds=self.cat_ids)
        anns = self.coco_dataset.loadAnns(anns_ids)
        mask = self.coco_dataset.annToMask(anns[0])
        for i in range(len(anns)):
            mask += self.coco_dataset.annToMask(anns[i])
        transforms_mask = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize(image_shape, interpolation=Image.NEAREST),
        ])
        mask_one_class = transforms_mask(np.where(mask > 0, 1, 0)).float()
        return mask_one_class
    

    
    