# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:48:09 2018

@author: Cheng
"""
import cv2
import sys
import numpy as np 

class codeword:
    def __init__(self, rgbVec):
        I = rgb2gray(rgbVec)
        self.min = np.maximum(0, I - alpha)
        self.max = np.minimum(255, I + alpha)
        self.f = 1
        self.l = 0
        self.first = t
        self.last = t
        
class codebook:
    
    def __init__(self, frame):#在于实例化调用codebook类时，self下的变量全都激活。
        self.Tdel = 200
        self.Tadd = 150
        self.Th = 200
        self.learningFrams = 10 
        self.h = frame.shape[0] 
        self.w = frame.shape[1]
        self.cbMain = tuple(tuple(list() for i in range(self.w)) for j in range(self.h))
        self.cbCache = tuple(tuple(list() for i in range(self.w)) for j in range(self.h))

    def add_codeword(self, I, rgbVec):#第一种情况，没有匹配值被返回的情况，创建新的codeword
        v = (rgbVec[0], rgbVec[1], rgbVec[2])#定义codeword，进来的点的颜色向量为v
        min = max = I#像素点的亮度
        f = 1 
        l = t-1
        first = last = t
        return (min, max, f, l, first, last, v)#包括了vi和aux
    
    def update_codeword(self, I, cw, rgbVec):#第二种情况，有匹配值时，更新book里的codeword
        f = cw[2]
        v = cw[6]
        v = ((f*v[0] + rgbVec[0])/(f+1), (f*v[1] + rgbVec[1])/(f+1), (f*v[2] + rgbVec[2])/(f+1))
        min = np.minimum(I, cw[0])
        max = np.maximum(I, cw[1])
        f = f + 1
        l = 0
        last = t
        return (min, max, f, l, cw[4], last, v)
    
    def fg_rec(self, frame, img_foreground):
        for i in range(0, self.h):
            for j in range(0, self.w):
                x = [frame[i][j][0], frame[i][j][1], frame[i][j][2]]
                I = rgb2gray(x)
                found = False
                bookM = self.cbMain[i][j]
                for cw in bookM:
                    if cw.min <= I <= cw.max and not found:
                        found = True
                        cw.min = (int) ((1 - beta)*(I - alpha)) + (beta*cw.min)
                        cw.max = (int) ((1 - beta)*(I + alpha)) + (beta*cw.max)
                        cw.f += 1
                        cw.l = 0
                        cw.last = t
                    else:
                        cw.l += 1

                    if t > self.learningFrams and cw.l >= self.Tdel:
                        bookM.remove(cw)

                if not found and t <= self.learningFrams:
                        bookM.append(codeword(x))

                if t > self.learningFrams:
                    if not found:
                        img_foreground[i][j][0:3] = 255

                if found:
                    continue

                if t > self.learningFrams:
                    found = False
                    bookC = self.cbCache[i][j]
                    for cw in bookC:
                        if cw.min <= I <= cw.max and not found:
                            found = True
                            cw.min = (int)((1 - beta) * (I - alpha)) + (beta * cw.min)
                            cw.max = (int)((1 - beta) * (I + alpha)) + (beta * cw.max)
                            cw.f += 1
                            cw.l = 0
                            cw.last = t
                        else:
                            cw.l += 1

                        if cw.l >= self.Th:
                            bookC.remove(cw)
                        else:
                            if cw.f > self.Tadd:
                                bookM.append(cw)
                                bookC.remove(cw)

                    if not found:
                        bookC.append(codeword(x))

def colordist(x, v):
    return np.sqrt(np.sum(np.square(x)) - np.square(np.sum(x*v))/np.sum(np.square(v)))

def brightness(I, cw):
    Ilow = 0.65*cw[1]
    Ihigh = np.minimum(1.3*cw[1], cw[0]/0.65)
    if (Ilow <= I <= Ihigh):
        return True
    else:
        return False

def rgb2gray(v):
    return (0.299*v[0] + 0.587*v[1] + 0.114*v[2])

def main(argv):
    global firstTime, t, Tdist, alpha, beta
    firstTime = True
    t = 0
    Tdist = 12.8
    alpha = 10
    beta = 0.8
    video = cv2.VideoCapture(argv)
   # fgbg = cv2.createBackgroundSubtractorMOG2()

    # Check if camera opened successfully
    if (video.isOpened() == False):
        print("Error opening video stream or file")

    # Read until video is completed
    while (video.isOpened()):

        # Capture frame-by-frame
        ret, frame = video.read()

        if ret:

            if firstTime is True:
                cb = codebook(frame)
                videoOut = cv2.VideoWriter("ForeGround.mp4", cv2.VideoWriter_fourcc(*'XVID'), 15, (cb.w, cb.h))#函数实例化调用，给变量videoOut
                firstTime = False

            img_foreground = np.zeros((cb.h, cb.w, 3), dtype="uint8")#zeros里面两个参数分别是形状和数据类型。形状shape里的三个参数分别是h,w,channel.
            cb.fg_rec(frame, img_foreground)

            # img_foreground = fgbg.apply(frame)

            videoOut.write(img_foreground)

            # # Display the resulting frame
            # cv2.imshow('Frame', frame)
            # cv2.imshow('ForeGround', img_foreground)
            #
            # # # Press Q on keyboard to  exit
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     break

            t += 1

        # Break the loop
        else:
            break

        print(t, (int) (t/15))
   
    video.release()
    videoOut.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if sys.argv.__len__() > 2:
        print("Only one file is accepted one time.")
    main('dadadada.mp4')