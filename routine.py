import os
import sys
import pygame


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
catches_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()


class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group)
        self.image = load_image('floor.jpg', 'textures')
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group, obstacles_group)
        self.image = load_image('wall.png', 'textures')
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.frames= []
        self.row, self.column = 0, 0

        self.cut_sheet(load_image('player_sprites.png', 'textures'), 4, 4)
        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, *args, **kwargs):
        if args:
            if args[0] == pygame.K_s:
                self.rect = self.rect.move(0, 15)
                self.row = 0
            if args[0] == pygame.K_a:
                self.rect = self.rect.move(-15, 0)
                self.row = 1
            if args[0] == pygame.K_d:
                self.rect = self.rect.move(15, 0)
                self.row = 2
            if args[0] == pygame.K_w:
                self.rect = self.rect.move(0, -15)
                self.row = 3
            if self.column < 3:
                self.column += 1
            else:
                self.column = 0
            self.image = self.frames[self.row * 4 + self.column]
        if pygame.sprite.spritecollide(self, obstacles_group, False):
            x, y = 0, 0
            if args[0] == pygame.K_s:
                y = -1
            if args[0] == pygame.K_a:
                x = 1
            if args[0] == pygame.K_d:
                x = -1
            if args[0] == pygame.K_w:
                y = 1
            while pygame.sprite.spritecollide(self, obstacles_group, False):
                self.rect = self.rect.move(x, y)


def load_image(name, directory):
    fullname = os.path.join(f'data/{directory}', name)
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    with open(f'data/levels/{filename}', 'r') as map_file:
        level_map = [line.strip() for line in map_file]
    return level_map


def generate_level(level):
    px, py = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Floor(x, y)
            elif level[y][x] == '#':
                Wall(x, y)
            elif level[y][x] == '@':
                Floor(x, y)
                px, py = x, y
    new_player = Player(px, py)
    return new_player


def terminate():
    pygame.quit()
    sys.exit()
