def sortByNumber(path):
  return int(re.findall(r'\d+', path)[0])


class SatelliteDataset():
    def __init__(self, ds_type = "train", path=configs['dataset_dir'], pad_shape = (6,6,9,9)):

        self.IMAGE_HEIGHT=180
        self.IMAGE_WIDTH=270
        self.img_dir = os.path.join(path, f"images/{ds_type}")
        self.mask_dir = os.path.join(path, f"mask/{ds_type}")
        self.pad_shape = pad_shape
    
        self.img_pathes = []
        self.mask_pathes = []

        for file_path in os.walk(self.img_dir):
            self.img_pathes.extend(list(filter(lambda x: x.endswith(".png"), file_path[-1])))

        for file_path in os.walk(self.mask_dir):
            self.mask_pathes.extend(list(filter(lambda x: x.endswith(".png"), file_path[-1])))
        self.img_pathes.sort(key=sortByNumber)
        self.mask_pathes.sort(key=sortByNumber)
        

    def __getitem__(self, index):
        mask_path = self.mask_pathes[index]
        img_path = self.img_pathes[index]
        print(f"img_path: {img_path}, mask_path: {mask_path}")

        mask = load_mask(os.path.join(self.mask_dir, mask_path))
        img = load_image(os.path.join(self.img_dir, img_path))

        print(f"img shape: {img.shape}, mask shape: {mask.shape}")
        aug = A.Compose(
          [
              A.RandomCrop(p=0.5, height=self.IMAGE_HEIGHT, width=self.IMAGE_WIDTH),
              A.Resize(height=self.IMAGE_HEIGHT, width=self.IMAGE_WIDTH)
           ],
          is_check_shapes=False
        )
        aug_data = aug(image=img, mask=mask)

        pad_transorm = torch.nn.ZeroPad2d(self.pad_shape)

        image = pad_transorm(torch.FloatTensor(aug_data['image'].transpose((2,0,1))))
        mask = pad_transorm(torch.FloatTensor(aug_data['mask'].transpose((2,0,1))))
        
        # print("img.shape aug_data['image'] ", aug_data['image'].shape)
        return image, mask

    def __len__(self):
        return len(self.img_pathes)