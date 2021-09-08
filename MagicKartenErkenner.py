import math
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
from mtgsdk import Card
import imutils

########################################################################################################################

# Vordefinierte Variablen
lang = {'DE': 'german'} # Erweiterbare Sprachen
langd = {'DE': 'deu'}   #
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract' # Verzeichnis von Tesseract
cardbool = False        # Boolean, das verhindert, dass mehr als nötig auf das MagicSDK zugegriffen wird
cam = cv2.VideoCapture(0) # Kamera 0, wenn keine andere angeschlossen ist
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Kamera auf 1080p setzen
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
i = 0                   # erkennung startet erst in Frame 10, daher braucht es einen Zähler

########################################################################################################################

while True:
    i += 1
    ret, im = cam.read()            # Aktuellen Frame von der Kamera holen
    imCopy = im.copy()              # Kopie davon erstellen, da das Orginalbild für die Maske verändert wird
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # nämlich erst Graustufen
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV) # Dann Schwarz-Weiß
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Daraus werden alle
    # äußeren Konturen gezogen
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours] # Alle Konturgrößen werden geholt
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]  # und die größte (die Karte) erkannt
    perimeter = 0.1 * cv2.arcLength(biggest_contour, True)       # hier wird ein Approximations Polygon erstellt
    approx = cv2.approxPolyDP(biggest_contour, perimeter, True)
    x = []                                                       # die eckpunkte des Polygons werden in Arrays gepackt,
    y = []                                                       # sortiert nach x und y
    for j in range(4):
        x.append(approx[j][0][0])
        y.append(approx[j][0][1])
    xmn = min(x)                                                 # dann werden min und max wert x und y werte bestimmt
    xmx = max(x)
    ymn = min(y)
    ymx = max(y)
    rect = cv2.minAreaRect(biggest_contour)                      # im Gegensatz zum Approx Polygon ist diese Box
    box = cv2.boxPoints(rect)                                    # Rechteckig, also nur 90° Winkel
    box = np.int0(box)                                           # Approximiert aber auch die Magic Karte
    x = []                                                       # es wird erneut nach x und y werten sortiert
    y = []
    xs = 0                                                       # und auch eine Summe aller x,y Werte gebildet
    ys = 0
    for j in range(4):
        xs += box[j][0]
        ys += box[j][1]
        x.append(box[j][0])
        y.append(box[j][1])
    xm = int(xs / len(x))                                        # um daraus den Kartenmittelpunkt zu bestimmen
    ym = int(ys / len(x))
    xr = []                                                      # alle x<mittelpunkt sind dann links, alle >mp rechts
    xl = []
    yt = []                                                      # equivalent y<mp oben und >mp unten
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
    rt = []                                                      # Daraus kann man die Punkte oben rechts(rt),
    rb = []                                                      # Unten rechts (rb)
    lt = []                                                      # Oben links (lt)
    lb = []                                                      # und unten links (lb) berechnen
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
    m = (lt[1] - lb[1]) / (lt[0] - lb[0])                      # es wird die Steigung an der linken langen Kante gesucht
    w = math.degrees(math.atan(m))                             # daras ein Winkel berechnet
    ad = 90 if w < 0 else -90
    imr = imutils.rotate(imCopy, ad + w, (xm, ym))             # um den das Bild dann gedreht wird
    imCopyr = imr.copy()                                       # In den folgenden ca 20 Zeilen wird erneut eine Box
    imgray = cv2.cvtColor(imr, cv2.COLOR_BGR2GRAY)             # Approximation gemacht, diesmal um die Boundries des
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)  # auszugebenden Bildes festzulegen
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    rect = cv2.minAreaRect(biggest_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    x = []
    y = []
    for j in range(4):
        x.append(box[j][0])
        y.append(box[j][1])
    xmn = min(x)
    xmx = max(x)
    ymn = min(y)
    ymx = max(y)
    imCopy = imCopyr[ymn:ymx, xmn:xmx]                          # Das gedrehte Bild wird auf die neuen maximalen x,y
    imCopy = cv2.resize(imCopy, (0, 0), fx=1000 / (ymx - ymn), fy=1000 / (ymx - ymn))# Werte gesetzt und um einen Faktor
    cv2.rectangle(imCopy, (50, 60), (550, 120), (0, 0, 255), 3) # geresized. Es wird ein rotes Rechteck über den Karten
    cardnimg = imCopy[60:120, 50:550]                           # Namen gelegt und der Inhalt in ein extrabild gelegt.
    imgrey = cv2.cvtColor(cardnimg, cv2.COLOR_RGB2GRAY)         # dieses wird auf Graustufen gestellt.
    if i == 40:                                                 # nachdem sich die Kamera gefocused hat (etwa 10 Frames)
        cardn = pytesseract.image_to_string(imgrey, 'deu', output_type=Output.STRING).strip('*/-|\_?)(&1234567890').lstrip().rstrip().split(' ')       # Tesseract OCR erkannt
        cardname=""
        for word in cardn:
            if len(word)>1:
                cardname+=word+' '
        cardname=cardname.lstrip().rstrip()
        print(cardname)                                # und einmalig ausgegeben
        card = Card.where(language='german').where(name=cardname).all()[0] # der Empfangene (bei mir deutsche) Kartenname
        print(card.name,card.id) # wird vom Magic SDK indefiziert und Name und Kartenid ausgegeben
        cardbool = True # da eine Karte gefunden wurde, wird der Cardbool auf true gesetz
    if cardbool: # ist dieser true wird der Kartenname auf das Bild übertragen
        cv2.putText(imCopy, str(card.name), (50, 180), cv2.FONT_HERSHEY_PLAIN, 4, (220, 220, 220), 12)
        cv2.putText(imCopy,str(card.name),(50,180),cv2.FONT_HERSHEY_PLAIN,4,(50,50,50),8)

    cv2.imshow("Karte", imCopy) # Das Bild wird an den Benutzer gegeben
    cv2.waitKey(1) # und eine ms gewartet bevor der loop wieder startet.