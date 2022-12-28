import pygame 

class sound:

    def __init__(self,soundName):
        self.soundName = soundName
        self.muted = False
        self.clicked = False

    def play(self):
        if self.muted == False:
            s = pygame.mixer.Sound(self.soundName)
            s.set_volume(0.5)
            s.play()

    def stop(self):
        if self.clicked == False:
            self.muted = True
            self.clicked = True
        else:
            self.muted = False
            self.clicked = False