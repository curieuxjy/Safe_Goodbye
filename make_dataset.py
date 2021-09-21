import json
from os import walk
import csv
from tqdm import tqdm
from operator import itemgetter
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

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

def check_people(label_folder, train=True):
    people_in_one_scene = []

    for scene, frames in tqdm(label_folder):
        frame_label = [scene+"\\"+frame for frame in frames]
        max_person=-1

        for path in frame_label:
            with open(path, "r") as js:
                data = json.load(js)

            if data["annotations"]==[]:
                pass
            else:
                for i in range(len(data["annotations"])):
                    person_id = data["annotations"][i]["id"]
                    if max_person<person_id:
                        max_person=person_id
                    
        people_in_one_scene.append(max_person)

    if train:
        tag = "train"
        assert len(people_in_one_scene) == 1200
    else:
        tag = "valid"
        assert len(people_in_one_scene) == 222

    return people_in_one_scene

def calculate_angle(keypoint):
    angle = 0
    return angle

def write_csv(label_folder, people_in_one_scene_list, train=True):
    assert len(label_folder)==len(people_in_one_scene_list)

    for i, (scene, frames) in tqdm(enumerate(label_folder)):
        one_dict=dict()
        one_dict["scene"] = scene.split("\\")[-1]
        frames_50 = frames[:50] # cut in 50 frames
        frame_label = [scene+"\\"+frame for frame in frames_50]

        dict_list=[]
        # print(people_in_one_scene_list)
        if people_in_one_scene_list[i] == -1:
            pass
        else:
            for person in range(people_in_one_scene_list[i]): # num ppl
                # print(person)
                id_dict = one_dict.copy()
                id_dict["id"]=person
                id_dict["keypoints"]=[]
                id_dict["frame_num"]=[]
                id_dict["angles"]=[]
                id_dict["get_off"]=[]
                dict_list.append(id_dict)
            # dict_list
            # [one_list(id==0), one_list(id==1), one_list(id==2), ...] 
            # len(dict_list) == people_in_one_scene

            for f_index, path in enumerate(frame_label):
                with open(path, "r") as js:
                    data = json.load(js)

                if data["annotations"]==[]:
                    pass
                else:
                    for anno in range(len(data["annotations"])):
                        one_anno = data["annotations"][anno]
                        person_id = one_anno["id"] # 해당 사람 찾기
                        print("-"*100)
                        print(len(dict_list))
                        print(person_id)
                        print(dict_list[person_id]["scene"])
                        print(dict_list[person_id]["frame_num"])
                        print(dict_list[person_id]["id"], one_anno["id"])
                        assert dict_list[person_id]["id"] == one_anno["id"]
                        # print(dict_list[person_id])
                        dict_list[person_id]["keypoints"].append(one_anno["keypoints"])
                        dict_list[person_id]["get_off"].append(one_anno["get_off"])
                        dict_list[person_id]["frame_num"].append(f_index)
                        angle = calculate_angle(one_anno["keypoints"])
                        dict_list[person_id]["angles"].append(angle)
    if train:
        tag = "train"
    else:
        tag = "valid"

    with open('./tmp_{}.csv'.format(tag), 'a', newline='') as csvfile:
        fieldnames = ["scene", "id", "frame_num", "keypoints", "angles"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for one_data in dict_list:
            writer.writerow(one_data)

def sort_numbering(file_list):
    before=[]
    for i, js in enumerate(file_list):
        num = js.split("_")[-1].split(".")[0].zfill(3)
        before.append((js, num))
    after = sorted(before,key=itemgetter(1))
    after = [i[0] for i in after]
    return after

def find_filelist_50(txt_path, train=True):
    f = open(txt_path, 'r')
    label_folder = []
    frames = []
    while True:
        line = f.readline()
        if not line: break
        txt_line = line[:-1]
        for (dirpath, dirnames, filenames) in walk(txt_line):
            label_folder.append([dirpath, filenames])
            frames.append(len(filenames))
    f.close()
    # folder-scene, frame
    for i in range(len(label_folder)):
        jsons = label_folder[i][1] # tuple
        label_folder[i][1] = sort_numbering(jsons)
    # sorting done
    # LABEL_FOLDER  
    # [[folder-scene], [frame list(.json)]]
    # ['D:\\data\\train\\label\\apt\\[apt]attend_010C',
    #           ['[apt]attend_010C_0.json','[apt]attend_010C_2.json', ...]]
    
    if train:
        tag = "train"
    else:
        tag = "valid"

    print("{} scenes {} frames in {} dataset".format(len(label_folder), sum(frames), tag))

    label_list_50 = []
    for scene, frames in label_folder:
        frames_50 = frames[:50] # cut in 50 frames
        frame_label = [scene+"\\"+frame for frame in frames_50]
        label_list_50.extend(frame_label)

    print("You have {} scenes in {}".format(len(label_folder), txt_path))
    print("You have {} frames in {} (cut in 50 frames)".format(len(label_list_50), txt_path))

    return label_folder, label_list_50

if __name__=="__main__":

    train_label_folder, train_label_list_50 = find_filelist_50("D:\\data\\train\\train_total.txt", train=True)
    valid_label_folder, valid_label_list_50 = find_filelist_50("D:\\data\\valid\\valid_total.txt", train=False)

    print(">> Checking people")
    people_in_one_scene_train = check_people(train_label_folder, train=True)
    people_in_one_scene_valid = check_people(valid_label_folder, train=False)

    print("Writing train CSV")
    write_csv(train_label_folder, people_in_one_scene_train, train=True)
    print("Writing valid CSV")
    write_csv(valid_label_folder, people_in_one_scene_valid, train=False)
