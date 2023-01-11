# https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/

import pygame
import json
from datetime import datetime

# 記錄檔相關參數初始化
filePath = '../data/sheetMusic03.json'

file = open(filePath)
dataArr = json.load(file)
p = 0
while(p < len(dataArr)):
    dataArr[p]['time'] += -380
    p += 1

with open(filePath, 'w') as f:
    json.dump(dataArr, f, indent=4)

file.close()

exit()
