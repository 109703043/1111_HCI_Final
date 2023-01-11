import pygame 
import cv2 as cv
import HandDetection as hand_detection
import button
import Sound
import ResultScene
import Game as game
# def main():

WIDTH = 1280
HEIGHT = 720
_smallHand = '../resources/hand_small_2.png'

#初始化遊戲
pygame.init()

#音樂初始化
pygame.mixer.init()

#視窗設定
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HAMUGA')

#背景圖
background_image = pygame.image.load('../images/monster.png')   
screen.blit(background_image,(0,0))

#遊戲名稱
hamuga_img = pygame.image.load('../images/name2.png')

#開始圖
start_img = pygame.image.load('../images/start.png')
# screen.blit(start_img,(370,400))

#設置圖
settings_img = pygame.image.load('../images/settings.png') 
# screen.blit(settings_img,(920,45))
# pygame.display.update()


#設置的背景圖
black_img = pygame.image.load('../images/black.jpeg')

#音樂鍵
music_img = pygame.image.load('../images/8.png')

#音效鍵
sound_img = pygame.image.load('../images/sound.png')

#返回鍵
back_img = pygame.image.load('../images/back.png')

#退出鍵
exit_img = pygame.image.load('../images/exit1.png')



start_buttun = button.Button(470, 405, start_img)
settings_button = button.Button(1120, 45, settings_img)
black_button = button.Button(400, 220, black_img)
music_button = button.Button(480, 300, music_img)
sound_button = button.Button(620, 300, sound_img)
back_button = button.Button(450, 420, back_img)
exit_button = button.Button(630, 420, exit_img)
btnInfos = [    [black_button.rect.topleft, black_img.get_size()],
                [music_button.rect.topleft, music_img.get_size()],
                [sound_button.rect.topleft, sound_img.get_size()],
                [back_button.rect.topleft, back_img.get_size()],
                [exit_button.rect.topleft, exit_img.get_size()],
                [start_buttun.rect.topleft, start_img.get_size()],
                [settings_button.rect.topleft, settings_img.get_size()]]

#Game variables
game_paused = False

#Music variables
music_muted = False

#背景音樂
musicName = '../resources/群青.mp3'
pygame.mixer.music.load(musicName)
pygame.mixer.music.play(3)
pygame.mixer.music.set_volume(0.2)

#音效
soundName = "../resources/button01.mp3"
sound_ = Sound.sound(soundName)

# camera
global cap
cap = cv.VideoCapture(0)  
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))      
#    cap.set(cv.CAP_PROP_FPS, 30)
success, frame = cap.read()
global camSize
camSize = frame.shape
# print(camSize)

# hand detection
global tracker
tracker = hand_detection.handTracker()
global smallHand
smallHand = pygame.image.load(_smallHand)
smallHand = pygame.transform.smoothscale(smallHand, (150, 150))
global handpicRect
handpicRect = smallHand.get_rect()



def ConvertLmlist(lmlist):
    for i in range(len(lmlist)):
        lmlist[i][1] *= WIDTH/camSize[1]
        lmlist[i][2] *= HEIGHT/camSize[0]
    return



def isClicked(lm, btnInfo):
    if( btnInfo[0][0] < lm[1]
        and lm[1] < btnInfo[0][0] + btnInfo[1][0]
        and btnInfo[0][1] < lm[2]
        and lm[2] < btnInfo[0][1] + btnInfo[1][1]):
        return True
    return False



#畫面
run = True
clickTime = 0
turnOffSound = False
while run:
    
    screen.blit(background_image,(0,0))
    screen.blit(hamuga_img,(350,200))

    # settings panel on
    if game_paused == True:
        if black_button.draw(screen):
            pass
        if music_button.draw(screen):
            clickTime = pygame.time.get_ticks()
            if music_muted == False:
                sound_.play()
                pygame.mixer.music.set_volume(0)
                music_muted = True
            else:                
                sound_.play()
                pygame.mixer.music.set_volume(0.2)
                music_muted = False
        if sound_button.draw(screen):
            clickTime = pygame.time.get_ticks()
            sound_.play()
            sound_.stop()

        if back_button.draw(screen):
            clickTime = pygame.time.get_ticks()
            sound_.play()
            game_paused = False
        
        if exit_button.draw(screen):
            sound_.play()
            run = False
            
    # settings panel off
    else:
        if start_buttun.draw(screen) and clickTime == 0:
            sound_.play()

            #擺遊戲介面進去
            if(game.main(cap, tracker) != 1):
                pygame.mixer.music.load(musicName)
                pygame.mixer.music.play(3)
                pygame.mixer.music.set_volume(0.2)

        if settings_button.draw(screen):
            clickTime = pygame.time.get_ticks()
            sound_.play()
            game_paused = True

    # read camera
    success, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # hand detection
    hd_results = tracker.handsFinder(frame)  # hand detection
    lmList = tracker.positionFinder(hd_results)
    ConvertLmlist(lmList)
    handpicRect = tracker.toImage(lmList, handpicRect)
    screen.blit(smallHand, handpicRect)

    # when the gesture is rock
    if(clickTime == 0 and len(lmList) > 0 and tracker.isRock(lmList)):
        # settings panel on
        if(game_paused):
            # black panel
            if(isClicked(lmList[9], btnInfos[0])):
                pass
            # music btn
            if(isClicked(lmList[9], btnInfos[1])):
                clickTime = pygame.time.get_ticks()
                if music_muted == False:
                    sound_.play()
                    pygame.mixer.music.set_volume(0)
                    music_muted = True
                else:                
                    sound_.play()
                    pygame.mixer.music.set_volume(0.2)
                    music_muted = False
            # sound btn
            if(isClicked(lmList[9], btnInfos[2])):
                clickTime = pygame.time.get_ticks()
                sound_.play()
                sound_.stop()
            # back btn
            if(isClicked(lmList[9], btnInfos[3])):
                clickTime = pygame.time.get_ticks()
                sound_.play()
                game_paused = False
            # exit btn
            if(isClicked(lmList[9], btnInfos[4])):
                sound_.play()
                run = False
        # settings panel off
        else:
            # start btn
            if(isClicked(lmList[9], btnInfos[5])):
                sound_.play()

                #擺遊戲介面進去
                if(game.main(cap, tracker) != 1):
                    pygame.mixer.music.load(musicName)
                    pygame.mixer.music.play(3)
                    pygame.mixer.music.set_volume(0.2)
            # settings btn
            if(isClicked(lmList[9], btnInfos[6])):
                clickTime = pygame.time.get_ticks()
                sound_.play()
                game_paused = True

    pygame.display.update()

    # click time
    if(pygame.time.get_ticks()-clickTime > 1000):
        clickTime = 0

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        if event.type == pygame.QUIT:
            run = False