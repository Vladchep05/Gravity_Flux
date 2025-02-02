import json
import math
import time
import datetime
from random import randint, random

import pygame


def check(name1, name2):
    """
    pass
    """

    with open('data/data.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    return data[name1][name2]


def check_levels(name1, name2):
    """
    pass
    """

    with open('data/cards.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    return data[name1][name2]


def transit(pos):
    transition.new_pos(pos)


def check_open_cards(name1, name2):
    """
    pass
    """

    with open('data/data.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    return data['open_cards'][name1][name2]


def setting_value(key, name) -> None:
    """
    pass
    """

    with open('data/data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    data['gameplay'][key] = name

    with open('data/data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def determination_levels():
    levels_selection.creating_buttons()


def loading():
    loading_screen.updaute()


def card_selection_easy() -> None:
    """
    pass
    """

    setting_value('level', 'easy')

    card_selection.creating_buttons('Тихая долина', 'Прогулка по роще', 'Рассветный путь')
    transit('cards')
    screen_change('levels', 'transition')


def card_selection_normal() -> None:
    """
    pass
    """

    setting_value('level', 'normal')

    card_selection.creating_buttons('Встреча ветров', 'Зеленый лабиринт', 'Скалистый склон')
    transit('cards')
    screen_change('levels', 'transition')


def card_selection_hard() -> None:
    """
    pass
    """

    setting_value('level', 'hard')

    card_selection.creating_buttons('Заточенные пики', 'Тень дракона', 'Дыхание вечного')
    transit('cards')
    screen_change('levels', 'transition')


def creating_buttons(spis) -> None:
    """
    pass
    """

    character_types.creating_buttons(spis[0], spis[1], spis[2])


def play_game():
    game.loading()


def screen_change(screen_one, screen_two) -> None:
    """
    pass
    """

    with open('data/data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    data['screen'][screen_one] = False
    data['screen'][screen_two] = True
    if screen_one != 'transition':
        data['screen']['past_position'] = screen_one

    with open('data/data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def start_screen() -> None:
    """
    pass
    """

    with open('data/data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    data['screen']['running'] = True
    data['screen']['past_position'] = 'fl_zastavka'
    data['screen']['fl_zastavka'] = True
    data['screen']['transition'] = False
    data['screen']['fl_menu'] = False
    data['screen']['settings'] = False
    data['screen']['levels'] = False
    data['screen']['cards'] = False
    data['screen']['card_type'] = False
    data['screen']['character_types'] = False
    data['screen']['loading_screen'] = False
    data['screen']['gemplay'] = False
    data['screen']['win'] = False
    data['screen']['loss'] = False

    data['gameplay']['level'] = ""
    data['gameplay']['name_card'] = ""
    data['gameplay']['type_card'] = ""
    data['gameplay']['character'] = ""

    with open('data/data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def music_menu() -> None:
    """
    pass
    """

    pygame.mixer.music.load('data/file_music/music_menu.mp3')
    pygame.mixer.music.set_volume(check('audio', 'music_volume'))
    pygame.mixer.music.play(-1)
    if not check('audio', 'mute_music'):
        pygame.mixer.music.pause()
    if not check('audio', 'mute_sound'):
        sound.set_volume(0)


def volume_change(value, name) -> None:
    """
    pass
    """

    with open('data/data.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    data['audio'][name] = round(value, 2)

    if name == 'music_volume':
        pygame.mixer.music.set_volume(data['audio']['music_volume'])
    elif name == 'sound_volume':
        sound.set_volume(data['audio']['sound_volume'])

    with open('data/data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def on_off_playback_music() -> None:
    """
    pass
    """

    if not check('audio', 'mute_music'):
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


def on_off_playback_sound() -> None:
    """
    pass
    """

    if not check('audio', 'mute_sound'):
        sound.set_volume(0)
    else:
        sound.set_volume(check('audio', 'sound_volume'))


def play_sound() -> None:
    """
    pass
    """

    sound.play()


class Zastavka:
    """
    Класс, реализующий окно Заставки
    """

    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Координаты положения элементов
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]

        # Цвета элементов
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Сохранение координат звезды
        self.star = []
        inner_angle, outer_radius = 2 * math.pi / 10, 80 / (2 * math.sin(math.pi / 5))
        inner_radius = 80 / (2 * math.tan(math.pi / 5)) * math.tan(math.pi / 10)
        for j in range(10):
            angle = j * inner_angle
            a = outer_radius if j % 2 == 0 else inner_radius
            self.star.append([a * math.cos(angle), a * math.sin(angle)])

        # Создание текста, названия игры
        custom_font = pygame.font.Font('data/Docker.ttf', 80)
        self.text = custom_font.render('Gravity Flux', True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(400, 300))

        # Создание счётчика
        self.n = 0

    def draw(self) -> None:
        """
        Метод отрисовки окна заставки
        """

        # Счётчик для отрисвки
        self.n = (self.n + 1) % 4
        if self.n == 0:
            # Изменение координат элементов
            for i in range(len(self.coord)):
                self.coord[i][0] = max(0, min(self.coord[i][0] + randint(-200, 200), 800))
                self.coord[i][1] = max(0, min(self.coord[i][1] + randint(-200, 200), 600))

        # Отрисовка элементов
        for i in range(len(self.coord)):
            x, y = self.coord[i][0], self.coord[i][1]
            p = randint(1, 4)
            if p % 2 == 0:
                pygame.draw.polygon(self.screen, self.collor[i], [[x, y], [x - 60, y + 80], [x - 30, y + 80],
                                                                  [x - 60, y + 140], [x, y + 60], [x - 30, y + 60]])
            else:
                pygame.draw.polygon(self.screen, self.collor[i], [[i[0] + x, i[1] + y] for i in self.star])

        # Отображение текста
        self.screen.blit(self.text, self.text_rect)


class Menu:
    """
    Класс, реализующий окно Главного меню
    """

    def __init__(self, screen, sound) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Координаты положения молний
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background_menu.jpg'), (800, 600))

        # Список цветов молний
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание счётчика
        self.n = 0

        # Создание кнопок
        self.button1 = Button([275, 125, 250, 50], screen, (255, 255, 255), (255, 0, 0), (70, 130, 180), 'Играть',
                              self.start_game, 30, "data/Docker.ttf", sound)
        self.button2 = Button([275, 200, 250, 50], screen, (255, 255, 255), (0, 255, 255), (70, 130, 180), 'Настройки',
                              self.open_setting, 30, "data/Docker.ttf", sound)
        self.button3 = Button([275, 275, 250, 50], screen, (255, 255, 255), (255, 0, 255), (70, 130, 180), 'Результаты',
                              self.close, 30, "data/Docker.ttf", sound)
        self.button4 = Button([275, 350, 250, 50], screen, (255, 255, 255), (0, 255, 255), (70, 130, 180), 'Сбросить',
                              self.open_setting, 30, "data/Docker.ttf", sound)
        self.button5 = Button([275, 425, 250, 50], screen, (255, 255, 255), (255, 0, 255), (70, 130, 180), 'Выход',
                              self.close, 30, "data/Docker.ttf", sound)

        # Создание текста
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.name_screen = font.render('Gravity Flux', True, (255, 255, 255))
        self.screen_rect = self.name_screen.get_rect(center=(55, 10))

    def draw(self) -> None:
        """
        Метод отрисовки окна Главного меню
        """

        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))

        # Счётчик для отрисвки
        self.n = (self.n + 1) % 50

        # Изменение координат
        self.change_coordinates()

        # Отображение всех молний
        for i in range(len(self.coord)):
            x, y = self.coord[i][0], self.coord[i][1]
            pygame.draw.polygon(self.screen, self.collor[i],
                                [[x, y], [x - 48, y + 64], [x - 24, y + 64], [x - 48, y + 112], [x, y + 48],
                                 [x - 24, y + 48]])

        # Отображение текста
        self.screen.blit(self.name_screen, self.screen_rect)

        # Отрисовка всех кнопок
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()
        self.button4.draw()
        self.button5.draw()

    def start_game(self) -> None:
        """
        Метод начала игры
        """

        determination_levels()
        transit('levels')
        screen_change('fl_menu', 'transition')

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('fl_menu', 'transition')

    def close(self) -> None:
        """
        Метод закрытия игры
        """

        screen_change('running', 'fl_menu')

    def change_coordinates(self) -> None:
        """
        Метод изменения координат молний
        """

        # Если счётчик равен нулю, то изменяются цвета и координаты молний
        if self.n == 0:
            self.collor = sorted(self.collor, key=lambda x: random())
            self.coord[0][0] = max(48, min(self.coord[0][0] + randint(-80, 80), 275))
            self.coord[0][1] = max(15, min(self.coord[0][1] + randint(-80, 80), 188))
            self.coord[1][0] = max(573, min(self.coord[1][0] + randint(-80, 80), 800))
            self.coord[1][1] = max(0, min(self.coord[1][1] + randint(-80, 80), 188))
            self.coord[2][0] = max(48, min(self.coord[2][0] + randint(-80, 80), 275))
            self.coord[2][1] = max(275, min(self.coord[2][1] + randint(-80, 80), 488))
            self.coord[3][0] = max(573, min(self.coord[3][0] + randint(-80, 80), 800))
            self.coord[3][1] = max(275, min(self.coord[3][1] + randint(-80, 80), 488))

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        self.button1.handle_event(event)
        self.button2.handle_event(event)
        self.button3.handle_event(event)
        self.button4.handle_event(event)
        self.button5.handle_event(event)


class Settings:
    """
    Класс, реализующий окно Настроек
    """

    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        music_volume = check('audio', 'music_volume')
        sound_volume = check('audio', 'sound_volume')
        zn1 = 'Выключить' if check('audio', 'mute_music') else 'Включить'
        zn2 = 'Выключить' if check('audio', 'mute_sound') else 'Включить'

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background_setting.jpg'),
                                                 (800, 600))

        # Создание кнопок
        self.button1 = Button([80, 120, 220, 50], screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn1,
                              self.onn_off_music, 30, "data/BlackOpsOne-Regular_RUS_by_alince.otf", False)
        self.button2 = Button([80, 320, 220, 50], screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn2,
                              self.onn_off_sound, 30, "data/BlackOpsOne-Regular_RUS_by_alince.otf", False)
        self.button3 = Button([300, 520, 200, 50], screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Назад',
                              self.close_seting, 30)
        self.button4 = Button([60, 520, 200, 50], screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Restart',
                              self.play_game, 30)
        self.button5 = Button([540, 520, 200, 50], screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Menu',
                              self.return_menu, 30)

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание слайдеров
        self.slider_music = Slider(screen, [400, 210, 300, 20], 0, 1, music_volume, 'music_volume')
        self.slider_sound = Slider(screen, [400, 410, 300, 20], 0, 1, sound_volume, 'sound_volume')

        # Создание вспомогательного текста
        self.font = pygame.font.Font(None, 28)
        self.text1 = self.font.render('Громкость музыки: ', True, (255, 255, 255))
        self.text1_rect = self.text1.get_rect(center=(180, 220))
        self.text2 = self.font.render('Громкость звуковых эфектов: ', True, (255, 255, 255))
        self.text2_rect = self.text2.get_rect(center=(200, 420))
        self.text5 = self.font.render('Музыка', True, (255, 255, 255))
        self.text5_rect = self.text1.get_rect(center=(250, 100))
        self.text6 = self.font.render('Звуковые эфекты', True, (255, 255, 255))
        self.text6_rect = self.text2.get_rect(center=(250, 300))

        self.text7 = self.font.render('A - движение влево', True, (255, 255, 255))
        self.text7_rect = self.text2.get_rect(center=(720, 50))
        self.text8 = self.font.render('D - движение вправо', True, (255, 255, 255))
        self.text8_rect = self.text2.get_rect(center=(720, 70))
        self.text9 = self.font.render('W - смена гравитации', True, (255, 255, 255))
        self.text9_rect = self.text2.get_rect(center=(720, 90))
        self.text10 = self.font.render('Q - атака', True, (255, 255, 255))
        self.text10_rect = self.text2.get_rect(center=(720, 110))
        self.text11 = self.font.render('Space - прыжок', True, (255, 255, 255))
        self.text11_rect = self.text2.get_rect(center=(720, 130))
        self.font_2 = pygame.font.Font(None, 30)
        self.text12 = self.font_2.render('Подсказка:', True, (255, 255, 255))
        self.text12_rect = self.text2.get_rect(center=(720, 24))

        # Создание текста - название окна
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font.render('Settings', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(42, 10))

    def draw(self) -> None:
        """
        Метод отрисовки окна настроек
        """

        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))

        # Отрисовка всех кнопок
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()

        if check('screen', 'past_position') == 'gemplay':
            self.button4.draw()
            self.button5.draw()

        # Отрисовка слайдера громкости музыки, если музыка включена
        if check('audio', 'mute_music'):
            self.slider_music.draw()
            self.screen.blit(self.text1, self.text1_rect)
            text3 = self.font.render(str(int(round(float(f'{check("audio", "music_volume"):.2f}') * 100, 0))), True,
                                     (255, 255, 255))
            text3_rect = text3.get_rect(center=(330, 220))
            self.screen.blit(text3, text3_rect)

        # Отрисовка слайдера громкости звуковых эффектов, если музыка включена
        if check('audio', 'mute_sound'):
            self.slider_sound.draw()
            self.screen.blit(self.text2, self.text2_rect)
            text4 = self.font.render(str(int(round(float(f'{check("audio", "sound_volume"):.2f}') * 100, 0))), True,
                                     (255, 255, 255))
            text4_rect = text4.get_rect(center=(370, 420))
            self.screen.blit(text4, text4_rect)

        # Отображение всех текстов
        self.screen.blit(self.text5, self.text5_rect)
        self.screen.blit(self.text6, self.text6_rect)
        self.screen.blit(self.text_surface, self.text_rect)

        if check('screen', 'past_position') == 'gemplay':
            self.screen.blit(self.text7, self.text7_rect)
            self.screen.blit(self.text8, self.text8_rect)
            self.screen.blit(self.text9, self.text9_rect)
            self.screen.blit(self.text10, self.text10_rect)
            self.screen.blit(self.text11, self.text11_rect)
            self.screen.blit(self.text12, self.text12_rect)

    def return_menu(self):
        start_screen()
        screen_change('fl_zastavka', 'fl_menu')
        transit('fl_menu')
        screen_change('fl_menu', 'transition')

    def play_game(self):
        play_game()
        transit('gemplay')
        screen_change('settings', 'transition')

    def onn_off_music(self) -> None:
        """
        Метод включения/выключения фоновой музыки
        """

        # Изменение настройки музыки
        self.onn_off('mute_music')

        # Включение/выключение проигрывания музыки
        on_off_playback_music()

    def onn_off_sound(self) -> None:
        """
        Метод включения/выключения звуковых эффектов
        """

        # Изменение настройки звуковых эффектов
        self.onn_off('mute_sound')

        # Включение/выключение проигрывания звуковых эффектов
        on_off_playback_sound()

    def onn_off(self, name) -> None:
        """
        Метод, который присваивает противоположное значение для "name" из файла 'data.json'
        """

        # Чтение данных из файла 'data.json'
        with open('data/data.json', 'r', encoding='utf8') as file:
            data = json.load(file)

        # Изменение полученных данных
        data['audio'][name] = not data['audio'][name]

        # Запись в файл 'data.json' изменённых данных
        with open('data/data.json', 'w', encoding='utf8') as file:
            json.dump(data, file, indent=2)

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        # Проверка событий слайдеров
        self.slider_music.handle_event(event)
        self.slider_sound.handle_event(event)

        # Проверка событий кнопок
        self.button1.handle_event(event)
        self.button2.handle_event(event)
        self.button3.handle_event(event)

        if check('screen', 'past_position') == 'gemplay':
            self.button4.handle_event(event)
            self.button5.handle_event(event)

    def close_seting(self) -> None:
        """
        Метод, который закрывает окно нстроек
        """

        # Определение в каком окне был пользователь, перед тем как зайти в настройки
        transit(check('screen', 'past_position'))
        screen_change('settings', 'transition')


class Levels_Selection:
    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background_levels.jpg'),
                                                 (800, 600))

        # Загрузка картинок
        self.image = []

        # Создание кнопок
        self.button1, self.button2, self.button3 = None, None, None

        self.button4 = Button([520, 500, 180, 40], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Назад',
                              self.closing_window, 25)
        self.button5 = Button([80, 500, 180, 40], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Настройки',
                              self.open_setting, 25)

        # Создание текста - название окна
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font.render('Levels', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(34, 10))

        font_2 = pygame.font.Font("data/Docker.ttf", 25)
        self.text = font_2.render('Выберите уровень сложности', True, (255, 255, 255))
        self.text_r = self.text.get_rect(center=(400, 60))

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('levels', 'transition')

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора ровня сложности
        """

        setting_value('level', '')
        transit('fl_menu')
        screen_change('levels', 'transition')

    def creating_buttons(self):
        # Создание кнопок
        if check('open_levels', 'easy'):
            collor = (255, 69, 0)
        else:
            collor = (105, 105, 105)
        self.image.append([pygame.transform.scale(pygame.image.load(f'images/levels/level_0.jpg'), (160, 280)),
                           [90, 100]])
        self.button1 = Button([80, 400, 180, 50], screen, (255, 255, 255), (0, 206, 209), collor, 'Easy',
                              card_selection_easy, 30)

        if check('open_levels', 'normal'):
            collor, ind = (255, 69, 0), 0
        else:
            collor, ind = (105, 105, 105), 1
        self.image.append([pygame.transform.scale(pygame.image.load(f'images/levels/level_1_{ind}.jpg'), (160, 280)),
                           [90 + 220, 100]])
        self.button2 = Button([300, 400, 180, 50], screen, (255, 255, 255), (0, 206, 209), collor, 'Normal',
                              card_selection_normal, 30)

        if check('open_levels', 'hard'):
            collor, ind = (255, 69, 0), 0
        else:
            collor, ind = (105, 105, 105), 1
        self.image.append([pygame.transform.scale(pygame.image.load(f'images/levels/level_2_{ind}.jpg'), (160, 280)),
                           [90 + 220 * 2, 100]])
        self.button3 = Button([520, 400, 180, 50], screen, (255, 255, 255), (0, 206, 209), collor, 'Hard',
                              card_selection_hard, 30)

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        self.screen.blit(self.background, (0, 0))
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()
        self.button4.draw()
        self.button5.draw()
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.text, self.text_r)
        for i in self.image:
            self.screen.blit(i[0], i[1])

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        # Проверка событий кнопок
        if check('open_levels', 'easy'):
            self.button1.handle_event(event)
        if check('open_levels', 'normal'):
            self.button2.handle_event(event)
        if check('open_levels', 'hard'):
            self.button3.handle_event(event)
        self.button4.handle_event(event)
        self.button5.handle_event(event)


class Card_Selection:
    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background_cards.jpg'),
                                                 (800, 600))

        self.button1, self.button2, self.button3 = None, None, None
        self.card_1, self.card_2, self.card_3, self.name = None, None, None, None

        # Создание кнопок
        self.button4 = Button([570, 500, 180, 40], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Назад',
                              self.closing_window, 25)
        self.button5 = Button([70, 500, 180, 40], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Настройки',
                              self.open_setting, 25)

        # Создание текста - название окна
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font.render('Card Selection', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(67, 10))

        font_2 = pygame.font.Font("data/Docker.ttf", 25)
        self.text = font_2.render('Выберите карту', True, (255, 255, 255))
        self.text_r = self.text.get_rect(center=(400, 68))

        # Загрузка картинок
        self.image = []

    def card_one(self) -> None:
        """
        Метод определения, записи названия выбранной карты
        """

        setting_value('name_card', self.card_1)
        self.open_card_type()

    def card_two(self) -> None:
        """
        Метод определения, записи названия выбранной карты
        """

        setting_value('name_card', self.card_2)
        self.open_card_type()

    def card_three(self) -> None:
        """
        Метод определения, записи названия выбранной карты
        """

        setting_value('name_card', self.card_3)
        self.open_card_type()

    def open_card_type(self) -> None:
        """
        Метод открытия окна выбора типа карты
        """

        creating_buttons(['G', 'D', 'E'])
        transit('card_type')
        screen_change('cards', 'transition')

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('cards', 'transition')

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора карты
        """

        setting_value('name_card', '')
        transit('levels')
        screen_change('cards', 'transition')

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        self.screen.blit(self.background, (0, 0))
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()
        self.button4.draw()
        self.button5.draw()
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.text, self.text_r)
        for i in self.image:
            self.screen.blit(i[0], i[1])

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        # Проверка событий кнопок
        if check_open_cards(self.name, self.card_1):
            self.button1.handle_event(event)
        if check_open_cards(self.name, self.card_2):
            self.button2.handle_event(event)
        if check_open_cards(self.name, self.card_3):
            self.button3.handle_event(event)
        self.button4.handle_event(event)
        self.button5.handle_event(event)

    def creating_buttons(self, name1, name2, name3) -> None:
        """
        Метод добавления кнопок
        """

        self.card_1 = name1
        self.card_2 = name2
        self.card_3 = name3

        if check('gameplay', 'level') == 'easy':
            name = 'easy'
        elif check('gameplay', 'level') == 'normal':
            name = 'normal'
        else:
            name = 'hard'
        self.name = name

        if check_open_cards(name, name1):
            collor, n = (75, 0, 130), ''
        else:
            collor, n = (105, 105, 105), '_close'
        self.image.append([pygame.transform.scale(pygame.image.load(f'images/cards/{name1}{n}.jpg'), (160, 280)),
                           [80, 100]])
        self.button1 = Button([40, 420, 240, 45], screen, (255, 255, 255), (0, 128, 0), collor, name1, self.card_one,
                              20, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

        if check_open_cards(name, name2):
            collor, n = (75, 0, 130), ''
        else:
            collor, n = (105, 105, 105), '_close'
        self.image.append([pygame.transform.scale(pygame.image.load(f'images/cards/{name2}{n}.jpg'), (160, 280)),
                           [80 + 250, 100]])
        self.button2 = Button([290, 420, 240, 45], screen, (255, 255, 255), (0, 128, 0), collor, name2, self.card_two,
                              20, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

        if check_open_cards(name, name3):
            collor, n = (75, 0, 130), ''
        else:
            collor, n = (105, 105, 105), '_close'
        self.image.append([pygame.transform.scale(pygame.image.load(f'images/cards/{name3}{n}.jpg'), (160, 280)),
                           [80 + 250 * 2, 100]])
        self.button3 = Button([540, 420, 240, 45], screen, (255, 255, 255), (0, 128, 0), collor, name3, self.card_three,
                              20, "data/BlackOpsOne-Regular_RUS_by_alince.otf")


class Card_Type:
    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background_cards_type.jpg'),
                                                 (800, 600))

        # Создание кнопок
        self.button1 = Button([100, 430, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Choco',
                              self.choice_choco, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button2 = Button([315, 430, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Grass',
                              self.choice_grass, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button3 = Button([530, 430, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Snow',
                              self.choice_snow, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button4 = Button([100, 290, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Cake',
                              self.choice_cake, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button5 = Button([315, 290, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Dirt',
                              self.choice_dirt, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button6 = Button([530, 290, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Sand',
                              self.choice_sand, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button7 = Button([100, 150, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Tundra',
                              self.choice_tundra, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button8 = Button([315, 150, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Castle',
                              self.choice_castle, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button9 = Button([530, 150, 150, 40], screen, (255, 255, 255), (30, 140, 255), (200, 20, 130), 'Purple',
                              self.choice_purple, 25, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

        self.button10 = Button([500, 500, 180, 40], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Назад',
                               self.closing_window, 25)
        self.button11 = Button([100, 500, 180, 40], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Настройки',
                               self.open_setting, 25)

        # Создание изображений
        self.images = []
        for i in range(9):
            self.images.append(
                [pygame.image.load(f'images/tiles/{i + 1}_1.png'), [140 + 215 * (i // 3), 70 + 140 * (i % 3)]])

        # Создание текста - название окна
        font_1 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font_1.render('Card Type', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(47, 10))

        font_2 = pygame.font.Font("data/Docker.ttf", 25)
        self.text = font_2.render('Выберите тип карты', True, (255, 255, 255))
        self.text_r = self.text.get_rect(center=(400, 40))

    def choice_choco(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'choco')
        self.open_character_types()

    def choice_grass(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'grass')
        self.open_character_types()

    def choice_snow(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'snow')
        self.open_character_types()

    def choice_cake(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'cake')
        self.open_character_types()

    def choice_dirt(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'dirt')
        self.open_character_types()

    def choice_sand(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'sand')
        self.open_character_types()

    def choice_tundra(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'tundra')
        self.open_character_types()

    def choice_castle(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'castle')
        self.open_character_types()

    def choice_purple(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        setting_value('type_card', 'purple')
        self.open_character_types()

    def open_character_types(self) -> None:
        """
        Метод открытия окна выбора персонажа
        """

        transit('character_types')
        screen_change('card_type', 'transition')

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('card_type', 'transition')

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора типа карты
        """

        setting_value('type_card', '')
        transit('cards')
        screen_change('card_type', 'transition')

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        self.screen.blit(self.background, (0, 0))
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()
        self.button4.draw()
        self.button5.draw()
        self.button6.draw()
        self.button7.draw()
        self.button8.draw()
        self.button9.draw()
        self.button10.draw()
        self.button11.draw()
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.text, self.text_r)

        for i in self.images:
            self.screen.blit(i[0], i[1])

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        # Проверка событий кнопок
        self.button1.handle_event(event)
        self.button2.handle_event(event)
        self.button3.handle_event(event)
        self.button4.handle_event(event)
        self.button5.handle_event(event)
        self.button6.handle_event(event)
        self.button7.handle_event(event)
        self.button8.handle_event(event)
        self.button9.handle_event(event)
        self.button10.handle_event(event)
        self.button11.handle_event(event)


class Character_Types:
    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        self.button1, self.button2, self.button3 = None, None, None
        self.name1, self.name2, self.name3 = None, None, None

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background_character_types.jpg'),
                                                 (800, 600))

        # Создание кнопок
        self.button4 = Button([570, 500, 180, 40], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Назад',
                              self.closing_window, 25)
        self.button5 = Button([70, 500, 180, 40], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Настройки',
                              self.open_setting, 25)
        self.button6 = Button([300, 490, 220, 60], screen, (255, 255, 255), (0, 255, 0), (255, 99, 71), 'Начать игру',
                              self.play_game, 30, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.start = False

        # Создание текста
        font_1 = pygame.font.Font("data/Docker.ttf", 25)
        self.text = font_1.render('Выберите персонажа', True, (255, 255, 255))
        self.text_r = self.text.get_rect(center=(400, 40))

        # Создание текста - название окна
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font.render('Character Types', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(76, 10))

    def player_one(self) -> None:
        setting_value('character', self.name1)
        self.start = True
        self.button1 = Button([40, 440, 240, 40], screen, (255, 255, 255), (255, 20, 150), (30, 145, 255), self.name1,
                              self.player_one, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button2 = Button([290, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name2,
                              self.player_two, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button3 = Button([540, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name3,
                              self.player_three, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

    def player_two(self) -> None:
        setting_value('character', self.name2)
        self.start = True
        self.button1 = Button([40, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name1,
                              self.player_one, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button2 = Button([290, 440, 240, 40], screen, (255, 255, 255), (255, 20, 150), (30, 145, 255), self.name2,
                              self.player_two, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button3 = Button([540, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name3,
                              self.player_three, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

    def player_three(self) -> None:
        setting_value('character', self.name3)
        self.start = True
        self.button1 = Button([40, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name1,
                              self.player_one, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button2 = Button([290, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name2,
                              self.player_two, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button3 = Button([540, 440, 240, 40], screen, (255, 255, 255), (255, 20, 150), (30, 145, 255), self.name3,
                              self.player_three, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('character_types', 'transition')

    def play_game(self):
        """
        Запуск загрузки
        """

        loading()
        transit('loading_screen')
        screen_change('character_types', 'transition')

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора персонажа
        """

        self.start = False
        setting_value('character', '')
        transit('card_type')
        screen_change('character_types', 'transition')
        self.rollback()

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        self.screen.blit(self.background, (0, 0))
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()
        self.button4.draw()
        self.button5.draw()
        if self.start:
            self.button6.draw()
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.text, self.text_r)

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        # Проверка событий кнопок
        self.button1.handle_event(event)
        self.button2.handle_event(event)
        self.button3.handle_event(event)
        self.button4.handle_event(event)
        self.button5.handle_event(event)
        if self.start:
            self.button6.handle_event(event)

    def creating_buttons(self, name1, name2, name3) -> None:
        """
        Метод добавления кнопок
        """

        # Сохранение названия игроков
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3

        # Создание кнопок
        self.button1 = Button([40, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), name1,
                              self.player_one, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button2 = Button([290, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), name2,
                              self.player_two, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button3 = Button([540, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), name3,
                              self.player_three, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

        self.start = False

    def rollback(self):
        self.button1 = Button([40, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name1,
                              self.player_one, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button2 = Button([290, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name2,
                              self.player_two, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")
        self.button3 = Button([540, 440, 240, 40], screen, (255, 255, 255), (0, 128, 0), (75, 0, 130), self.name3,
                              self.player_three, 18, "data/BlackOpsOne-Regular_RUS_by_alince.otf")


class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen

        self.progress = None
        self.rotation, self.message, self.font, self.clock, self.step = None, None, None, None, None

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background_loading.jpg'),
                                                 (800, 600))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        text_surface = self.font.render(self.message, True, (255, 215, 0))
        text_rect = text_surface.get_rect(center=(400, 250))
        self.screen.blit(text_surface, text_rect)

        radius = 20
        angle = math.radians(self.rotation)
        x = int(400 + radius * math.cos(angle))
        y = int(300 + radius * math.sin(angle))
        pygame.draw.circle(self.screen, (210, 105, 30), (x, y), 10)

        bar_x = 200
        bar_y = 350
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, 400, 22), 3)
        fill_width = int(400 * self.progress)
        pygame.draw.rect(self.screen, (255, 215, 0), (bar_x, bar_y, fill_width, 22))

        pygame.display.flip()

    def update(self):
        self.progress = self.step / 20
        self.message = f"Loading... ({int(self.progress * 100)}%)"

        self.rotation += randint(20, 50)
        if self.rotation >= 360:
            self.rotation = 0

        time.sleep(0.1)
        self.step += randint(1, 2)

        if self.step > 20:
            play_game()
            transit('gemplay')
            screen_change('loading_screen', 'transition')

        self.draw()

    def updaute(self):
        self.progress = 0.0
        self.rotation = 0
        self.message = "Loading..."
        self.font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 40)
        self.clock = pygame.time.Clock()
        self.step = 0


class Button:
    """
    Класс реализующий кнопку
    """

    def __init__(self, coord, screen, collor_text, hover_color, collor_button, text, funk, zn, font="data/Docker.ttf",
                 fl=True) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Задаёт координаты
        self.rect = pygame.Rect(coord)

        # Флаг отслеживания наведения мыши
        self.fl = fl

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Присваивание цветов объектам
        self.collor_text = collor_text
        self.collor_button = collor_button
        self.hover_color = hover_color

        # Сохранение ссылки на функцию, которая будет вызываться по нажатию на кнопку
        self.funk = funk

        # Задание шрифта
        self.font = pygame.font.Font(font, zn)

        # Реализация текста для кнопки
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.collor_text)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        # Флаг, показывающий находится ли курсор на кнопке
        self.hove = False

    def draw(self) -> None:
        """
        Метод отрисовки кнопки
        """

        # Рисование прямоугольника по заданным параметрам
        pygame.draw.rect(self.screen, (self.collor_button if not self.hove else self.hover_color), self.rect)

        # Отображение текста кнопки, поверх прямоугольника
        self.screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event) -> None:
        """
        Метод, который обрабатывает события связанные с кнопкой
        """

        # Проверяет тип события (наведения на кнопку курсора)
        if event.type == pygame.MOUSEMOTION:
            self.hove = self.rect.collidepoint(event.pos)
        # Проверяет тип события (нажатия на кнопку курсором)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hove and self.funk:
                # Вызов функций по нажатию кнопоки
                play_sound()
                self.funk()

                if self.fl:
                    self.hove = False

                self.check_text()

    def check_text(self) -> None:
        """
        Класс изменяющий текст кнопок
        """

        # При тексте "Выключить" на кнопке он заменяется на "Включить"
        if self.text == 'Выключить':
            self.text = 'Включить'
            self.text_surface = self.font.render(self.text, True, self.collor_text)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        # При тексте "Включить" на кнопке он заменяется на "Выключить"
        elif self.text == 'Включить':
            self.text = 'Выключить'
            self.text_surface = self.font.render(self.text, True, self.collor_text)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)


class Slider:
    """
    Класс слайдера
    """

    def __init__(self, screen, coord, min_value, max_value, start_value, name) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Название слайдера
        self.name = name

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Координаты x и y
        self.x = coord[0]
        self.y = coord[1]

        # Ширина и высота слайдера
        self.width = coord[2]
        self.height = coord[3]

        # Минимальное и максимальное значения
        self.min_value = min_value
        self.max_value = max_value

        # Начальное значение
        self.value = start_value

        # Геометрия слайдера
        self.slider_rect = pygame.Rect(coord)

        # Геометрия курсора слайдера
        self.cursor_width = 10
        self.cursor_rect = pygame.Rect(self.x + (self.width * self.value) - self.cursor_width // 2, self.y,
                                       self.cursor_width, self.height)

        # Флаг перемещения курсора
        self.dragging = False

    def draw(self) -> None:
        """
        Метод отрисовки слайдеров
        """

        # Отрисовка слайдера
        pygame.draw.rect(self.screen, (150, 150, 150), self.slider_rect)

        # Отрисовка ползунка слайдера
        pygame.draw.rect(self.screen, (200, 200, 200), self.cursor_rect)

    def handle_event(self, event) -> None:
        """
        Метод для обработки событий мыши
        """

        # Проверка, является ли текущее событие нажатием кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка, находится ли курсор мыши на ползунке слайдера
            if self.cursor_rect.collidepoint(event.pos):
                # Устанавливает атрибут перемещения курсора True
                self.dragging = True

        # Проверка, является ли текущее событие отпусканием кнопки мыши
        elif event.type == pygame.MOUSEBUTTONUP:
            # Устанавливает атрибут перемещения курсора False
            self.dragging = False

        # Проверка, является ли текущее событие перемещением мыши
        elif event.type == pygame.MOUSEMOTION:
            # Проверка, находится ли ползунок в режиме перетаскивания
            if self.dragging:
                # Получаем координату x мыши
                mouse_x = event.pos[0]

                # Вычисление относительное положение ползунка на слайдере
                self.value = (mouse_x - self.x) / self.width

                # Ограничивание значение self.value между минимальным и максимальным
                self.value = max(self.min_value, min(self.value, self.max_value))
                self.cursor_rect.x = self.x + (self.width * self.value) - self.cursor_width // 2
                volume_change(self.value, self.name)


class ScreenTransition:
    """
    Класс для создания эффекта перехода (затемнения) экрана.
    """

    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        self.collor = (0, 0, 0)

        self.scren = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        self.alpha = 0
        self.pos = None

        self.n = 0

    def draw(self) -> None:
        """
        Отображает эффект затемнения на экране.
        """

        self.n += 1
        if self.n >= 30:
            self.close()

        self.alpha += 2

        self.scren.fill((*self.collor, self.alpha))
        self.screen.blit(self.scren, (0, 0))

    def close(self) -> None:
        screen_change('transition', self.pos)

    def new_pos(self, new_pos) -> None:
        self.alpha = 0
        self.n = 0
        self.pos = new_pos


class Gamplay:
    def __init__(self, screen):
        self.screen = screen
        self.level, self.name_card, self.background_map, self.cards, self.tile_images = None, None, None, None, None
        self.character, self.type_card_background, self.tiles, self.player, self.numb = None, None, None, None, None
        self.time, self.dis_time, self.dis_time_rect, self.start_time, self.date_start = None, None, None, None, None
        self.spis_enemy = []
        self.button_setting = Button([6, 6, 32, 32], screen, (255, 255, 255), (100, 100, 100), (0, 0, 0), 'X',
                                     self.open_setting, 32, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

    def loading(self):
        self.time = 0
        self.start_time = f'{datetime.datetime.now().time():%H:%M}'
        self.date_start = '.'.join(f'{datetime.datetime.now().date()}'.split('-')[::-1])
        self.level = check('gameplay', 'level')
        self.name_card = check('gameplay', 'name_card')
        type_card = check('gameplay', 'type_card')
        self.character = check('gameplay', 'character')
        self.type_card_background = check('type_card_background', type_card)
        self.background_map = pygame.transform.scale(
            pygame.image.load(check('type_card_background', type_card)).convert_alpha(), (800, 600))
        self.tiles = pygame.sprite.Group()
        self.generate_map(type_card)
        self.creating_enemy()
        self.player = self.Eloise(self.screen, 400, 200, self.tiles, self.numb)

    def draw(self):
        self.time += 1
        self.draw_map()
        self.draw_enemy()
        self.player.update()

    def draw_map(self):
        x_bac = self.player.cord_bac()
        self.screen.blit(self.background_map, (x_bac, 0))
        self.screen.blit(self.background_map, (800 + x_bac, 0))
        num_one, num_two = self.player.cords_map()
        for tile in self.tiles:
            tile.draw(num_one, num_two)

        # Обновление текста, время
        custom_font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 12)
        if self.time < 216000:
            zn1, zn2 = str(self.time // 3600), str(self.time % 3600 // 60)
            time = f'{"0" * (2 - len(zn1)) + zn1}:{"0" * (2 - len(zn2)) + zn2}'
        else:
            zn1, zn2, zn3 = str(self.time // 216000), str(self.time % 216000 // 3600), str(
                self.time % 216000 % 3600 // 60)
            time = f'{"0" * (2 - len(zn1)) + zn1}:{"0" * (2 - len(zn2)) + zn2}:{"0" * (2 - len(zn3)) + zn3}'
        self.dis_time = custom_font.render(f'time: {time}', True, (0, 0, 0))
        self.dis_time_rect = self.dis_time.get_rect(topleft=(2, 586))

        self.screen.blit(self.dis_time, self.dis_time_rect)
        self.button_setting.draw()

    def creating_enemy(self):
        self.spis_enemy = []
        self.spis_enemy.append(self.Enemy(screen, 1120, 270, 2, 3, self.tiles, -1, 12, 50, 132))
        self.spis_enemy.append(self.Enemy(screen, 1760, 250, 2, 3, self.tiles, -1, 12, 50, 150))
        self.spis_enemy.append(self.Enemy(screen, 2752, 200, 2, 3, self.tiles, -1, 12, 50, 132))
        self.spis_enemy.append(self.Enemy(screen, 3328, 384, 2, 3, self.tiles, 1, 12, 80, 200))

    def draw_enemy(self):
        num_one, num_two = self.player.cords_map()
        for enemy in self.spis_enemy:
            enemy.draw(num_one, num_two)

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        # Проверка событий кнопок
        self.button_setting.handle_event(event)

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('gemplay', 'transition')

    def load_images(self, t_s, number_cart):
        images = {
            'A': pygame.image.load(f"images/tiles/{number_cart}_1.png").convert_alpha(),
            'B': pygame.image.load(f"images/tiles/{number_cart}_2.png").convert_alpha(),
            'C': pygame.image.load(f"images/tiles/{number_cart}_3.png").convert_alpha(),
            'D': pygame.image.load(f"images/tiles/{number_cart}_4.png").convert_alpha(),
            'E': pygame.image.load(f"images/tiles/{number_cart}_5.png").convert_alpha(),
            'F': pygame.image.load(f"images/tiles/{number_cart}_6.png").convert_alpha(),
            'G': pygame.image.load(f"images/tiles/{number_cart}_7.png").convert_alpha(),
            'H': pygame.image.load(f"images/tiles/{number_cart}_8.png").convert_alpha(),
            'I': pygame.image.load(f"images/tiles/{number_cart}_9.png").convert_alpha(),
            'J': pygame.image.load(f"images/tiles/{number_cart}_10.png").convert_alpha(),
            'K': pygame.image.load(f"images/tiles/{number_cart}_11.png").convert_alpha(),
            'L': pygame.image.load(f"images/tiles/{number_cart}_12.png").convert_alpha(),
            'M': pygame.image.load(f"images/tiles/{number_cart}_13.png").convert_alpha()
        }

        for key, image in images.items():
            images[key] = pygame.transform.scale(image, (t_s, t_s))

        return images

    def generate_map(self, type_card):
        number_cart = {
            "tundra": "1",
            "cake": "2",
            "choco": "3",
            "castle": "4",
            "dirt": "5",
            "grass": "6",
            "purple": "7",
            "sand": "8",
            "snow": "9"
        }
        tile_images = self.load_images(32, number_cart[type_card])
        cards = check_levels('levels', self.name_card)
        self.numb = len(cards[0]) * 32
        for y, row in enumerate(cards):
            for x, symbol in enumerate(row):
                if symbol in tile_images:
                    image = tile_images[symbol]
                    tile = self.Tile(self.screen, image, x * 32, y * 32)
                    self.tiles.add(tile)

        # Создание текста, время
        custom_font = pygame.font.Font('data/Docker.ttf', 18)
        self.dis_time = custom_font.render(f'time: 00:00', True, (0, 0, 0))
        self.dis_time_rect = self.dis_time.get_rect(center=(700, 500))

    class Tile(pygame.sprite.Sprite):
        def __init__(self, screen, image, x, y):
            super().__init__()
            self.screen = screen
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def draw(self, pos_player, pos_player_display):
            tile_pos = (self.rect.x - (pos_player - pos_player_display), self.rect.y)
            if -32 < tile_pos[0] < 800 and -32 < tile_pos[1] < 600:
                self.screen.blit(self.image, tile_pos)

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, screen, x, y, speed, health, list_tile, grav, jump, rad, max_rad):
            super().__init__()
            self.screen = screen
            self.x, self.y = x, y
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 0, 0))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.speed = speed
            self.health = health
            self.list_tile = list_tile
            self.napr_right = True
            self.persecution = False
            self.player_pos = None
            self.expectation = True
            self.max_rad = max_rad
            self.rad = rad
            self.counter = 0
            self.is_jump = 1
            self.grav = grav
            self.jump = jump
            self.pos = 0
            self.v_y = 0

        def draw(self, pos_player, pos_player_display):
            if self.x - self.max_rad < pos_player < self.x or self.x < pos_player < self.x + self.max_rad:
                self.player_pos = pos_player
                if self.expectation:
                    self.expectation = False
                self.persecution = True
            else:
                self.persecution = False
                self.player_pos = None

            self.update_x()
            self.update_y()
            print(self.rect.x)
            enemy_pos = (self.rect.x - (pos_player - pos_player_display), self.rect.y)
            if -30 < enemy_pos[0] < 800:
                self.screen.blit(self.image, enemy_pos)

        def update_x(self):
            if self.persecution:
                if self.player_pos < self.rect.x:
                    self.change_x(-self.speed)
                else:
                    self.change_x(self.speed)
            elif not self.expectation:
                if self.rect.x < self.x - self.rad:
                    self.change_x(self.speed)
                elif self.rect.x > self.x + self.rad:
                    self.change_x(-self.speed)
                else:
                    self.expectation = True
            else:
                if self.napr_right:
                    if self.rect.x < self.x + self.rad:
                        self.change_x(self.speed)
                    elif self.rect.x >= self.x + self.rad:
                        self.counter += 1
                        if self.counter == 20:
                            self.counter = 0
                            self.napr_right = False
                else:
                    if self.rect.x > self.x - self.rad:
                        self.change_x(-self.speed)
                    elif self.rect.x <= self.x + self.rad:
                        self.counter += 1
                        if self.counter == 20:
                            self.counter = 0
                            self.napr_right = True

                # if self.rect.x < self.x + 50:
                #    self.change_x(self.speed)
                # elif self.rect.x > self.x + 50:
                #    self.change_x(-self.speed)

        def change_x(self, speed):
            old_x = self.rect.x
            self.rect.x += speed
            if pygame.sprite.spritecollide(self, self.list_tile, False):
                self.rect.x = old_x
                if not self.is_jump:
                    self.v_y = -self.jump * self.grav
                    self.is_jump = True

        def update_y(self):
            self.v_y += self.grav
            self.rect.y += self.v_y
            if collisions := pygame.sprite.spritecollide(self, self.list_tile, False):
                if self.v_y > 0:
                    self.rect.bottom = collisions[0].rect.top
                    if self.grav > 0:
                        self.is_jump = False
                elif self.v_y < 0:
                    self.rect.top = collisions[0].rect.bottom
                    if self.grav < 0:
                        self.is_jump = False

                self.v_y = 0

            # if not (0 - 80 * 2 < self.rect.y < 600 + 80):
            #     print(1)

    class Player(pygame.sprite.Sprite):
        def __init__(self, screen, x, y, image_folder, animation_frames, speed, jump_height, gravity, tiles, numb):
            super().__init__()

            self.image_folder = image_folder  # Папка с изображениями анимации
            self.animation_frames = animation_frames  # Словарь с кадрами анимации
            self.current_frame = 0
            self.screen = screen
            self.frame_delay = 5  # Задержка между кадрами анимации
            self.frame_timer = 0  # Таймер для анимации
            self.gravity = gravity
            self.jump_height = jump_height
            self.speed = speed
            self.tiles = tiles
            self.numb = numb
            self.x = x
            self.x_bac = 0
            self.velocity_y = 0
            self.attack = False
            self.change_graviti = True
            self.smen_grav = True
            self.is_jumping = False
            self.run = False
            self.current_animation = 'mest'
            self.pressing_space = False
            self.grav = 1
            self.direction = 'right'

            # Инициализация изображения и rect
            self.image = pygame.transform.flip(self.animation_frames['mest'][0], False, False)
            self.rect = self.image.get_rect(topleft=(x, y))

        def draw(self):
            self.screen.blit(self.image, (self.x, self.rect.y))

        def get_current_image(self):
            """Возвращает текущий кадр анимации с учетом направления."""

            old = self.current_animation
            if not self.attack:
                if self.change_graviti:
                    if self.is_jumping:
                        self.current_animation = 'jump'
                    else:
                        if self.run:
                            self.current_animation = 'run'
                        else:
                            self.current_animation = 'mest'
                else:
                    self.current_animation = 'smen_graviti'
            else:
                self.current_animation = 'attack'

            if old == self.current_animation:
                self.frame_delay += 1
                if self.frame_delay > 4:
                    self.frame_delay = 0
                    self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.current_animation])
            else:
                self.frame_delay = 0
                self.current_frame = 0

            if self.direction == 'right':
                if self.grav == 1:
                    self.image = pygame.transform.flip(
                        self.animation_frames[self.current_animation][self.current_frame],
                        False, False)
                else:
                    self.image = pygame.transform.flip(
                        self.animation_frames[self.current_animation][self.current_frame],
                        False, True)
            else:
                if self.grav == 1:
                    self.image = pygame.transform.flip(
                        self.animation_frames[self.current_animation][self.current_frame],
                        True, False)
                else:
                    self.image = pygame.transform.flip(
                        self.animation_frames[self.current_animation][self.current_frame],
                        True, True)

        def update(self):
            self.moving_x()
            self.moving_y()
            self.get_current_image()
            self.draw()

        def game_over(self):
            transit('loss')
            screen_change('gemplay', 'transition')

        def win(self):
            pass

        def moving_x(self):
            dx = 0
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and not self.is_jumping and not self.pressing_space and self.velocity_y == 0:
                self.is_jumping, self.pressing_space = True, True
                self.velocity_y = -self.jump_height * self.grav
            elif not keys[pygame.K_SPACE] and not self.is_jumping:
                self.pressing_space = False

            if keys[pygame.K_a] and not keys[pygame.K_d]:
                dx -= self.speed
                self.run = True
                self.direction = 'left'
            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                dx += self.speed
                self.run = True
                self.direction = 'right'
            else:
                self.run = False

            if keys[pygame.K_w] and not self.is_jumping and self.change_graviti:
                self.is_jumping = True
                self.change_graviti = False
                self.grav = -self.grav
            elif not keys[pygame.K_w] and not self.change_graviti and not self.is_jumping:
                self.change_graviti = True

            old_x = self.rect.x
            self.rect.x = max(min(self.rect.x + dx, self.numb), 0)
            if pygame.sprite.spritecollide(self, self.tiles, False):
                self.rect.x = old_x
            else:
                if self.rect.x <= 200:
                    self.x = max(min(self.x + dx, 600), 0)
                elif self.rect.x >= self.numb - 200:
                    self.x = max(min(self.x + dx, 800), 0)
                else:
                    if self.x + dx > 600:
                        self.x_bac = self.x_bac - 2
                    elif self.x + dx < 200:
                        self.x_bac = self.x_bac + 2
                    if self.x_bac < -800:
                        self.x_bac = 0
                    elif self.x_bac > 0:
                        self.x_bac = -800
                    self.x = max(min(self.x + dx, 600), 200)

        def moving_y(self):
            self.velocity_y += self.gravity * self.grav
            self.rect.y += self.velocity_y

            if collisions := pygame.sprite.spritecollide(self, self.tiles, False):
                if self.velocity_y > 0:
                    self.rect.bottom = collisions[0].rect.top
                    if self.grav == 1:
                        self.is_jumping = False
                elif self.velocity_y < 0:
                    self.rect.top = collisions[0].rect.bottom
                    if self.grav == -1:
                        self.is_jumping = False

                self.smen_grav = True
                self.velocity_y = 0

            if not (0 - 80 * 2 < self.rect.y < 600 + 80):
                self.game_over()

        def cords_map(self):
            return self.rect.x, self.x

        def cord_bac(self):
            return self.x_bac

    class Eloise(Player):
        def __init__(self, screen, x, y, tiles, numb):
            image_folder = "image_Eloise"
            animation_frames = {
                'run': [pygame.transform.scale(pygame.image.load(f'image_Eloise/Run_{i}.png'), (40, 80)) for i in
                        range(9)],
                'mest': [pygame.transform.scale(pygame.image.load(f'image_Eloise/mest_{i}.png'), (40, 80)) for i in
                         range(9)],
                'jump': [pygame.transform.scale(pygame.image.load(f'image_Eloise/Jump_{i}.png'), (40, 80)) for i in
                         range(9)],
                'smen_graviti': [pygame.transform.scale(pygame.image.load(f'image_Eloise/Jump_0.png'), (40, 80))],
                'attack': [pygame.transform.scale(pygame.image.load(f'image_Eloise/Run_0.png'), (40, 80))]
            }
            speed = 4
            jump_height = 10
            gravity = 0.5
            super().__init__(screen, x, y, image_folder, animation_frames, speed, jump_height, gravity, tiles, numb)


def main():
    global screen, zastavka, main_menu, setting, levels_selection

    pygame.mixer.music.load("data/file_music/intro.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(1)

    fps = 60
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while check('screen', 'running'):
        for event in pygame.event.get():
            if check('screen', 'fl_menu'):
                main_menu.check_event(event)
            elif check('screen', 'settings'):
                setting.check_event(event)
            elif check('screen', 'levels'):
                levels_selection.check_event(event)
            elif check('screen', 'cards'):
                card_selection.check_event(event)
            elif check('screen', 'card_type'):
                card_type.check_event(event)
            elif check('screen', 'character_types'):
                character_types.check_event(event)
            elif check('screen', 'gemplay'):
                game.check_event(event)

        if check('screen', 'fl_zastavka'):
            if pygame.time.get_ticks() - start_time >= 9200:
                screen_change('fl_zastavka', 'fl_menu')
                music_menu()
            zastavka.draw()
        elif check('screen', 'fl_menu'):
            main_menu.draw()
        elif check('screen', 'settings'):
            setting.draw()
        elif check('screen', 'levels'):
            levels_selection.draw()
        elif check('screen', 'cards'):
            card_selection.draw()
        elif check('screen', 'card_type'):
            card_type.draw()
        elif check('screen', 'character_types'):
            character_types.draw()
        elif check('screen', 'loading_screen'):
            loading_screen.update()
        elif check('screen', 'transition'):
            transition.draw()
        elif check('screen', 'gemplay'):
            game.draw()
        elif check('screen', 'loss'):
            print(1)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    width, height = 800, 600
    start_screen()

    pygame.init()
    sound = pygame.mixer.Sound("data/file_music/button_sound.wav")
    sound.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)

    screen = pygame.display.set_mode((width, height), flags=pygame.NOFRAME)

    zastavka = Zastavka(screen)

    transition = ScreenTransition(screen)

    main_menu = Menu(screen, sound)

    setting = Settings(screen)

    levels_selection = Levels_Selection(screen)

    card_selection = Card_Selection(screen)

    card_type = Card_Type(screen)

    character_types = Character_Types(screen)

    loading_screen = LoadingScreen(screen)

    game = Gamplay(screen)

    main()

    start_screen()
