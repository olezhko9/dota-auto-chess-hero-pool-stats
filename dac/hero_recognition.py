from PIL import Image
from dac.ocr import recognize_heroes_on_image_file
import os


crop_config = {
    'x': 285,
    'y': 150,
    'margin': 90,
    'w': 160,
    'h': 200,
}

unique_hero_img_count = 0
for filename in os.listdir('../images'):
    filename = '../images/' + filename
    if os.path.isdir(filename):
        continue
    heroes = recognize_heroes_on_image_file(filename, show=False)
    # print(heroes)

    if len(heroes) == 5:
        im = Image.open(filename)

        hero_img_width = (1560 - 360) / 5
        for i in range(5):
            hero_crop = im.crop((crop_config['x'] + crop_config['margin'] * (i + 1) + crop_config['w'] * i,
                                 crop_config['y'],
                                 crop_config['x'] + (crop_config['margin'] + crop_config['w']) * (i + 1),
                                 crop_config['y'] + crop_config['h']
                                 ))

            hero_crop.save("../images/heroes/" + heroes[i] + " - " + str(unique_hero_img_count) + ".png")
            unique_hero_img_count += 1
