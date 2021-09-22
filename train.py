import numpy as np
from config import *
from dataset import *
from simple_dataset_keras import *
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense, Bidirectional, LSTM, Input

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def simple_bilstm():
    model = Sequential()
    # model.add(Embedding(input_dim=(MAX_LEN, 13), output_dim=13, input_length=MAX_LEN))
    model.add(Input(shape=(MAX_LEN, 13), batch_size=BATCH))
    model.add(Bidirectional(LSTM(128,activation='relu',recurrent_dropout=0.1)))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    print(model.summary())
    return model

if __name__=="__main__":
    train_dataset = BusDataset("D:\\data\\train\\train.csv")
    valid_dataset = BusDataset("D:\\data\\valid\\valid.csv")

    (x_train, y_train) = train_dataset.load_data_angle()
    (x_valid, y_valid) = valid_dataset.load_data_angle()

    # print(x_train.shape)
    # print(y_train.shape)
    # print(x_valid.shape)
    # print(y_valid.shape)
    # (3024, 35, 13)
    # (3024,)
    # (574, 35, 13)
    # (574,)

    trainGenSet = Bus_DataGenerator(x_train, y_train, BATCH, (MAX_LEN, 13), 2)
    # print(trainGenSet.__getitem__(0)[0][0])
    validGenSet = Bus_DataGenerator(x_valid, y_valid, BATCH, (MAX_LEN, 13), 2)

    model = simple_bilstm()

    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

    model.fit_generator(trainGenSet,
                        steps_per_epoch=20,
                        epochs=300,
                        validation_data=validGenSet,
                        validation_steps=10)
                        
    scores = model.evaluate_generator(validGenSet)
    print(scores)
