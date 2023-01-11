# https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/

import pygame
import json
from datetime import datetime

# 記錄檔相關參數初始化
filePath = '../data/'

# 音訊初始化
dataList = []
startTime = 0
stopTime = 0
t = 1
unit = 686
start = 0

while t*unit < 90000:
    dataList.append({'time':t*unit+start, 'noteNum':0})
    t += 1

if dataList.__len__() != 0:
    timeNow = datetime.now()
    fileName = filePath + timeNow.strftime('data_%Y%m%d-%H%M%S') + '_fixed.json'
    with open(fileName, 'w') as f:
        json.dump(dataList, f, indent=4)

exit()
