"""
DATA ANALYSIS
- 각 Scene당 frame 수
- 한 프레임에서 보이는 사람의 수 max, min
"""
import json
from os import walk
import pandas as pd
import seaborn as sns
from tqdm import tqdm
from operator import itemgetter
import matplotlib.pyplot as plt
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

def read_txt(txt_path, train=True):
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
    else:
        tag = "valid"

    print("{} scenes {} frames in {} dataset".format(len(a_list), sum(frames), tag))
    return a_list

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

def check_people_plot(people_in_one_scene, people_in_one_frame, tag):
    sns_plot_scene = sns.histplot(data=people_in_one_scene,x="people_in_one_scene", discrete=True, shrink=.8)
    sns_plot_scene.set_title("People in one Scene {}".format(tag))
    fig_scene = sns_plot_scene.get_figure()
    fig_scene.savefig(".\\assets\\people_in_one_scene_{}.png".format(tag))
    fig_scene.clf()
    sns_plot_frame = sns.histplot(data=people_in_one_frame,x="people_in_one_frame", discrete=True, shrink=.8)
    sns_plot_frame.set_title("People in one Frame {}".format(tag))
    fig_frame = sns_plot_frame.get_figure()
    fig_frame.savefig(".\\assets\\people_in_one_frame_{}.png".format(tag))
    fig_frame.clf()

def check_people(label_folder, train=True):
    people_in_one_frame = []
    people_in_one_scene = []

    for scene, frames in tqdm(label_folder):
        scene_label = [scene+"\\"+frame for frame in frames]
        one_scene=set()

        for path in scene_label:
            with open(path, "r") as js:
                data = json.load(js)

            if data["annotations"]==[]:
                    one_frame = 0
            else:
                one_frame = len(data["annotations"])
                for i in range(len(data["annotations"])):
                    person_id = data["annotations"][i]["id"]
                    one_scene.add(person_id)
            people_in_one_frame.append(one_frame)
        people_in_one_scene.append(len(one_scene))
    
    people_in_one_scene = pd.DataFrame(people_in_one_scene)
    people_in_one_scene.columns = ["people_in_one_scene"]
    people_in_one_frame = pd.DataFrame(people_in_one_frame)
    people_in_one_frame.columns = ["people_in_one_frame"]

    if train:
        tag = "train"
        assert len(people_in_one_scene) == 1200
        assert len(people_in_one_frame) == 129986
    else:
        tag = "valid"
        assert len(people_in_one_scene) == 222
        assert len(people_in_one_frame) == 23720

    check_people_plot(people_in_one_scene, people_in_one_frame, tag)

def find_getoff(label_folder):
    
    num_getoff_ppl=[]
    num_not_getoff_ppl=[]

    for scene, frames in label_folder:
        scene_label = [scene+"\\"+frame for frame in frames]
        getoff_person_id=set()
        not_getoff_person_id=set()

        for path in scene_label:
            with open(path, "r") as js:
                data = json.load(js)
                
                # 데이터 없는 사진은 제외
                if data["annotations"]==[]:
                    pass
                else:
                    for i in range(len(data["annotations"])):
                        get_off = data["annotations"][i]["get_off"]
                        person_id = data["annotations"][i]["id"]
                        if get_off == True:
                            getoff_person_id.add(person_id)
                        else:
                            not_getoff_person_id.add(person_id)

        num_getoff_ppl.append(len(getoff_person_id))
        num_not_getoff_ppl.append(len(not_getoff_person_id))

    assert len(num_getoff_ppl)==len(num_not_getoff_ppl)
    print("-"*30)
    print("There are {} get off people.".format(sum(num_getoff_ppl)))
    print("There are {} NOT get off people.".format(sum(num_not_getoff_ppl)))
    print("-"*30)
    return sum(num_getoff_ppl), sum(num_not_getoff_ppl)

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

    train_labels = read_txt("D:\\data\\train\\train_total.txt", train=True)
    valid_labels = read_txt("D:\\data\\valid\\valid_total.txt", train=False)
    print(">> Checking people")
    check_people(train_labels, train=True)
    check_people(valid_labels, train=False)

    print(">> Finding GET OFF people")
    train_getoff, train_not_getoff = find_getoff(train_labels)
    valid_getoff, valid_not_getoff = find_getoff(valid_labels)

    alpha = 0.5
    index = ["Train", "Valid"]
    p1 = plt.bar(index, [train_getoff, valid_getoff], color='b', alpha=alpha)
    p2 = plt.bar(index, [train_not_getoff, valid_not_getoff], color='r', alpha=alpha, bottom=[train_getoff, valid_getoff]) # stacked bar chart
    plt.legend((p1[0], p2[0]), ("Get off True", "Get off False"), fontsize=15)
    plt.title('Get off ratio in Train/Valid dataset', fontsize=20)
    plt.savefig(".\\assets\\get_off_ratio.png")
    plt.clf()
