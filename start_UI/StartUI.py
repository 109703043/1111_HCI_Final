import pygame 
import button as button
# def main():

#初始化遊戲
pygame.init()

#音樂初始化
pygame.mixer.init()

#視窗設定
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Music Game')

#背景圖
background_image = pygame.image.load('../images/monster.png')   
screen.blit(background_image,(0,0))

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

#Game variables
game_paused = False

#Music variables
music_muted = False

#背景音樂
musicName = '../resources/群青.mp3'
pygame.mixer.music.load(musicName)
pygame.mixer.music.play(3)
pygame.mixer.music.set_volume(0.5)

#音效
def play_sound():
    sound = pygame.mixer.Sound("../resources/soundDrum.wav")
    sound.play()


#畫面
run = True
while run:
    
    if game_paused == True:
        # black panel
        if black_button.draw(screen):
            pass
        # music button
        if music_button.draw(screen):
            if music_muted == False:
                play_sound()
                pygame.mixer.music.set_volume(0)
                music_muted = True
            else:                
                play_sound()
                pygame.mixer.music.set_volume(100)
                music_muted = False
        # if sound_button.draw(screen):

        # close panel button
        if back_button.draw(screen):
            game_paused = False
            print('BACK')
        # exit game button
        if exit_button.draw(screen):
            print('EXIT')
            run = False
    else:
        screen.blit(background_image, (0, 0))
        # start button
        if start_buttun.draw(screen):
            #擺遊戲介面進去
            
            #背景音樂關閉
            pygame.mixer.music.pause()
            print('START')

        # setting button
        if settings_button.draw(screen):
            # screen.blit(background_image,(0,0))
            play_sound()
            game_paused = True
            # print('SETTINGS')
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        if event.type == pygame.QUIT:
            run = False

# if __name__ == "__main__":
#     main()