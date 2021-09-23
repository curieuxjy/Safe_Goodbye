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

def simple_bilstm():
    model = Sequential()
    # model.add(Embedding(input_dim=(MAX_LEN, 13), output_dim=13, input_length=MAX_LEN))
    model.add(Input(shape=(MAX_LEN, 13), batch_size=BATCH))
    model.add(Bidirectional(LSTM(64,activation='relu',recurrent_dropout=0.1)))
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

    checkpoint_filepath = 'checkpoint/{epoch:02d}-{val_loss:.5f}.h5'
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        monitor='val_accuracy',
        mode='max',
        save_best_only=True)

    hist = model.fit_generator(trainGenSet,epochs=90,
                                validation_data=validGenSet,
                                callbacks=[tensorboard, model_checkpoint_callback])

    scores = model.evaluate_generator(validGenSet)

    print(scores)

    # model.save('bus_intention_model.h5')

    

    # fig, loss_ax = plt.subplots()

    # acc_ax = loss_ax.twinx()

    # loss_ax.plot(hist.history['loss'], 'y', label='train loss')
    # loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')

    # acc_ax.plot(hist.history['acc'], 'b', label='train acc')
    # acc_ax.plot(hist.history['val_acc'], 'g', label='val acc')

    # loss_ax.set_xlabel('epoch')
    # loss_ax.set_ylabel('loss')
    # acc_ax.set_ylabel('accuray')

    # loss_ax.legend(loc='upper left')
    # acc_ax.legend(loc='lower left')

    # plt.show()
    # plt.savefig("./train.png")
