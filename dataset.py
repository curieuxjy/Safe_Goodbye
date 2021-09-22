import os
from os import walk
import pandas as pd
import numpy as np
from config import *

class BusDataset():
    def __init__(self, csv_dir):
        self.csv_dir = csv_dir
        self.dataframe = self.get_dataframe()
        self.keypoints_series = self.dataframe["keypoints"]
        self.framenums_series = self.dataframe["frame_num"]
        self.join_data = self.join_framenum_keypoint() #list
        self.getoff_series = self.dataframe["get_off"]

    def __len__(self):
        print(len(self.dataframe))
    
    def get_dataframe(self):
        df = pd.read_csv(self.csv_dir)
        drop_index = df[df["frame_num"]=="[]"].index
        return df.drop(drop_index)

    def join_framenum_keypoint(self):
        join_data=[]
        for idx in self.dataframe.index:
            keypoint = self.get_keypoint(self.keypoints_series[idx]) # array
            framenum = self.get_framenum(self.framenums_series[idx]) # array
            join_data.append((framenum, keypoint)) # tuple(# array, # array)
        return join_data

    def get_framenum(self, row):
        framenum = [int(i) for i in row[1:-1].split(", ")] # string -> int
        return np.array(framenum)

    def normalize_keypoint(self, str_data):
        int_data=[]
        for i, dt in enumerate(str_data):
            if i%3==0:
                int_data.append(int(dt)/1920)
            elif i%3==1:
                int_data.append(int(dt)/1080)
            else:
                pass
        return int_data


    def get_keypoint(self, row):
        # row: frames
        ky = [i for i in row[2:-2].split("], [")] # string
        keypoint=[]
        for j in range(len(ky)):
            str_data = ky[j].split(", ")
            # normalize
            int_data = self.normalize_keypoint(str_data)
            # int_data = [int(float(str_data[i])) for i in range(len(str_data)) if i%3 != 2]
            keypoint.append(np.array(int_data))
        return np.array(keypoint) # list /list element

    def get_y(self):
        # get_off
        y = []
        for index in self.dataframe.index:
            if self.getoff_series[index][1]=="F":
                y.append(0)
            else:
                y.append(1) # T
        return np.array(y)

    def load_data(self):
        X = []
        y = self.get_y()
        for check, (framenum, keypoint) in enumerate(self.join_data):
            assert keypoint.shape[0] == framenum.shape[0]
            ky_series=[] # len MAX_LEN
            for index in range(MAX_LEN): # index = 0, 1, 2, ..., 49
                if index in framenum:
                    # print("framenum ", framenum.shape)
                    idx = np.where(framenum == index) # find idx
                    # print(index)
                    # print(framenum[idx])
                    # print(check)
                    if framenum[idx].shape!=(1,):
                        ky_series.append(np.zeros(32)) # exception
                    else:
                        ky_series.append(np.squeeze(keypoint[idx])) # array
                else:
                    ky_series.append(np.zeros(32))
            ky_series = np.array(ky_series)
            assert ky_series.shape ==(MAX_LEN, 32)
            X.append(np.array(ky_series))
        # X = (len(df), MAX_LEN, 16x2)
        # y = (len(df),)
        X = np.array(X)
        assert len(X)==len(y)
        return X, y

if __name__ == "__main__":

    train_dataset = BusDataset("D:\\data\\train\\train.csv")
    valid_dataset = BusDataset("D:\\data\\valid\\valid.csv")

    (x_train, y_train) = train_dataset.load_data()
    (x_test, y_test) = valid_dataset.load_data()
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)