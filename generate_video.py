import re
import os
import cv2
from tqdm import tqdm 
from operator import itemgetter

def generate_video(txt_path:str, tag="train"):
    f = open(txt_path, 'r')
    a_list = []
    while True:
        line = f.readline()
        if not line: break
        a_list.append(line[:-1])
    f.close()

    for i in tqdm(a_list):

        path = i.replace("label", "image") #"D:\\data\\valid\\image\\apt\\[apt]attend_016C\\"
        paths = [os.path.join(path , i ) for i in os.listdir(path) if re.search(".jpg$", i )]
        num_list = [i[:-4].split("_")[-1] for i in paths]
        # pathIn= "D:\\data\\train\\label\\district\\[district]day_440B\\"
        name = i.split("\\")[-1]
        pathOut = 'D:\\data\\{}\\video\\'.format(tag)+name+".mp4"
        fps = 10

        before=[]
        for num, path in zip(num_list, paths):
            num = str(num).zfill(3)
            before.append((num, path))
        after = sorted(before,key=itemgetter(0))
        after = [i[1] for i in after]

        size=0
        frame_array = []
        for idx , path in enumerate(after) : 
            img = cv2.imread(path)
            height, width, layers = img.shape
            size = (width,height)
            frame_array.append(img)
        out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

        for i in range(len(frame_array)):
            # writing to a image array
            out.write(frame_array[i])
        out.release()

if __name__ =="__main__":
    valid_path = "D:\\data\\valid\\valid_total.txt"
    train_path = "D:\\data\\train\\train_total.txt"
    print(">> Generating Valid videos")
    generate_video(valid_path, tag="valid")
    print(">> Generating Train videos")
    generate_video(train_path, tag="train")
    