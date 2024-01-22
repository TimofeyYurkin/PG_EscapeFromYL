from screens import StartScreens, FinalScreen
from sound_music import Music
from objects_load import *

# Инициализация Pygame
pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.display.set_caption('Побег из Яндекс.Лицея')

pygame.mixer.music.load('data/sounds/normal_bg_music.mp3')
pygame.mixer.music.set_volume(0.25)

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

SPECIAL_ENEMY = pygame.USEREVENT + 7
pygame.time.set_timer(SPECIAL_ENEMY, 0)

SPECIAL_COIN = pygame.USEREVENT + 8
pygame.time.set_timer(SPECIAL_COIN, 0)

SPECIAL_HEALTH = pygame.USEREVENT + 0
pygame.time.set_timer(SPECIAL_HEALTH, 0)

# Функция для вывода уровня на экран
def show_level(special_events=False):
    pause = False
    level_music = Music()
    if special_events:
        pygame.time.set_timer(SPECIAL_ENEMY, 10000)
        pygame.time.set_timer(SPECIAL_COIN, 5000)
        pygame.time.set_timer(SPECIAL_HEALTH, 30000)
    while True:
        screen.fill(pygame.Color('#442869'))
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
            if not pause:
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
                                    pygame.time.set_timer(DOOR_UNLOCK, 150)
                                    level_music.door_open()
                                    break
                        if pygame.sprite.spritecollideany(player, exits_group):
                            return False
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
                if event.type == SPECIAL_ENEMY:
                    enemy = random.choice(('e', 'E'))
                    if enemy == 'e':
                        Ghost(random.randint(4, 16), random.randint(4, 9), 'x', plus_speed=random.randint(1, 5))
                    else:
                        Ghost(random.randint(4, 16), random.randint(4, 9), 'y', plus_speed=random.randint(1, 5))
                if event.type == SPECIAL_COIN:
                    Coin(random.randint(4, 16), random.randint(4, 9))
                if event.type == SPECIAL_HEALTH:
                    lives.lives_left = 3
                    lives.image = lives.frames[3]
        if not pause:
            result = player.update()
            for result_type in result.keys():
                if result[result_type][0] and result_type == 'spikes' and not player.invulnerability:
                    lives.lose_life()
                    player.invulnerability = True
                    pygame.time.set_timer(PLAYER_INVULNERABILITY, 1200)
                    level_music.get_damage()
                elif result_type == 'dang_floor' and result[result_type][0]:
                    if not result[result_type][1].checked and result[result_type][1].true_type == 'trap_floorf.png':
                        lives.lose_life()
                        result[result_type][1].checked = True
                        player.invulnerability = True
                        pygame.time.set_timer(PLAYER_INVULNERABILITY, 1200)
                        level_music.get_damage()
                    elif not result[result_type][1].checked and result[result_type][1].true_type == 'trap_floort.png':
                        coins.update()
                        result[result_type][1].checked = True
                elif result_type == 'enemy' and result[result_type][0]:
                    lives.lose_life()
                    player.invulnerability = True
                    pygame.time.set_timer(PLAYER_INVULNERABILITY, 1200)
                    level_music.get_damage()
                elif result_type == 'coin' and result[result_type][0]:
                    coins.update()
                    result[result_type][1].kill()
                    level_music.get_coin()
                elif result_type == 'key' and result[result_type][0]:
                    result[result_type][1].kill()
                    player.keys += 1
                    level_music.get_key()
            if lives.lives_left == 0:
                return True
        all_sprites.draw(screen)
        stats_group.draw(screen)
        coins.show_stat(screen)
        time.show_time(screen)
        enemies_group.draw(screen)
        if pause:
            pause_screen(screen, W, H)
        pygame.display.flip()


def ready_for_level():
    pygame.mixer.music.play(-1)
    lives.lives_left = 3
    lives.image = lives.frames[3]


while running:
    clear_sprites(all_sprites, stats_group)
    start_screen.main_start()

    pygame.time.set_timer(SPECIAL_ENEMY, 0)
    pygame.time.set_timer(SPECIAL_COIN, 0)
    pygame.time.set_timer(SPECIAL_HEALTH, 0)

    player, lives, coins, time = generate_level(load_level(random.choice(('first_type1.txt', 'first_type2.txt'))), 1)
    ready_for_level()
    live = show_level()

    if not live:
        clear_sprites(all_sprites)
        player = generate_level(load_level('second_type1.txt'), 2)
        ready_for_level()
        live = show_level()

    if not live:
        clear_sprites(all_sprites)
        player = generate_level(load_level('third_type1.txt'), 3)
        ready_for_level()
        live = show_level()

    if not live:
        clear_sprites(all_sprites)
        player = generate_level(load_level('final.txt'), 4)
        ready_for_level()
        show_level(special_events=True)

    pygame.mixer.music.pause()
    final = FinalScreen(screen, SIZE, start_screen.player, coins.stat, time.time)
    final.final_start()


terminate()
