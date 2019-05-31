import os
from PIL import Image
import numpy as np
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Flatten, Activation
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.optimizers import SGD

# Задаем seed для повторяемости результатов
np.random.seed(42)
labels = ['Abaddon', 'Chaos Knight', 'Tinker', 'Tiny']

def load_data(datapath):
    x_train = []

    y_train = []
    for file in os.listdir(datapath):
        file_label = file.split(' - ')[0]
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
nb_epoch = 25

Y_train = np_utils.to_categorical(Y_train, nb_classes)

model = Sequential()
# Первый сверточный слой
model.add(Conv2D(32, (3, 3), padding='same', input_shape=(40, 32, 3), activation='relu'))
# Второй сверточный слой
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
# Первый слой подвыборки
model.add(MaxPooling2D(pool_size=(2, 2)))
# Слой регуляризации Dropout
model.add(Dropout(0.25))

# Третий сверточный слой
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
# Четвертый сверточный слой
model.add(Conv2D(64, (3, 3), activation='relu'))
# Второй слой подвыборки
model.add(MaxPooling2D(pool_size=(2, 2)))
# Слой регуляризации Dropout
model.add(Dropout(0.25))
# Слой преобразования данных из 2D представления в плоское
model.add(Flatten())
# Полносвязный слой для классификации
model.add(Dense(512, activation='relu'))
# Слой регуляризации Dropout
model.add(Dropout(0.5))
# Выходной полносвязный слой
model.add(Dense(nb_classes, activation='softmax'))

# Задаем параметры оптимизации
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
# Обучаем модель
model.fit(X_train, Y_train,
              epochs=nb_epoch,
              shuffle=True,
              verbose=2)

# Оцениваем качество обучения модели на тестовых данных
scores = model.evaluate(X_train, Y_train, verbose=0)
print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))

y_pred = model.predict(X_train)

for i, pred in enumerate(y_pred):
    print(i, np.argmax(pred))
