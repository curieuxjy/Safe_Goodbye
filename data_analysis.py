"""
DATA ANALYSIS
- 각 Scene당 frame 수
- 한 프레임에서 보이는 사람의 수 max, min
"""
import json
import pandas as pd
import seaborn as sns
from tqdm import tqdm
from operator import itemgetter
from utils import *
import warnings
warnings.filterwarnings("ignore")

def write_txt(input_list, file_name:str, train=True):

    print(">> Writing {}.txt".format(file_name))
    if train:
        f = open("D:\\data\\train\\{}.txt".format(file_name), "w")
    else:
        f = open("D:\\data\\valid\\{}.txt".format(file_name), "w")

    for i in input_list:
        one_data = i+"\n"
        f.write(one_data)
    f.close()

def caculate_frame_num(label_folder,
                        MIN, MAX,
                        train=True):
    num_frame=[]
    scene_list=[]
    for scene, frames in label_folder:
        num_frame.append(len(frames))
        if len(frames)<MIN:
            pass
        elif len(frames)>MAX:
            pass
        else:
            scene_list.append(scene)

    num_frame = pd.DataFrame(num_frame)
    if train:
        num_frame.columns = ["train_frames"]
    else:
        num_frame.columns = ["valid_frames"]
    return num_frame, scene_list

def check_frame(train_frames, valid_frames):
    # dataframe
    num_frame = pd.concat([train_frames, valid_frames], axis=1)

    sns_plot = sns.histplot(data=num_frame, kde=True)
    fig = sns_plot.get_figure()
    fig.savefig(".\\assets\\check_frame.png")

def check_people(label_folder):
    people_in_one_frame = []
    people_in_one_scene = []

    for scene, frames in label_folder:
        people_in_one_scene = []
        scene_label = [scene+"\\"+frame for frame in frames]
        scene_person_id=set()

        for path in scene_label:
            with open(path, "r") as js:
                data = json.load(js)

if __name__=="__main__":
    train_label_path= "D:\\data\\train\\label"
    valid_label_path= "D:\\data\\valid\\label"
    MIN = 98
    MAX = 119
    train_label_folder, train_label_list = find_filelist(train_label_path)
    valid_label_folder, valid_label_list = find_filelist(valid_label_path)

    train_frames, train_scene_list = caculate_frame_num(train_label_folder, MIN=MIN, MAX=MAX, train=True)
    print(train_frames.describe())
    write_txt(train_scene_list, "train_total", train=True)
    valid_frames, valid_scene_list = caculate_frame_num(valid_label_folder, MIN=MIN, MAX=MAX, train=False)
    print(valid_frames.describe())
    write_txt(valid_scene_list, "valid_total", train=False)
    check_frame(train_frames, valid_frames)

    # label_folder, _ = find_filelist(label_path)
