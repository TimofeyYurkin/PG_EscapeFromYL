from screens import StartScreens
from objects_load import *

# Инициализация Pygame
pygame.init()
pygame.display.set_caption('Побег из Яндекс.Лицея')

SIZE = W, H = (1050, 700)
screen = pygame.display.set_mode(SIZE)
running = True

start_screen = StartScreens(SIZE, screen)
start_screen.main_start()

# Пользовательские ивенты для обработки анимаций, событий и т.д.
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 100)

UPDATE_DECORATION = pygame.USEREVENT + 2
pygame.time.set_timer(UPDATE_DECORATION, 250)

ACTIVATE_SPIKES = pygame.USEREVENT + 3
pygame.time.set_timer(ACTIVATE_SPIKES, 400)

PLAYER_INVULNERABILITY = pygame.USEREVENT + 4
pygame.time.set_timer(PLAYER_INVULNERABILITY, 0)

TIMER_CHANGE = pygame.USEREVENT + 5
pygame.time.set_timer(TIMER_CHANGE, 1000)

# Первый уровень (На данный момент тестовый)
player, lives, coins, time = generate_level(load_level('first.txt'))

while running:
    screen.fill(pygame.Color('#442869'))
    pygame.time.Clock().tick(60)
    result = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.update(pygame.K_w)
            elif keys[pygame.K_d]:
                player.update(pygame.K_d)
            elif keys[pygame.K_s]:
                player.update(pygame.K_s)
            elif keys[pygame.K_a]:
                player.update(pygame.K_a)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and player.keys > 0:
                pass
        if event.type == UPDATE_DECORATION:
            decoration_group.update()
        if event.type == ACTIVATE_SPIKES:
            spikes_group.update()
        if event.type == PLAYER_INVULNERABILITY:
            pygame.time.set_timer(PLAYER_INVULNERABILITY, 0)
            player.invulnerability = False
        if event.type == TIMER_CHANGE:
            time.update()
    result = player.update()
    for result_type in result.keys():
        if result[result_type][0] and result_type == 'spikes' and not player.invulnerability:
            lives.lose_life()
            player.invulnerability = True
            pygame.time.set_timer(PLAYER_INVULNERABILITY, 1500)
        elif result_type == 'dang_floor' and result[result_type][0]:
            if not result[result_type][1].checked and result[result_type][1].true_type == 'trap_floorf.png':
                lives.lose_life()
                result[result_type][1].checked = True
            elif not result[result_type][1].checked and result[result_type][1].true_type == 'trap_floort.png':
                coins.update()
                result[result_type][1].checked = True
            player.invulnerability = True
            pygame.time.set_timer(PLAYER_INVULNERABILITY, 1500)
        elif result_type == 'coin' and result[result_type][0]:
            coins.update()
            result[result_type][1].kill()
        elif result_type == 'key' and result[result_type][0]:
            result[result_type][1].kill()
            player.keys += 1
    all_sprites.draw(screen)
    coins.show_stat(screen)
    time.show_time(screen)
    pygame.display.flip()


terminate()
