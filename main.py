import os
import time
import numpy as np
from dac.ocr.heroes_on_image import recognize_heroes_on_image, recognize_heroes_on_image_file
from util.sreenshooter import screenshot
from util.bar_plotter import plot_bar

from dac.hero_list import all_heroes

# TODO: pip install dash dash-render dash-html-components dash-core-components


def main():
    """ recognize from screenshot """
    heroes_chart = {}

    prev_heroes = []
    while True:
        time.sleep(1)
        # TODO: добавить поддержку разных разрешений
        screen = screenshot((280, 365, 1350+280, 35+365))
        heroes = recognize_heroes_on_image(screen, show=False)
        if len(heroes) == 5 and prev_heroes != heroes:
            print(heroes)
            for hero in heroes:
                if heroes_chart.get(hero[0]) is None:
                    heroes_chart[hero[0]] = hero[1]
                else:
                    heroes_chart[hero[0]] += hero[1]
            prev_heroes = heroes
            plot_bar(heroes_chart)


def test():
    """ recognize from files """
    heroes_chart = {}
    classes_chart = {}
    species_chart = {}
    images_path = './images'
    for img in os.listdir(images_path):
        image_path = os.path.join(images_path, img)
        if os.path.isdir(image_path):
            continue
        heroes = recognize_heroes_on_image_file(image_path, show=False)
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


def cnn():
    from dac.cnn.cifar_nn import CifarNet
    from dac.cnn.hero_img_croper import crop_heroes
    from dac.hero_list import all_heroes

    cifar = CifarNet()
    cifar.load_model()

    while True:
        time.sleep(2)
        screen = screenshot()
        cropped_heroes = crop_heroes(screen)
        if len(cropped_heroes) == 5:
            heroes = []
            print('----- TRUE -----')
            for hero_name, cropped_hero in cropped_heroes:
                cropped_hero = np.array(cropped_hero)
                print(hero_name)
                heroes.append(cropped_hero)

            X_test, _ = cifar.preprocess_data(np.array(heroes), None)
            y_pred = cifar.predict(X_test)
            print('----- PRED -----')
            for pred in y_pred:
                print(all_heroes[np.argmax(pred)], pred[np.argmax(pred)])


if __name__ == '__main__':
    # main()
    test()
    # cnn()
