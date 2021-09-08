import cv2
import pytesseract
from pytesseract  import Output
import numpy as np
from mtgsdk import Set
from mtgsdk import Card
##################################

lang = {'DE':'german'}
langd = {'DE':'deu'}
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

##################################


cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

i = 0
while True:
    ret, frame = cam.read()
    frame = frame[160:850,830:1300]
    framer = frame
    pt1 = (0,660)
    pt2 = (70,680)
    pt1c = (10,17)
    pt2c = (405,50)
    framer = cv2.rectangle(framer,pt1,pt2,(0,0,255),2)
    framer = cv2.rectangle(framer, pt1c, pt2c, (0, 0, 255), 2)
    cv2.imshow("Kamera", framer)
    cv2.waitKey(1)
    i+=1
    if i ==500:
        cv2.imwrite("Karte.jpg",frame)
        cv2.destroyAllWindows()
        break

im = cv2.imread("Karte.jpg")
greyscale=cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
var,thresh = cv2.threshold(greyscale,60,255,cv2.THRESH_BINARY_INV)
var,thresh2 = cv2.threshold(greyscale,127,255,cv2.THRESH_BINARY)
kernel = np.ones((1,1),np.uint8)
imgerr = cv2.erode(thresh,kernel,iterations=1)
imgerr2 = cv2.erode(thresh2,kernel,iterations=1)
croppedls = imgerr[660:680,0:75]
croppedcard = imgerr2[17:50,10:405]
cv2.imwrite("setlang.jpg", croppedls)
setlang = pytesseract.image_to_string(croppedls, lang='deu', output_type=Output.STRING).strip(' ').strip("+.\'\\|*")
setlang=[setlang[0:3],setlang[4:6]]
print(setlang)
setc = setlang[0].rstrip().lstrip()
langk = lang[setlang[1]]
langs = langd[setlang[1]]
print(langs)
set=Set.find(setc)
print(set.code)
print(set.name)
print(set,langk)

cardn = pytesseract.image_to_string(croppedcard,lang=langs,output_type=Output.STRING).strip("+.\'\\|*").strip("'").lstrip().rstrip().split(' ')
cardname =""
for word in cardn:
    if len(word)>1:
        cardname+=' '+word
cardname=cardname.lstrip().rstrip()
print(cardname)

cards=Card.where(language=langk).where(name=cardname).all()
foundcard = ""
for card in cards:
    print(card.set_name,set.name)
    if card.set_name == set.name:
        foundcard = [card]
        break
    else:
        foundcard=[1,1]

if len(foundcard)==1:
    print(foundcard[0].name)
    print(foundcard[0].id)

while True:
    cv2.imshow("croppedcard",croppedcard)
    cv2.waitKey(1)
