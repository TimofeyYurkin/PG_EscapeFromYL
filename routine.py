import os
import sys
import pygame


def load_image(name, directory):
    fullname = os.path.join(f'data/{directory}', name)
    image = pygame.image.load(fullname)
    return image


def cut_sheet(sheet, columns, rows):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
    frames = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))
    return rect, frames


def load_level(filename):
    with open(f'data/levels/{filename}', 'r') as map_file:
        level_map = [line.strip() for line in map_file]
    return level_map


def terminate():
    pygame.quit()
    sys.exit()
