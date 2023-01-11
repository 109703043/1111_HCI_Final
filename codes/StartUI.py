import pygame 
import button
import Sound
import ResultScene
import Game as game
# def main():

#初始化遊戲
pygame.init()

#音樂初始化
pygame.mixer.init()

#視窗設定
screen = pygame.display.set_mode((1280,720))
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

#畫面
run = True
clickTime = 0
while run:
    
    screen.blit(background_image,(0,0))
    screen.blit(hamuga_img,(350,200))

    # settings panel on
    if game_paused == True:
        if black_button.draw(screen):
            pass
        if music_button.draw(screen):
            if music_muted == False:
                sound_.play()
                pygame.mixer.music.set_volume(0)
                music_muted = True
            else:                
                sound_.play()
                pygame.mixer.music.set_volume(0.2)
                music_muted = False
        if sound_button.draw(screen):
            sound_.play()
            sound_.stop()

        if back_button.draw(screen):
            screen.blit(background_image,(0,0))
            sound_.play()
            game_paused = False
            clickTime = pygame.time.get_ticks()
        
        if exit_button.draw(screen):
            sound_.play()
            run = False
            
    # settings panel off
    else:
        if start_buttun.draw(screen) and clickTime == 0:

            sound_.play()

            #擺遊戲介面進去
            if(game.main() != 1):
                pygame.mixer.music.load(musicName)
                pygame.mixer.music.play(3)
                pygame.mixer.music.set_volume(0.2)


        if settings_button.draw(screen):
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