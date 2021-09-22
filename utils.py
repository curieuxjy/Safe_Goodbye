import json
from os import walk
import os
from tqdm import tqdm
from operator import itemgetter

body_points_tag = ["r_ankle", "r_knee", "r_hip", "l_hip", "l_knee", "l_ankle", "hip", "chest", "neck",
                    "head", "r_wrist", "r_elbow", "r_shoulder", "l_shoulder", "l_elbow", "l_wrist"]

keypoint_names =   {0: 'r_ankle',
                    1: 'r_knee',
                    2: 'r_hip',
                    3: 'l_hip',
                    4: 'l_knee',
                    5: 'l_ankle',
                    6: 'hip',
                    7: 'chest',
                    8: 'neck',
                    9: 'head',
                    10: 'r_wrist',
                    11: 'r_elbow',
                    12: 'r_shoulder',
                    13: 'l_shoulder',
                    14: 'l_elbow',
                    15: 'l_wrist'}

edges = [(9, 8), (8, 7), (7, 12), (12, 11), (11, 10), (7, 13), (13, 14),
         (14, 15), (7, 6), (6, 2), (2, 1), (1, 0), (6, 3),
         (3, 4), (4, 5)]

ankles = [(9, 8, 7),
          (8, 7, 12),
          (11, 12, 7),
          (10, 11, 12),
          (13, 7, 8),
          (7, 13, 14),
          (13, 14, 15),
          (7, 6, 2),
          (6, 2, 1),
          (2, 1, 0),
          (7, 6, 3),
          (6, 3, 4),
          (3, 4, 5)]

def calculate_angle(left_point, center_point, right_point):
    return angle

def draw_keypoints(image,
                   keypoints,
                   edges= None,
                   ankles= None,
                   keypoint_names= None,
                   dpi: int = 200):
    """
    Args:
        image (ndarray): [H, W, C]
        keypoints (ndarray): [N, 3]
        edges (List(Tuple(int, int))): 
    """
    np.random.seed(42)
    colors = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}

#     if boxes:
#         x1, y1 = min(keypoints[:, 0]), min(keypoints[:, 1])
#         x2, y2 = max(keypoints[:, 0]), max(keypoints[:, 1])
#         cv2.rectangle(image, (x1, y1), (x2, y2), (255, 100, 91), thickness=3)

    for k, v in keypoints.items():
#         print(k, v)
        cv2.circle(
            image, 
            v, 
            3, colors.get(k), thickness=3, lineType=cv2.FILLED)

        if keypoint_names is not None:
            cv2.putText(
                image, 
                f'{k}', 
                keypoints[k], 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    if edges is not None:
        for i, edge in enumerate(edges):
            cv2.line(
                image, 
                keypoints[keypoint_names[edge[0]]], 
                keypoints[keypoint_names[edge[1]]],
                colors.get(edge[0]), 3, lineType=cv2.LINE_AA)
    
    fig, ax = plt.subplots(dpi=dpi)
    if ankles is not None:
        for i, (l, c, r) in enumerate(ankles[:5]):
            AngleAnnotation(keypoints[keypoint_names[c]],
                            keypoints[keypoint_names[l]],
                            keypoints[keypoint_names[r]],
                            ax = ax, size=20, linestyle="--", color="green",
                            text="{}".format(i), textposition="outside",
                            text_kw=dict(fontsize=10, color="green"))
    ax.imshow(image)
    ax.axis('off')
    plt.show()
    fig.savefig('example.png')

def cut_bbox():
    return crop_img # n

def mod_keypoints():
    return mod_keypoint

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
    
    # label_path= "D:\\data\\train\\label"
    # find_filelist(label_path)

    img_path = r"D:\data\train\image\apt\[apt]attend_016C"
    img_path = img_path+"\[apt]attend_016C_0.jpg"
    img = mpimg.imread(img_path)
    imgplot = plt.imshow(img)

    draw_keypoints(crop_img, body_points, edges, ankles, keypoint_names, dpi=150)