from pickle import TRUE
import sys
from tkinter import Y
import pygame
import json
import cv2 as cv
import numpy as np
from pygame.locals import *
import HandDetection as hand_detection


musicName = "../resources/music01.mp3"
soundName = "../resources/soundDrum.wav"
noteName = "../resources/circle.png"
fileName = "../data/data.json"
movingNoteName = "../resources/circular-arrow_small.png"
backgroudName = "../resources/background_combined_3.png"
ciecleName = "../resources/circle_2.png"
width = 1280
height = 720
bg = (255, 255, 255)
NOTE_SIZE = 200
MOVINGNOTE_SIZE = 150
APPEAR_TIME = 330
SPEED = 15


def GenerateMovingNote(noteNum, handpicRect):
    global speed
    position = movingNote.get_rect()
    x, y = width / 2, height / 2  # screen center

    # the final position of each movingNote
    if noteNum == 0:  # up
        x, y = x, y - NOTE_SIZE - MOVINGNOTE_SIZE / 2
        speed = [0, SPEED]
        position.center = (x, 0)
    elif noteNum == 1:  # left
        x, y = x - NOTE_SIZE - MOVINGNOTE_SIZE / 2, y
        speed = [SPEED, 0]
        position.center = (0, y)
    elif noteNum == 2:  # right
        x, y = x + NOTE_SIZE - MOVINGNOTE_SIZE / 2, y
        speed = [-SPEED, 0]
        position.center = (width, y)
    elif noteNum == 3:  # down
        x, y = x, y + NOTE_SIZE - MOVINGNOTE_SIZE / 2
        speed = [0, -SPEED]
        position.center = (x, height)

    run = True
    while run:
        position = position.move(speed)
        #screen.fill(bg)
        screen.blit(background,(0,0))
        
        # hand detection
        success, frame = cap.read()
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) 
        hd_results = tracker.handsFinder(frame)
        lmList = tracker.positionFinder(hd_results)  
        handpicRect = tracker.toImage(lmList, handpicRect)
        screen.blit(handpic, handpicRect)   

        screen.blit(text_perfect, text_P_Rect)
        screen.blit(text_miss, text_M_Rect)
        screen.blit(movingNote, position)
        pygame.display.update()         
        if noteNum == 0:
            if position.y > y:
                run = False
        elif noteNum == 1:
            if position.x > x:
                run = False
        elif noteNum == 2:
            if position.x < x:
                run = False
        elif noteNum == 3:
            if position.y < y:
                run = False

    # pygame.mixer.Sound.play(drum)
    # screen.blit(note, (x, y))
    # pygame.display.update()


def GenerateNote(noteNum):
#    pygame.mixer.Sound.play(drum)
    x, y = width / 2 - NOTE_SIZE / 2, height / 2 - NOTE_SIZE / 2
    if noteNum == 0:  # up
        x, y = x, y - NOTE_SIZE
    elif noteNum == 1:  # left
        x, y = x - NOTE_SIZE, y
    elif noteNum == 2:  # right
        x, y = x + NOTE_SIZE, y
    elif noteNum == 3:  # down
        x, y = x, y + NOTE_SIZE
    # screen.fill((255, 255, 255))
    screen.blit(note, (x, y))
    pygame.display.update()

def CheckArea(noteNum):
    if noteNum == 0:
        return rect_0
    if noteNum == 1:
        return rect_1
    if noteNum == 2:
        return rect_2
    if noteNum == 3:
        return rect_3

def pointsInArea(handpicRect, noteNum):
    rect_now = CheckArea(noteNum)
    counter = 0
    if len(handpicRect) != 0:
        if rect_now[0] < handpicRect[0] and handpicRect[0] < rect_now[0]+200 and rect_now[1] < handpicRect[1] and handpicRect[1] < rect_now[1]+200:
            counter += 1
    return counter


def main():

    pygame.init()
    global screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Final")

    global cap
    cap = cv.VideoCapture(0)        
#    cap.set(cv.CAP_PROP_FPS, 30)
    # hand detection
    global tracker
    tracker = hand_detection.handTracker() 
    global background
    background = pygame.image.load(backgroudName)
    background = pygame.transform.smoothscale(background, (width, height))

    global handpic
    handpic = pygame.image.load("../resources/hand_small_2.png")
    handpic = pygame.transform.smoothscale(handpic, (150, 150))
    handpic.convert_alpha()
    handpicRect = handpic.get_rect()   
    # Settings
    perfect=0
    miss=0
    font = pygame.font.Font('freesansbold.ttf', 38)
    # 矩形範圍
    global rect_0, rect_1, rect_2, rect_3
    rect_0 = pygame.Rect(0, 0, NOTE_SIZE, NOTE_SIZE)        #上
    rect_0.center = (width/2, height/2-NOTE_SIZE)
    rect_1 = pygame.Rect(0, 0, NOTE_SIZE, NOTE_SIZE)        #左
    rect_1.center = (width/2-NOTE_SIZE, height/2)
    rect_2 = pygame.Rect(0, 0, NOTE_SIZE, NOTE_SIZE)        #右
    rect_2.center = (width/2+NOTE_SIZE, height/2)
    rect_3 = pygame.Rect(0, 0, NOTE_SIZE, NOTE_SIZE)        #下
    rect_3.center = (width/2, height/2+NOTE_SIZE)

    #可以改成選歌畫面
    screen.fill(bg)
    msg_font = pygame.font.SysFont("DFKai-SB", 40)
    msg1 = msg_font.render("space to play music", True, (100, 100, 100))
    msg2 = msg_font.render("Esc to quit", True, (100, 100, 100))
    screen.blit(msg1, (20, 100))
    screen.blit(msg2, (20, 200))
    pygame.display.update()

    global drum
    pygame.mixer.music.load(musicName)
    pygame.mixer.music.set_volume(0.1)
    drum = pygame.mixer.Sound(soundName)
    startTime = 0

    global note
    note = pygame.image.load(noteName)
    note = pygame.transform.smoothscale(note, (NOTE_SIZE, NOTE_SIZE))
    note.convert_alpha()

    # initialize the moving notes
    global movingNote, position
    movingNote = pygame.image.load(movingNoteName)
    movingNote = pygame.transform.smoothscale(
        movingNote, (MOVINGNOTE_SIZE, MOVINGNOTE_SIZE)
    )
    movingNote.convert_alpha()
    position = movingNote.get_rect()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                run = False

    screen.fill(bg)
    pygame.display.update()

    # main loop
    musicStartAt = 0
    pygame.mixer.music.play(0, musicStartAt / 1000)
    startTime = pygame.time.get_ticks()
    print("Play music...")
    file = open(fileName)
    dataArr = json.load(file)

    # distance to move
    global distance_x, distance_y
    distance_x = width / 2 - NOTE_SIZE / 2 - MOVINGNOTE_SIZE / 2
    distance_y = height / 2 - NOTE_SIZE / 2 - MOVINGNOTE_SIZE / 2

    global PREVIEW_TIME
    p = 0
    run = True
    while run:
        # read camera
        success, frame = cap.read()
        frame = cv.flip(frame, 1)
        #frame = np.rot90(frame)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        # hand detection
        hd_results = tracker.handsFinder(frame)  # hand detection
        lmList = tracker.positionFinder(hd_results)
        
        # handToPic
        handpicRect = tracker.toImage(lmList, handpicRect)
        surf = pygame.surfarray.make_surface(hd_results)
        surf = pygame.transform.scale(surf,(width,height))      #調整webcam畫面大小
        #screen.blit(surf, (0,0))
        
        # Display background and handpic
        screen.blit(background,(0,0))
        screen.blit(handpic, handpicRect)
        pygame.display.flip()
        
        # Display score
        global text_perfect,text_miss,text_M_Rect,text_P_Rect
        text_perfect = font.render('PERFECT: '+str(perfect), True, (255, 255, 255)) #display score
        text_P_Rect = text_perfect.get_rect()
        text_P_Rect.center = (1000, 100)
        screen.blit(text_perfect, text_P_Rect)
        text_miss = font.render('MISS: '+str(miss), True, (255, 255, 255)) #display score
        text_M_Rect = text_miss.get_rect()
        text_M_Rect.center = (1000, 200)
        screen.blit(text_miss, text_M_Rect)        

        duration = pygame.time.get_ticks() - startTime + musicStartAt

        # setting PREVIEW_TIME
        if dataArr[p]["noteNum"] == 1 or dataArr[p]["noteNum"] == 2:
            PREVIEW_TIME = distance_x / SPEED
        elif dataArr[p]["noteNum"] == 0 or dataArr[p]["noteNum"] == 3:
            PREVIEW_TIME = distance_y / SPEED

        if dataArr[p]["time"] == -1:  # music end
            while pygame.mixer.music.get_busy():
                continue
            run = False
        elif duration > dataArr[p]["time"] - PREVIEW_TIME:  # note start moving
            noteNum = dataArr[p]["noteNum"]
            p += 1
            GenerateMovingNote(noteNum, handpicRect)
            pygame.display.flip()
            # Counting Score
            if pointsInArea(handpicRect, noteNum)==1:
                GenerateNote(noteNum)
                pygame.mixer.Sound.play(drum) 
                perfect=perfect+1
            else:
                miss=miss+1
            pygame.display.flip()
        elif p > 0 and duration > dataArr[p - 1]["time"] + APPEAR_TIME:
            #screen.fill(bg)
            pygame.display.update()

        if not pygame.mixer.music.get_busy():
            #可以加上結算畫面
            pygame.quit()
            exit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

    file.close()

    pygame.quit()
#    exit()


#main()
