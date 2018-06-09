# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 16:54:07 2018

@author: Cheng
"""

import cv2

#使用KNN
bs = cv2.createBackgroundSubtractorKNN(detectShadows = True)
camera = cv2.VideoCapture('D:\\lalalalala\\documents\\beautifulLife\\python_3\\dadadada.mp4')

while True:
  ret, frame = camera.read()
  fgmask = bs.apply(frame)
  th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
  th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 2)
  dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,3)), iterations = 2)
  #识别目标，轮廓检测，绘制结果
  image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  for c in contours:
    if cv2.contourArea(c) > 1000:
      (x,y,w,h) = cv2.boundingRect(c)
      cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)

  cv2.imshow("mog", fgmask) 
  cv2.imshow("thresh", th)
  cv2.imshow("diff", frame & cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR))
  cv2.imshow("detection", frame)
  k = cv2.waitKey(30) & 0xff#在此等待30Ms及以上，等待时间内waitKey函数的输出是255，与0xff对应的十进制255相与，
  #直到键盘输入一个键，它对应的ascii码值会存入k。
 # print("%s" %k)#验证此时的k值，运行起来后每按一次esc就打印1个27
  if k == 27: #27是esc的ascii码值。
      break
  
exit()#exit的作用是程序退出后更新console，注释掉就不更新，保留之前运行的结果


camera.release()
cv2.destroyAllWindows()