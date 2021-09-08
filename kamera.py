import cv2
import pytesseract
from pytesseract import Output
from mtgsdk import Card
from mtgsdk import Set

##################################

lang = {'DE':'german'}
langd = {'DE':'deu'}
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

##################################

orig_imgsl=cv2.imread("magic8.jpg")
croppedsl = orig_imgsl[975:1000,730:850]
greyscalesl = cv2.cvtColor(croppedsl, cv2.COLOR_BGR2GRAY)

orig_img=cv2.imread("magic8.jpg")
cropped = orig_img[80:150,750:1200]
greyscale = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

setlang = (pytesseract.image_to_string(greyscalesl, lang='deu', output_type=Output.STRING).split(" ")[0]).split('-')
setc = setlang[0].rstrip().lstrip()
langk = lang[setlang[1]]
langs = langd[setlang[1]]
print(langs)
set=Set.find(setc)
print(set.code)
print(set.name)
print(set,langk)

cardn = pytesseract.image_to_string(greyscale,lang=langs, output_type=Output.STRING).rstrip().lstrip()

print(cardn)

cards = Card.where(language=langk).where(name=cardn).all()
for card in cards:
    if card.set==set.name:
        retcard=card
    else:
        retcard=""

print(card.name,card.id)

while True:
    cv2.imshow("Cropped",cropped)
    cv2.waitKey(1)