import os
from PIL import Image
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.optimizers import SGD

np.random.seed(42)
labels = []
img_names = []


def load_data(datapath):
    x_train = []

    y_train = []
    for file in os.listdir(datapath):
        file_label = file.split(' - ')[0]
        img_names.append(file_label)

        if file_label not in labels:
            labels.append(file_label)

        y_train.append([labels.index(file_label)])

        im = Image.open(datapath + file)
        im = np.array(im)
        x_train.append(im)
    return np.array(x_train), np.array(y_train)


X_train, Y_train = load_data("../../images/heroes/")
print(X_train.shape)
print(Y_train.shape)
print(Y_train)

X_train = X_train.astype('float32')
X_train /= 255

nb_classes = len(labels)
print(nb_classes)
nb_epoch = 30

Y_train = np_utils.to_categorical(Y_train, nb_classes)

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
model.add(Dense(nb_classes, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(X_train, Y_train,
              epochs=nb_epoch,
              shuffle=True,
              verbose=2)

scores = model.evaluate(X_train, Y_train, verbose=0)
print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))

y_pred = model.predict(X_train)

for i, pred in enumerate(y_pred):
    print(i, img_names[i], labels[np.argmax(pred)])
