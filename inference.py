import numpy as np
from config import *
from dataset import *
from simple_dataset_keras import *
from datetime import datetime
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense, Bidirectional, LSTM, Input
from tensorflow.python.keras.models import load_model
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


if __name__=="__main__":
    test_dataset = BusDataset("D:\\data\\test\\test.csv")

    (x_test, y_test) = test_dataset.load_data_angle()
    print(x_test.shape)

    # testGenSet = Bus_DataGenerator(x_test, y_test, 1, (MAX_LEN, 13))

    model = load_model('./checkpoint/38-0.23478.h5')

    # y_hat = model.predict_classes(x_test)
    y_hat = model.predict_proba(x_test)
    print(y_hat)

    for i in range(8):
        print('True : ', y_test[i],', Predict : ',y_hat[i])
