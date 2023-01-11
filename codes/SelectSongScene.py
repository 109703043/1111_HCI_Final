import pygame
import cv2 as cv
import HandDetection as hand_detection
import json
import button
import Sound

# init parameters of resources
WIDTH = 1280
HEIGHT = 720
ORIGIN = (0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (100, 100, 100)
_sound = "../resources/button01.mp3"
_bg = '../resources/BG.png'
_bgFilter = '../resources/BGFilter.png'
_selectSong_song = '../resources/SelectSongScene_song.png'
_selectSong_btn0 = '../resources/SelectSongScene_btnPrevious.png'
_selectSong_btn1 = '../resources/SelectSongScene_btnNext.png'
_selectSong_back = '../images/back.png'
_smallHand = '../resources/hand_small_2.png'
songListPath = '../data/songList.json'
songListFile = open(songListPath)
songList = json.load(songListFile)
DELAY_TIME = 30



def ResetScreen(_screen):
    _screen.blit(bg, ORIGIN)
    _screen.blit(bgFilter, ORIGIN)



def ChangeSong(_screen, _index):
    ResetScreen(_screen)

    # buttons
    song.draw(_screen)
    btn0.draw(_screen)
    btn1.draw(_screen)
    back.draw(_screen)

    # song name
    txt_font = pygame.font.Font('../fonts/nasalization/nasalization-rg.otf', 48)
    msg = txt_font.render(songList[_index]['name'], True, COLOR_WHITE)
    _screen.blit(msg, (WIDTH*0.5 - msg.get_width()/2, HEIGHT*0.4))

    # song author
    txt_font = pygame.font.Font('../fonts/nasalization/nasalization-rg.otf', 32)
    msg = txt_font.render('by ' + songList[_index]['author'], True, COLOR_WHITE)
    _screen.blit(msg, (WIDTH*0.5 - msg.get_width()/2, HEIGHT*0.6))

    # song index
    txt_font = pygame.font.Font('../fonts/nasalization/nasalization-rg.otf', 20)
    msg = txt_font.render(str(_index+1) + '/' + str(len(songList)), True, COLOR_WHITE)
    _screen.blit(msg, (WIDTH*0.5 - msg.get_width()/2, HEIGHT*0.8))

    _screen.blit(smallHand, handpicRect)

    pygame.display.update()



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



def StartSelectSongScene(_screen, cap, tracker):
    # sound effect
    sound = Sound.sound(_sound)

    # background
    global bg
    bg = pygame.image.load(_bg).convert_alpha()
    bg = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
    global bgFilter
    bgFilter = pygame.image.load(_bgFilter).convert_alpha()
    bgFilter = pygame.transform.smoothscale(bgFilter, (WIDTH, HEIGHT))
    
    # elements in select song scene
    global song, btn0, btn1, back
    selectSong_song = pygame.image.load(_selectSong_song)
    selectSong_btn0 = pygame.image.load(_selectSong_btn0)
    selectSong_btn1 = pygame.image.load(_selectSong_btn1)
    selectSong_back = pygame.image.load(_selectSong_back)
    selectSong_back = pygame.transform.smoothscale(selectSong_back, (WIDTH*0.1, HEIGHT*0.1))
    song = button.Button(WIDTH*0.5-selectSong_song.get_width()/2, HEIGHT*0.5-selectSong_song.get_height()/2, selectSong_song)
    btn0 = button.Button(WIDTH*0.1, HEIGHT*0.5-100, selectSong_btn0)
    btn1 = button.Button(WIDTH*0.9-80, HEIGHT*0.5-100, selectSong_btn1)
    back = button.Button(WIDTH*0.1, HEIGHT*0.1, selectSong_back)
    btnInfos = [    [btn0.rect.topleft, selectSong_btn0.get_size()],
                    [btn1.rect.topleft, selectSong_btn1.get_size()],
                    [song.rect.topleft, selectSong_song.get_size()],
                    [back.rect.topleft, selectSong_back.get_size()]]

    # hand
    global smallHand
    smallHand = pygame.image.load(_smallHand)
    smallHand = pygame.transform.smoothscale(smallHand, (150, 150))
    global handpicRect
    handpicRect = smallHand.get_rect()

    # camera
    success, frame = cap.read()
    global camSize
    camSize = frame.shape
    # print(camSize)

    # main loop
    run = True
    clickTime = pygame.time.get_ticks()
    index = 0
    ChangeSong(_screen, index)
    while run:
        pygame.time.delay(DELAY_TIME)

        # update screen
        ChangeSong(_screen, index)

        # read camera
        success, frame = cap.read()
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        # hand detection
        hd_results = tracker.handsFinder(frame)  # hand detection
        lmList = tracker.positionFinder(hd_results)
        ConvertLmlist(lmList)
        handpicRect = tracker.toImage(lmList, handpicRect)

        # when the gesture is rock
        if(clickTime == 0 and len(lmList) > 0 and tracker.isRock(lmList)):
            # btn0 (previous song)
            if(isClicked(lmList[9], btnInfos[0])):
                clickTime = pygame.time.get_ticks()
                sound.play()
                index -= 1

            # btn1 (next song)
            elif(isClicked(lmList[9], btnInfos[1])):
                clickTime = pygame.time.get_ticks()
                sound.play()
                index += 1

            # select song
            elif(isClicked(lmList[9], btnInfos[2])):
                sound.play()
                run = False

            # back to StartScene
            elif(isClicked(lmList[9], btnInfos[3])):
                sound.play()
                index = -1
                run = False

        # click time
        if(pygame.time.get_ticks()-clickTime > 500):
            clickTime = 0

        # events
        for event in pygame.event.get():
            # exit program
            if(event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]):
                pygame.quit()
                exit()

            # click button
            if(pygame.mouse.get_pressed()[0]):
                # previous song
                if(btn0.draw(_screen) and index > 0 and clickTime == 0):
                    clickTime = pygame.time.get_ticks()
                    sound.play()
                    index -= 1

                # next song
                if(btn1.draw(_screen) and index < len(songList)-1 and clickTime == 0):
                    clickTime = pygame.time.get_ticks()
                    sound.play()
                    index += 1

                # background of song
                if(song.draw(_screen) and clickTime == 0):
                    sound.play()
                    run = False

                # back to StartScene
                if(back.draw(_screen) and clickTime == 0):
                    sound.play()
                    index = -1
                    run = False

    songListFile.close()
    return index



if(__name__ == '__main__'):

    # init game
    pygame.init()

    # init screen
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Select Song Scene (Test)')

    # init resources
    bg = pygame.image.load(_bg).convert_alpha()
    bg = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
    bgFilter = pygame.image.load(_bgFilter).convert_alpha()
    bgFilter = pygame.transform.smoothscale(bgFilter, (WIDTH, HEIGHT))

    # init standby scene for test
    ResetScreen(screen)
    msg_font = pygame.font.SysFont('arial', 40)
    msg1 = msg_font.render('SPACE: start test', True, COLOR_WHITE)
    msg2 = msg_font.render('ESE to exit', True, COLOR_WHITE)
    screen.blit(msg1, (20, 100))
    screen.blit(msg2, (20, 200))
    pygame.display.update()

    # loop: standby scene for test
    run = True
    while run:
        for event in pygame.event.get():
            # exit program
            if(event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]):
                pygame.quit()
                exit()
            # enter the next stage
            if(pygame.key.get_pressed()[pygame.K_SPACE]):
                run = False

    # start test
    StartSelectSongScene(screen)

    pygame.quit()
    exit()