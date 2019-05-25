import os
import time
from dac.ocr import recognize_heroes_on_image, recognize_heroes_on_image_file
from util.sreenshooter import screenshot


def main():
    """ recognize from screenshot """
    heroes_chart = {}

    prev_heroes = []
    while True:
        time.sleep(1)
        screen = screenshot((280, 365, 1350+280, 35+365))
        heroes = recognize_heroes_on_image(screen, show=False)
        if sum([hero[1] for hero in heroes]) == 5 and prev_heroes != heroes:
            # print(heroes)
            for hero in heroes:
                if heroes_chart.get(hero[0]) is None:
                    heroes_chart[hero[0]] = hero[1]
                else:
                    heroes_chart[hero[0]] += hero[1]
            print(heroes_chart)
            prev_heroes = heroes


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

    print(heroes_chart)


if __name__ == '__main__':
    main()
    # test()





