# Побег из Яндекс Лицея
**Данный проект представляет собой игру-головоломку на клетчатом поле с разными уровнями сложностями:**

**1) Лёгкий. Отсутствие логически задач, обычный лабиринт состоящий из стен.**

**2) Средний. Для прохождения требуется решить несколько простых задач. Требует чуть больше времени, чем лёгкий.**

**3) Сложный. Для прохождения нужно поработать мозгами, потратить время на изучение уровня и загадок.**

**4) Невозможный. Ну, просто невозможный. Из Яндекс Лицея нереально сбежать.**

**Цель - пройти уровень как можно быстрее, чтобы оказаться выше всех в строке лидеров.**

*Мораль: Дорогие маленкие неокрепшие умы яндекс-лицеистов первого года обучения! Единственный способ сбежать - его нет, просто учитесь, а этот проект всего лишь больная мечта автора!*

# Техническое задание
## **1. Создание БД:**

ㅤ**1.1 Реализовать таблицу для логинов и результатов игроков с помощью библиотеки sqlite3.**

ㅤㅤ**Столбик login - имя аккаунта пользователя в игре.**

ㅤㅤ**Столбик time - лучшее время прохождения.**

ㅤㅤ**Столбик score - лучший показатель очков за прохождение.**

ㅤ**1.2 Написать необходимые функции для работы с БД:**

ㅤㅤ**Получение информации о лучших результатов игроков: логин, время, очки.**

ㅤㅤ**Добавление в базу информации о новых игроках.**

ㅤㅤ**Обновление информации в базе о игроках.**

ㅤ**1.3 Провести тесты и убедиться в работоспособности.**

## **2. Продумывание идеи:**

ㅤ**2.1 Определиться с общим стилем игры и объектами, которые должны быть в игре для выбора текстур.**

ㅤㅤ**Стиль игры: пиксельный.**

ㅤㅤ**Объект игрока, т.е. то, кем будет управлять игрок (Какой-нибудь полумёртвый яндекс-лицеист).**

ㅤㅤ**Основные объекты: поверхность для передвижения, стены, декоративные объекты.**

ㅤㅤ**Интерактивные объекты: шипы, ловушки, пропасти (опасности для игрока); кнопки, двери, стулья, столы (вспомогательные объекты для прохождения).**

ㅤㅤ**Дополнительные объекты: то, что не описано выше, но может быть придумано при создании проекта.**

ㅤ**2.2 С использованием интернет-ресурсов найти нужные текстуры для объектов.**

ㅤ**2.3 В случае, если не получится найти все нужные текстуры, создать свои.**

## **3. Реализация скелета игры:**

ㅤ**3.1 Создать основной файл игры с первичным кодом на Pygame и классы для объектов в отдельных файлах. Добавить возможность добавления уровней в виде текстовых файлов, где определённые символы - объекты игры.**

ㅤ**3.2 На тестовомо уровне проработать все функции игры и убедиться полной работоспособности. Список:**

ㅤㅤ**Игрок. Возможность передвигаться с полноценными анимациями и взаимодействие с окружением.**

ㅤㅤ**Объекты без важных функций. Корректное отображение на экране и косвенное взаимодействие с игроком.**

ㅤㅤ**Интерактивные объекты. Возможности взаимодействия с игроком и объектами окружения.**

ㅤㅤ**Дополнительные объекты. Исключительно декоративные функции для уменьшения ощущения пустоты уровней.**

ㅤ**3.3 Создать 4 уровня от разработчика. Добавить функцию внедрения своих уровней в игру.**

## **4. Визуальная доработка игры:**

ㅤ**4.1 Создать окна главного меню, лидерборд и окно с результатами после уровня (Время, очки и т.п.)**

ㅤ**4.2 Связать все компоненты воедино и провести финальные тесты игры**
