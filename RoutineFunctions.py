import os
import sys
import pygame


def load_image(name, directory):
    fullname = os.path.join(f'data/{directory}', name)
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()
