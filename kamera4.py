import math

import cv2
import pytesseract
from cv2 import polylines
from pytesseract import Output
import numpy as np
from mtgsdk import Set
from mtgsdk import Card
import imutils

##################################

lang = {'DE': 'german'}
langd = {'DE': 'deu'}
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
approxbool = True
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
i = 0

##################################
while True:
    i += 1
    ret, im = cam.read()
    im = im[200:980, 200:1720]
    imCopy = im.copy()
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    rect = cv2.minAreaRect(biggest_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    #if i < 10:
    p00 = (box[0][0], box[0][1])
    p10 = (box[1][0], box[1][1])
    p20 = (box[2][0], box[2][1])
    p30 = (box[3][0], box[3][1])
    xvalues0 = [p00[0], p10[0], p20[0], p30[0]]
    yvalues0 = [p00[1], p10[1], p20[1], p30[1]]
    xmin0 = min(xvalues0) if min(xvalues0) > 0 else 0
    xmax0 = max(xvalues0)
    ymin0 = min(yvalues0) if min(yvalues0) > 0 else 0
    ymax0 = max(yvalues0)
    # cv2.drawContours(imCopy, [biggest_contour], 0, (0, 255, 0), 3)
    m0 = (p00[1] - p10[1]) / (p00[0] - p10[0])
    m1 = (p10[1] - p20[1]) / (p10[0] - p20[0])
    m2 = (p20[1] - p30[1]) / (p20[0] - p30[0])
    m3 = (p30[1] - p00[1]) / (p30[0] - p00[0])
    winkel=0
    if i == 10:
        winkel = math.degrees(math.atan(m0))
    im = imutils.rotate_bound(imCopy, winkel)
    # cv2.drawContours(imCopy, contours, -1, (0, 255, 0), 2)
    # imCopy = im.copy()
    # imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    # biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    # rect = cv2.minAreaRect(biggest_contour)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # if i < 10:
    #     p01 = (box[0][0], box[0][1])
    #     p11 = (box[1][0], box[1][1])
    #     p21 = (box[2][0], box[2][1])
    #     p31 = (box[3][0], box[3][1])
    #     xvalues1 = [p01[0], p11[0], p21[0], p31[0]]
    #     yvalues1 = [p01[1], p11[1], p21[1], p31[1]]
    #     xmin1 = min(xvalues1)+5 if min(xvalues1)>-5 else 0
    #     xmax1 = max(xvalues1)-5
    #     ymin1 = min(yvalues1)+5 if min(yvalues1)>-5 else 0
    #     ymax1 = max(yvalues1)-5
    # # cv2.drawContours(imCopy, [biggest_contour], 0, (0, 255, 0), 3)
    # imCopy = imCopy[ymin1:ymax1, xmin1:xmax1]
    # if i > 10:
    #     cv2.rectangle(imCopy, (40, 40), (400, 90), (0, 0, 255), 4)
    #     cni = imCopy[40:90, 40:400]
    #     cnic = imCopy[40:90, 40:400]
    #     cnig = cv2.cvtColor(cni, cv2.COLOR_RGB2GRAY)
    #     var, cnit = cv2.threshold(cnig, 30, 255, cv2.THRESH_BINARY_INV)
    #     contours, hierarchy = cv2.findContours(cnit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #     contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    #     biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    #     # kernel = np.ones((2, 2), np.uint8)
    #     # kernele = np.ones((1, 1), np.uint8)
    #     # cnid = cv2.dilate(cnit, kernel, iterations=1)
    #     # cnie = cv2.erode(cnid, kernele, iterations=3)
    #     # cv2.imwrite("Cardn.jpg",cnie)
    #     cardn = pytesseract.image_to_string(cnig, "deu", output_type=Output.STRING).strip("+-*/\\\'").lstrip().rstrip()
    #     print(cardn)
    #     cnic = cv2.drawContours(cnic, [biggest_contour], -1, (0, 255, 0), 4)
    #     cv2.imshow("texterkennung", cnic)
    cv2.imshow('draw contours', im)
    cv2.waitKey(1)
