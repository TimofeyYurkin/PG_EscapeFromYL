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


def clear_sprites(every=None, stats=None):
    if every is not None:
        for sprite in every:
            sprite.kill()
    if stats is not None:
        for sprite in stats:
            sprite.kill()


def pause_screen(screen, W, H):
    alpha_surface = pygame.Surface((W, H))
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(150)

    text_render = pygame.font.Font(None, 50).render('Чтобы вернуться на урок, повторно нажмите ESC.', 1, pygame.Color('White'))
    text_rect = text_render.get_rect()
    text_rect.center = (W // 2, H // 2)

    title_render = pygame.font.Font(None, 70).render('ПЕРЕМЕНА', 1, pygame.Color('White'))
    title_rect = text_render.get_rect()
    title_rect.x = W // 2 - 120
    title_rect.y = 100

    screen.blit(alpha_surface, (0, 0))
    screen.blit(title_render, title_rect)
    screen.blit(text_render, text_rect)


def terminate():
    pygame.quit()
    sys.exit()
