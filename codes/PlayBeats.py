# https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/

import pygame
import json

# 記錄檔相關參數初始化
musicName = '../resources/music01.mp3'		# 改成你要播的音樂
soundName = '../resources/soundDrum.wav'
fileName = '../data/data.json'

# 遊戲初始化
pygame.init()

# 視窗設定
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Beats Recorder')
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
drum = pygame.mixer.Sound(soundName)
dataList = []
startTime = 0
stopTime = 0

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
msg_font = pygame.font.SysFont('DFKai-SB', 60)
msg1 = msg_font.render('播放音樂和節奏中', True, (0, 0, 0))
screen.blit(msg1, (20, 100))
pygame.display.update()

# 記錄拍點 loop
musicStartAt = 0
pygame.mixer.music.play(0, musicStartAt/1000)
startTime = pygame.time.get_ticks()
print('Playing music...')
run = True
file = open(fileName)
dataArr = json.load(file)
p = 0
while run:
    if p == len(dataArr):
        while pygame.mixer.music.get_busy():
            continue
        run = False
    elif pygame.time.get_ticks()-startTime+musicStartAt > dataArr[p]['time']:
        pygame.mixer.Sound.play(drum)
        p += 1

file.close()

pygame.quit()
exit()
