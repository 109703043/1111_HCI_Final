# https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/

import pygame
import json

# 使用檔案相關參數初始化
musicName = '../resources/music01.mp3'	    # 改成你要播的音樂
soundName = '../resources/soundDrum.wav'
fileName = '../data/data_slowVer.json'
noteName = '../resources/circle.png'
WIDTH = 1280
HEIGHT = 720
NOTE_SIZE = 150
APPEAR_TIME = 330
# PREVIEW_TIME = 1000
PREVIEW_TIME = 0
MUSIC_START_AT = 50000

NOTE_POSITION = [(WIDTH/2-NOTE_SIZE/2, HEIGHT/2-3*NOTE_SIZE/2), (WIDTH/2-3*NOTE_SIZE/2, HEIGHT/2-NOTE_SIZE/2), (WIDTH/2+NOTE_SIZE/2, HEIGHT/2-NOTE_SIZE/2), (WIDTH/2-NOTE_SIZE/2, HEIGHT/2+NOTE_SIZE/2)]



def ResetScreen():
    screen.fill((255, 255, 255))
    pygame.display.update()

def GenerateNote(noteNum):
    pygame.mixer.Sound.play(drum)
    screen.fill((255, 255, 255))
    screen.blit(note, NOTE_POSITION[noteNum])
    pygame.display.update()



def main():

    # 遊戲初始化
    pygame.init()

    # 視窗設定
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Beats Visual Player')

    # 畫面設定
    screen.fill((255, 255, 255))
    msg_font = pygame.font.SysFont('DFKai-SB', 40)
    msg1 = msg_font.render('空白鍵：播音樂', True, (100, 100, 100))
    msg2 = msg_font.render('Esc：退出', True, (100, 100, 100))
    screen.blit(msg1, (20, 100))
    screen.blit(msg2, (20, 200))
    pygame.display.update()

    # 音訊初始化
    pygame.mixer.init()
    pygame.mixer.music.load(musicName)
    global drum
    drum = pygame.mixer.Sound(soundName)
    startTime = 0

    # 圓圈初始化
    global note
    note = pygame.image.load(noteName)
    note = pygame.transform.smoothscale(note, (NOTE_SIZE, NOTE_SIZE))
    note.convert_alpha()
    global notes
    notes = [False, False, False, False]
    global X, y
    X = [WIDTH/2-NOTE_SIZE/2, WIDTH/2-NOTE_SIZE/2*3, WIDTH/2+NOTE_SIZE/2*3, WIDTH/2-NOTE_SIZE/2]
    Y = [HEIGHT/2-NOTE_SIZE/2]

    # 待機畫面 loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                run = False

    # 更新畫面
    screen.fill((255, 255, 255))
    pygame.display.update()

    # main loop
    pygame.mixer.music.play(0, MUSIC_START_AT/1000)
    startTime = pygame.time.get_ticks()
    print('Playing music...')
    run = True
    file = open(fileName)
    dataArr = json.load(file)
    p = 0
    while run:
        duration = pygame.time.get_ticks()-startTime+MUSIC_START_AT
        if(dataArr[p]['time'] == -1):
            while pygame.mixer.music.get_busy():
                continue
            run = False
        elif duration > dataArr[p]['time'] - PREVIEW_TIME:
            noteNum = dataArr[p]['noteNum']
            p += 1
            GenerateNote(noteNum)
        elif(p > 0 and duration > dataArr[p-1]['time'] + APPEAR_TIME):
            ResetScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

    file.close()

    pygame.quit()
    exit()



main()