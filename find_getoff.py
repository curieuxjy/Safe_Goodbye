import json
from os import walk
import os
from tqdm import tqdm
from operator import itemgetter

label_path= "D:\\data\\train\\label"

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

# def write_txt(input_list, file_name, indices=False, indices=None):

#     print(">> Writing {}.txt".format(file_name))
#     f = open("D:\\work\\train\\{}.txt".format(file_name), "w")
#     if indices:
#         for i in indices:
#             one_data = input_list[i]+"\n"
#             f.write(one_data)
#         f.close()
#     else:
#         for i in input_list:
#             one_data = i+"\n"
#             f.write(one_data)
#         f.close()

if __name__ =="__main__":
    label_folder, label_list = find_filelist(label_path)
    find_getoff(label_folder)
    # indices = [i for i, x in enumerate(get_off_list) if x > 1]
    # write_txt(get_off_label, file_name="get_off")
    # write_txt(get_off_label, file_name="get_off_over1", indices=True, indices=indices)