import re
import pytesseract
import cv2
from dota_auto_chess.hero_list import all_heroes
from dota_auto_chess.util.screenshot import crop_screenshot

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def recognize_heroes(image, heroes_names_box):
    image = crop_screenshot(image, heroes_names_box)
    image_text = recognize_image_text(image, threshold=150)
    return get_heroes_from_text(image_text)


def recognize_round(image, round_box):
    image = crop_screenshot(image, round_box)
    image_text = recognize_image_text(image, threshold=160)
    return get_round_from_text(image_text)


def recognize_battle_state(image, battle_state_box):
    image = crop_screenshot(image, battle_state_box)
    image_text = recognize_image_text(image, threshold=80)
    return get_battle_state_from_text(image_text)


def recognize_image_text(image, threshold):
    # насыщенные буквы на черном фоне
    retval, saturated_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    # переводим в оттенки серого
    grayscaled = cv2.cvtColor(saturated_image, cv2.COLOR_BGR2GRAY)

    # бинаризация изображения
    retval, bw_image = cv2.threshold(grayscaled, 20, 255, cv2.THRESH_BINARY)

    # черные буквы на белом фоне
    bw_image = cv2.bitwise_not(bw_image)

    return pytesseract.image_to_string(bw_image, lang='eng', config='--psm 7')


def get_heroes_from_text(text):
    text = re.sub(r"[^A-Z ]", " ", text)
    text = re.sub(r"\b(?!AXE|LO|IO)[A-Z]{1,3}\b", " ", text)
    hero_names_in_text = re.split(r"\s{2,}", text.strip())

    hero_list = []
    for i, hero_name in enumerate(hero_names_in_text):
        if len(hero_name) < 2:
            continue

        hero_name = hero_name.replace(" ", "")
        if hero_name == 'LO':
            hero_name = 'IO'

        for hero in all_heroes:
            if hero.replace(" ", "").upper().startswith(hero_name):
                hero_list.append((i, hero))
                break

    hero_list = [h[1] for h in sorted(hero_list, key=lambda x: x[0])]

    return hero_list


def get_round_from_text(text):
    text = re.sub(r"\D", "", text.strip())
    return int(text) if text.isdecimal() else None


def get_battle_state_from_text(text):
    text = re.sub(r"[^A-Z]", "", text)
    return text if text in ('PREPARE', 'READY', 'BATTLE', 'DEFEAT', 'VICTORY') else None
