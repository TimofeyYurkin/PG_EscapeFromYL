import os
import sys
import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()
