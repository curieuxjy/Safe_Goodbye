import numpy as np
from config import *
from dataset import *
from simple_dataset_keras import *
from datetime import datetime
import tensorflow as tf
# from tf.keras.callbacks.TensorBoard
# from tensorflow.keras.callbacks import Tensorboard
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

def simple_lstm():
    model = Sequential()
    # model.add(Embedding(input_dim=(MAX_LEN, 13), output_dim=13, input_length=MAX_LEN))
    model.add(Input(shape=(MAX_LEN, 13), batch_size=BATCH))
    model.add(LSTM(64, activation='relu'))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    print(model.summary())
    return model

def simple_dnn():
    model = Sequential()
    # model.add(Embedding(input_dim=(MAX_LEN, 13), output_dim=13, input_length=MAX_LEN))
    model.add(Input(shape=(MAX_LEN, 13), batch_size=BATCH))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='sigmoid'))
    print(model.summary())
    return model

# def denset():
#     return model

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

    trainGenSet = Bus_DataGenerator(x_train, y_train, BATCH, (MAX_LEN, 13))
    validGenSet = Bus_DataGenerator(x_valid, y_valid, BATCH, (MAX_LEN, 13))

    # model = simple_lstm()
    model = simple_bilstm()

    log_dir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")

    tensorboard = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

    history = model.fit_generator(trainGenSet,epochs=300,
                                validation_data=validGenSet,
                                 callbacks=[tensorboard])

    scores = model.evaluate_generator(validGenSet)

    print(scores)
