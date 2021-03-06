import cv2
import pytesseract
from pytesseract import Output
from mtgsdk import Card

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# img_source = cv2.imread('magic6.jpg')
img_source=cv2.imread("magic8.jpg")
greyscale = cv2.cvtColor(img_source, cv2.COLOR_BGR2GRAY)
cutimage = greyscale[80:150,750:1200]
# cutimage =greyscale[20:40,20:190]
cardn = ''
j = -1
binval = (80, 100, 127, 150)
binaryt = cutimage
foundcards = []
while True:
    if(j==-1):
        print("Bildmodus: Graustufen")
    cardn = pytesseract.image_to_string(binaryt, lang='deu', output_type=Output.STRING).rstrip().lstrip().strip(
        '.').split(' ')
    str1 = ' '.join(cardn)
    str1.rstrip().lstrip()
    print(str1)
    while len(foundcards) != 1:
        cv2.imshow("Card", binaryt)
        cv2.waitKey(1)
        if str1 != '' and str1 != 'Gobl':
            foundcards = Card.where(language='german').where(name=str1).all()
            if len(foundcards)>0:
                temp_name=foundcards[0].name
                for card in foundcards:
                    if card.name==temp_name:
                        foundcardsz=[foundcards[0]]
                    else:
                        foundcardsz=[1,1]
                        break
                foundcards=foundcardsz
        if len(foundcards) != 1:
            if len(cardn) != 0:
                cardn.pop(-1)
                str1 = ' '.join(cardn)
                print(str1)
        else:
            break
        if len(cardn) == 0 and len(foundcards) != 1:
            j += 1
            if j < 4:
                var1, binaryt= cv2.threshold(cutimage, binval[j], 255, cv2.THRESH_BINARY)
                print("Bildmodus: Threshold-"+str(binval[j]))
            break
    if len(foundcards) == 1:
        break
    elif j > 3:
        print("Karte konnte nicht erkannt werden.")
        break
if len(foundcards) == 1:
    foundcard = foundcards[0]
    print(foundcard.name, '\n', foundcard.id)
