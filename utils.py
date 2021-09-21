import json
from os import walk
import os
from tqdm import tqdm
from operator import itemgetter


def sort_numbering(file_list):
    before=[]
    for i, js in enumerate(file_list):
        num = js.split("_")[-1].split(".")[0].zfill(3)
        before.append((js, num))
    after = sorted(before,key=itemgetter(1))
    after = [i[0] for i in after]
    return after

def find_filelist(label_path):
    label_folder=[]
    for (dirpath, dirnames, filenames) in walk(label_path):
        label_folder.append((dirpath, dirnames, filenames))
        
    label_folder = [[i[0], i[2]] for i in label_folder if i[1]==[]]
    # folder-scene, frame

    for i in range(len(label_folder)):
        jsons = label_folder[i][1]
        label_folder[i][1] = sort_numbering(jsons)
    # sorting done
    # LABEL_FOLDER  
    # [[folder-scene], [frame list(.json)]]
    # ['D:\\data\\train\\label\\apt\\[apt]attend_010C',
    #           ['[apt]attend_010C_0.json','[apt]attend_010C_2.json', ...]]

    label_list = []
    for scene, frames in label_folder:
        scene_label = [scene+"\\"+frame for frame in frames]
        label_list.extend(scene_label)

    print("You have {} scenes in {}".format(len(label_folder), label_path))
    print("You have {} frames in {}".format(len(label_list), label_path))

    return label_folder, label_list

if __name__=="__main__":
    
    label_path= "D:\\data\\train\\label"
    find_filelist(label_path)