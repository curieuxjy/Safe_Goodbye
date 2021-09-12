import re
import os
from operator import itemgetter
import cv2
from tqdm import tqdm 

f = open("D:\\work\\trainc\\get_off_notframe.txt", 'r')
a_list = []
while True:
    line = f.readline()
    if not line: break
    a_list.append(line[:-1])
f.close()

for i in tqdm(a_list):

    path = i.replace("label", "image") #"D:\\work\\trainc\\image\\apt\\[apt]attend_016C\\"
    # print(path)
    paths = [os.path.join(path , i ) for i in os.listdir(path) if re.search(".jpg$", i )]
    num_list = [i[:-4].split("_")[-1] for i in paths]
    # pathIn= "D:\\work\\trainb\\label\\district\\[district]day_440B\\"
    name = i.split("\\")[-1]
    pathOut = 'D:\\work\\trainc\\video\\'+name+".mp4"
    fps = 15

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
        print()
        print("------------------------------------------", path)
        height, width, layers = img.shape
        size = (width,height)
        frame_array.append(img)
    # print(pathOut)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()