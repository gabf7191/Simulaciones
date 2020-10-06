#GB modulo de Scaneo de QR.
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import time
Num = 0

def Scan():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    Num = "0"

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    Listbarcode = decode(frame)
    #time.sleep(.5)
    for barcode in Listbarcode:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)

        #print(barcode.data)
        #print(barcode.type)
        Num = barcode.data
        #print(int(Num[len(Num)-1:len(Num)]))


        #cv2.imshow('frame',gray)





    cap.release()
    cv2.destroyAllWindows()
    dato= int(Num[len(Num)-1:len(Num)])
    return (dato)

