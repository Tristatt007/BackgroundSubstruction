# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 21:41:36 2018

@author: Cheng
"""

import cv2

camera = cv2.VideoCapture('D:\\lalalalala\\documents\\beautifulLife\\python_3\\dadadada.mp4')# 参数0表示第一个摄像头
mog = cv2.createBackgroundSubtractorMOG2()#混合高斯分离的方法，放进对象mog里面

while (1):
    ret, frame_lwpCV = camera.read()#camera读到后，ret作为返回值，frame_lwpCV为读到的图片序列
    fgmask = mog.apply(frame_lwpCV)#把读到的每一帧都过一遍mog函数，然后存在fgmask里面
    cv2.imshow('frame', fgmask)#把fgmask放进frame，然后显示出来
    k = cv2.waitKey(30)&0xff
    #print("%s" %k)
    if k==27:#27是esc的ascii码值。
        break
camera.release()
#exit()
cv2.destroyAllWindows()