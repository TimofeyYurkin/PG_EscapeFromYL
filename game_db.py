import sqlite3
from db_errors import *


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('EFLY.sqlite')
        self.cur = self.connection.cursor()

        self.cur.execute('CREATE TABLE IF NOT EXISTS Players('
        'name TEXT UNIQUE NOT NULL, '
        'best_time TEXT NOT NULL, '
        'best_score NUMERIC NOT NULL);')

        self.connection.commit()

    def registration_player(self, name):
        try:
            if not name.replace(' ', ''):
                raise DataError
            if (name,) in self.cur.execute('SELECT name FROM Players'):
                raise ExistingNameError
            if len(name) < 3:
                raise ShortNameError
            self.cur.execute('INSERT INTO Players(name, best_time, best_score) VALUES(?, ?, ?);',
                             (name, '0:00', '0'))
            self.connection.commit()
            return 'Аккаунт успешно зарегистрирован!'
        except DataError:
            return 'Некорректный ввод данных.'
        except ExistingNameError:
            return 'Игрок с таким никнеймом уже существует.'
        except ShortNameError:
            return 'Никнейм должно содержать в себе 3 и более символов.'


    def login_player(self, name):
        try:
            if (name,) not in self.cur.execute('SELECT name FROM Players'):
                raise NotExistingPlayerError
            return 'Вы успешно зашли в аккаунт!'
        except NotExistingPlayerError:
            return 'Игрока с таким никнеймом не существует.'

    def update_time(self, name, time):
        self.cur.execute('UPDATE Players SET best_time = ? WHERE name = ?',
                         (time, name))
        self.connection.commit()

    def update_score(self, name, score):
        self.cur.execute('UPDATE Players SET best_score = ? WHERE name = ?',
                         (score, name))
        self.connection.commit()

    def get_results(self, name):
        results = self.cur.execute('SELECT best_time, best_score FROM Players WHERE name = ?',
                                   (name,)).fetchone()
        return results
