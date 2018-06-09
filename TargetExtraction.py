# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 22:44:52 2018

@author: Cheng
"""

import numpy as np
import cv2


cap = cv2.VideoCapture('D:\\lalalalala\\documents\\beautifulLife\\python_3\\dadadada.mp4')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame1 = np.zeros((640,480))
#out = cv2.VideoWriter(datetime.datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S%p")+'.avi',fourcc, 5.0, np.shape(frame1))

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    (_,cnts, _) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maxArea = 0
    for c in cnts:
        Area = cv2.contourArea(c)
        if Area < maxArea :
        #if cv2.contourArea(c) < 500:
            (x, y, w, h) = (0,0,0,0)
            continue
        else:
            if Area < 1000:
                (x, y, w, h) = (0,0,0,0)
                continue
            else:
                maxArea = Area
                m=c
                (x, y, w, h) = cv2.boundingRect(m)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame',frame)
    k = cv2.waitKey(30)&0xff
    if k==27:
        break
    

cap.release()
exit()
cv2.destroyAllWindows()