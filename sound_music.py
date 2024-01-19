import pygame


class Music:
    def __init__(self):
        self.current_step = 1

    def walking(self):
        if self.current_step == 1:
            sound = pygame.mixer.Sound('data/sounds/step1.wav')
        else:
            sound = pygame.mixer.Sound('data/sounds/step2.wav')
        sound.set_volume(0.15)
        sound.play(0)
        self.current_step = -self.current_step

    def get_coin(self):
        sound = pygame.mixer.Sound('data/sounds/coin_get.wav')
        sound.set_volume(0.25)
        sound.play(0)

    def get_key(self):
        sound = pygame.mixer.Sound('data/sounds/key_get.wav')
        sound.set_volume(0.3)
        sound.play(0)

    def get_damage(self):
        sound = pygame.mixer.Sound('data/sounds/get_damage.wav')
        sound.set_volume(1.0)
        sound.play(0)

    def door_open(self):
        sound = pygame.mixer.Sound('data/sounds/door_open.wav')
        sound.set_volume(1.0)
        sound.play(0)
