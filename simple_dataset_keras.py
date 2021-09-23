import numpy as np
from dataset import *
from config import *
import tensorflow as tf
from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import to_categorical
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class Bus_DataGenerator(Sequence):
    def __init__(self, X, y, batch_size, dim, shuffle = True):
        self.X = X
        self.y = y if y is not None else y
        self.batch_size = batch_size
        self.dim = dim
        # self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()
        
    def on_epoch_end(self):
        self.indexes = np.arange(len(self.X))
        if self.shuffle:
            np.random.shuffle(self.indexes)
            
    def __len__(self):
        return int(np.floor(len(self.X) / self.batch_size))
    
    def __data_generation(self, X_list, y_list):
        X = np.empty((self.batch_size, *self.dim))
        y = np.empty((self.batch_size), dtype = int)
        
        if y is not None:
            for i, (img, label) in enumerate(zip(X_list, y_list)):
                X[i] = img
                y[i] = label
                # print(img)
                # print(label)
                # print(X[i])
                # print(y[i])
                
            return X, y
        
        else:
            for i, img in enumerate(X_list):
                X[i] = img
                
            return X
        
    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size : (index + 1) * self.batch_size]
        X_list = [self.X[k] for k in indexes]
        
        if self.y is not None:
            y_list = [self.y[k] for k in indexes]
            # print(y_list)
            X, y = self.__data_generation(X_list, y_list)
            # print(X, y)
            return X, y
        else:
            y_list = None
            X = self.__data_generation(X_list, y_list)
            return X

if __name__=="__main__":
    # from dataset.py
    train_dataset = BusDataset("D:\\data\\train\\train.csv")
    valid_dataset = BusDataset("D:\\data\\valid\\valid.csv")

    (x_train, y_train) = train_dataset.load_data_angle()
    (x_valid, y_valid) = valid_dataset.load_data_angle()

    print(x_train.shape)
    print(y_train.shape)
    print(x_valid.shape)
    print(y_valid.shape)

    dg = Bus_DataGenerator(x_train, y_train, BATCH, (MAX_LEN, 13))
    print(dg.__len__)
    X_instance, y_instance = dg.__getitem__(0)
    # print(type(X_instance))
    print(X_instance.shape)
    print(y_instance.shape)

    import matplotlib.pyplot as plt

    for i, (x, y) in enumerate(dg):
        if(i <= 10):
            x_first = x[0]
            plt.title(y[0])
            plt.imshow(x_first)
            plt.show()