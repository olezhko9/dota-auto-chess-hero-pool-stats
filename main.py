import time
from dota_auto_chess.util import screenshot
from dota_auto_chess.ocr import recognize_heroes as recognize_heroes_ocr
from dota_auto_chess.stat import update_heroes_stat, plot_bar


if __name__ == '__main__':
    prev_heroes = []

    while True:
        time.sleep(0.05)
        screen = screenshot.take_screenshot()

        heroes_names_box = (360, 380, 1210, 25)
        heroes = recognize_heroes_ocr(screen, heroes_names_box)

        if len(heroes) == 5 and prev_heroes != heroes:
            print(heroes)

            stat = update_heroes_stat(heroes)
            plot_bar('heroes.html', *stat)
            prev_heroes = heroes
