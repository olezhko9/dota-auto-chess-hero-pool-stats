import os
import time
import plotly.graph_objs as go
import plotly.tools
from plotly.offline import plot
from dac.ocr import recognize_heroes_on_image, recognize_heroes_on_image_file
from util.sreenshooter import screenshot

# TODO: pip install dash dash-render dash-html-components dash-core-components
plotly.tools.set_credentials_file(username='olezhko', api_key='7HhZ0uvGRZoW1JBI44E1')


def plot_bar(heroes_stat):
    labels = [key for key in heroes_stat.keys()]
    values = [heroes_stat[key] for key in heroes_stat.keys()]

    data = [go.Bar(
        x=labels,
        y=values
    )]

    plot(data, filename='heroes.html', auto_open=False)


def main():
    """ recognize from screenshot """
    heroes_chart = {}

    prev_heroes = []
    while True:
        time.sleep(1)
        # TODO: добавить поддержку разных разрешений
        screen = screenshot((280, 365, 1350+280, 35+365))
        heroes = recognize_heroes_on_image(screen, show=False)
        if sum([hero[1] for hero in heroes]) == 5 and prev_heroes != heroes:
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

    for img in os.listdir('./images'):
        heroes = recognize_heroes_on_image_file('./images/' + img, show=False)
        print(img, heroes)

        for hero in heroes:
            if heroes_chart.get(hero[0]) is None:
                heroes_chart[hero[0]] = hero[1]
            else:
                heroes_chart[hero[0]] += hero[1]
        plot_bar(heroes_chart)

    print(heroes_chart)


if __name__ == '__main__':
    # main()
    test()
