import os
import time
import numpy as np
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot
from dac.ocr import recognize_heroes_on_image, recognize_heroes_on_image_file
from util.sreenshooter import screenshot

from dac.hero_list import all_heroes

# TODO: pip install dash dash-render dash-html-components dash-core-components


def plot_bar(heroes_stat, species_chart, classes_chart):

    bar_1 = go.Bar(
         x=[key for key in heroes_stat.keys()],
         y=[heroes_stat[key] for key in heroes_stat.keys()]
    )

    bar_2 = go.Bar(
         x=[key for key in species_chart.keys()],
         y=[species_chart[key] for key in species_chart.keys()]
    )

    bar_3 = go.Bar(
         x=[key for key in classes_chart.keys()],
         y=[classes_chart[key] for key in classes_chart.keys()]
    )

    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=('Heroes', 'Species', 'Classes'))
    fig.append_trace(bar_1, 1, 1)
    fig.append_trace(bar_2, 2, 1)
    fig.append_trace(bar_3, 3, 1)

    plot(fig, filename='heroes.html', auto_open=False)


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
