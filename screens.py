import pygame

from routine import load_image, terminate
from game_db import Database


class StartScreens:
    def __init__(self, SIZE, screen):
        self.SIZE = SIZE
        self.screen = screen
        self.btns = []

        self.title_font = pygame.font.Font(None, 70)
        self.undertitle_font = pygame.font.Font(None, 30)
        self.typical_font = pygame.font.Font(None, 50)

        self.player = ''
        self.db = Database()

    def main_start(self):
        self.set_background()
        screen_text = [
            'Побег из Яндекс.Лицея',
            'Скачайте Яндекс-Браузер для образования...',
            'Начать игру',
            'Правила игры',
            'Зарегистрироваться',
            'Войти в аккаунт'
        ]
        if self.player:
            screen_text[4] = f'Ваш ник: {self.player}'
            screen_text[5] = f'Ваши лучшие результаты: {self.db.get_results(self.player)}'

        y_pos = 30
        for line in range(len(screen_text)):
            line_render = self.text_render(screen_text, line)
            line_rect = line_render.get_rect()
            line_rect.x, line_rect.y = 50, y_pos
            if line > 1:
                y_pos += line_rect.height + 50
                self.btns.append((line_rect.x, line_rect.y, line_rect.x + line_rect.width, line_rect.y + line_rect.height))
            elif line == 1:
                y_pos += line_rect.height + 150
            else:
                y_pos += line_rect.height + 5
            self.screen.blit(line_render, line_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.btns[0][0] <= event.pos[0] <= self.btns[0][2] and self.btns[0][1] <= event.pos[1] <=
                            self.btns[0][3]):
                        return
                    elif (self.btns[1][0] <= event.pos[0] <= self.btns[1][2] and self.btns[1][1] <= event.pos[1] <=
                            self.btns[1][3]):
                        self.info_start()
                    elif (self.btns[2][0] <= event.pos[0] <= self.btns[2][2] and self.btns[2][1] <= event.pos[1] <=
                            self.btns[2][3]) and not self.player:
                        self.registration_start()
                    elif (self.btns[3][0] <= event.pos[0] <= self.btns[3][2] and self.btns[3][1] <= event.pos[1] <=
                            self.btns[3][3]) and not self.player:
                        self.login_start()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def info_start(self):
        self.set_background()
        screen_text = (
            'Правила игры "Побег из Яндекс.Лицея"',
            'Чтобы вернуться нажмите Esc',
            '1. Остерегайтесь ловушек и всего, что движется.',
            '2. Проходите уровни как можно быстрее.',
            '3. Набирайте как можно больше баллов, чтобы выжить.',
            '4. Пользуйтесь A, W, S, D для передвижения.',
            '5. Пользуйте F для взаимодействия с объектами.'
        )
        y_pos = 100
        for line in range(len(screen_text)):
            line_render = self.text_render(screen_text, line)
            if line < 2:
                line_rect = line_render.get_rect(center=(self.SIZE[0] // 2, y_pos))
            else:
                line_rect = line_render.get_rect()
                line_rect.x, line_rect.y = 50, y_pos
            if line != 1:
                y_pos += line_rect.height + 10
            else:
                y_pos += line_rect.height + 80
            self.screen.blit(line_render, line_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_start()
                        return
            pygame.display.flip()
            pygame.time.Clock().tick(60)


    def registration_start(self):
        screen_text = [
            'Регистрация аккаунта',
            'Чтобы вернуться нажмите Esc',
            'Введите никнейм:'
        ]

        while True:
            self.set_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.player = ''
                        self.main_start()
                        return
                    if event.key == pygame.K_BACKSPACE:
                        self.player = self.player[:-1]
                    if event.key == 13:
                        answer = self.db.registration_player(self.player)
                        if answer[-1] == '!':
                            self.main_start()
                            return
                        else:
                            self.player = ''
                            screen_text[2] = answer
                    if 39 <= event.key <= 127:
                        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                            self.player += chr(event.key).capitalize()
                        else:
                            self.player += chr(event.key)
            y_pos = 100
            for line in range(len(screen_text)):
                line_render = self.text_render(screen_text, line)
                if line != 2:
                    line_rect = line_render.get_rect(center=(self.SIZE[0] // 2, y_pos))
                    y_pos += line_rect.height + 10
                else:
                    line_rect = line_render.get_rect(center=(self.SIZE[0] // 2, self.SIZE[1] // 2 - 100))
                self.screen.blit(line_render, line_rect)

            name_render = self.typical_font.render(self.player, 1, pygame.Color('white'))
            name_rect = name_render.get_rect(center=(self.SIZE[0] // 2, self.SIZE[1] // 2))
            self.screen.blit(name_render, name_rect)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def login_start(self):
        screen_text = [
            'Вход в аккаунт',
            'Чтобы вернуться нажмите Esc',
            'Введите ваш никнейм:'
        ]

        while True:
            self.set_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.player = ''
                        self.main_start()
                        return
                    if event.key == pygame.K_BACKSPACE:
                        self.player = self.player[:-1]
                    if event.key == 13:
                        answer = self.db.login_player(self.player)
                        if answer[-1] == '!':
                            self.main_start()
                            return
                        else:
                            self.player = ''
                            screen_text[2] = answer
                    if 39 <= event.key <= 127:
                        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                            self.player += chr(event.key).capitalize()
                        else:
                            self.player += chr(event.key)
            y_pos = 100
            for line in range(len(screen_text)):
                line_render = self.text_render(screen_text, line)
                if line != 2:
                    line_rect = line_render.get_rect(center=(self.SIZE[0] // 2, y_pos))
                    y_pos += line_rect.height + 10
                else:
                    line_rect = line_render.get_rect(center=(self.SIZE[0] // 2, self.SIZE[1] // 2 - 100))
                self.screen.blit(line_render, line_rect)

            name_render = self.typical_font.render(self.player, 1, pygame.Color('white'))
            name_rect = name_render.get_rect(center=(self.SIZE[0] // 2, self.SIZE[1] // 2))
            self.screen.blit(name_render, name_rect)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def set_background(self):
        background = pygame.transform.scale(load_image('StartScreenBG.jpg', 'bgs'), self.SIZE)
        alpha_surface = pygame.Surface(self.SIZE)
        alpha_surface.fill((0, 0, 0))
        alpha_surface.set_alpha(150)
        self.screen.blit(background, (0, 0))
        self.screen.blit(alpha_surface, (0, 0))

    def text_render(self, screen_text, line):
        if line == 0:
            line_render = self.title_font.render(screen_text[line], 1, pygame.Color('White'))
        elif line == 1:
            line_render = self.undertitle_font.render(screen_text[line], 1, pygame.Color('White'))
        else:
            line_render = self.typical_font.render(screen_text[line], 1, pygame.Color('White'))
        return line_render
