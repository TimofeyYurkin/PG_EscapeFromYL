from screens import StartScreens
from sound_music import Music
from objects_load import *

# Инициализация Pygame
pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.display.set_caption('Побег из Яндекс.Лицея')

SIZE = W, H = (1050, 700)
screen = pygame.display.set_mode(SIZE)
start_screen = StartScreens(SIZE, screen)
running = True

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

DOOR_UNLOCK = pygame.USEREVENT + 6
pygame.time.set_timer(DOOR_UNLOCK, 0)

# Функция для вывода уровня на экран
def show_level():
    level_music = Music()
    while True:
        screen.fill(pygame.Color('#442869'))
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == MOVE_EVENT:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    level_music.walking()
                    player.update(pygame.K_w)
                elif keys[pygame.K_d]:
                    level_music.walking()
                    player.update(pygame.K_d)
                elif keys[pygame.K_s]:
                    level_music.walking()
                    player.update(pygame.K_s)
                elif keys[pygame.K_a]:
                    level_music.walking()
                    player.update(pygame.K_a)
                enemies_group.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if player.keys > 0 and pygame.sprite.spritecollideany(player, doors_group):
                        player.keys -= 1
                        for door in doors_group:
                            if pygame.sprite.collide_rect(player, door):
                                unlock_door = door
                                break
                    if pygame.sprite.spritecollideany(player, exits_group):
                        return
                    pygame.time.set_timer(DOOR_UNLOCK, 150)
                    level_music.door_open()
            if event.type == UPDATE_DECORATION:
                decoration_group.update()
            if event.type == ACTIVATE_SPIKES:
                spikes_group.update()
            if event.type == PLAYER_INVULNERABILITY:
                pygame.time.set_timer(PLAYER_INVULNERABILITY, 0)
                player.invulnerability = False
            if event.type == TIMER_CHANGE:
                time.update()
            if event.type == DOOR_UNLOCK:
                if unlock_door.column < 13:
                    unlock_door.update()
                else:
                    unlock_door.kill()
                    pygame.time.set_timer(DOOR_UNLOCK, 0)
        result = player.update()
        for result_type in result.keys():
            if result[result_type][0] and result_type == 'spikes' and not player.invulnerability:
                lives.lose_life()
                player.invulnerability = True
                pygame.time.set_timer(PLAYER_INVULNERABILITY, 1500)
                level_music.get_damage()
            elif result_type == 'dang_floor' and result[result_type][0]:
                if not result[result_type][1].checked and result[result_type][1].true_type == 'trap_floorf.png':
                    lives.lose_life()
                    result[result_type][1].checked = True
                    player.invulnerability = True
                    pygame.time.set_timer(PLAYER_INVULNERABILITY, 1500)
                    level_music.get_damage()
                elif not result[result_type][1].checked and result[result_type][1].true_type == 'trap_floort.png':
                    coins.update()
                    result[result_type][1].checked = True
            elif result_type == 'enemy' and result[result_type][0]:
                lives.lose_life()
                player.invulnerability = True
                pygame.time.set_timer(PLAYER_INVULNERABILITY, 2000)
                level_music.get_damage()
            elif result_type == 'coin' and result[result_type][0]:
                coins.update()
                result[result_type][1].kill()
                level_music.get_coin()
            elif result_type == 'key' and result[result_type][0]:
                result[result_type][1].kill()
                player.keys += 1
                level_music.get_key()
        all_sprites.draw(screen)
        coins.show_stat(screen)
        time.show_time(screen)
        enemies_group.draw(screen)
        pygame.display.flip()


while running:
    start_screen.main_start()
    player, lives, coins, time = generate_level(load_level(random.choice(('first_type1.txt', 'first_type2.txt'))), 1)
    pygame.mixer.music.load('data/sounds/normal_bg_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    show_level()
    pygame.mixer.music.pause()

    lives.lives_left = 3
    lives.image = lives.frames[3]


terminate()
