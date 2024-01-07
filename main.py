import pygame
from Screens import StartScreens

pygame.init()
pygame.display.set_caption('Побег из Яндекс.Лицея')

SIZE = W, H = (1200, 900)
screen = pygame.display.set_mode(SIZE)

start_screen = StartScreens(SIZE, screen)
start_screen.main_start()
