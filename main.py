import pytesseract
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def recognize_heroes_on_image(image_path, show=False):
    # x, y, w, h
    crop = (280, 365, 1350, 35)
    image = cv2.imread(image_path)

    crop_img = image[crop[1]:crop[1] + crop[3], crop[0]:crop[0] + crop[2]]
    grayscaled = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    retval, bw_image = cv2.threshold(grayscaled, 103, 255, cv2.THRESH_BINARY)

    bw_image[bw_image == 255] = 100
    bw_image[bw_image == 0] = 255
    bw_image[bw_image == 100] = 0

    if show:
        cv2.imshow('threshold', bw_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return pytesseract.image_to_string(bw_image, lang='eng', config='--psm 7')

if __name__ == '__main__':

    for img in os.listdir('./images'):
        print(img)
        text = recognize_heroes_on_image('./images/' + img, show=True)
        print(text)
        print()