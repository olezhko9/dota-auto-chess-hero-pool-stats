import os
import time
import numpy as np
from dac.ocr import heroes_on_image
from util.sreenshooter import screenshot
from util.bar_plotter import plot_bar
from dac.hero_list import all_heroes


def get_stat_from_screen_with_ocr():
    """ recognize from screenshot """
    heroes_chart = {}
    classes_chart = {}
    species_chart = {}
    prev_heroes = []
    while True:
        time.sleep(1)
        screen = screenshot()
        heroes = heroes_on_image.recognize_heroes_on_image(screen, need_crop=True, show=False)
        if len(heroes) == 5 and prev_heroes != heroes:
            print(heroes)
            for hero in heroes:
                if heroes_chart.get(hero) is None:
                    heroes_chart[hero] = 1
                else:
                    heroes_chart[hero] += 1

                for species in all_heroes[hero].species:
                    if species_chart.get(species) is None:
                        species_chart[species] = 1
                    else:
                        species_chart[species] += 1

                for classes in all_heroes[hero].classes:
                    if classes_chart.get(classes) is None:
                        classes_chart[classes] = 1
                    else:
                        classes_chart[classes] += 1
            prev_heroes = heroes
            plot_bar(heroes_chart, species_chart, classes_chart)


def get_stat_from_files_with_ocr():
    """ recognize from files """
    heroes_chart = {}
    classes_chart = {}
    species_chart = {}
    images_path = './images'
    for img in os.listdir(images_path):
        image_path = os.path.join(images_path, img)
        if os.path.isdir(image_path):
            continue
        heroes = heroes_on_image.recognize_heroes_on_image(image_path, need_crop=True, show=False)
        print(img, heroes)

        if len(heroes) == 5:
            for hero in heroes:
                if heroes_chart.get(hero) is None:
                    heroes_chart[hero] = 1
                else:
                    heroes_chart[hero] += 1

                for species in all_heroes[hero].species:
                    if species_chart.get(species) is None:
                        species_chart[species] = 1
                    else:
                        species_chart[species] += 1

                for classes in all_heroes[hero].classes:
                    if classes_chart.get(classes) is None:
                        classes_chart[classes] = 1
                    else:
                        classes_chart[classes] += 1

        plot_bar(heroes_chart, species_chart, classes_chart)

    print(heroes_chart)


def get_stat_from_screen_with_cnn():
    from dac.cnn.cifar_nn import CifarNet
    from util.img_croper import crop_heroes
    from dac.hero_list import all_heroes

    cifar = CifarNet()
    cifar.load_model()

    while True:
        time.sleep(4)
        screen = screenshot()
        cropped_heroes = crop_heroes(screen)
        if len(cropped_heroes) == 5:
            heroes = []
            for cropped_hero in cropped_heroes:
                cropped_hero = np.array(cropped_hero)
                # print(hero_name)
                heroes.append(cropped_hero)

            X_test, _ = cifar.preprocess_data(np.array(heroes), None)
            y_pred = cifar.predict(X_test)
            print('----- PRED -----')
            for pred in y_pred:
                print(list(all_heroes.keys())[np.argmax(pred)], pred[np.argmax(pred)])
