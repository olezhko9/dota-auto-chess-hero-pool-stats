import pytesseract
import cv2


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


if __name__ == '__main__':

    image_path = './images/2.png'

    # x, y, w, h
    crop = (280, 365, 1350, 35)

    image = cv2.imread(image_path, 3)
    crop_img = image[crop[1]:crop[1] + crop[3], crop[0]:crop[0] + crop[2]]

    grayscaled = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    retval, bw_image = cv2.threshold(grayscaled, 160, 255, cv2.THRESH_BINARY)
    bw_image[bw_image == 255] = 100
    bw_image[bw_image == 0] = 255
    bw_image[bw_image == 100] = 0

    cv2.imshow('threshold', bw_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    text = pytesseract.image_to_string(bw_image, config='', lang='eng')
    print(text)
