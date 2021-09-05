import cv2
import imutils
import pytesseract
import numpy as np
from pytesseract import Output
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog


def findcard(cardn):
    return Card.where(language='german').where(name=cardn).all(),Card.where(language='german').where(name=cardn).all()[0]


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
img_source = cv2.imread('magic3.jpg')
greyscale = cv2.cvtColor(img_source, cv2.COLOR_BGR2GRAY)
cutimage = greyscale[20:40, 20:190]

i = 0
binvalues = (80, 100, 127, 150)
binv = 80
while True:
    contu, hierarchy = cv2.findContours(cutimage, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print(str(len(contu)))
    print(contu[0])
    #c = max(contu,key=cv2.contourArea)
    #r = tuple(c[c[:, :, 0].argmax()][0])[0]
    #t = tuple(c[c[:, :, 1].argmax()][0])[1]
    #print(r)
    #cutimage = greyscale[t:t+20, 20:r]
    # if binv == 0:
    #     binaryt = cutimage
    # else:
    #     var1, binaryt = cv2.threshold(cutimage, binv, 255, cv2.THRESH_BINARY)
    boolv = True
    cv2.imshow("Cardname", cutimage)
    # while boolv:
    #     try:
    #         cardn = pytesseract.image_to_string(binaryt, output_type=Output.STRING, lang='deu').lstrip().rstrip().strip(
    #             '.')
    #         print(cardn)
    #         # foundcard1,foundcard = findcard(cardn)
    #         #if len(foundcard1) == 1:
    #         #   boolv = False
    #     except:
    #         i += 1
    #         binv = binvalues[i]
    #         print(binv)
    #         if binv == 0:
    #             binaryt = cutimage
    #         else:
    #             var1, binaryt = cv2.threshold(cutimage, binv, 255, cv2.THRESH_BINARY)
    #foundcard = foundcard1[0]
    #print(foundcard.name, '\n', foundcard.rarity, '\n', foundcard.colors, '\n', foundcard.text, '\n', foundcard.flavor,
         # '\n')
    cv2.waitKey(1)
   #if len(foundcard1) > 0:
    #    print(binv)
    #    break
