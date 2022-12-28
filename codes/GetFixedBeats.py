# https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/

import pygame
import json
from datetime import datetime

# 記錄檔相關參數初始化
musicName = '../resources/music01.mp3'   # 改成你要播的音樂
musicStartAt = 0				        # 改成你要開始的時間點
filePath = '../data/'

# 遊戲初始化
pygame.init()

# 音訊初始化
dataList = []
startTime = 0
stopTime = 0
t = 1
unit = 353
start = 1900

while t*353 < 100000:
    dataList.append({'time':t*unit+start, 'noteNum':0})
    t += 1

if dataList.__len__() != 0:
    timeNow = datetime.now()
    fileName = filePath + timeNow.strftime('data_%Y%m%d-%H%M%S') + '_fixed.json'
    with open(fileName, 'w') as f:
        json.dump(dataList, f, indent=4)

pygame.quit()
exit()
