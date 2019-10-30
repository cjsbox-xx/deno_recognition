import numpy as np
import cv2
import sys
from coins import *
from denominations import *

def is_rectangle(approxPoly):
    return len(approxPoly) == 4

def is_circle(approxPoly):
    return len(approxPoly) >= 12 and len(approxPoly) <= 14

font = cv2.FONT_HERSHEY_COMPLEX
image_path = sys.argv[1]
roi = cv2.imread(image_path)
orig_image = roi.copy()

change = 0.0
edged = cv2.Canny(roi, 30, 200) 
cv2.imshow('Detected thres ',edged)

contours,h = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    if is_rectangle(approx):
        cv2.drawContours(roi,[cnt],0,(0,0,255),3)
        x,y,w,h = cv2.boundingRect(approx)
        #cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 0, 255), 1);

        cropped = orig_image[y: y + h, x: x + w]
        #cv2.imshow('Detected denomination',cropped)
        valueProvider = DenominationImageValueProvider(cropped)
        denomination_value = valueProvider.provide()
        change = change + denomination_value

        cv2.putText(roi, str(denomination_value), (x, y - 5), font, 0.8, (0, 0, 255), lineType=cv2.LINE_AA) 
        
    elif is_circle(approx):
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        x = int(x)
        y = int(y)
        radius = int(radius)
        cv2.circle(roi,(x,y),radius,(0,0,255),2)

        cropped = orig_image[y - radius: y + radius, x - radius: x + radius]
        #cv2.imshow('Detected coins',cropped)
        valueProvider = CoinImageValueProvider(cropped)
        coin_value = valueProvider.provide()
        change = change + coin_value

        cv2.putText(roi, str(coin_value), (x, y - radius), font, 0.8, (0, 0, 255), lineType=cv2.LINE_AA) 

cv2.imshow('Detected coins',roi)
print("Total denominations and coins sum: %.2f" % round(change, 2))
while(1):
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k) # else print its value
