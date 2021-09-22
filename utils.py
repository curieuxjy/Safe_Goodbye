import json
import os
import cv2
import numpy as np
from os import walk
from tqdm import tqdm
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Arc
from matplotlib.transforms import IdentityTransform, TransformedBbox, Bbox

KEYPOINTS_TAG = ["r_ankle", "r_knee", "r_hip", "l_hip", "l_knee", "l_ankle", "hip", "chest", "neck",
                    "head", "r_wrist", "r_elbow", "r_shoulder", "l_shoulder", "l_elbow", "l_wrist"]

KEYPOINT_NAMES =   {0: 'r_ankle',
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

EDGES = [(9, 8), (8, 7), (7, 12), (12, 11), (11, 10), (7, 13), (13, 14),
         (14, 15), (7, 6), (6, 2), (2, 1), (1, 0), (6, 3),
         (3, 4), (4, 5)]

# left, center, right
ANKLES = [(9, 8, 7),
          (8, 7, 12),
          (11, 12, 7),
          (10, 11, 12),
          (13, 7, 8),
          (7, 13, 14),
          (13, 14, 15),
          (7, 6, 2),
          (1, 2, 6),
          (0, 1, 2),
          (3, 6, 7),
          (6, 3, 4),
          (3, 4, 5)]

class AngleAnnotation(Arc):
    """
    Draws an arc between two vectors which appears circular in display space.
    """
    def __init__(self, xy, p1, p2, size=75, unit="points", ax=None,
                 text="", textposition="inside", text_kw=None, **kwargs):

        self.ax = ax or plt.gca()
        self._xydata = xy  # in data coordinates
        self.vec1 = p1
        self.vec2 = p2
        self.size = size
        self.unit = unit
        self.textposition = textposition

        super().__init__(self._xydata, size, size, angle=0.0,
                         theta1=self.theta1, theta2=self.theta2, **kwargs)

        self.set_transform(IdentityTransform())
        self.ax.add_patch(self)

        self.kw = dict(ha="center", va="center",
                       xycoords=IdentityTransform(),
                       xytext=(0, 0), textcoords="offset points",
                       annotation_clip=True)
        self.kw.update(text_kw or {})
        self.text = ax.annotate(text, xy=self._center, **self.kw)

    def get_size(self):
        factor = 1.
        if self.unit == "points":
            factor = self.ax.figure.dpi / 72.
        elif self.unit[:4] == "axes":
            b = TransformedBbox(Bbox.from_bounds(0, 0, 1, 1),
                                self.ax.transAxes)
            dic = {"max": max(b.width, b.height),
                   "min": min(b.width, b.height),
                   "width": b.width, "height": b.height}
            factor = dic[self.unit[5:]]
        return self.size * factor

    def set_size(self, size):
        self.size = size

    def get_center_in_pixels(self):
        """return center in pixels"""
        return self.ax.transData.transform(self._xydata)

    def set_center(self, xy):
        """set center in data coordinates"""
        self._xydata = xy

    def get_theta(self, vec):
        vec_in_pixels = self.ax.transData.transform(vec) - self._center
        theta = np.rad2deg(np.arctan2(vec_in_pixels[1], vec_in_pixels[0]))
        return theta

    def get_theta1(self):
        return self.get_theta(self.vec1)

    def get_theta2(self):
        return self.get_theta(self.vec2)

    def set_theta(self, angle):
        pass

    # Redefine attributes of the Arc to always give values in pixel space
    _center = property(get_center_in_pixels, set_center)
    theta1 = property(get_theta1, set_theta)
    theta2 = property(get_theta2, set_theta)
    width = property(get_size, set_size)
    height = property(get_size, set_size)

    # The following two methods are needed to update the text position.
    def draw(self, renderer):
        self.update_text()
        super().draw(renderer)

    def update_text(self):
        c = self._center
        s = self.get_size()
        angle_span = (self.theta2 - self.theta1) % 360
        tmp = self.theta1 + angle_span / 2
        print(tmp)
        angle = np.deg2rad(self.theta1 + angle_span / 2)
        r = s / 2
        if self.textposition == "inside":
            r = s / np.interp(angle_span, [60, 90, 135, 180],
                                          [3.3, 3.5, 3.8, 4])
        self.text.xy = c + r * np.array([np.cos(angle), np.sin(angle)])
        if self.textposition == "outside":
            def R90(a, r, w, h):
                if a < np.arctan(h/2/(r+w/2)):
                    return np.sqrt((r+w/2)**2 + (np.tan(a)*(r+w/2))**2)
                else:
                    c = np.sqrt((w/2)**2+(h/2)**2)
                    T = np.arcsin(c * np.cos(np.pi/2 - a + np.arcsin(h/2/c))/r)
                    xy = r * np.array([np.cos(a + T), np.sin(a + T)])
                    xy += np.array([w/2, h/2])
                    return np.sqrt(np.sum(xy**2))

            def R(a, r, w, h):
                aa = (a % (np.pi/4))*((a % (np.pi/2)) <= np.pi/4) + \
                     (np.pi/4 - (a % (np.pi/4)))*((a % (np.pi/2)) >= np.pi/4)
                return R90(aa, r, *[w, h][::int(np.sign(np.cos(2*a)))])

            bbox = self.text.get_window_extent()
            X = R(angle, r, bbox.width, bbox.height)
            trans = self.ax.figure.dpi_scale_trans.inverted()
            offs = trans.transform(((X-s/2), 0))[0] * 72
            self.text.set_position([offs*np.cos(angle), offs*np.sin(angle)])

def angle_between(p1, p2):  
    # 두점 사이의 각도:(getAngle3P 계산용) 
    # 시계 방향으로 계산한다. 
    # P1-(0,0)-P2의 각도를 시계방향으로
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    res = np.rad2deg((ang1 - ang2) % (2 * np.pi))
    return res

def getAngle3P(p1, p2, p3, direction="CW"): 
    #세점 사이의 각도 1->2->3
    pt1 = (p1[0] - p2[0], p1[1] - p2[1])
    pt2 = (p3[0] - p2[0], p3[1] - p2[1])
    res = angle_between(pt1, pt2)
    res = (res + 360) % 360
    if direction == "CCW":
        #반시계방향
        res = (360 - res) % 360
    return res

def draw_keypoints(image,
                   keypoints,
                   edges= None,
                   ankles= None,
                   keypoint_names= None,
                   dpi= 96*2.295):
    """
    Args:
        image (ndarray): [H, W, C]
        keypoints (ndarray): [N, 3]
        edges (List(Tuple(int, int))): 
    """
    np.random.seed(42)
    colors = {k: tuple(map(int, np.random.randint(0, 255, 3))) for k in range(24)}
    # if boxes:
    #     x1, y1 = min(keypoints[:, 0]), min(keypoints[:, 1])
    #     x2, y2 = max(keypoints[:, 0]), max(keypoints[:, 1])
    #     cv2.rectangle(image, (x1, y1), (x2, y2), (255, 100, 91), thickness=3)
    for k, v in keypoints.items():
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
        for i, (l, c, r) in enumerate(ankles):
            AngleAnnotation(keypoints[keypoint_names[c]],
                            keypoints[keypoint_names[l]],
                            keypoints[keypoint_names[r]],
                            ax = ax, size=20, linestyle="--", color="green",
                            text="{}".format(i), textposition="outside",
                            text_kw=dict(fontsize=10, color="green"))
    ax.imshow(image)
    ax.axis('off')
    plt.show()
    fig.savefig('./example.jpg')

def cut_image(data):
    bbox1 = data["bbox"][0]
    bbox2 = data["bbox"][1]
    bbox3 = data["bbox"][2]
    bbox4 = data["bbox"][3]
    h = bbox4 - bbox2
    w = bbox3 - bbox1
    y = bbox2
    x = bbox1
    # height, width, layers = img.shape
    crop_img = img[y:y+h, x:x+w]
    return crop_img 

def get_keypoint(data):
    keypoints = data['keypoints']
    xs = [d for i, d in enumerate(keypoints) if i%3==0]
    ys = [d for i, d in enumerate(keypoints) if i%3==1]
    xs_mod = [x-bbox1 for x in xs]
    ys_mod = [y-bbox2 for y in ys]
    return xs, ys, xs_mod, ys_mod

def get_mod_keypoint(xs_mod, ys_mod):
    body_points={}
    for i in range(len(xs_mod)):
        body_points[KEYPOINTS_TAG[i]] = (xs_mod[i], ys_mod[i])
    return body_points

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
    # imgplot = plt.imshow(img)

    label_path = img_path.replace("image", "label")
    label_path = label_path.replace("jpg", "json")
    with open(label_path, "r") as js:
        datas = json.load(js)

    # datas["annotations"][0].keys()
    data = datas["annotations"][2] # random_person
    crop_img = cut_image(data)
    xs, ys, xs_mod, ys_mod = get_keypoint(data)

    plt.imshow(crop_img)
    plt.axis('off')
    plt.savefig("./test.jpg", bbox_inches='tight', pad_inches=0, dpi=96*2.295)

    body_points = get_mod_keypoint(xs_mod, ys_mod)

    # draw_keypoints(crop_img, body_points, edges, ankles, keypoint_names, dpi=96*2.295)
    draw_keypoints(crop_img, body_points, edges=EDGES, ankles = ANKLES, dpi=96*2.295)