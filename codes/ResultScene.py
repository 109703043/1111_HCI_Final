import pygame
import cv2 as cv
import mediapipe as mp

# init parameters of resources
WIDTH = 1280
HEIGHT = 720
ORIGIN = (0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (100, 100, 100)
_result_bg = 'resources/ResultScene_BG.png'
_result_bgFilter = 'resources/ResultScene_BGFilter.png'
_result_title = 'resources/ResultScene_ResultTitle.png'
_result_box = 'resources/ResultScene_ResultBox.png'
MAX_SCORE = 100000
DELAY_TIME = 30
ANIMATION_FRAME = 12

# init parameters for test
test_name = "Fluorite Eyes' Song"
test_perfect = 100
test_miss = 12



def ResetScreen():
    screen.blit(result_bg, ORIGIN)
    screen.blit(result_bgFilter, ORIGIN)
    pygame.display.update()



def StartResultScene(_songName, _perfect, _miss):
    # init resources
    score = MAX_SCORE/(_perfect+_miss)*_perfect + -100*_miss
    if(score < 0):
        score = 0
    result_resources = []
    result_title = pygame.image.load(_result_title).convert_alpha()
    result_title = pygame.transform.smoothscale(result_title, (WIDTH, HEIGHT))
    result_box = pygame.image.load(_result_box).convert_alpha()
    result_box = pygame.transform.smoothscale(result_box, (WIDTH, HEIGHT))
    result_txt = [  ['RESULT', 56],
                    [_songName, 40],
                    ['perfect', 32],
                    ['miss', 32],
                    ['accuracy', 32],
                    [str(_perfect), 32],
                    [str(_miss), 32],
                    [str(round(_perfect/(_perfect+_miss)*100, ndigits=2)) + '%', 36],
                    [str(round(score)) + '/' + str(MAX_SCORE), 40],
                    ['tap to continue...', 24]]
    result_positions = [    ORIGIN,
                            [WIDTH*0.1, HEIGHT*0.15],
                            ORIGIN,
                            [WIDTH*0.1, HEIGHT*0.35],
                            [WIDTH*0.15, HEIGHT*0.5],
                            [WIDTH*0.15, HEIGHT*0.6],
                            [WIDTH*0.15, HEIGHT*0.7],
                            [WIDTH*0.5, HEIGHT*0.5],
                            [WIDTH*0.5, HEIGHT*0.6],
                            [WIDTH*0.5, HEIGHT*0.7],
                            [WIDTH*0.618, HEIGHT*0.35],
                            [WIDTH*0.75, HEIGHT*0.8]    ]
    flySpeed = WIDTH/ANIMATION_FRAME
    fadeInSpeed = 256/ANIMATION_FRAME

    # title image
    result_resources.append(result_title)
    # title text
    txt_font = pygame.font.Font('fonts/nasalization/nasalization-rg.otf', result_txt[0][1])
    msg = txt_font.render(result_txt[0][0], True, COLOR_WHITE)
    result_resources.append(msg)
    # box
    result_resources.append(result_box)
    # texts
    for i in range(1, len(result_txt)):
        txt_font = pygame.font.Font('fonts/nasalization/nasalization-rg.otf', result_txt[i][1])
        msg = txt_font.render(result_txt[i][0], True, COLOR_WHITE)
        result_resources.append(msg)

    # loading resources (fly)
    index = 0
    x, y = -result_resources[index].get_width(), result_positions[index][1]
    skipClock = 0
    toAddIndex = False
    while(index < len(result_resources)-2):
        pygame.time.delay(DELAY_TIME)

        # moving
        if(x <= result_positions[index][0]):
            ResetScreen()

            # the loaded resources
            for i in range(index):
                screen.blit(result_resources[i], result_positions[i])
            # the loading resource
            screen.blit(result_resources[index], (x, y))
            pygame.display.update()

            # adjust position
            x += flySpeed
            if(x > result_positions[index][0]):
                x = result_positions[index][0]
            if(x == result_positions[index][0]):    # reached target position
                toAddIndex = True

        # events
        for event in pygame.event.get():
            # exit program
            if(event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]):
                pygame.quit()
                exit()
            # skip to the next step
            elif(pygame.key.get_pressed()[pygame.K_SPACE] and skipClock == 0):
                skipClock = pygame.time.get_ticks()
                index = len(result_resources)-2
        
        # check if index was added
        if(toAddIndex):
            toAddIndex = False
            index += 1
            if(index < len(result_resources)-2):
                x, y = -result_resources[index].get_width(), result_positions[index][1]

    # loading resources (fade in)
    alpha = 0
    toAddIndex = False
    while(index < len(result_resources)):
        pygame.time.delay(DELAY_TIME)

        # moving
        if(alpha < 255):
            ResetScreen()

            # the loaded resources
            for i in range(index):
                screen.blit(result_resources[i], result_positions[i])
            # the loading resource
            result_resources[index].set_alpha(alpha)
            screen.blit(result_resources[index], result_positions[index])
            pygame.display.update()

            # adjust transparency
            alpha += fadeInSpeed
            if(alpha > 255):
                alpha = 255
            if(alpha == 255):    # reached target alpha
                toAddIndex = True

        # events
        for event in pygame.event.get():
            # exit program
            if(event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]):
                pygame.quit()
                exit()
            # skip to the next step
            elif(pygame.key.get_pressed()[pygame.K_SPACE] and skipClock == 0):
                skipClock = pygame.time.get_ticks()
                index = len(result_resources)
        
        # check if index was added
        if(toAddIndex):
            toAddIndex = False
            index += 1
            if(index < len(result_resources)):
                alpha = 0

    # done loading
    ResetScreen()
    for i in range(len(result_resources)):
        screen.blit(result_resources[i], result_positions[i])
    pygame.display.update()
    # wait until player wanna go to the next scene
    run = True
    while run:
        # allow player to press space key again
        if(pygame.time.get_ticks()-skipClock > 500):
            skipClock = 0

        for event in pygame.event.get():
            # exit program
            if(event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]):
                pygame.quit()
                exit()
            # enter the next stage
            if(pygame.key.get_pressed()[pygame.K_SPACE] and skipClock == 0):
                run = False
    return



if(__name__ == "__main__"):

    # init game
    pygame.init()

    # init screen
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Result Scene (Test)')

    # init resources
    # global result_bg
    result_bg = pygame.image.load(_result_bg).convert_alpha()
    result_bg = pygame.transform.smoothscale(result_bg, (WIDTH, HEIGHT))
    # global result_bgFilter
    result_bgFilter = pygame.image.load(_result_bgFilter).convert_alpha()
    result_bgFilter = pygame.transform.smoothscale(result_bgFilter, (WIDTH, HEIGHT))

    # init standby scene for test
    ResetScreen()
    msg_font = pygame.font.SysFont('arial', 40)
    msg1 = msg_font.render('SPACE: start test', True, COLOR_WHITE)
    msg2 = msg_font.render('ESE to exit', True, COLOR_WHITE)
    screen.blit(msg1, (20, 100))
    screen.blit(msg2, (20, 200))
    pygame.display.update()

    # def parameters of mediapipe
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # For webcam input:
    # global cap
    cap = cv.VideoCapture(0)

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
    StartResultScene(test_name, test_perfect, test_miss)

    pygame.quit()
    cap.release()
    exit()