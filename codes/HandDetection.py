from datetime import datetime
import cv2 as cv
import argparse
import mediapipe as mp
import pygame

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                            OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

picPath = './GeneratedPictures/'

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self,image,draw=True):
        imageRGB = cv.cvtColor(image,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self,image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
            if draw:
                cv.circle(image,(cx,cy), 15 , (255,0,255), cv.FILLED)

        return lmlist

    def pointsInArea(self,lmList,x1,y1,x2,y2):  #no use
        counter = 0
        if len(lmList) != 0:
#            for id in range(len(lmList)):
                if x1 < lmList[9][1] and lmList[9][1] < x2 and y1 < lmList[9][2] and lmList[9][2] < y2:
                        counter += 1
        return counter
    
    def toImage(self, lmList, position):
        if len(lmList) != 0 and lmList[9][1]!=0 and lmList[9][2]!=0:
            position.center = (lmList[9][1],lmList[9][2])

        return position