import os
from os import walk
from operator import itemgetter
import pandas as pd
from torch.utils.data import Dataset
from torchvision.io import read_image

class BusDataset(Dataset):
    def __init__(self, txt_path, train=True, transform=None, target_transform=None):
        print(">> DATASET LOAD")
        print("label_dir")
        self.label_dir = self.read_txt(txt_path, train=train)
        # [scene, frame(s)]
        self.img_dir = self.get_img_dir(self.label_dir)
        assert len(self.label_dir)==len(self.img_dir)
        # self.label_list = self.get_label_list()
        # self.image_list = self.get_image_list(self.label_list)

        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        assert len(self.label_list) == len(self.image_list)
        return len(self.label_list)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_list[idx])
        image = read_image(img_path)
        label = self.label_list[idx] # [scence, frame(s)]
        skeletons, getoffs = self.get_json(label)
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, img_path, label # 최종은 사람별 스켈레톤 정보와 앵글, 내렸는지 여부 필요

    # def sort_numbering(self, file_list):
    #     before=[]
    #     for i, js in enumerate(file_list):
    #         num = js.split("_")[-1].split(".")[0].zfill(3)
    #         before.append((js, num))
    #     after = sorted(before,key=itemgetter(1))
    #     after = [i[0] for i in after]
    #     return after
    
    def get_img_dir(self, label_dir):
        img_dir = []
        for scene, frames in label_dir:
            img_scene = scene.replace("label", "image")
            img_frames = []
            for f in frames:
                img_frames.append(f.replace("json", "jpg"))
            img_dir.append([img_scene, img_frames])
        return img_dir
            
    # def get_label_list(self):
    #     label_folder=[]
    #     for (dirpath, dirnames, filenames) in walk(self.label_dir):
    #         label_folder.append((dirpath, dirnames, filenames))
            
    #     label_folder = [[i[0], i[2]] for i in label_folder if i[1]==[]]
    #     # folder-scene, frame

    #     for i in range(len(label_folder)):
    #         jsons = label_folder[i][1]
    #         label_folder[i][1] = self.sort_numbering(jsons)
    #     # sorting done
    #     # LABEL_FOLDER  
    #     # [[folder-scene], [frame list(.json)]]
    #     # ['D:\\data\\train\\label\\apt\\[apt]attend_010C',
    #     #           ['[apt]attend_010C_0.json','[apt]attend_010C_2.json', ...]]

    #     # label_list = []
    #     # for scene, frames in label_folder:
    #     #     scene_label = [scene+"\\"+frame for frame in frames]
    #     #     label_list.extend(scene_label)
                
    #     return label_folder

    def get_json(self, label_folder):
        # 풀기는 각자해야 할듯
        label_list = []
        for scene, frames in label_folder:
            scene_label = [scene+"\\"+frame for frame in frames]
            label_list.extend(scene_label)

        with open(label, "r") as js:
            data = json.load(js)

        anno = data["annotation"]
        info = data["info"]
        w, h = info['width'], info["height"]
        anno_num = len(anno)

        return skeletons, getoffs

    def read_txt(self, txt_path, train=True):
        f = open(txt_path, 'r')
        a_list = []
        frames = []
        while True:
            line = f.readline()
            if not line: break
            label_folder = line[:-1]
            for (dirpath, dirnames, filenames) in walk(label_folder):
                a_list.append((dirpath, filenames))
                frames.append(len(filenames))
        f.close()
        if train:
            tag = "train"
            assert tag in txt_path.split("\\")
        else:
            tag = "valid"
            assert tag in txt_path.split("\\")

        print("{} scenes {} frames in {} dataset".format(len(a_list), sum(frames), tag))
        return a_list

if __name__ == "__main__":
    train_labels = read_txt("D:\\data\\train\\train_total.txt", train=True)
    valid_labels = read_txt("D:\\data\\valid\\valid_total.txt", train=False)
    trainset = BusDataset("D:\\data\\train\\train_total.txt", train=True)
    print(trainset.__len__())
    print(trainset.__getitem__(0))