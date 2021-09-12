import json
from os import walk
import os
from tqdm import tqdm

label_path= "D:\\work\\trainb\\label"

label_folder=[]
for (dirpath, dirnames, filenames) in tqdm(walk(label_path)):
    label_folder.append((dirpath, dirnames, filenames)) # directory

clean=[]
for i in tqdm(range(len(label_folder))):
    if len(label_folder[i][0].split("\\"))<6:
        pass
    else:
        clean.append(label_folder[i])

# checking
for i in range(len(clean)):
    if clean[i][1]!=[]:
        print("nope")
    else:
        clean[i] = (clean[i][0], clean[i][2])


label_list=[]
for root, files in clean:
    root_path=root
    for file in files:
        image_path = root+"\\"+file
        label_list.append(image_path)

print("You have {} labels in {}".format(len(label_list), label_path))

get_off_list=[]
get_off_label=[]
for path in tqdm(label_list):
    with open(path, "r") as st_json:
        data = json.load(st_json)
        
        # 데이터 없는 사진은 제외
        if data["annotations"]==[]:
            pass
        else:
            is_getoff_true=0
            for i in range(len(data["annotations"])):
                # 겟오프 부분만 가져와서
                get_off = data["annotations"][i]["get_off"]
                # 하차하는 사람이 있다면
                if get_off == True:
                    is_getoff_true+= 1
                    
            if is_getoff_true != 0:
                get_off_label.append(path) # 1번 이상 어노테이션 되어 있는 데이터 라벨
                get_off_list.append(is_getoff_true) # 몇번 true로 어노테이션 되어 있는지

assert len(get_off_list) == len(get_off_label) 
print("-"*30)
print("There are {} get off(True) labels.".format(sum(get_off_list)))
print("There are {} labels with more than one get off".format(len(get_off_label)))
print("-"*30)

print(">> Writing get_off_all.txt")
f = open("D:\\work\\trainb\\get_off_all.txt", "w")
for i in get_off_label:
    # print(get_off_label[i])
    label_one_path = i+"\n"
    f.write(label_one_path)
f.close()

indices = [i for i, x in enumerate(get_off_list) if x > 1]

print(">> Writing get_off_find.txt")
f = open("D:\\work\\trainb\\get_off_find.txt", "w")
for i in indices:
    # print(get_off_label[i])
    label_one_path = get_off_label[i]+"\n"
    f.write(label_one_path)
f.close()