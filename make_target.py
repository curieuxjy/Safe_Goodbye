import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import json
from os import walk
import matplotlib.pyplot as plt
from utils import *
from matplotlib.patches import Arc
from matplotlib.transforms import IdentityTransform, TransformedBbox, Bbox

def get_person(anno):
    person_id = anno["id"]
    bbox = anno["bbox"]
    keypoint = anno["keypoints"]
    get_off = anno["get_off"]
    return person_id, bbox, keypoint, get_off

def get_bodypoint(keypoint):
    xs = [d for i, d in enumerate(keypoint) if i%3==0]
    ys = [d for i, d in enumerate(keypoint) if i%3==1]
    body_points={}
    for i in range(len(xs)):
        body_points[KEYPOINTS_TAG[i]] = (xs[i], ys[i])
    return body_points

def draw_keypoints(image,
                   keypoints,
                   edges= None,
                   boxes = None,
                   get_off=False,
                   keypoint_names= None,
                   dpi: int = 200):

    np.random.seed(42)
    colors = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}

    if boxes:
        x1 = boxes[0] # xmin
        y1 = boxes[1] # ymin
        x2 = boxes[2] # xmax
        y2 = boxes[3] # ymax
        if get_off:
            color = (255, 0, 91)
        else:
            color = (255, 255, 91)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness=5)

    for k, v in keypoints.items():
        cv2.circle(
            image, 
            v, 
            3, colors.get(k), thickness=3, lineType=cv2.FILLED)

    if edges is not None:
        for i, edge in enumerate(edges):
            cv2.line(
                image, 
                keypoints[keypoint_names[edge[0]]], 
                keypoints[keypoint_names[edge[1]]],
                colors.get(edge[0]), 3, lineType=cv2.LINE_AA)
    
    fig, ax = plt.subplots(dpi=dpi)
    ax.imshow(image)
    ax.axis('off')
    # plt.show()
    return fig

def draw_keypoints2(image,
                   keypoints,
                   edges= None,
                   boxes = None,
                   get_off=False,
                   keypoint_names= None,
                   dpi: int = 200):

    np.random.seed(42)
    colors = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}

    if boxes:
        x1 = boxes[0] # xmin
        y1 = boxes[1] # ymin
        x2 = boxes[2] # xmax
        y2 = boxes[3] # ymax
        color = (255, 255, 255)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness=5)

    for k, v in keypoints.items():
        cv2.circle(
            image, 
            v, 
            3, colors.get(k), thickness=3, lineType=cv2.FILLED)

    if edges is not None:
        for i, edge in enumerate(edges):
            cv2.line(
                image, 
                keypoints[keypoint_names[edge[0]]], 
                keypoints[keypoint_names[edge[1]]],
                colors.get(edge[0]), 3, lineType=cv2.LINE_AA)
    
    fig, ax = plt.subplots(dpi=dpi)
    ax.imshow(image)
    ax.axis('off')
    # plt.show()
    return fig

if __name__=="__main__":
    path_folder=[]
    path = "C:\\Users\\Jungyeon\\Desktop\\Arrival_project\\target\\together\\"

    for (dirpath, dirnames, filenames) in walk(path):
        path_folder.append((dirpath, dirnames, filenames))

    target1 = (path_folder[1][0], sort_numbering(path_folder[1][2]))
    target2 = (path_folder[2][0], sort_numbering(path_folder[2][2]))

    # img list
    target1_list = [target1[0]+"\\"+target1[1][i] for i in range(len(target1[1]))]
    target1_imglist = [target1_list[i] for i in range(len(target1_list)) if i%2==0]
    target1_lablist = [target1_list[i] for i in range(len(target1_list)) if i%2==1]
    target2_list = [target2[0]+"\\"+target2[1][i] for i in range(len(target2[1]))]
    target2_imglist = [target2_list[i] for i in range(len(target2_list)) if i%2==0]
    target2_lablist = [target2_list[i] for i in range(len(target2_list)) if i%2==1]

    ##  get one img
    frame_num = 0
    for i in range(len(target1_imglist)):
        frame_num += 1
        img = mpimg.imread(target1_imglist[i])
        lab = target1_lablist[i]
        with open(lab, "r") as st_json:
            js = json.load(st_json)

        anno = js["annotations"]
        if frame_num>40:
            for k in range(len(anno)):
                person_id_, bbox_, keypoint_, get_off_ = get_person(anno[k])
                fig = draw_keypoints(img,
                                    get_bodypoint(keypoint_),
                                    EDGES,
                                    bbox_,
                                    get_off_,
                                    KEYPOINT_NAMES,
                                    dpi=150)
        else :
            for k in range(len(anno)):
                person_id_, bbox_, keypoint_, get_off_ = get_person(anno[k])
                fig = draw_keypoints2(img,
                                    get_bodypoint(keypoint_),
                                    EDGES,
                                    bbox_,
                                    get_off_,
                                    KEYPOINT_NAMES,
                                    dpi=150)

        fig.savefig("./target1/{}".format(str(frame_num).zfill(3)))


    frame_num = 0
    for i in range(len(target2_imglist)):
        frame_num += 1
        img = mpimg.imread(target2_imglist[i])
        lab = target2_lablist[i]
        with open(lab, "r") as st_json:
            js = json.load(st_json)

        anno = js["annotations"]
        if frame_num>40:
            for k in range(len(anno)):
                person_id_, bbox_, keypoint_, get_off_ = get_person(anno[k])
                fig = draw_keypoints(img,
                                    get_bodypoint(keypoint_),
                                    EDGES,
                                    bbox_,
                                    get_off_,
                                    KEYPOINT_NAMES,
                                    dpi=150)
        else :
            for k in range(len(anno)):
                person_id_, bbox_, keypoint_, get_off_ = get_person(anno[k])
                fig = draw_keypoints2(img,
                                    get_bodypoint(keypoint_),
                                    EDGES,
                                    bbox_,
                                    get_off_,
                                    KEYPOINT_NAMES,
                                    dpi=150)

        fig.savefig("./target2/{}".format(str(frame_num).zfill(3)))


    ## get one json
    ## # get one_person / ...
    ## save fig

    # img_path = r"C:\Users\Jungyeon\Desktop\Arrival_project\target\together\[district]attend_024C\[district]attend_024C_100.jpg"
    # img = mpimg.imread(img_path)
    # label_path = img_path.replace("jpg", "json")
    # with open(label_path, "r") as st_json:
    #     js = json.load(st_json)

    # anno = js["annotations"]

    # fig = draw_keypoints(img, get_bodypoint(keypoint_2), EDGES, bbox_2, get_off_2, KEYPOINT_NAMES, dpi=150)
    # fig.savefig('example.png')
