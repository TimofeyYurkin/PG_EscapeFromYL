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
            results = self.db.get_results(self.player)
            screen_text[4] = f'Ваш ник: {self.player}'
            screen_text[5] = f'Ваши лучшие результаты: {results[0]} - время; {results[1]} - баллы.'

        y_pos = 30
        for line in range(len(screen_text)):
            line_render = self.text_render(screen_text, line)
            line_rect = line_render.get_rect()
            line_rect.x, line_rect.y = 50, y_pos
            if line > 1:
                y_pos += line_rect.height + 50
                self.btns.append((line_rect.x, line_rect.y, line_rect.x + line_rect.width, line_rect.y +
                                  line_rect.height))
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
            pygame.time.Clock().tick(60)
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


    def registration_start(self):
        screen_text = [
            'Регистрация аккаунта',
            'Чтобы вернуться нажмите Esc',
            'Введите никнейм:'
        ]

        while True:
            pygame.time.Clock().tick(60)
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

    def login_start(self):
        screen_text = [
            'Вход в аккаунт',
            'Чтобы вернуться нажмите Esc',
            'Введите ваш никнейм:'
        ]

        while True:
            pygame.time.Clock().tick(60)
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

    def set_background(self):
        background = pygame.transform.scale(load_image('start_background.jpg', 'bgs'), self.SIZE)
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


class FinalScreen:
    def __init__(self, screen, SIZE, player, score, time):
        self.SIZE = SIZE
        self.screen = screen
        self.btns = []

        self.player = player
        self.score = score
        self.time = time.split(':')

        self.db = Database()

    def final_start(self):
        self.set_background()

        title_render = pygame.font.Font(None, 50).render('ВЫ СВОДИТЕ КОНЦЫ С КОНЦАМИ', 1,
                                                         pygame.Color('White'))
        title_rect = title_render.get_rect(center=(self.SIZE[0] // 2, 100))
        self.screen.blit(title_render, title_rect)

        under_title_render = pygame.font.Font(None, 50).render('РАБОТНИКОМ ВКУСНО И ТОЧКА!', 1,
                                                              pygame.Color('White'))
        under_title_rect = title_render.get_rect(center=(self.SIZE[0] // 2 + 20, 180))
        self.screen.blit(under_title_render, under_title_rect)

        best_results = ''
        if self.player != '':
            best_results = self.db.get_results(self.player)
        if best_results:
            if int(self.time[0]) > int(best_results[0].split(':')[0]) or (int(self.time[1]) >
                        int(best_results[0].split(':')[1] and int(self.time[1] == int(best_results[0].split(':')[0])))):
                time_render = pygame.font.Font(None, 40).render(f'Вы улучшили показатель времени с {best_results[0]} до '
                                                                   f'{":".join(self.time)}!', 1, pygame.Color('White'))
                self.db.update_time(self.player, ':'.join(self.time))
            else:
                time_render = pygame.font.Font(None, 40).render(f'Ваш лучший результат выживаемости остался прежним: '
                                                                f'{best_results[0]}', 1, pygame.Color('White'))

            if int(self.score) > int(best_results[1]):
                score_render = pygame.font.Font(None, 40).render(f'Вы улучшили показатель собранных рублей с '
                                                                 f'{best_results[1]} до {self.score}!', 1, pygame.Color('White'))
                self.db.update_score(self.player, self.score)
            else:
                score_render = pygame.font.Font(None, 40).render(f'Вы умрёте от голода. Ваш лучший результат '
                                                                 f'остался прежним: {best_results[1]}.', 1, pygame.Color('White'))
            time_rect = time_render.get_rect(center=(self.SIZE[0] // 2, self.SIZE[1] // 2 - 30))
            self.screen.blit(time_render, time_rect)
            score_rect = score_render.get_rect(center=(self.SIZE[0] // 2, self.SIZE[1] // 2 + 30))
            self.screen.blit(score_render, score_rect)
        else:
            final_render = pygame.font.Font(None, 35).render('ВЫ нн. Партия яндекс-браузера изымает у вас '
                                                             'кошка-баллы и пачку времени.', 1, pygame.Color('White'))
            final_rect = final_render.get_rect(center=(self.SIZE[0] // 2, self.SIZE[1] // 2))
            self.screen.blit(final_render, final_rect)
        return_render = pygame.font.Font(None, 40).render('Вернуться в главное меню', 1, pygame.Color('White'))
        return_rect = return_render.get_rect(center=(self.SIZE[0] // 2, self.SIZE[1] // 2 + 200))
        self.btns.append((return_rect.x, return_rect.x + return_rect.width, return_rect.y, return_rect.y + return_rect.height))
        self.screen.blit(return_render, return_rect)

        while True:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.btns[0][0] <= event.pos[0] <= self.btns[0][1] and self.btns[0][2] <= event.pos[1] <=
                            self.btns[0][3]):
                        return
            pygame.display.flip()


    def set_background(self):
        background = pygame.transform.scale(load_image('final_background.jpg', 'bgs'), self.SIZE)
        alpha_surface = pygame.Surface(self.SIZE)
        alpha_surface.fill((0, 0, 0))
        alpha_surface.set_alpha(150)
        self.screen.blit(background, (0, 0))
        self.screen.blit(alpha_surface, (0, 0))