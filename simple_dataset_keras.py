import tensorflow as tf
from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import to_categorical
import numpy as np
from dataset import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class DataGenerator(Sequence):
    def __init__(self, X, y, batch_size, dim, n_channels, n_classes, shuffle = True):
        self.X = X
        self.y = y if y is not None else y
        self.batch_size = batch_size
        self.dim = dim
        self.n_channels = n_channels
        self.n_classes = n_classes
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
            # 지금 같은 경우는 MNIST를 로드해서 사용하기 때문에
            # 배열에 그냥 넣어주면 되는 식이지만,
            # custom image data를 사용하는 경우 
            # 이 부분에서 이미지를 batch_size만큼 불러오게 하면 됩니다. 
            for i, (img, label) in enumerate(zip(X_list, y_list)):
                X[i] = img
                y[i] = label
                
            return X, to_categorical(y, num_classes = self.n_classes)
        
        else:
            for i, img in enumerate(X_list):
                X[i] = img
                
            return X
        
    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size : (index + 1) * self.batch_size]
        X_list = [self.X[k] for k in indexes]
        
        if self.y is not None:
            y_list = [self.y[k] for k in indexes]
            X, y = self.__data_generation(X_list, y_list)
            return X, y
        else:
            y_list = None
            X = self.__data_generation(X_list, y_list)
            return X

if __name__=="__main__":
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    #----------여기까지는 내가 만들어야

    dg = DataGenerator(x_train, y_train, 4, (28, 28), 1, 10)

    import matplotlib.pyplot as plt

    for i, (x, y) in enumerate(dg):
        if(i <= 1):
            x_first = x[0]
            plt.title(y[0])
            plt.imshow(x_first)
            plt.show()