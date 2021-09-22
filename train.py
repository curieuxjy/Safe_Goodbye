import tensorflow as tf
from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import to_categorical
import numpy as np
from dataset import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__=="__main__":
    train_dataset = BusDataset("D:\\data\\train\\train.csv")
    valid_dataset = BusDataset("D:\\data\\valid\\valid.csv")

    (x_train, y_train) = train_dataset.load_data()
    (x_valid, y_valid) = valid_dataset.load_data()

    # TODO
    x_train, x_valid = x_train / 255.0, x_valid / 255.0

    print(x_train.shape)
    print(y_train.shape)
    print(x_valid.shape)
    print(y_valid.shape)

    dg = DataGenerator(x_train, y_train, 8, (50, 32), 2)

    model = Sequential()
    model.add(Embedding(input_dim=own_embedding_vocab_size, output_dim=32, input_length=maxlen))

    model.add(Bidirectional(LSTM(32,activation='relu',recurrent_dropout=0.1)))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    model.fit(padded_decs_oe, labels, epochs=50, verbose=0)  # Fit the model
    loss, accuracy = model.evaluate(padded_decs_oe, labels, verbose=0)  # Evaluate the model
    print('loss : %0.3f'%loss ,'Accuracy: %0.3f' % accuracy)
