import os
from dac.ocr import recognize_heroes_on_image, recognize_heroes_on_image_file
from util.sreenshooter import screenshot
import time

if __name__ == '__main__':
    heroes_in_file = {}

    # recognize from screenshot
    time.sleep(1)
    screen = screenshot((280, 365, 1350+280, 35+365))
    heroes = recognize_heroes_on_image(screen, show=True)
    print(heroes)

    # recognize from files
    for img in os.listdir('./images'):
        heroes = recognize_heroes_on_image_file('./images/' + img, show=False)
        print(img, heroes)
        heroes_in_file[img] = heroes

