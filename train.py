import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense, Bidirectional, LSTM, Input
import numpy as np
from dataset import *
from simple_dataset_keras import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__=="__main__":
    train_dataset = BusDataset("D:\\data\\train\\train.csv")
    valid_dataset = BusDataset("D:\\data\\valid\\valid.csv")

    (x_train, y_train) = train_dataset.load_data()
    (x_valid, y_valid) = valid_dataset.load_data()

    # print(x_train.shape)
    # print(y_train.shape)
    # print(x_valid.shape)
    # print(y_valid.shape)

    trainGenSet = Bus_DataGenerator(x_train, y_train, 8, (50, 32), 2)
    print(trainGenSet.__getitem__(0)[0][0])
    # validGenSet = Bus_DataGenerator(x_valid, y_valid, 8, (50, 32), 2)

    # model = Sequential()
    # # model.add(Embedding(input_dim=own_embedding_vocab_size, output_dim=32, input_length=maxlen))
    # model.add(Input(shape=(50, 32), batch_size=8))
    # model.add(Bidirectional(LSTM(32,activation='relu',recurrent_dropout=0.1)))
    # model.add(Flatten())
    # model.add(Dense(1, activation='sigmoid'))

    # print(model.summary())

    # model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    # model.fit_generator(trainGenSet,
    #                     steps_per_epoch=20,
    #                     epochs=300,
    #                     validation_data=validGenSet,
    #                     validation_steps=10)
    # scores = model.evaluate_generator(validGenSet)
    # print(scores)
