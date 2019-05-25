from PIL import ImageGrab


def screenshot(box=None):
    img = ImageGrab.grab(box)
    return img
