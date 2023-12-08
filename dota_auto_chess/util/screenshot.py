from PIL import ImageGrab
import numpy as np


def take_screenshot(box=None):
    return ImageGrab.grab(box)


def crop_screenshot(screenshot, box):
    screenshot = np.array(screenshot)
    return screenshot[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
