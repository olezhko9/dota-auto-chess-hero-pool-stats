import os
from PIL import Image
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.optimizers import SGD
from keras.models import model_from_json

np.random.seed(42)


class CifarNet:

    def __init__(self):
        self.nb_classes = 0
        self.model = None

    def load_data(self, datapath):
        x_train = []
        y_train = []
        labels_name = []
        img_names = []
        for file in os.listdir(datapath):
            file_label = file.split(' - ')[0]
            img_names.append(file_label)

            if file_label not in labels_name:
                labels_name.append(file_label)

            y_train.append([labels_name.index(file_label)])

            im = Image.open(datapath + file)
            im = np.array(im)
            x_train.append(im)
        self.nb_classes = len(labels_name)
        return np.array(x_train), np.array(y_train), labels_name

    def preprocess_data(self, X_train, Y_train):
        X_train = X_train.astype('float32')
        X_train /= 255
        Y_train = np_utils.to_categorical(Y_train, self.nb_classes)
        return X_train, Y_train

    def _get_model(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same', input_shape=(40, 32, 3), activation='relu'))
        model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.nb_classes, activation='softmax'))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd,
                      metrics=['accuracy'])
        return model

    def fit(self, X_train, Y_train, nb_epoch):
        if self.model is None:
            self.model = self._get_model()
        self.model.fit(X_train, Y_train, epochs=nb_epoch, shuffle=True, verbose=2)

    # scores = model.evaluate(X_train, Y_train, verbose=0)
    # print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))

    def predict(self, X_test):
        y_pred = self.model.predict(X_test)
        return y_pred

    def save_model(self):
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        self.model.save_weights("model.h5")

    def load_model(self):
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights("model.h5")

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy',
                      optimizer=sgd,
                      metrics=['accuracy'])


if __name__ == '__main__':
    cnn = CifarNet()
    X_train, Y_train, labels = cnn.load_data("../../images/heroes/")
    X_train, Y_train = cnn.preprocess_data(X_train, Y_train)
    print(X_train.shape)
    print(Y_train.shape)

    # cnn.fit(X_train, Y_train, nb_epoch=30)
    # cnn.save_model()
    cnn.load_model()
    y_pred = cnn.predict(X_train)

    for i, pred in enumerate(y_pred):
        print(i, labels[np.argmax(Y_train[i])], labels[np.argmax(pred)])


