import os
from os import walk
import pandas as pd
from torch.utils.data import Dataset
from torchvision.io import read_image

class BusDataset(Dataset):
    def __init__(self, label_dir, img_dir, transform=None, target_transform=None):
#         self.img_labels = pd.read_csv(annotations_file)
        self.label_dir = label_dir
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
        self.label_list = self.get_label_list()
        self.image_list = self.get_image_list()

    def __len__(self):
        assert len(self.label_list) == len(self.image_list)
        return len(self.label_list)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_list[idx])
        image = read_image(img_path)
        label = self.label_list[idx]
        label = self.get_json(label)
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label
    
    def get_image_list(self):
        image_folder=[]
        for (dirpath, dirnames, filenames) in walk(self.img_dir):
            image_folder.append((dirpath, dirnames, filenames)) # directory

        # print(image_folder)

        clean=[]
        for i in range(len(image_folder)):
            if len(image_folder[i][0].split("\\"))<6:
                pass
            else:
                clean.append(image_folder[i])
        for i in range(len(clean)):
            if clean[i][1]!=[]:
                print("nope")
            else:
                clean[i] = (clean[i][0], clean[i][2])        
        image_list=[]
        for root, files in clean:
            for file in files:
                image_path = root+"\\"+file
                image_list.append(image_path)
                
        return image_list
            
    def get_label_list(self):
        label_folder=[]
        for (dirpath, dirnames, filenames) in walk(self.label_dir):
            label_folder.append((dirpath, dirnames, filenames)) # directory
            
        clean=[]
        for i in range(len(label_folder)):
            if len(label_folder[i][0].split("\\"))<6:
                pass
            else:
                clean.append(label_folder[i])

        for i in range(len(clean)):
            if clean[i][1]!=[]:
                print("nope")
            else:
                clean[i] = (clean[i][0], clean[i][2])

        # print(clean[0])        
        label_list=[]
        for root, files in clean:
            for file in files:
                label_path = root+"\\"+file
                label_list.append(label_path)
                
        return label_list

    def get_json(self, label):
        with open(label, "r") as st_json:
            data = json.load(st_json)
        anno = data["annotation"]
        info = data["info"]
        w, h = info['width'], info["height"]
        anno_num = len(anno)
        for in range()


if __name__ == "__main__":

    a = BusDataset("D:\\work\\train\\label", "D:\\work\\train\\image")
    print(a.__len__())
    print(a.__getitem__(0))