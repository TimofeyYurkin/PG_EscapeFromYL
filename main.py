from screens import StartScreens
from objects_load import *

pygame.init()
pygame.display.set_caption('Побег из Яндекс.Лицея')

SIZE = W, H = (1050, 700)
screen = pygame.display.set_mode(SIZE)
running = True

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 100)

UPDATE_DECORATION = pygame.USEREVENT + 2
pygame.time.set_timer(UPDATE_DECORATION, 250)

start_screen = StartScreens(SIZE, screen)
start_screen.main_start()

player = generate_level(load_level('first.txt'))

while running:
    pygame.time.Clock().tick(60)
    screen.fill(pygame.Color('#442869'))
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
        if event.type == UPDATE_DECORATION:
            decoration_group.update()
    all_sprites.draw(screen)
    pygame.display.flip()

terminate()
