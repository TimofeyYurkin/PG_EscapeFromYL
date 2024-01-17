import random

import pygame.sprite

from routine import *

# Основные группы
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()

# Группы взаимодействия
coins_group = pygame.sprite.Group()
keys_group = pygame.sprite.Group()
doors_group = pygame.sprite.Group()

# Группы игрока
player_group = pygame.sprite.Group()
stats_group = pygame.sprite.Group()

# Группы опасностей для игрока
traps_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

# Дополнительные группы
decoration_group = pygame.sprite.Group()


# Классы основных объектов
class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, index):
        super().__init__(all_sprites, tiles_group)
        floor = ('floor_type1.png', 'floor_type2.png', 'floor_type3.png', 'floor_type4.png', 'floor_type5.png')

        self.image = load_image(floor[index], 'textures/tiles/floor')
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, index):
        super().__init__(all_sprites, tiles_group, obstacles_group)
        walls = ('wall_type1.png', 'wall_type2.png', 'wall_type3.png', 'wall_top.png', 'wall_topl.png', 'wall_topr.png',
                 'wall_l.png', 'wall_r.png', 'wall_btml.png', 'wall_btmr.png')

        self.image = load_image(walls[index], 'textures/tiles/walls')
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, filename, x_plus=0, y_plus=0):
        super().__init__(all_sprites, obstacles_group)
        self.image = load_image(filename, 'textures/furniture')
        self.rect = self.image.get_rect().move(50 * pos_x + x_plus, 50 * pos_y + y_plus)
        self.mask = pygame.mask.from_surface(self.image)


# Классы игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.row, self.column = 0, 0
        self.rect, self.frames = cut_sheet(load_image('player_sprites.png', 'textures'), 4, 4)

        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

        self.invulnerability = False
        self.keys = 0

    def update(self, *args, **kwargs):
        result = {
            'spikes': [False,],
            'dang_floor': [False,],
            'coin': [False,],
            'key': [False,]
        }
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
        if pygame.sprite.spritecollideany(self, obstacles_group, pygame.sprite.collide_mask):
            x, y = 0, 0
            if args[0] == pygame.K_s:
                y = -1
            if args[0] == pygame.K_a:
                x = 1
            if args[0] == pygame.K_d:
                x = -1
            if args[0] == pygame.K_w:
                y = 1
            while pygame.sprite.spritecollideany(self, obstacles_group, pygame.sprite.collide_mask):
                self.rect = self.rect.move(x, y)
        if not self.invulnerability:
            for sprite in traps_group:
                if (pygame.sprite.collide_mask(self, sprite) and sprite.rect.y <= self.rect.y +
                        self.rect.height - 17 <= sprite.rect.y + sprite.rect.width and isinstance(sprite, Spikes)
                        and sprite.column > 5):
                    result['spikes'] = [True,]
                elif (pygame.sprite.collide_mask(self, sprite) and sprite.rect.y <= self.rect.y +
                      self.rect.height - 17 <= sprite.rect.y + sprite.rect.width and isinstance(sprite, DangerousFloor)
                      and not sprite.checked):
                    result['dang_floor'] = [True, sprite]
                    sprite.update()
        for coin in coins_group:
            if pygame.sprite.collide_mask(self, coin):
                result['coin'] = [True, coin]
        for key in keys_group:
            if pygame.sprite.collide_mask(self, key):
                result['key'] = [True, key]
        return result


class Life(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, stats_group)
        self.lives_left = 3
        self.rect, self.frames = cut_sheet(load_image('life_sprites.png', 'textures/stats'), 4, 1)

        self.frames = self.frames[::-1]
        self.image = self.frames[3]
        self.rect = self.image.get_rect().move(25, 20)

    def lose_life(self):
        self.lives_left -= 1
        if self.lives_left > -1:
            self.image = self.frames[self.lives_left]


class StatsCoin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, stats_group, coins_group)
        self.image = load_image('coin.png', 'textures/stats')
        self.rect = self.image.get_rect().move(72, 20)

        self.stat = 0
        self.stat_font = pygame.font.Font(None, 50)

    def show_stat(self, screen):
        stat_render = self.stat_font.render(str(self.stat), True, pygame.Color('White'))
        stat_rect = stat_render.get_rect()
        stat_rect.x, stat_rect.y = 115, 22
        screen.blit(stat_render, stat_rect)

    def update(self):
        self.stat += 1


class Time(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, stats_group)
        self.image = load_image('time.png', 'textures/stats')
        self.rect = self.image.get_rect().move(25, 58)

        self.minutes = 0
        self.seconds = 0
        self.time_font = pygame.font.Font(None, 50)

    def show_time(self, screen):
        if self.seconds >= 10:
            str_time = f'{self.minutes}:{self.seconds}'
        else:
            str_time = f'{self.minutes}:0{self.seconds}'
        time_render = self.time_font.render(str_time, True, pygame.Color('White'))
        stat_rect = time_render.get_rect()
        stat_rect.x, stat_rect.y = 72, 60
        screen.blit(time_render, stat_rect)

    def update(self):
        self.seconds += 1
        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1


# Предметы для взаимодействия с игроком
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, coins_group)
        self.image = load_image('coin_collect.png', 'textures/interaction')
        self.rect = self.image.get_rect().move(pos_x * 50 + 10, pos_y * 50 + 10)
        self.mask = pygame.mask.from_surface(self.image)


class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, keys_group)
        self.image = load_image('key.png', 'textures/interaction')
        self.rect = self.image.get_rect().move(pos_x * 50, pos_y * 50)
        self.mask = pygame.mask.from_surface(self.image)


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, obstacles_group, doors_group)
        self.column = 0
        self.rect, self.frames = cut_sheet(load_image('door_sprites.png', 'textures/furniture'), 14, 1)

        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(pos_x * 50, pos_y * 50 - 10)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.column += 1
        self.image = self.frames[self.column]



# Классы опасных объектов для игрока
class Spikes(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group, traps_group, spikes_group)
        self.column = 0
        self.rect, self.frames = cut_sheet(load_image('spikes_sprites.png', 'textures/traps'), 10, 1)

        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)

    def update(self):
        if self.column < 9:
            self.column += 1
        else:
            self.column = 0
        self.image = self.frames[self.column]


class DangerousFloor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group, traps_group)
        self.true_type = random.choice(('trap_floorf.png', 'trap_floort.png'))

        self.image = load_image('trap_floorn.png', 'textures/traps')
        self.rect = self.image.get_rect().move(pos_x * 50, pos_y * 50)
        self.checked = False

    def update(self):
        self.image = load_image(self.true_type, 'textures/traps')


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, enemies_group)
        self.row, self.column = 0, 0
        self.rect, self.frames = cut_sheet(load_image('enemy_sprites.png', 'textures'), 9, 4)

        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)

    def update(self):
        pass


# Классы декоративных объектов
class Decoration(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, filename):
        super().__init__(all_sprites, decoration_group)
        self.image = load_image(filename, 'textures/decorations')
        self.rect = self.image.get_rect().move(50 * pos_x, 50 * pos_y)


class Torch(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, decoration_group)
        self.column = 0
        self.rect, self.frames = cut_sheet(load_image('torch_sprites.png', 'textures/furniture'), 6, 1)

        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(50 * pos_x + 10, 50 * pos_y + 10)

    def update(self):
        if self.column < 5:
            self.column += 1
        else:
            self.column = 0
        self.image = self.frames[self.column]


class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x=0, pos_y=0):
        super().__init__(all_sprites, decoration_group)
        self.image = load_image('box.png', 'textures/decorations')
        self.rect = self.image.get_rect().move(pos_x, pos_y)


# Функция для загрузки уровня из .txt файла
def generate_level(level):
    px, py = None, None
    wall_types = ('#', '%', '_', '<', '>', '[', ']', '{', '}')
    corners = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.' and level[y][x - 1] != 'H':
                Floor(x, y, random.randint(0, 3))
                if random.randint(1, 30) == random.randint(1, 30):
                    Coin(x, y)
            elif level[y][x] in wall_types:
                if (x, y) not in corners:
                    if level[y][x] in ('_', '<', '>') and y == 0:
                        Floor(x, y, 4)
                    else:
                        Floor(x, y, random.randint(0, 3))
                if level[y][x] == '%' and level[y][x - 2] == '%':
                    Torch(x - 1, y)
                if level[y][x] == '#':
                    Wall(x, y, random.randint(0, 1))
                    if len(level[y]) - 1 != x and len(level) - 1 != y:
                        if random.randint(0, 10) > 7 and level[y][x + 1] != '%':
                            Decoration(x, y, 'dead_lycst.png')
                elif 4 <= wall_types.index(level[y][x]) + 1 <= 5:
                    Wall(x, y, 3)
                    Wall(x, y + 1, random.randint(0, 1))
                    Wall(x + 1, y, wall_types.index(level[y][x]) + 1)
                    corners.append((x, y + 1))
                else:
                    Wall(x, y, wall_types.index(level[y][x]) + 1)
            elif level[y][x] == 'h':
                Floor(x, y, random.randint(0, 3))
                if level[y + 1][x] == 'H' or level[y + 1][x - 1] == 'H':
                    Obstacle(x, y, 'Chair_up.png')
                if level[y - 1][x] == 'H' or level[y - 1][x - 1] == 'H':
                    Obstacle(x, y, 'Chair_down.png')
                if level[y][x + 1] == 'H' or level[y][x + 1] == 'L':
                    Obstacle(x, y, 'Chair_left.png')
                if level[y][x - 2] == 'H' or level[y][x - 1] == 'L':
                    Obstacle(x, y, 'Chair_right.png')
            elif level[y][x] == 'H':
                Floor(x, y, random.randint(0, 3))
                Floor(x + 1, y, random.randint(0, 3))
                Obstacle(x, y, 'table.png')
            elif level[y][x] == 'L':
                Floor(x, y, random.randint(0, 3))
                Obstacle(x, y, 'little_table.png')
            elif level[y][x] == 'B':
                Floor(x, y, random.randint(0, 3))
                Obstacle(x, y, 'bookshelf.png', 0, -5)
            elif level[y][x] == '@':
                Floor(x, y, random.randint(0, 3))
                px, py = x, y
            elif level[y][x] == 'x':
                Spikes(x, y)
            elif level[y][x] == 'o':
                DangerousFloor(x, y)
            elif level[y][x] == 'D':
                Floor(x, y, random.randint(0, 3))
                Door(x, y)
            elif level[y][x] == 'k':
                Floor(x, y, random.randint(0, 3))
                Key(x, y)
    Box()
    lives = Life()
    time = Time()
    coins = StatsCoin()
    new_player = Player(px, py)
    return new_player, lives, coins, time
