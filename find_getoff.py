import json
from os import walk
import os
from tqdm import tqdm
from operator import itemgetter
from utils import *

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



if __name__ =="__main__":
    label_path= "D:\\data\\train\\label"
    label_folder, label_list = find_filelist(label_path)
    find_getoff(label_folder)
    # indices = [i for i, x in enumerate(get_off_list) if x > 1]
    # write_txt(get_off_label, file_name="get_off")
    # write_txt(get_off_label, file_name="get_off_over1", indices=True, indices=indices)