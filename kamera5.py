import math

import cv2
import pytesseract
from cv2 import polylines
from pytesseract import Output
import numpy as np
from mtgsdk import Set
from mtgsdk import Card
import imutils

########################################################################################################################

lang = {'DE': 'german'}
langd = {'DE': 'deu'}
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
approxbool = True
cardbool = True
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
i = 0
ct = 20

########################################################################################################################

while True:
    i += 1
    ret, im = cam.read()
    imCopy = im.copy()
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    perimeter = 0.1 * cv2.arcLength(biggest_contour, True)
    approx = cv2.approxPolyDP(biggest_contour, perimeter, True)
    imno = imCopy.copy()
    x = []
    y = []
    for j in range(4):
        x.append(approx[j][0][0])
        y.append(approx[j][0][1])
    xmn = min(x)
    xmx = max(x)
    ymn = min(y)
    ymx = max(y)
    rect = cv2.minAreaRect(biggest_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    x = []
    y = []
    xs = 0
    ys = 0
    for j in range(4):
        xs += box[j][0]
        ys += box[j][1]
        x.append(box[j][0])
        y.append(box[j][1])
    xm = int(xs / len(x))
    ym = int(ys / len(x))
    xr = []
    xl = []
    yt = []
    yb = []
    for j in range(4):
        if x[j] < xm:
            xl.append(x[j])
        else:
            xr.append(x[j])
        if y[j] < ym:
            yt.append(y[j])
        else:
            yb.append(y[j])
    rt = []
    rb = []
    lt = []
    lb = []
    for x in xr:
        for y in yt:
            for point in box:
                if x in point and y in point:
                    rt = point
        for y in yb:
            for point in box:
                if x in point and y in point:
                    rb = point
    for x in xl:
        for y in yt:
            for point in box:
                if x in point and y in point:
                    lt = point
        for y in yb:
            for point in box:
                if x in point and y in point:
                    lb = point
    m = (lt[1] - lb[1]) / (lt[0] - lb[0])
    w = math.degrees(math.atan(m))
    ad = 90 if w < 0 else -90
    imr = imutils.rotate(imCopy, ad + w, (xm, ym))
    imCopyr = imr.copy()
    imgray = cv2.cvtColor(imr, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    rect = cv2.minAreaRect(biggest_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    imno = imr.copy()
    x = []
    y = []
    for j in range(4):
        x.append(box[j][0])
        y.append(box[j][1])
    xmn = min(x)
    xmx = max(x)
    ymn = min(y)
    ymx = max(y)
    cv2.circle(imCopyr, (xm, ym), 5, (0, 255, 0), 5)
    imCopy = imCopyr[ymn:ymx, xmn:xmx]
    imCopy = cv2.resize(imCopy, (0, 0), fx=1000 / (ymx - ymn), fy=1000 / (ymx - ymn))
    cv2.rectangle(imCopy, (50, 60), (600, 120), (0, 0, 255), 3)
    cardnimg = imCopy[60:120, 50:600]
    imgrey = cv2.cvtColor(cardnimg, cv2.COLOR_RGB2GRAY)
    if cardbool and i == 10:
        cardn = pytesseract.image_to_string(imgrey, 'deu', output_type=Output.STRING).strip(
            "'*/-_?)(\\\n").lstrip().rstrip()
        print(cardn)
        card = Card.where(language='german').where(name=cardn).all()[0]
        print(card.name,card.id)
        cardbool = False
    if not cardbool:
        cv2.putText(imCopy,str(card.name),(50,180),cv2.FONT_HERSHEY_PLAIN,4,(50,50,50),8)
    cv2.imshow("Karte", imCopy)
    cv2.waitKey(1)
