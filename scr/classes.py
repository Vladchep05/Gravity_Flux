from math import radians, degrees, pi, sin, cos, tan
from random import randint, random, uniform, sample
from time import sleep
import threading
import datetime
import pygame
import json

from scr.functions import (
    check, check_levels, transit, check_open_cards, setting_value, determination_levels, play_musik, loading,
    time_check, card_selection_easy, card_selection_normal, card_selection_hard, play_game, screen_change,
    start_screen, recording_data, music_menu, player_inform, update_improvement, res_loss, res_win, volume_change,
    on_off_playback_music, character_update_but, factory_reset, update_text_info
)

from scr.constants import (
    rating_cost, portal_cords, spawn_coordinates, type_card_background, maximum_improvement,
    catering_coefficients_levels, catering_coefficients_cards, range_rating, rating_character, list_name_card,
    spavn_mobs, list_tiles, animation_frames_character, animations_mob,
    coin_animation, character_level, level_improvement, x_offset_characters, x_offset_mobs, character_genitive,
    attack_soun
)


def initialization():
    global screen, zastavka, transition, main_menu, setting, reset_confirmation, results, levels_selection
    global card_selection, card_type, character_types, improvement_character, pl_info, loading_screen, game, result

    width, height = 800, 600

    pygame.init()

    screen = pygame.display.set_mode((width, height), flags=pygame.NOFRAME)

    zastavka = Zastavka(screen)

    transition = ScreenTransition(screen)

    main_menu = Menu(screen)

    setting = Settings(screen)

    reset_confirmation = Reset_confirmation(screen)

    results = Results(screen)

    levels_selection = Levels_Selection(screen)

    card_selection = Card_Selection(screen)

    card_type = Card_Type(screen)

    character_types = Character_Types(screen)

    improvement_character = Improvement_character(screen)

    pl_info = Playear_info(screen)

    loading_screen = LoadingScreen(screen)

    game = Gamplay(screen)

    result = Result(screen)


class Zastavka:
    """
    Класс, реализующий окно Заставки
    """

    def __init__(self, screen) -> None:
        """
        Конструктор класса, инициализирующий заставку
        """

        # Координаты положения элементов
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]

        # Цвета элементов
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Сохранение координат звезды
        self.star = []
        inner_angle, outer_radius = 2 * pi / 10, 80 / (2 * sin(pi / 5))
        inner_radius = 80 / (2 * tan(pi / 5)) * tan(pi / 10)
        for j in range(10):
            angle = j * inner_angle
            a = outer_radius if j % 2 == 0 else inner_radius
            self.star.append([a * cos(angle), a * sin(angle)])

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
        self.n = (self.n + 1) % 3
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

    def __init__(self, screen) -> None:
        """
        Конструктор класса, который инициализирует главное меню
        """

        # Координаты положения молний
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'), (800, 600))

        # Список цветов молний
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Список кнопок в меню (инициализируется позже)
        self.buttons = []

        # Инициализация кнопок
        self.update_buttom()

        # Создание счётчика кадров для анимации молний
        self.n = 0

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

        # Обновление счетчика анимации молний
        self.n = (self.n + 1) % 50

        # Изменение координат молний
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
        for button in self.buttons:
            button.draw()

    def update_buttom(self) -> None:
        """
        Метод обновления кнопок
        """

        # Очистка списка кнопок, что бы старых элементов не было
        self.buttons = []

        # Добавление кнопок в список
        self.buttons.append(
            ImageButton(
                [260, 125, 280, 60], self.screen, "images/buttons/main_menu/play_0.png",
                "images/buttons/main_menu/play_1.png", self.start_game, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [260, 200, 280, 60], self.screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [260, 275, 280, 60], self.screen, "images/buttons/main_menu/result_0.png",
                "images/buttons/main_menu/result_1.png", self.open_results, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [260, 350, 280, 60], self.screen, "images/buttons/main_menu/reset_0.png",
                "images/buttons/main_menu/reset_1.png", self.open_reset_confirmation, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [260, 425, 280, 60], self.screen, "images/buttons/main_menu/exit_0.png",
                "images/buttons/main_menu/exit_1.png",
                self.close, scale=1.0, hover_scale=1.1
            )
        )

    def open_results(self) -> None:
        """
        Метод перехода к экрану результатов
        """

        # Изменения сцены
        transit('results')

        # Замена текущий экрана с fl_menu на transition
        screen_change('fl_menu', 'transition')

    def open_reset_confirmation(self) -> None:
        """
         Метод перехода к экрану подтверждения сброса
        """

        # Изменения сцены
        transit('reset_confirmation')

        # Замена текущий экрана с fl_menu на transition
        screen_change('fl_menu', 'transition')

        # Обновление кнопок окна главного меню
        self.update_buttom()

    def start_game(self) -> None:
        """
        Метод начала игры
        """

        # Подгрузка уровней
        determination_levels()

        # Переходит к экрану уровней
        transit('levels')
        screen_change('fl_menu', 'transition')

        # Обновление кнопок окна главного меню
        self.update_buttom()

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        # Переходит к экрану настроек
        transit('settings')
        screen_change('fl_menu', 'transition')

        # Обновление кнопок окна главного меню
        self.update_buttom()

    def close(self) -> None:
        """
        Метод закрытия игры
        """

        # Закрывает игру, меняя активное окно
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
        Метод обработки событий Pygame

        :param event: Событие, которое нужно обработать
        """

        # Прохождение по всему списку кнопок
        for button in self.buttons:
            # Проверяется, был ли выполнен клик по кнопке
            button.handle_event(event)


class Settings:
    """
    Класс, реализующий окно Настроек
    """

    def __init__(self, screen) -> None:
        """
        Конструктор класса, который инициализирует настройки
        """

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'),
                                                 (800, 600))

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        self.slider_music, self.slider_sound = None, None

        # Создание слайдеров
        self.update_sliders()

        # Создание и обновление кнопок
        self.button1, self.button2, self.button3, self.button4, self.button5 = None, None, None, None, None
        self.update_button()

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

    def update_sliders(self) -> None:
        """
        Метод обновления слайдеров
        """

        music_volume = check('audio', 'music_volume')
        sound_volume = check('audio', 'sound_volume')

        # Создание слайдеров
        self.slider_music = Slider(screen, [400, 210, 300, 20], 0, 1, music_volume, 'music_volume')
        self.slider_sound = Slider(screen, [400, 410, 300, 20], 0, 1, sound_volume, 'sound_volume')

    def draw(self) -> None:
        """
        Метод отрисовки окна настроек
        """

        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))

        # Отрисовка кнопок
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
            text3 = self.font.render(
                str(int(round(float(f'{check("audio", "music_volume"):.2f}') * 100, 0))), True, (255, 255, 255)
            )
            text3_rect = text3.get_rect(center=(330, 220))
            self.screen.blit(text3, text3_rect)

        # Отрисовка слайдера громкости звуковых эффектов, если музыка включена
        if check('audio', 'mute_sound'):
            self.slider_sound.draw()
            self.screen.blit(self.text2, self.text2_rect)
            text4 = self.font.render(
                str(int(round(float(f'{check("audio", "sound_volume"):.2f}') * 100, 0))), True, (255, 255, 255)
            )
            text4_rect = text4.get_rect(center=(370, 420))
            self.screen.blit(text4, text4_rect)

        # Отображение всех текстов
        self.screen.blit(self.text5, self.text5_rect)
        self.screen.blit(self.text6, self.text6_rect)
        self.screen.blit(self.text_surface, self.text_rect)

        # Отображение управления, если игрок пришел из игрового экрана.
        if check('screen', 'past_position') == 'gemplay':
            self.screen.blit(self.text7, self.text7_rect)
            self.screen.blit(self.text8, self.text8_rect)
            self.screen.blit(self.text9, self.text9_rect)
            self.screen.blit(self.text10, self.text10_rect)
            self.screen.blit(self.text11, self.text11_rect)
            self.screen.blit(self.text12, self.text12_rect)

    def return_menu(self):
        """
        Метод, который возвращает игрока в главное меню
        """

        # Запускаем окна заставки
        start_screen()

        # Включаем музыку меню
        music_menu()

        # Меняем состояние окна
        screen_change('fl_zastavka', 'fl_menu')
        transit('fl_menu')
        screen_change('fl_menu', 'transition')

        # Обновление кнопок
        self.update_button()

    def play_game(self):
        """
        Метод, который запускает игровой процесс
        """

        # Показываем экран загрузки
        loading(True)
        transit('loading_screen')
        # Меняем состояние экрана
        screen_change('settings', 'transition')
        self.update_button()

        thread = threading.Thread(target=play_game)
        thread.daemon = True
        thread.start()

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

        :param event: Событие, которое нужно обработать
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
        past_position = check('screen', 'past_position')
        transit(past_position)
        screen_change('settings', 'transition')
        self.update_button()

    def update_button(self):
        # Создание/бновление кнопок

        zn1 = 'Выключить' if check('audio', 'mute_music') else 'Включить'
        zn2 = 'Выключить' if check('audio', 'mute_sound') else 'Включить'
        self.button1 = Button(
            [80, 120, 220, 50], self.screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn1, self.onn_off_music,
            30, "data/BlackOpsOne-Regular_RUS_by_alince.otf", False
        )
        self.button2 = Button(
            [80, 320, 220, 50], self.screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn2, self.onn_off_sound,
            30, "data/BlackOpsOne-Regular_RUS_by_alince.otf", False
        )
        self.button3 = ImageButton(
            [280, 510, 240, 60], self.screen, f"images/buttons/other/back_{randint(0, 3)}.png",
            "images/buttons/other/back_0.png", self.close_seting, scale=1.0, hover_scale=1.1
        )
        self.button4 = ImageButton(
            [30, 510, 240, 60], self.screen, "images/buttons/other/restart_0.png", "images/buttons/other/restart_1.png",
            self.play_game, scale=1.0, hover_scale=1.1
        )
        self.button5 = ImageButton(
            [530, 510, 240, 60], self.screen, "images/buttons/other/menu_0.png", "images/buttons/other/menu_1.png",
            self.return_menu, scale=1.0, hover_scale=1.1
        )


class Levels_Selection:
    """
    Класс, реализующий окно выбора уровня сложности
    """

    def __init__(self, screen) -> None:
        """
        Конструктор класса, инициализирует экран, фон, текстовые элементы и списки кнопок и изображений
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'),
                                                 (800, 600))

        # Загрузка картинок
        self.image = []

        # Создание кнопок
        self.buttons = []

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
        self.creating_buttons()

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора ровня сложности
        """

        setting_value('level', '')
        transit('fl_menu')
        screen_change('levels', 'transition')
        self.creating_buttons()

    def creating_buttons(self):
        # Создание кнопок
        self.buttons = []

        # Загрузка картинок
        self.image = []

        self.image.append(
            [pygame.transform.scale(pygame.image.load(f'images/levels/easy.jpg'), (160, 280)), [90, 100]]
        )

        self.buttons.append(
            ImageButton(
                [70, 400, 200, 65], screen, "images/buttons/levels/easy_0.png", "images/buttons/levels/easy_1.png",
                card_selection_easy, scale=1.0, hover_scale=1.1
            )
        )

        if check('open_levels', 'normal'):
            img_one, img_two = f'images/buttons/levels/normal_0.png', f'images/buttons/levels/normal_1.png'
            name, k = f'images/levels/normal.jpg', 1.1
        else:
            img_one, img_two = f'images/buttons/levels/close.png', f'images/buttons/levels/close.png'
            name, k = f'images/levels/close.png', 1.0

        self.image.append(
            [pygame.transform.scale(pygame.image.load(name), (160, 280)), [90 + 220, 100]]
        )

        self.buttons.append(
            ImageButton(
                [290, 400, 200, 65], screen, img_one, img_two, card_selection_normal, scale=1.0, hover_scale=k
            )
        )

        if check('open_levels', 'hard'):
            img_one, img_two = f'images/buttons/levels/hard_0.png', f'images/buttons/levels/hard_1.png'
            name, k = f'images/levels/hard.jpg', 1.1
        else:
            img_one, img_two = f'images/buttons/levels/close.png', f'images/buttons/levels/close.png'
            name, k = f'images/levels/close.png', 1.0

        self.image.append(
            [pygame.transform.scale(pygame.image.load(name), (160, 280)), [90 + 220 * 2, 100]]
        )

        self.buttons.append(
            ImageButton(
                [510, 400, 200, 65], screen, img_one, img_two, card_selection_hard, scale=1.0, hover_scale=k
            )
        )

        self.update_button()

    def update_button(self):
        # Обновление кнопок "Назад" и "Настройки"
        self.buttons.append(
            ImageButton(
                [495, 500, 210, 50], screen, f"images/buttons/other/back_{randint(0, 3)}.png",
                "images/buttons/other/back_0.png", self.closing_window, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [75, 500, 210, 50], screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))

        # Отрисовка кнопок
        for button in self.buttons:
            button.draw()

        # Отрисовка тексат названия окна
        self.screen.blit(self.text_surface, self.text_rect)

        # Отрисовка вспомогательного текста
        self.screen.blit(self.text, self.text_r)

        # Отрисовка изображений уровней
        for i in self.image:
            self.screen.blit(i[0], i[1])

    def check_event(self, event) -> None:
        """
        Метод проверки событий

        :param event: Событие, которое нужно обработать
        """

        # Проверка событий кнопок
        for button in range(len(self.buttons)):
            if button > 2:
                self.buttons[button].handle_event(event)
            else:
                if check('open_levels', ['easy', 'normal', 'hard'][button]):
                    self.buttons[button].handle_event(event)


class Card_Selection:
    """
    Класс, реализующий окно выбора карты
    """

    def __init__(self, screen) -> None:
        """
        Конструктор класса. Инициализирует основные параметры окна, загружает фон,
        текстовые элементы и создает пустые списки для кнопок и изображений
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'),
                                                 (800, 600))

        self.card_1, self.card_2, self.card_3, self.level = None, None, None, None
        self.rating_r, self.rating = None, None
        self.rt_one, self.rt_r_one = None, None
        self.rt_two, self.rt_r_two = None, None
        self.rt_free, self.rt_r_free = None, None
        self.buttons = []

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

        # Устанавливает первую карту как выбранну
        setting_value('name_card', self.card_1)

        # Вызывает метод открытия окна выбора типа карты
        self.open_card_type()

    def card_two(self) -> None:
        """
        Метод определения, записи названия выбранной карты
        """

        # Устанавливает вторую  карту как выбранну
        setting_value('name_card', self.card_2)

        # Вызывает метод открытия окна выбора типа карты
        self.open_card_type()

    def card_three(self) -> None:
        """
        Метод определения, записи названия выбранной карты
        """

        # Устанавливает третью  карту как выбранну
        setting_value('name_card', self.card_3)

        # Вызывает метод открытия окна выбора типа карты
        self.open_card_type()

    def open_card_type(self) -> None:
        """
        Метод открытия окна выбора типа карты
        """

        transit('card_type')
        screen_change('cards', 'transition')

        # Обновление кнопок
        self.creating_buttons(self.card_1, self.card_2, self.card_3)

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('cards', 'transition')

        # Обновление кнопок
        self.creating_buttons(self.card_1, self.card_2, self.card_3)

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора карты
        """

        # Сброс выбранной карты
        setting_value('name_card', '')
        transit('levels')
        screen_change('cards', 'transition')

        # Обновление кнопок
        self.creating_buttons(self.card_1, self.card_2, self.card_3)

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        # Отображение фона
        self.screen.blit(self.background, (0, 0))

        # Отображение всех кнопок
        for button in self.buttons:
            button.draw()

        # Отображение текста - названия окна
        self.screen.blit(self.text_surface, self.text_rect)

        # Отображение вспомогательного текста
        self.screen.blit(self.text, self.text_r)

        # Отображение изображений
        for i in self.image:
            self.screen.blit(i[0], i[1])

        # Отображение текста - рейтинга
        self.screen.blit(self.rating, self.rating_r)

        # Отоюражение рейтинга каждой карты
        self.screen.blit(self.rt_one, self.rt_r_one)
        self.screen.blit(self.rt_two, self.rt_r_two)
        self.screen.blit(self.rt_free, self.rt_r_free)

    def check_event(self, event) -> None:
        """
        Метод проверки событий

        :param event: Событие, которое нужно обработать
        """

        # Проверка событий кнопок
        for button in range(len(self.buttons)):
            if button > 2:
                self.buttons[button].handle_event(event)
            else:
                if check_open_cards(self.level, [self.card_1, self.card_2, self.card_3][button]):
                    self.buttons[button].handle_event(event)

    def creating_buttons(self, name1, name2, name3) -> None:
        """
        Метод добавления кнопок
        """

        self.buttons = []

        # Запоминание названия всех карт
        self.card_1 = name1
        self.card_2 = name2
        self.card_3 = name3

        # Получение уровня сложности
        self.level = check('gameplay', 'level')

        # Далее код создания всех нужных текстов и кнопок
        font_2 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 18)
        rating = check('gameplay', 'rating')
        self.rating = font_2.render(f"Рейтинг: {rating}", True, (255, 255, 255))
        if rating < 1000:
            x = 720
        elif 1000 < rating < 10000:
            x = 712
        else:
            x = 704
        self.rating_r = self.rating.get_rect(center=(x, 20))

        self.rt_one = font_2.render(f"{rating}/{rating_cost[name1]}", True, (255, 255, 255))
        self.rt_r_one = self.rt_one.get_rect(center=(160, 400))
        self.rt_two = font_2.render(f"{rating}/{rating_cost[name2]}", True, (255, 255, 255))
        self.rt_r_two = self.rt_two.get_rect(center=(410, 400))
        self.rt_free = font_2.render(f"{rating}/{rating_cost[name3]}", True, (255, 255, 255))
        self.rt_r_free = self.rt_free.get_rect(center=(660, 400))

        self.image = []

        if check_open_cards(self.level, name1):
            img_one, img_two = f'images/buttons/cards/{name1}_0.png', f'images/buttons/cards/{name1}_1.png'
            name, k = f'images/cards/{name1}.png', 1.1
        else:
            img_one, img_two = f'images/buttons/cards/close.png', f'images/buttons/cards/close.png'
            name, k = 'images/cards/close.png', 1.0

        self.image.append(
            [pygame.transform.scale(pygame.image.load(name), (160, 280)), [80, 100]]
        )
        self.buttons.append(
            ImageButton(
                [45, 420, 230, 50], screen, img_one, img_two, self.card_one, scale=1.0, hover_scale=k
            )
        )

        if check_open_cards(self.level, name2):
            img_one, img_two = f'images/buttons/cards/{name2}_0.png', f'images/buttons/cards/{name2}_1.png'
            name, k = f'images/cards/{name2}.png', 1.1
        else:
            img_one, img_two = f'images/buttons/cards/close.png', f'images/buttons/cards/close.png'
            name, k = 'images/cards/close.png', 1.0

        self.image.append(
            [pygame.transform.scale(pygame.image.load(name), (160, 280)), [80 + 250, 100]]
        )
        self.buttons.append(
            ImageButton(
                [295, 420, 230, 50], screen, img_one, img_two, self.card_two, scale=1.0, hover_scale=k
            )
        )

        if check_open_cards(self.level, name3):
            img_one, img_two = f'images/buttons/cards/{name3}_0.png', f'images/buttons/cards/{name3}_1.png'
            name, k = f'images/cards/{name3}.png', 1.1
        else:
            img_one, img_two = f'images/buttons/cards/close.png', f'images/buttons/cards/close.png'
            name, k = 'images/cards/close.png', 1.0

        self.image.append(
            [pygame.transform.scale(pygame.image.load(name), (160, 280)), [80 + 250 * 2, 100]]
        )
        self.buttons.append(
            ImageButton(
                [545, 420, 230, 50], screen, img_one, img_two, self.card_three, scale=1.0, hover_scale=k
            )
        )

        self.update_botton()

    def update_botton(self):
        """
        Метод, который добавляет кнопки "Назад" и "Настройки" в интерфейс
        """

        # Обновление кнопок
        self.buttons.append(
            ImageButton(
                [550, 500, 210, 50], screen, f"images/buttons/other/back_{randint(0, 3)}.png",
                "images/buttons/other/back_0.png", self.closing_window, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [55, 500, 210, 50], screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )


class Card_Type:
    """
    Класс, реализующий окно выбора типа карты
    """

    def __init__(self, screen) -> None:
        """
        Метод, который нициализирует класс, загружает фон, создаёт кнопки и заголовки

        :param screen: объект экрана, на котором будет отображаться окно выбора карты.
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'), (800, 600))

        self.buttons = []
        self.update_button()

        # Создание изображений
        self.images = []
        for i in range(9):
            self.images.append(
                [pygame.image.load(f'images/tiles/{list_tiles[i]}/1.png'), [140 + 215 * (i // 3), 70 + 140 * (i % 3)]])

        # Создание текста - название окна
        font_1 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font_1.render('Card Type', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(47, 10))

        font_2 = pygame.font.Font("data/Docker.ttf", 25)
        self.text = font_2.render('Выберите тип карты', True, (255, 255, 255))
        self.text_r = self.text.get_rect(center=(400, 40))

    def update_button(self) -> None:
        """
        Метод, который создаёт и обновляет список кнопок
        """

        # Создание кнопок
        self.buttons = []

        self.buttons.append(
            ImageButton(
                [90, 430, 170, 50], self.screen, "images/buttons/tiles/choco_0.png", "images/buttons/tiles/choco_1.png",
                self.choice_choco, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [305, 430, 170, 50], self.screen, "images/buttons/tiles/grass_0.png",
                "images/buttons/tiles/grass_1.png", self.choice_grass, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [520, 430, 170, 50], self.screen, "images/buttons/tiles/snow_0.png", "images/buttons/tiles/snow_1.png",
                self.choice_snow, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(ImageButton(
            [90, 290, 170, 50], self.screen, "images/buttons/tiles/cake_0.png", "images/buttons/tiles/cake_1.png",
            self.choice_cake, scale=1.0, hover_scale=1.1
        )
        )
        self.buttons.append(
            ImageButton(
                [305, 290, 170, 50], self.screen, "images/buttons/tiles/dirt_0.png", "images/buttons/tiles/dirt_1.png",
                self.choice_dirt, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [520, 290, 170, 50], self.screen, "images/buttons/tiles/sand_0.png", "images/buttons/tiles/sand_1.png",
                self.choice_sand, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [90, 150, 170, 50], self.screen, "images/buttons/tiles/tundra_0.png",
                "images/buttons/tiles/tundra_1.png", self.choice_tundra, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [305, 150, 170, 50], self.screen, "images/buttons/tiles/castle_0.png",
                "images/buttons/tiles/castle_1.png", self.choice_castle, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [520, 150, 170, 50], self.screen, "images/buttons/tiles/purple_0.png",
                "images/buttons/tiles/purple_1.png", self.choice_purple, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [500, 500, 210, 50], self.screen, f"images/buttons/other/back_{randint(0, 3)}.png",
                "images/buttons/other/back_0.png", self.closing_window, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [65, 500, 210, 50], self.screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )

    def choice_choco(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'choco')
        self.open_character_types()

    def choice_grass(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'grass')
        self.open_character_types()

    def choice_snow(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'snow')
        self.open_character_types()

    def choice_cake(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'cake')
        self.open_character_types()

    def choice_dirt(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'dirt')
        self.open_character_types()

    def choice_sand(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'sand')
        self.open_character_types()

    def choice_tundra(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'tundra')
        self.open_character_types()

    def choice_castle(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'castle')
        self.open_character_types()

    def choice_purple(self) -> None:
        """
        Метод определения и записи выбранный тип карты
        """

        # Записываем выбранный тип карты и переходим к следующему окну
        setting_value('type_card', 'purple')
        self.open_character_types()

    def open_character_types(self) -> None:
        """
        Метод открытия окна выбора персонажа
        """

        # Переход к окну выбора персонажа
        transit('character_types')
        screen_change('card_type', 'transition')

        # Обновление кнопок
        self.update_button()

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        # Открытие окна настроек
        transit('settings')
        screen_change('card_type', 'transition')

        # Обновление кнопок
        self.update_button()

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора типа карты
        """

        # Закрытие окна выбора типа карты и возврат к предыдущему окну
        setting_value('type_card', '')
        transit('cards')
        screen_change('card_type', 'transition')

        # Обновление кнопок
        self.update_button()

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))

        # Отрисовка всех кнопок
        for button in self.buttons:
            button.draw()

        # Отрисовка текста - названия окна
        self.screen.blit(self.text_surface, self.text_rect)

        # Отрисовка вспомогательного текста
        self.screen.blit(self.text, self.text_r)

        # Отрисовка изображений
        for i in self.images:
            self.screen.blit(i[0], i[1])

    def check_event(self, event) -> None:
        """
        Метод проверки событий

        :param event: Событие, которое нужно обработать
        """

        # Проверка событий кнопок
        for button in self.buttons:
            button.handle_event(event)


class Character_Types:
    """
    Класс, реализующий окно выбора персонажа
    """

    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения

        :param screen: объект экрана для отображения
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        self.name1, self.name2, self.name3 = None, None, None
        self.rating_r, self.rating = None, None
        self.rt_one, self.rt_r_one = None, None
        self.rt_two, self.rt_r_two = None, None
        self.rt_free, self.rt_r_free = None, None
        self.button = None
        self.buttons = []

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'),
                                                 (800, 600))

        self.start = False
        self.fl = False
        self.count = 0

        # Изображения
        self.pl_image = []

        # Создание текста
        font_1 = pygame.font.Font("data/Docker.ttf", 30)
        self.text = font_1.render('Выберите персонажа', True, (255, 255, 255))
        self.text_r = self.text.get_rect(center=(400, 60))

        # Создание текста - название окна
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font.render('Character Types', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(76, 10))

    def chek_open_pl_but(self, name, fl=False) -> str:
        """
        Метод, который проверяет, открыт ли персонаж, и возвращает пути к изображениям кнопок

        :param name: имя персонажа
        :param fl: флаг для состояния кнопки
        :return: пути к изображениям кнопок и коэффициенты масштабирования
        """

        if check('open_characters', name):
            if fl:
                return f'images/buttons/characters/{name}_2.png', f'images/buttons/characters/{name}_1.png', 1.0, 1.1
            else:
                return f'images/buttons/characters/{name}_0.png', f'images/buttons/characters/{name}_1.png', 1.0, 1.1
        else:
            return f'images/buttons/characters/close.png', f'images/buttons/characters/close.png', 1.0, 1.0

    def chek_open_pl_img(self, name) -> str:
        """
        Метод, который проверяет доступность персонажа и возвращает путь к изображению

        :param name: имя персонажа
        :return: путь к изображению персонажа
        """

        if check('open_characters', name):
            return f'open/{name}'
        else:
            return f'close/{randint(0, 2)}'

    def player_one(self) -> None:
        """
        Метод выбора первого персонажа, обновления кнопок
        """

        # Добавление имени выбраннного персонажа
        setting_value('character', self.name1)
        self.start = True

        # Очистка от старых кнопок
        self.buttons = []

        # Добавление кнопок
        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name1, True)
        self.buttons.append(
            ImageButton(
                [40, 420, 240, 50], screen, img_one, img_two, self.player_one, scale=k1, hover_scale=k2
            )
        )

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name2)
        self.buttons.append(
            ImageButton(
                [290, 420, 240, 50], screen, img_one, img_two, self.player_two, scale=k1, hover_scale=k2
            )
        )

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name3)
        self.buttons.append(
            ImageButton(
                [540, 420, 240, 50], screen, img_one, img_two, self.player_three, scale=k1, hover_scale=k2
            )
        )

        self.fl = True

        # Обновление кнопок
        self.update_button()

    def player_two(self) -> None:
        """
        Метод выбора второго  персонажа, обновления кнопок
        """

        # Добавление имени выбраннного персонажа
        setting_value('character', self.name2)
        self.start = True

        # Очистка от старых кнопок
        self.buttons = []

        # Добавление кнопок
        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name1)
        self.buttons.append(
            ImageButton(
                [40, 420, 240, 50], screen, img_one, img_two, self.player_one, scale=k1, hover_scale=k2
            )
        )

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name2, True)
        self.buttons.append(
            ImageButton(
                [290, 420, 240, 50], screen, img_one, img_two, self.player_two, scale=k1, hover_scale=k2
            )
        )

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name3)
        self.buttons.append(
            ImageButton(
                [540, 420, 240, 50], screen, img_one, img_two, self.player_three, scale=k1, hover_scale=k2
            )
        )

        self.fl = True

        # Обновление кнопок
        self.update_button()

    def player_three(self) -> None:
        """
        Метод выбора третьего  персонажа, обновления кнопок
        """

        # Добавление имени выбраннного персонажа
        setting_value('character', self.name3)
        self.start = True

        # Очистка от старых кнопок
        self.buttons = []

        # Добавление кнопок
        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name1)
        self.buttons.append(
            ImageButton(
                [40, 420, 240, 50], screen, img_one, img_two, self.player_one, scale=k1, hover_scale=k2
            )
        )

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name2)
        self.buttons.append(
            ImageButton(
                [290, 420, 240, 50], screen, img_one, img_two, self.player_two, scale=k1, hover_scale=k2
            )
        )

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name3, True)
        self.buttons.append(
            ImageButton(
                [540, 420, 240, 50], screen, img_one, img_two, self.player_three, scale=k1, hover_scale=k2
            )
        )

        self.fl = True

        # Обновление кнопок
        self.update_button()

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('character_types', 'transition')

        # Обновление кнопок
        self.update_button()

    def play_game(self) -> None:
        """
        Запуск загрузки
        """

        transit('loading_screen')
        screen_change('character_types', 'transition')
        loading(True)

        thread = threading.Thread(target=play_game)
        thread.daemon = True
        thread.start()

        # Обновление кнопок
        self.rollback()

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора персонажа
        """

        setting_value('character', '')
        transit('card_type')
        screen_change('character_types', 'transition')

        self.start = False
        self.rollback()

    def open_info_pl_one(self) -> None:
        """
        Метод открытия окна информации о первом персонаже
        """

        player_inform(self.name1)
        transit('info_player')
        screen_change('character_types', 'transition')

    def open_info_pl_two(self) -> None:
        """
        Метод открытия окна информации о втором персонаже
        """

        player_inform(self.name2)
        transit('info_player')
        screen_change('character_types', 'transition')

    def open_info_pl_three(self) -> None:
        """
        Метод открытия окна информации о третьем персонаже
        """

        player_inform(self.name3)
        transit('info_player')
        screen_change('character_types', 'transition')

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        # Обновление счётчика кадров
        self.count += 1
        if self.count > 30:
            self.count, self.fl = 0, True

        # Отбражение фона
        self.screen.blit(self.background, (0, 0))

        # Отбражение всех кнопок
        for button in self.buttons:
            button.draw()

        # Отбражение кнопки начала игры, если персонаж выбран
        if self.start and self.fl:
            self.button.draw()

        # Отбражение текста - название окна
        self.screen.blit(self.text_surface, self.text_rect)

        # Отбражение текста
        self.screen.blit(self.text, self.text_r)

        # Отбражение изображений персонажей
        for i in range(len(self.pl_image)):
            size = self.pl_image[i].get_size()
            self.screen.blit(self.pl_image[i], (40 + 250 * i + ((240 - size[0]) // 2), 170))

        # Отбражение рейтинга
        self.screen.blit(self.rating, self.rating_r)

        # Отбражение текста рейтинга открытия персонажей
        self.screen.blit(self.rt_one, self.rt_r_one)
        self.screen.blit(self.rt_two, self.rt_r_two)
        self.screen.blit(self.rt_free, self.rt_r_free)

    def check_event(self, event) -> None:
        """
        Метод проверки событий

        :param event: Событие, которое нужно обработать
        """

        # Проверка событий кнопок
        for button in range(len(self.buttons)):
            if button > 5:
                self.buttons[button].handle_event(event)
            else:
                if check('open_characters', [self.name1, self.name2, self.name3][button % 3]):
                    self.buttons[button].handle_event(event)

        if self.start:
            self.button.handle_event(event)

    def creating_buttons(self, name1, name2, name3) -> None:
        """
        Метод добавления кнопок

        :param name1: имя первого персонажа
        :param name2: имя второго персонажа
        :param name3: имя третьего персонажа
        """

        # Сохранение названия игроков
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3

        self.rollback()

    def rollback(self) -> None:
        """
        Метод, который сбрасывает интерфейс, создавая кнопки заново
        """

        # Создание кнопок
        self.buttons = []

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name1)
        self.buttons.append(
            ImageButton(
                [40, 420, 240, 50], screen, img_one, img_two, self.player_one, scale=k1, hover_scale=k2
            )
        )

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name2)
        self.buttons.append(
            ImageButton(
                [290, 420, 240, 50], screen, img_one, img_two, self.player_two, scale=k1, hover_scale=k2
            )
        )

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name3)
        self.buttons.append(
            ImageButton(
                [540, 420, 240, 50], screen, img_one, img_two, self.player_three, scale=k1, hover_scale=k2
            )
        )

        # Создание изображений персонажей
        self.pl_image = []

        self.pl_image.append(
            pygame.image.load(f'images/players/{self.chek_open_pl_img(self.name1)}.png').convert_alpha()
        )
        self.pl_image.append(
            pygame.image.load(f'images/players/{self.chek_open_pl_img(self.name2)}.png').convert_alpha()
        )
        self.pl_image.append(
            pygame.image.load(f'images/players/{self.chek_open_pl_img(self.name3)}.png').convert_alpha()
        )

        self.start = False
        self.fl = False
        self.count = 0

        # Обновление кнопок
        self.update_button()

    def update_button(self) -> None:
        """
        Метод обновления кнопок и текста на экране
        """

        # Обновление кнопок
        font_2 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 18)
        rating = check('gameplay', 'rating')
        self.rating = font_2.render(f"Рейтинг: {rating}", True, (255, 255, 255))
        if rating < 1000:
            x = 720
        elif 1000 < rating < 10000:
            x = 712
        else:
            x = 704
        self.rating_r = self.rating.get_rect(center=(x, 20))

        self.rt_one = font_2.render(f"{rating}/{rating_character[self.name1]}", True, (255, 255, 255))
        self.rt_r_one = self.rt_one.get_rect(center=(110, 395))
        self.rt_two = font_2.render(f"{rating}/{rating_character[self.name2]}", True, (255, 255, 255))
        self.rt_r_two = self.rt_two.get_rect(center=(360, 395))
        self.rt_free = font_2.render(f"{rating}/{rating_character[self.name3]}", True, (255, 255, 255))
        self.rt_r_free = self.rt_free.get_rect(center=(610, 395))

        if check('open_characters', self.name1):
            col1, col2 = (200, 150, 0), (150, 0, 0)
        else:
            col1, col2 = (120, 120, 120), (120, 120, 120)
        self.buttons.append(
            Button(
                [200, 385, 80, 22], screen, (255, 255, 255), col1, col2, 'info', self.open_info_pl_one, 15,
                "data/BlackOpsOne-Regular_RUS_by_alince.otf"
            )
        )

        if check('open_characters', self.name2):
            col1, col2 = (210, 150, 0), (150, 0, 0)
        else:
            col1, col2 = (120, 120, 120), (120, 120, 120)
        self.buttons.append(
            Button(
                [450, 385, 80, 22], screen, (255, 255, 255), col1, col2, 'info', self.open_info_pl_two, 15,
                "data/BlackOpsOne-Regular_RUS_by_alince.otf"
            )
        )

        if check('open_characters', self.name3):
            col1, col2 = (200, 150, 0), (150, 0, 0)
        else:
            col1, col2 = (120, 120, 120), (120, 120, 120)
        self.buttons.append(
            Button(
                [700, 385, 80, 22], screen, (255, 255, 255), col1, col2, 'info', self.open_info_pl_three, 15,
                "data/BlackOpsOne-Regular_RUS_by_alince.otf"
            )
        )

        self.buttons.append(
            ImageButton(
                [550, 500, 210, 50], screen, f"images/buttons/other/back_{randint(0, 3)}.png",
                "images/buttons/other/back_0.png", self.closing_window, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [55, 500, 210, 50], screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )
        self.button = ImageButton(
            [290, 490, 240, 70], screen, "images/buttons/other/start_game_0.png",
            "images/buttons/other/start_game_1.png", self.play_game, scale=1.0, hover_scale=1.1
        )


class LoadingScreen:
    """
    Класс, реализующий окно загрузки
    """

    def __init__(self, screen) -> None:
        """
        Инициализация атрибутов класса и загрузка фона экрана

         :param screen: Экран, на котором будет отображаться окно загрузки
        """

        self.screen = screen

        self.progress = None
        self.rotation, self.message, self.font, self.clock, self.step, self.fl = None, None, None, None, None, None

        # Создание фона
        self.background = pygame.transform.scale(
            pygame.image.load('images/background/background_loading.jpg'), (800, 600)
        )

        self.pl_music = True

    def draw(self) -> None:
        """
        Метод отображения окна загрузки
        """

        # Отображение фона
        self.screen.blit(self.background, (0, 0))

        # Отображение текстового индикатора загрузки
        text_surface = self.font.render(self.message, True, (255, 215, 0))
        text_rect = text_surface.get_rect(center=(400, 250))
        self.screen.blit(text_surface, text_rect)

        # Анимация вращающейся точки
        radius = 20
        angle = radians(self.rotation)
        x = int(400 + radius * cos(angle))
        y = int(300 + radius * sin(angle))
        pygame.draw.circle(self.screen, (210, 105, 30), (x, y), 10)

        # Отображение полосы загрузки
        bar_x = 200
        bar_y = 350
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, 400, 22), 3)
        fill_width = int(400 * self.progress)
        pygame.draw.rect(self.screen, (255, 215, 0), (bar_x, bar_y, fill_width, 22))

    def update(self) -> None:
        """
        Метод, который обновляет состояние экрана загрузки
        """

        # Начинает проигрывать музыку загрузки при открытии окна
        if self.pl_music:
            pygame.mixer.music.load('data/file_music/loading.mp3')
            pygame.mixer.music.set_volume(check('audio', 'music_volume'))
            pygame.mixer.music.play(-1)
            self.pl_music = False

        # Обновление прогресса загрузки
        self.progress = self.step / 20
        self.message = f"Loading... ({int(self.progress * 100)}%)"

        # Анимированние вращающегося элемента
        self.rotation += randint(10, 60)
        if self.rotation >= 360:
            self.rotation = 0

        sleep(0.03)
        self.step += randint(1, 2)
        # Определение момента завершения загрузки, опсле чего выполняется переход на следующий экран
        if self.step > 20 and self.fl:
            pygame.mixer.music.stop()
            play_musik()
            transit('gemplay')
            screen_change('loading_screen', 'transition')
        elif self.step > 20 and not self.fl:
            music_menu()
            transit(check('screen', 'past_position'))
            screen_change('loading_screen', 'transition')

        self.draw()

    def initial_update(self, fl) -> None:
        """
        Метод, который обновляет параметры окна загрузки

        :param fl: Флаг, который определяет, какой экран будет загружен после завершения загрузки
        """

        self.pl_music = True
        self.progress = 0.0
        self.rotation = 0
        self.message = "Loading..."
        self.font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 40)
        self.clock = pygame.time.Clock()
        self.step = 0
        self.fl = fl


class ImageButton:
    """
    Класс, реализующий кнопку с изображением
    """

    def __init__(self, coord, screen, image_path, hover_image_path, funk, scale=1.0, hover_scale=1.2) -> None:
        """
        Конструктор: инициализирует кнопку, загружает изображения,
        задает начальные размеры и подготавливает её к отрисовке

        :param coord: Кортеж, содержащий координаты кнопки (x, y) и её размеры (width, height)
        :param screen: Экран, на котором будет отображаться кнопка
        :param image_path: Путь к изображению кнопки в обычном состоянии
        :param hover_image_path: Путь к изображению кнопки при наведении
        :param funk: Функция, которая будет вызвана при нажатии на кнопку
        :param scale: Масштаб кнопки в обычном состоянии (по умолчанию 1.0)
        :param hover_scale: Масштаб кнопки при наведении (по умолчанию 1.2)
        """

        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), coord[2:])
        self.hover_image = pygame.image.load(hover_image_path).convert_alpha()

        # Функция для вызова при нажатии
        self.funk = funk

        self.scale = scale
        self.hover_scale = hover_scale
        self.current_image = self.image

        # Изначальный rect на основе исходного изображения
        self.rect = self.current_image.get_rect(topleft=coord[:2])
        self.original_width = self.rect.width
        self.original_height = self.rect.height
        self.is_hovered = False

        # Первоначальное масштабирование
        self.update_image()

    def update_image(self) -> None:
        """
        Обновляет изображение и rect в соответствии с текущим масштабом
        """

        scale = self.hover_scale if self.is_hovered else self.scale
        width = int(self.original_width * scale)
        height = int(self.original_height * scale)
        image = self.hover_image if self.is_hovered else self.image
        self.current_image = pygame.transform.scale(image, (width, height))

        # Обновляем rect, сохраняя центр кнопки на месте
        center = self.rect.center
        self.rect = self.current_image.get_rect(center=center)

    def draw(self) -> None:
        """
        Метод отрисовки кнопки
        """

        self.screen.blit(self.current_image, self.rect)

    def handle_event(self, event) -> None:
        """
        Метод, который обрабатывает события, связанные с кнопкой

        :param event: Событие, которое нужно обработать
        """

        if event.type == pygame.MOUSEMOTION:
            # Проверка пересечения области кнопки и позиции мыши
            if self.rect.collidepoint(event.pos):
                if not self.is_hovered:
                    self.is_hovered = True

                    # Обновляем изображение при наведении
                    self.update_image()
            else:
                if self.is_hovered:
                    self.is_hovered = False

                    # Возвращаем исходное изображение
                    self.update_image()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка нажатия на кнопку
            if self.is_hovered and self.funk:
                # Вызов функции
                self.funk()

                # Загрузка звука нажатия кнопки
                sound = pygame.mixer.Sound("data/file_music/button_sound.mp3")
                sound.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)

                # Проигрыш звука нажатия кнопки
                sound.play()


class Button:
    """
    Класс реализующий кнопку
    """

    def __init__(self, coord, screen, collor_text, hover_color, collor_button, text, funk, zn, font="data/Docker.ttf",
                 fl=True, scale=1.0, hover_scale=1.1) -> None:
        """
        Инициализирует новый объект кнопки с заданными параметрами

        :param coord: Кортеж, содержащий координаты и размеры кнопки (x, y, width, height)
        :param screen: Экран, на котором будет отображаться кнопка
        :param collor_text: Цвет текста кнопки в формате RGB
        :param hover_color: Цвет фона кнопки при наведении
        :param collor_button: Цвет фона кнопки в обычном состоянии
        :param text: Текст, отображаемый на кнопке
        :param funk: Функция, которая будет вызвана при нажатии на кнопку
        :param zn: Размер шрифта для текста на кнопке
        :param font: Путь к файлу шрифта, который будет использоваться для текста на кнопке
        :param fl: Флаг, определяющий, отслеживаем ли мы наведение мыши (по умолчанию True)
        :param scale: Масштаб кнопки в обычном состоянии (по умолчанию 1.0)
        :param hover_scale: Масштаб кнопки при наведении (по умолчанию 1.1)
        """

        # Задаём координаты
        self.original_rect = pygame.Rect(coord)

        # rect для текущего состояния (с учетом масштаба)
        self.rect = self.original_rect.copy()

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
        self.font_name = font  # Сохраняем имя шрифта

        # Сохраняем размер шрифта
        self.font_size = zn

        # Создаем шрифт
        self.font = pygame.font.Font(font, zn)

        # Реализация текста для кнопки
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.collor_text)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        # Флаг, показывающий находится ли курсор на кнопке
        self.hove = False

        # Изначальный масштаб
        self.scale = scale

        # Масштаб при наведении
        self.hover_scale = hover_scale

        # Применяем начальный масштаб
        self.update_scale()

    def update_font(self) -> None:
        """
        Обновляет шрифт и текстовую поверхность с учетом масштаба
        """

        self.font = pygame.font.Font(self.font_name,
                                     int(self.font_size * (self.hover_scale if self.hove else self.scale)))
        self.text_surface = self.font.render(self.text, True, self.collor_text)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def update_scale(self) -> None:
        """
        Обновляет размер кнопки с учетом масштаба
        """

        scale = self.hover_scale if self.hove else self.scale
        width = int(self.original_rect.width * scale)
        height = int(self.original_rect.height * scale)

        # Сохраняем центр
        center = self.rect.center

        # Создаем новый rect
        self.rect = pygame.Rect(0, 0, width, height)

        # Восстанавливаем центр
        self.rect.center = center

        # Обновляем шрифт при изменении размера
        self.update_font()

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
        Метод, который обрабатывает события, связанные с кнопкой

        :param event: Событие, которое нужно обработать
        """

        # Проверяет тип события (наведения на кнопку курсора)
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if not self.hove:
                    self.hove = True

                    # Обновляем размер
                    self.update_scale()

            else:
                if self.hove:
                    self.hove = False

                    # Возвращаем размер
                    self.update_scale()

        # Проверяет тип события (нажатия на кнопку курсором)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hove and self.funk:
                sound = pygame.mixer.Sound("data/file_music/button_sound.mp3")
                sound.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)
                sound.play()
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
            self.update_font()  # Обновляем текст
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        # При тексте "Включить" на кнопке он заменяется на "Выключить"
        elif self.text == 'Включить':
            self.text = 'Выключить'
            self.update_font()  # Обновляем текст
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)


class Slider:
    """
    Класс слайдера
    """

    def __init__(self, screen, coord, min_value, max_value, start_value, name) -> None:
        """
        Инициализирует новый слайдер с заданными параметрами

        :param screen: Экран, на котором будет отображаться слайдер
        :param coord: Кортеж из четырех чисел (x, y, width, height), определяющих положение и размеры слайдера
        :param min_value: Минимальное значение слайдера
        :param max_value: Максимальное значение слайдера
        :param start_value: Начальное значение слайдера
        :param name: Название слайдера
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
        Отрисовывает слайдер и его ползунок на экране

        Этот метод рисует два элемента: сам слайдер и его ползунок, используя методы отрисовки Pygame
        """

        # Отрисовка слайдера
        pygame.draw.rect(self.screen, (150, 150, 150), self.slider_rect)

        # Отрисовка ползунка слайдера
        pygame.draw.rect(self.screen, (200, 200, 200), self.cursor_rect)

    def handle_event(self, event) -> None:
        """
        Обрабатывает события взаимодействия с мышью, такие как нажатие, отпускание и перемещение

        :param event: Событие, которое нужно обработать
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


class Improvement_character:
    """
    Класс окна улучшения персонажа
    """

    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        self.text1, self.text_r1, self.text2, self.text_r2 = None, None, None, None
        self.text3, self.text_r3, self.text4, self.text_r4 = None, None, None, None
        self.text5, self.text_r5 = None, None

        self.number_coins, self.number_coins_r = None, None
        self.damage, self.hp, self.delay = None, None, None
        self.character, self.price = None, None
        self.fl_lack_coins = None
        self.image = None
        self.fl = None

        # Создание текста - название окна
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font.render('Improvement', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(65, 10))

        self.img_coin = pygame.transform.scale(pygame.image.load('images/coin/0.png'), (32, 32))

        self.screen = screen
        self.buttons = []

    def draw(self) -> None:
        """
        Метод отрисовки окна улучшения
        """

        # Заливка фона чёрным
        self.screen.fill((0, 0, 0))

        # Отображение всех кнопок
        for button in self.buttons:
            button.draw()

        # Отображение текста
        self.screen.blit(self.text1, self.text_r1)
        self.screen.blit(self.text2, self.text_r2)
        self.screen.blit(self.text3, self.text_r3)

        self.screen.blit(self.text4, self.text_r4)

        # Отрисовка изображения монеты
        self.screen.blit(self.img_coin, (8, 25))

        # Отрисовка количество монет
        self.screen.blit(self.number_coins, self.number_coins_r)

        # Отображение изображения персонажа
        self.screen.blit(self.image, (275 + (250 - self.image.get_width()) // 2, 122))

        # Отображение рамки вокруг картинки
        pygame.draw.rect(
            self.screen, (0, 255, 255), [275, 100, 250, 250], 5
        )

        # Отображение текста
        if self.fl_lack_coins:
            self.screen.blit(self.text5, self.text_r5)

        # Отображение текста - названия окна
        self.screen.blit(self.text_surface, self.text_rect)

    def update_button(self, name_character) -> None:
        """
        Метод агрузки изображения персонажа и создания кнопок улучшения

        :param name_character: Имя выбранного персонажа
        """

        # Очистка списка кнопок
        self.buttons = []
        self.character = name_character

        self.image = pygame.image.load(f'images/players/open/{name_character}.png')

        # Открытие data/characteristics_character/name_character.txt в режиме чтения
        with open(f'data/characteristics_character/{name_character}.txt', 'r', encoding='utf8') as file:
            # Загрузка данных из файла txt
            data = file.read().split('\n')

        self.damage, self.hp, self.delay = int(data[1]), int(data[0]), int(data[4])
        self.fl = [True, True, True]

        self.price = level_improvement[character_level[name_character]]

        # Создание кнопок
        self.buttons.append(
            ImageButton(
                [50, 410, 200, 50], screen, f"images/buttons/price/price_{self.price}_0.png",
                f"images/buttons/price/price_{self.price}_1.png", self.improvement_damage, scale=1.0,
                hover_scale=1.1
            )
        )

        self.buttons.append(
            ImageButton(
                [300, 410, 200, 50], screen, f"images/buttons/price/price_{self.price}_0.png",
                f"images/buttons/price/price_{self.price}_1.png", self.improvement_hp, scale=1.0, hover_scale=1.1
            )
        )

        self.buttons.append(
            ImageButton(
                [550, 410, 200, 50], screen, f"images/buttons/price/price_{self.price}_1.png",
                f"images/buttons/price/price_{self.price}_1.png", self.improvement_delay, scale=1.0,
                hover_scale=1.1
            )
        )

        self.buttons.append(
            ImageButton(
                [550, 500, 210, 50], screen, f"images/buttons/other/back_{randint(0, 3)}.png",
                "images/buttons/other/back_0.png", self.closing_window, scale=1.0, hover_scale=1.1
            )
        )

        self.buttons.append(
            ImageButton(
                [40, 500, 210, 50], screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )

        # Обновление текста
        self.update_text()

    def update_text(self) -> None:
        """
        Метод обновления текста окна
        """

        data = self.read_data()

        self.fl_lack_coins = False

        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 20)

        # Создание текста - количество монет на данный момент
        self.number_coins = font.render(f'{check("gameplay", "coins")}', True, (255, 255, 255))
        self.number_coins_r = self.number_coins.get_rect(topleft=(43, 30))

        # Изменение кнопок, если макчимальные характеристики и вывод текста при нехватке монет
        max_damage = maximum_improvement[self.character]['damage']
        if self.damage >= max_damage:
            self.buttons[0] = ImageButton(
                [50, 410, 200, 50], screen, f"images/buttons/price/max.png", f"images/buttons/price/max.png",
                self.improvement_damage, scale=1.1, hover_scale=1.1
            )
            self.fl[0] = False
        self.text1 = font.render(f"Урон: {data[1]}", True, (255, 255, 255))
        self.text_r1 = self.text1.get_rect(center=(150, 390))

        max_hp = maximum_improvement[self.character]['hp']
        if self.hp >= max_hp:
            self.buttons[1] = ImageButton(
                [300, 410, 200, 50], screen, f"images/buttons/price/max.png", f"images/buttons/price/max.png",
                self.improvement_hp, scale=1.1, hover_scale=1.1
            )
            self.fl[1] = False
        self.text2 = font.render(f"Здоровье: {data[0]}", True, (255, 255, 255))
        self.text_r2 = self.text2.get_rect(center=(400, 390))

        max_delay = maximum_improvement[self.character]['delay']
        if self.delay <= max_delay:
            self.buttons[2] = ImageButton(
                [550, 410, 200, 50], screen, f"images/buttons/price/max.png", f"images/buttons/price/max.png",
                self.improvement_delay, scale=1.1, hover_scale=1.1
            )
            self.fl[2] = False

        self.text3 = font.render(f'Перезарядка: {"{:.2f}".format(int(data[4]) / 60)}', True, (255, 255, 255))
        self.text_r3 = self.text3.get_rect(center=(650, 390))

        font1 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 30)
        self.text4 = font1.render(f"Прокачка {character_genitive[self.character]}", True, (200, 0, 200))
        self.text_r4 = self.text4.get_rect(center=(400, 50))

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора типа карты
        """

        setting_value('improvement_character', '')
        transit('info_player')
        screen_change('improvement_character', 'transition')

        # Обновление текстак характеристик окна тнформации
        update_text_info(self.character)

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('improvement_character', 'transition')

        # Обновление кнопок
        self.update_button(self.character)

    def improvement_damage(self) -> None:
        """
        Метод улучшения црона персонажа
        """

        max_damage = maximum_improvement[self.character]['damage']

        if check('gameplay', 'coins') >= self.price:
            self.fl_lack_coins = False
            if self.damage < max_damage:
                data = self.read_data()
                self.damage += 1
                data[1] = self.damage
                self.write_data([str(i) + '\n' for i in data[:-1]] + [data[-1]])
                self.subtraction()

                self.update_text()
        else:
            self.fl_lack_coins = True
            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 25)
            self.text5 = font.render(f"Недостаточно монет!", True, (randint(0, 255), randint(0, 255), randint(0, 255)))
            self.text_r5 = self.text5.get_rect(center=(400, 480))

    def improvement_hp(self):
        max_hp = maximum_improvement[self.character]['hp']

        if check('gameplay', 'coins') >= self.price:
            self.fl_lack_coins = False
            if self.hp < max_hp:
                data = self.read_data()
                self.hp += 1
                data[0] = str(self.hp)
                self.write_data([str(i) + '\n' for i in data[:-1]] + [data[-1]])
                self.subtraction()

                self.update_text()
        else:
            self.fl_lack_coins = True
            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 25)
            self.text5 = font.render(f"Недостаточно монет!", True, (randint(0, 255), randint(0, 255), randint(0, 255)))
            self.text_r5 = self.text5.get_rect(center=(400, 480))

    def improvement_delay(self) -> None:
        max_delay = maximum_improvement[self.character]['delay']

        if check('gameplay', 'coins') >= self.price:
            self.fl_lack_coins = False
            if self.delay > max_delay:
                data = self.read_data()
                self.delay -= 1
                data[4] = self.delay
                self.write_data([str(i) + '\n' for i in data[:-1]] + [str(data[-1])])
                self.subtraction()

                self.update_text()
        else:
            self.fl_lack_coins = True
            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 25)
            self.text5 = font.render(f"Недостаточно монет!", True, (randint(0, 255), randint(0, 255), randint(0, 255)))
            self.text_r5 = self.text5.get_rect(center=(400, 480))

    def subtraction(self) -> None:
        with open('data/data.json', 'r', encoding='utf8') as file:
            data = json.load(file)

        data['gameplay']['coins'] -= 1

        with open('data/data.json', 'w', encoding='utf8') as file:
            json.dump(data, file, indent=2)

    def read_data(self) -> list:
        with open(f'data/characteristics_character/{self.character}.txt', 'r', encoding='utf8') as file:
            data = file.read().split('\n')

        return data

    def write_data(self, data) -> None:
        with open(f'data/characteristics_character/{self.character}.txt', 'w', encoding='utf8') as file:
            file.writelines(data)

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        for button in range(len(self.buttons)):
            if button < 3:
                if self.fl[button]:
                    self.buttons[button].handle_event(event)
            else:
                self.buttons[button].handle_event(event)


class ScreenTransition:
    """
    Класс для создания эффекта перехода (затемнения) экрана
    """

    def __init__(self, screen) -> None:
        """
        Конструктор класса
        Инициализирует параметры для создания эффекта затемнения на экране

        :param screen: Объект экрана, на котором будет отображаться эффект затемнения
        """

        # Сохранение экрана, на котором будет отображаться эффект
        self.screen = screen

        # Цвет затемнения (черный)
        self.collor = (0, 0, 0)

        # Создание поверхности для затемнения с учетом размеров экрана
        self.scren = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        # Начальная прозрачность (0 = полностью прозрачный, 255 = полностью непрозрачный)
        self.alpha = 0

        # Начальная позиция для перехода (будет обновляться)
        self.pos = None

        # Счетчик, необходимый для контроля времени выполнения эффекта
        self.n = 0

    def draw(self) -> None:
        """
        Отображает эффект затемнения на экране
        Каждое обновление увеличивает уровень прозрачности, создавая эффект затемнения
        После 30 кадров переход завершается, и экран переключается на новый
        """

        # Увеличение счетчика кадров
        self.n += 1

        # Если прошло 30 кадров, завершаем переход
        if self.n >= 30:
            self.close()

        # Увеличиваем прозрачность
        self.alpha += 2

        # Заполняем поверхность с затемнением цветом (черный с увеличивающейся прозрачностью)
        self.scren.fill((*self.collor, self.alpha))

        # Отображаем затемнение на экране
        self.screen.blit(self.scren, (0, 0))

    def close(self) -> None:
        """
        Закрывает эффект перехода и запускает следующий экран
        Когда эффект завершен, вызывается изменение экрана с помощью функции `screen_change`
        """

        # Выполняет переход на новый экран (согласно заданной позиции)
        screen_change('transition', self.pos)

    def new_pos(self, new_pos) -> None:
        """
        Обновляет позицию для следующего экрана при переходе
        Это метод позволяет задавать новую цель для перехода

        :param new_pos: Название нового экрана или сцены, на которую необходимо переключиться
        """

        # Сброс состояния затемнения для нового перехода
        self.alpha = 0
        self.n = 0

        # Устанавливаем новую позицию для перехода
        self.pos = new_pos


class Reset_confirmation:
    """
    Класс для отображения окна подтверждения сброса настроек игры
    """

    def __init__(self, screen) -> None:
        """
        Конструктор класса. Инициализирует экран и кнопки,
        а также создает текстовое содержание для окна подтверждения сброса

        :param screen: Экран, на котором будет отображаться окно подтверждения сброса
        """

        # Сохранение экрана, на котором будет отображаться окно
        self.screen = screen

        # Инициализация кнопок (будут созданы позже)
        self.button1, self.button2 = None, None

        # Создание текста для окна подтверждения
        font1 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 30)
        self.text1 = font1.render(f'Вы действительно хотите сбросить', True, (0, 255, 255))
        self.text_r1 = self.text1.get_rect(center=(400, 150))

        self.text2 = font1.render(f'настройки игры?', True, (255, 255, 0))
        self.text_r2 = self.text2.get_rect(center=(400, 185))

        font2 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 20)
        self.text3 = font2.render(f'(все ваши достижения и результаты удаляются)', True, (140, 40, 230))
        self.text_r3 = self.text3.get_rect(center=(400, 235))

        # Обновление кнопок
        self.update_button()

    def draw(self) -> None:
        """
        Метод для отрисовки окна подтверждения сброса настроек
        """

        # Заполнение фона черным цветом
        self.screen.fill((0, 0, 0))

        # Отображение кнопок
        self.button1.draw()
        self.button2.draw()

        # Отображение текстов
        self.screen.blit(self.text1, self.text_r1)
        self.screen.blit(self.text2, self.text_r2)
        self.screen.blit(self.text3, self.text_r3)

    def update_button(self) -> None:
        """
        Метод для создания и обновления кнопок на экране
        """

        # Создание кнопки "Да"
        self.button1 = ImageButton(
            [500, 400, 200, 80], self.screen, 'images/buttons/other/yes_0.png', 'images/buttons/other/yes_1.png',
            self.update, scale=1.0, hover_scale=1.1
        )

        # Создание кнопки "Нет"
        self.button2 = ImageButton(
            [100, 400, 200, 80], self.screen, 'images/buttons/other/no_0.png', 'images/buttons/other/no_1.png',
            self.close_window, scale=1.0, hover_scale=1.1
        )

    def update(self) -> None:
        """
        Метод для выполнения сброса настроек игры (сброс всех достижений и результатов)
        """

        # Выполняет сброс игры
        factory_reset()

    def close_window(self) -> None:
        """
        Метод для закрытия окна подтверждения сброса и перехода к главному меню
        """

        # Переход к главному меню
        transit('fl_menu')
        screen_change('reset_confirmation', 'transition')

        # Обновление кнопок
        self.update_button()

    def check_event(self, event) -> None:
        """
        Метод для обработки событий, связанных с нажатием на кнопки

        :param event: Событие, которое нужно обработать
        """

        # Обработка событий для кнопок
        self.button1.handle_event(event)
        self.button2.handle_event(event)


class Results:
    """
    Класс для отображения результатов игры, включая таблицу лучших карт и времени
    """

    def __init__(self, screen) -> None:
        """
        Конструктор класса. Инициализирует экран и все элементы, такие как кнопки и текстовые поля

        :param screen: Экран, на котором будет отображаться окно с результатами
        """

        self.screen = screen

        # Инициализация кнопки и списков для названий карт и времен
        self.button = None
        self.list_time, self.list_name_card = [], []
        self.text1, self.text2, self.text3, self.text4 = None, None, None, None
        self.text_r1, self.text_r2, self.text_r3, self.text_r4 = None, None, None, None
        self.text5, self.text6 = None, None
        self.text_r5, self.text_r6 = None, None

        # Обновление кнопки и данных
        self.update_button()

    def update_button(self) -> None:
        """
        Метод для создания и обновления кнопки и текстовых элементов
        """

        self.button = ImageButton(
            [550, 500, 210, 50], self.screen, f"images/buttons/other/back_{randint(0, 3)}.png",
            "images/buttons/other/back_0.png", self.closing_window, scale=1.0, hover_scale=1.1
        )

        font1 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 25)
        self.list_name_card = []
        y = 100
        for i in list_name_card:
            text = font1.render(i, True, (randint(0, 255), randint(0, 255), randint(0, 255)))
            text_r = text.get_rect(center=(200, y))
            y += 45
            self.list_name_card.append([text, text_r])

        self.text1 = font1.render('Названия карт', True, (255, 255, 255))
        self.text_r1 = self.text1.get_rect(center=(200, 55))

        self.text2 = font1.render('Наилучшее время', True, (255, 255, 255))
        self.text_r2 = self.text2.get_rect(center=(600, 55))

        self.text3 = font1.render('Лучший рейтинг:', True, (255, 255, 255))
        self.text_r3 = self.text3.get_rect(center=(150, 510))

        with open('data/better_time.txt', 'r', encoding='utf8') as file:
            data = file.read().split('\n')
            rat = data[0]
            data_time = data[1:]

        self.text4 = font1.render(rat, True, (255, 215, 0))
        self.text_r4 = self.text4.get_rect(topleft=(280, 495))

        self.text5 = font1.render('Текущий рейтинг:', True, (255, 255, 255))
        self.text_r5 = self.text5.get_rect(center=(150, 540))

        self.text6 = font1.render(str(check('gameplay', 'rating')), True, (255, 215, 0))
        self.text_r6 = self.text6.get_rect(topleft=(280, 525))

        self.list_time = []
        y = 100
        for i in data_time:
            if i != '-':
                if int(i) < 3600:
                    time = f'{int(i) // 60}сек'
                elif int(i) < 216000:
                    time = f'{int(i) // 3600}мин {int(i) % 3600 // 60}сек'
                else:
                    time = f'{int(i) // 216000}ч {int(i) % 216000 // 3600}мин {int(i) % 216000 % 3600 // 60}сек'
            else:
                time = '-'
            text = font1.render(time, True, (0, 255, 255))
            text_r = text.get_rect(center=(600, y))
            y += 45
            self.list_time.append([text, text_r])

    def draw(self) -> None:
        """
        Метод для отрисовки экрана с результатами
        """

        self.screen.fill((0, 0, 0))
        self.button.draw()

        for card in self.list_name_card:
            self.screen.blit(card[0], card[1])

        for time in self.list_time:
            self.screen.blit(time[0], time[1])

        for y in range(78, 484, 45):
            pygame.draw.line(self.screen, (255, 255, 255), [20, y], [780, y], 2)
        pygame.draw.line(self.screen, (255, 255, 255), [400, 40], [400, 483], 2)

        self.screen.blit(self.text1, self.text_r1)
        self.screen.blit(self.text2, self.text_r2)
        self.screen.blit(self.text3, self.text_r3)
        self.screen.blit(self.text4, self.text_r4)
        self.screen.blit(self.text5, self.text_r5)
        self.screen.blit(self.text6, self.text_r6)

    def closing_window(self) -> None:
        """
        Метод для закрытия окна с результатами и перехода к главному меню
        """

        transit('fl_menu')
        screen_change('results', 'transition')
        self.update_button()

    def check_event(self, event) -> None:
        """
        Метод проверки событий для кнопки

        :param event: Событие, которое нужно обработать
        """

        self.button.handle_event(event)


class Playear_info:
    """
    Класс для отображения информации о персонаже
    """

    def __init__(self, screen):
        """
        Конструктор класса. Инициализирует экран и элементы интерфейса

        :param screen: Экран, на котором будет отображаться информация о персонаже
        """

        self.screen = screen

        self.buttons = []
        self.update_button()

        self.image, self.name = None, None

        self.text1, self.text_r1, self.text2, self.text_r2, self.text3 = None, None, None, None, None
        self.text_r3, self.text4, self.text_r4, self.text5, self.text_r5 = None, None, None, None, None
        self.text6, self.text_r6, self.text7, self.text_r7 = None, None, None, None

        # Создание текста - название окна
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 15)
        self.text_surface = font.render('Information', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(58, 10))

    def draw(self) -> None:
        """
        Метод для отрисовки экрана с информацией о персонаже
        """

        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (105, 105, 105), (100, 80, 400, 400))
        size = self.image.get_size()
        self.screen.blit(self.image, (525 + (250 - size[0]) // 2, 105))
        pygame.draw.rect(self.screen, (255, 0, 0), (525, 80, 250, 250), 5)

        self.screen.blit(self.text1, self.text_r1)
        self.screen.blit(self.text2, self.text_r2)
        self.screen.blit(self.text3, self.text_r3)
        self.screen.blit(self.text4, self.text_r4)
        self.screen.blit(self.text5, self.text_r5)
        self.screen.blit(self.text6, self.text_r6)
        self.screen.blit(self.text7, self.text_r7)

        self.screen.blit(self.text_surface, self.text_rect)

        for button in self.buttons:
            button.draw()

    def update_button(self) -> None:
        """
        Метод для обновления кнопок в окне
        """

        self.buttons = []

        self.buttons.append(
            Button(
                [560, 500, 180, 50], self.screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Назад',
                self.closing_window, 25
            )
        )
        self.buttons.append(
            Button(
                [330, 500, 180, 50], self.screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Прокачать',
                self.open_improvement, 25
            )
        )
        self.buttons.append(
            Button(
                [100, 500, 180, 50], self.screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Настройки',
                self.open_setting, 25
            )
        )

    def open_improvement(self) -> None:
        """
        Метод открытия окна улучшения персонажа
        """

        update_improvement(self.name)
        transit('improvement_character')
        screen_change('info_player', 'transition')
        self.update_button()

    def open_setting(self) -> None:
        """
        Метод открытия окна настроек
        """

        transit('settings')
        screen_change('info_player', 'transition')

    def closing_window(self) -> None:
        """
        Метод закрытия окна с информацией о персонаже
        """

        transit('character_types')
        character_update_but()
        screen_change('info_player', 'transition')

    def update(self, name) -> None:
        """
        Метод обновления данных персонажа

        :param name: Имя персонажа, чью информацию нужно обновить
        """

        self.name = name
        self.image = pygame.image.load(f'images/players/open/{name}.png')

        # Создание текста
        font1 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 27)

        self.text1 = font1.render(f'Имя персонажа: {self.name}', True, (255, 255, 255))
        self.text_r1 = self.text1.get_rect(center=(300, 120))

        font2 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 24)

        date = self.read_data()

        self.text2 = font2.render(f'Здоровье: {date[0]}', True, pygame.Color('green'))
        self.text_r2 = self.text2.get_rect(center=(300, 200))

        self.text3 = font2.render(f'Атака: {date[1]}', True, pygame.Color('red'))
        self.text_r3 = self.text3.get_rect(center=(300, 240))

        self.text4 = font2.render(f'Пыжок: {date[2]}', True, pygame.Color('yellow'))
        self.text_r4 = self.text4.get_rect(center=(300, 280))

        self.text5 = font2.render(f'Скорость: {date[3]}', True, (0, 255, 255))
        self.text_r5 = self.text5.get_rect(center=(300, 320))

        self.text6 = font2.render(f'Задержка: {"{:.2f}".format(int(date[4]) / 60)} сек', True, (255, 0, 255))
        self.text_r6 = self.text6.get_rect(center=(300, 360))

        font3 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 30)

        self.text7 = font3.render(f'Информация о персонаже', True, (255, 255, 255))
        self.text_r7 = self.text6.get_rect(center=(320, 40))

    def read_data(self) -> list:
        """
        Метод для чтения данных персонажа из файла

        :return: Список с характеристиками персонажа
        """

        with open(f'data/characteristics_character/{self.name}.txt', 'r', encoding='utf8') as file:
            data = file.read().split('\n')
        return data

    def check_event(self, event) -> None:
        """
        Метод проверки событий для кнопок

        :param event: Событие, которое нужно обработать
        """

        for button in self.buttons:
            button.handle_event(event)


class Result:
    def __init__(self, screen):
        """
        Инициализация экрана результатов

        :param screen: Экран, на котором будет отображаться окно результатов
        """

        self.screen = screen
        self.background = pygame.image.load("images/background/background.png").convert()

        # Инициализация переменных результата
        self.time, self.mobs, self.coins, self.res, self.rat, self.name_level = None, None, None, None, None, None
        self.button2, self.button1 = None, None
        self.name_card, self.font = None, None
        self.confetti = []

        # Обновление кнопок
        self.update_button()

    def update_button(self):
        """
        Обновление кнопок на экране результатов
        Создает кнопки для перезапуска и возврата в меню
        """

        # Создание кнопки для перезапуска
        self.button1 = Button(
            [60, 520, 200, 50], self.screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Restart', self.restart, 30
        )
        # Создание кнопки для возврата в меню
        self.button2 = Button(
            [540, 520, 200, 50], self.screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Menu', self.return_menu,
            30
        )

    def return_menu(self):
        """
        Возврат в главное меню
        """

        start_screen()
        music_menu()
        screen_change('fl_zastavka', 'fl_menu')
        transit('fl_menu')
        screen_change('fl_menu', 'transition')

        self.update_button()

    def restart(self):
        """
        Перезапуск игры
        """

        loading()
        transit('loading_screen')
        screen_change('character_types', 'transition')

        character_update_but()
        self.update_button()

    def draw(self):
        """
        Отображение экрана результатов на экране

        Это включает в себя отображение текста результата (победа/поражение),
        статистики, конфетти (если победа) и кнопок управления
        """

        self.screen.blit(self.background, (0, 0))  # Отображение фона
        self.font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 36)

        # Отображение текста в зависимости от результата игры
        if self.res == 'win':
            if not self.confetti:
                self.init_confetti()

            self.update_confetti()
            self.draw_confetti()

            text_surface = self.font.render('ПОБЕДА!', True, (255, 255, 0))
            text_rect = text_surface.get_rect(center=(400, 100))
            self.screen.blit(text_surface, text_rect)

            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 24)
            congrats_text = font.render('Превосходно! Вы одержали победу!', True, (0, 255, 255))
            congrats_rect = congrats_text.get_rect(center=(400, 160))
            self.screen.blit(congrats_text, congrats_rect)

        else:
            text_surface = self.font.render('ПОРАЖЕНИЕ', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(400, 100))
            self.screen.blit(text_surface, text_rect)

            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 20)
            text_sur = font.render('Повезёт в следующий раз...', True, (0, 255, 255))
            text_rct = text_sur.get_rect(center=(400, 165))
            self.screen.blit(text_sur, text_rct)

        # Форматирование времени
        if self.time < 3600:
            time = f'{self.time // 60}сек'
        elif self.time < 216000:
            time = f'{self.time // 3600}мин {self.time % 3600 // 60}сек'
        else:
            time = f'{self.time // 216000}ч {self.time % 216000 // 3600}мин {self.time % 216000 % 3600 // 60}сек'

        # Статистика
        stats = [
            f"Врагов повержено: {self.mobs}",
            f"Время прохождения: {time}",
            f"Монет собрано: {self.coins}" if self.res == 'win' else f"Монет потеряно: {self.coins}",
            f"Получено рейтинга: {self.rat}"
        ]
        y_offset = 220
        for stat in stats:
            stat_surface = self.font.render(stat, True, (255, 255, 255))
            stat_rect = stat_surface.get_rect(center=(400, y_offset))
            self.screen.blit(stat_surface, stat_rect)
            y_offset += 40

        # Отображение кнопок
        self.button1.draw()
        self.button2.draw()

    def check_event(self, event) -> None:
        """
        Обработка событий для кнопок

        :param event: Событие, которое будет обработано
        """

        self.button1.handle_event(event)
        self.button2.handle_event(event)

    def rating_calculation(self) -> int:
        """
        Расчет рейтинга на основе игровой статистики

        :return: Рейтинг, который зависит от количества убитых врагов, собранных монет и времени
        """

        if self.res == 'loss':
            n1, n2 = range_rating[self.name_card]['loss']
            rating = self.mobs * 14 + self.coins * 14 + \
                     min(int(self.time / 3600 * 100 * catering_coefficients_levels[self.name_level] *
                             catering_coefficients_cards[self.name_card]),
                         int(randint(n1, n2) * catering_coefficients_levels[self.name_level] *
                             catering_coefficients_cards[self.name_card]))
        else:
            n1, n2 = range_rating[self.name_card]['win']
            rating = self.mobs * 22 + self.coins * 22 + max(
                int(randint(n1, n2) - self.time / 3600 * 10 / catering_coefficients_levels[self.name_level] /
                    catering_coefficients_cards[self.name_card]), 0)

        # Запись данных и проверка времени на уровне
        recording_data(rating, self.coins, self.name_card, self.res)
        if self.res == 'win':
            time_check(self.name_card, self.time)

        return rating

    def update(self, mobs, time, coins, res, name_level, name_card) -> None:
        """
        Обновление данных на экране результатов

        :param mobs: Количество убитых врагов
        :param time: Время, затраченное на уровень
        :param coins: Количество собранных монет
        :param res: Результат (win/lose)
        :param name_level: Имя уровня
        :param name_card: Имя карты
        """

        pygame.mixer.music.load(f'data/file_music/result/{res}.mp3')
        pygame.mixer.music.set_volume(check('audio', 'music_volume'))
        pygame.mixer.music.play(-1)
        self.time = time
        self.mobs = mobs
        self.coins = coins
        self.res = res
        self.name_level = name_level
        self.name_card = name_card
        self.rat = self.rating_calculation()

    def init_confetti(self) -> None:
        """
        Инициализация частиц конфетти, которые будут отображаться при победе

        Генерируются случайные параметры для каждой частицы
        """

        for _ in range(200):
            x = randint(0, self.screen.get_width())
            y = randint(0, self.screen.get_height())
            size = randint(5, 15)
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            # Горизонтальное движение
            speed_x = uniform(-2, 2)
            speed_y = uniform(1, 5)
            self.confetti.append({'x': x, 'y': y, 'size': size, 'color': color, 'speed_x': speed_x, 'speed_y': speed_y})

    def update_confetti(self) -> None:
        """
        Обновление положения частиц конфетти

        Каждая частица двигается в зависимости от своего направления и скорости
        """

        for particle in self.confetti:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']

            # Перемещение частиц на экране
            if particle['x'] < 0:
                particle['x'] = self.screen.get_width()
            elif particle['x'] > self.screen.get_width():
                particle['x'] = 0

            if particle['y'] > self.screen.get_height():
                particle['y'] = 0

    def draw_confetti(self) -> None:
        """
        Отображение частиц конфетти на экране
        """

        for particle in self.confetti:
            pygame.draw.circle(
                self.screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])


class Gamplay:
    def __init__(self, screen) -> None:
        """
        Инициализация объекта класса Gamplay, создание необходимых атрибутов

        :param screen: Экран, на котором будет происходить рендеринг игры
        """

        self.screen = screen

        # Инициализация переменных уровня, карты, фона и других атрибутов
        self.level, self.name_card, self.background_map, self.cards, self.tile_images = None, None, None, None, None
        self.character, self.tiles, self.port, self.player, self.numb = None, None, None, None, None
        self.time, self.dis_time, self.dis_time_rect, self.start_time, self.date_start = None, None, None, None, None
        self.spis_enemy = []
        self.count, self.ind, self.mobs, self.coin = 0, 0, 0, 0

        # Загрузка анимации для портала и монеты
        self.anim_port = [
            pygame.transform.scale(pygame.image.load(f'images/portal/{i}.png'), (32, 80)) for i in range(4)
        ]
        self.image_coin = pygame.transform.scale(pygame.image.load('images/coin/0.png'), (32, 32))
        self.button_setting = None

        # Обновление кнопки настроек
        self.update_button()

    def loading(self) -> None:
        """
        Загрузка начальных данных и подготовка к игре

        :param Запуск таймера, настройка карты и персонажа
        """

        self.time = 0

        # Установка времени начала игры
        self.start_time = f'{datetime.datetime.now().time():%H:%M}'
        self.date_start = '.'.join(f'{datetime.datetime.now().date()}'.split('-')[::-1])

        # Загрузка уровня и карты
        self.level = check('gameplay', 'level')
        self.coin, self.mobs = 0, 0
        self.name_card = check('gameplay', 'name_card')
        type_card = check('gameplay', 'type_card')

        # Подготовка фона карты
        self.background_map = pygame.transform.scale(
            pygame.image.load(type_card_background[type_card]).convert_alpha(), (800, 600)
        )
        self.tiles = pygame.sprite.Group()

        # Генерация карты
        self.generate_map(type_card)

        # Создание врагов
        self.creating_enemy()

        # Настройка портала
        self.port = portal_cords[self.name_card]

        # Создание персонажа
        self.player = self.Player()
        self.player.definition_character(
            check('gameplay', 'character'), self.screen, spawn_coordinates[self.name_card], self.tiles, self.numb,
            self.collision_with_mobs, type_card
        )

    def update_button(self) -> None:
        """
        Создание или обновление кнопки настройки
        """

        self.button_setting = Button([6, 6, 32, 32], self.screen, (255, 255, 255), (100, 100, 100), (0, 0, 0), 'X',
                                     self.open_setting, 32, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

    def draw(self) -> None:
        """
        Отображение всех элементов на экране
        """

        # Увеличение времени
        self.time += 1

        # Анимация телепорта
        self.teleport()

        # Отображение карты
        self.draw_map()

        # Отображение врагов
        self.draw_enemy()

        # Отображение статистики персонажа
        self.draw_stats()

        # Отображение портала
        self.draw_portal()

        # Отображение монет
        self.draw_coin()

        # Обновление персонажа
        self.player.update()

    def draw_portal(self) -> None:
        """
        Отображение анимации портала
        """

        self.count += 1
        if self.count > 10:
            self.count = 0
            # Плавное переключение кадров анимации портала
            self.ind = (self.ind + 1) % len(self.anim_port)

        num_one, num_two = self.player.cords_map()
        # Расчет позиции портала
        pos_port = (self.port[0] - (num_one - num_two), self.port[1])
        if -32 < pos_port[0] < 800 and -32 < pos_port[1] < 600:
            self.screen.blit(self.anim_port[self.ind], pos_port)

    def draw_stats(self) -> None:
        """
        Отображение статистики персонажа
        """

        # Получение текущих значений здоровья или другой статистики
        current_value, max_value = self.player.draw_stat()
        center_x, center_y = 765, 563
        radius = 18

        # Начинаем с 90 градусов (верх)
        start_angle = -pi / 2
        end_angle = start_angle + (2 * pi * ((current_value / max_value) * 100 / 100))

        # Расчет координат для отрисовки окружности
        # Начальная точка в центре круга
        points = [[center_x, center_y]]

        for angle in range(int(degrees(start_angle)), int(degrees(end_angle)) + 1):
            rad = radians(angle)
            x = int(center_x + radius * cos(rad))
            y = int(center_y + radius * sin(rad))
            points.append((x, y))
        if len(points) > 2:
            # Рисуем сектор круга
            pygame.draw.polygon(self.screen, (30, 144, 255, 180), points)

        # Рисуем окружность по периметру
        pygame.draw.circle(self.screen, (10, 10, 10), (center_x, center_y), radius + 2, 2)

        # Отображение текста для статистики
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 12)
        text = font.render(f'recharge', True, (0, 0, 0))
        text_r = text.get_rect(center=(765, 589))
        self.screen.blit(text, text_r)

    def draw_coin(self) -> None:
        """
        Отображение монет на экране
        """

        # Отображение изображения монеты
        self.screen.blit(self.image_coin, [760, 8])
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 22)

        # Отображение количества монет
        text = font.render(f'{self.coin}', True, (255, 255, 255))
        text_r = text.get_rect(center=(747, 26))
        self.screen.blit(text, text_r)

    def draw_map(self) -> None:
        """
        Отображение карты на экране
        """

        x_bac = self.player.cord_bac()

        # Отображение фона карты
        self.screen.blit(self.background_map, (x_bac, 0))

        # Дополнительный фон для плавности
        self.screen.blit(self.background_map, (800 + x_bac, 0))
        num_one, num_two = self.player.cords_map()

        for tile in self.tiles:
            # Отображение тайлов карты
            tile.draw(num_one, num_two)

        # Обновление времени
        custom_font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 12)
        if self.time < 216000:
            # Вычисление времени в формате чч:мм
            zn1, zn2 = str(self.time // 3600), str(self.time % 3600 // 60)
            time = f'{"0" * (2 - len(zn1)) + zn1}:{"0" * (2 - len(zn2)) + zn2}'
        else:
            # Вычисление времени в формате чч:мм:сс
            zn1, zn2, zn3 = str(self.time // 216000), str(self.time % 216000 // 3600), str(
                self.time % 216000 % 3600 // 60)
            time = f'{"0" * (2 - len(zn1)) + zn1}:{"0" * (2 - len(zn2)) + zn2}:{"0" * (2 - len(zn3)) + zn3}'
        self.dis_time = custom_font.render(f'time: {time}', True, (0, 0, 0))
        self.dis_time_rect = self.dis_time.get_rect(topleft=(2, 586))

        # Отображение времени
        self.screen.blit(self.dis_time, self.dis_time_rect)

        # Отображение кнопки настроек
        self.button_setting.draw()

    def creating_enemy(self) -> None:
        """
        Создание врагов на карте
        """

        self.spis_enemy = pygame.sprite.Group()

        # Получение данных для создания врагов
        number_mobs, data, damage, hp = spavn_mobs[self.name_card]
        data_mobs = sample(data, number_mobs)
        for i in data_mobs:
            range_x, y, rad, rad_max, grav = i
            x = randint(range_x[0], range_x[1])
            name = randint(0, 2)
            # Добавление врагов в группу
            self.spis_enemy.add(
                self.Enemy(
                    self.screen, x, y, randint(2, 3), self.tiles, grav, 10, rad, rad_max, animations_mob[name],
                    randint(hp[0], hp[1]), self.collision_with_player, randint(60, 80), randint(damage[0], damage[1]),
                    self.pos_pl, self.kill_mob, name, self.collecting_coins
                )
            )

    def pos_pl(self) -> list:
        """
        Получение позиции игрока

        :return: Список, содержащий текущие координаты игрока
        """

        return self.player.pos_player()

    def kill_mob(self) -> None:
        """
        Увеличение количества убитых врагов
        """

        self.mobs += 1

    def collision_with_player(self, self_mob, pos_mob, dmg, reg, napr) -> None:
        """
        Обработка столкновения игрока с мобом

        :param self_mob: Моб, с которым происходит столкновение
        :param pos_mob: Позиция моба
        :param dmg: Урон, который наносит моб
        :param reg: Функция регенерации для игрока
        :param napr: Направление, в котором движется моб
        """

        pos_pl = self.player.pos_player()
        self.player.gen_mask()
        self_mob.gen_mask()

        if pygame.sprite.collide_mask(self.player, self_mob):
            # Если игрок и моб столкнулись по горизонтали в одном направлении
            if (pos_pl[0] > pos_mob[0] and napr == 'right') or (pos_pl[0] < pos_mob[0] and napr == 'left'):
                # Игрок получает урон
                self.player.taking_damage(dmg)

                # Регенерация игрока
                reg()

    def collision_with_mobs(self) -> None:
        """
        Обработка столкновения игрока с мобами
        """

        pos_pl = self.player.pos_player()
        self.player.gen_mask()

        for enemy in self.spis_enemy:
            enemy.gen_mask()

            if pygame.sprite.collide_mask(self.player, enemy):
                pos_mob = enemy.pos_mobs()

                # Проверка направления столкновения
                if (pos_pl[0] > pos_mob[0] and self.player.direct() == 'left') or (
                        pos_pl[0] < pos_mob[0] and self.player.direct() == 'right'):
                    # Моб получает урон
                    enemy.taking_damage(self.player.dm())

                    # Регенерация игрока
                    self.player.reg()
                    break

    def draw_enemy(self) -> None:
        """
        Отображение врагов на экране
        """

        num_one, num_two = self.player.cords_map()
        pl_rect = self.player.pos_player()
        # Получаем гравитацию игрока
        graviti_player = self.player.grvit()
        for enemy in self.spis_enemy:
            enemy.draw(num_one, num_two, graviti_player, pl_rect)

    def inf(self) -> tuple:
        """
        Получение информации о текущем игровом процессе

        :return: Кортеж с данными: количество убитых мобов, время, количество монет, уровень и название карты
        """

        return self.mobs, self.time, self.coin, self.level, self.name_card

    def check_event(self, event) -> None:
        """
        Проверка событий на экране

        :param event: Событие, которое нужно обработать
        """

        self.button_setting.handle_event(event)

    def open_setting(self) -> None:
        """
        Открытие окна настроек
        """

        transit('settings')
        screen_change('gemplay', 'transition')

    def teleport(self) -> None:
        """
        Обработка телепортации игрока при попадании в портал
        """

        port_rect = self.anim_port[0].get_rect()
        port_rect.x = self.port[0]
        port_rect.y = self.port[1]
        pl_rect = self.player.pos_player()

        # Если игрок соприкасается с порталом
        if pl_rect.colliderect(port_rect):
            # Игрок выигрывает
            self.player.win()

    def load_images(self, t_s, number_cart) -> dict:
        """
        Загрузка изображений для тайлов

        :param t_s: Размер тайла
        :param number_cart: Номер карты, с которой будут загружены тайлы
        :return: Словарь с изображениями для каждого типа тайла
        """

        images = {
            'A': pygame.image.load(f"images/tiles/{number_cart}/1.png").convert_alpha(),
            'B': pygame.image.load(f"images/tiles/{number_cart}/2.png").convert_alpha(),
            'C': pygame.image.load(f"images/tiles/{number_cart}/3.png").convert_alpha(),
            'D': pygame.image.load(f"images/tiles/{number_cart}/4.png").convert_alpha(),
            'E': pygame.image.load(f"images/tiles/{number_cart}/5.png").convert_alpha(),
            'F': pygame.image.load(f"images/tiles/{number_cart}/6.png").convert_alpha(),
            'G': pygame.image.load(f"images/tiles/{number_cart}/7.png").convert_alpha(),
            'H': pygame.image.load(f"images/tiles/{number_cart}/8.png").convert_alpha(),
            'I': pygame.image.load(f"images/tiles/{number_cart}/9.png").convert_alpha(),
            'J': pygame.image.load(f"images/tiles/{number_cart}/10.png").convert_alpha(),
            'K': pygame.image.load(f"images/tiles/{number_cart}/11.png").convert_alpha(),
            'L': pygame.image.load(f"images/tiles/{number_cart}/12.png").convert_alpha(),
            'M': pygame.image.load(f"images/tiles/{number_cart}/13.png").convert_alpha()
        }

        # Масштабирование всех изображений
        for key, image in images.items():
            images[key] = pygame.transform.scale(image, (t_s, t_s))

        return images

    def generate_map(self, type_card) -> None:
        """
        Генерация карты на основе данных карты

        :param type_card: Тип карты, которую нужно сгенерировать
        """

        tile_images = self.load_images(32, type_card)
        cards = check_levels('levels', self.name_card)
        self.numb = len(cards[0]) * 32
        for y, row in enumerate(cards):
            for x, symbol in enumerate(row):
                if symbol in tile_images:
                    image = tile_images[symbol]
                    tile = self.Tile(self.screen, image, x * 32, y * 32)
                    self.tiles.add(tile)

        # Создание текста для отображения времени
        custom_font = pygame.font.Font('data/Docker.ttf', 18)
        self.dis_time = custom_font.render(f'time: 00:00', True, (0, 0, 0))
        self.dis_time_rect = self.dis_time.get_rect(center=(700, 500))

    def update_coin(self) -> None:
        """
        Увеличение количества монет
        """

        self.coin += 1

    def collecting_coins(self, coin_pos, kill) -> None:
        """
        Обработка сбора монеты игроком

        :param coin_pos: Позиция монеты
        :param kill: Функция, которая убивает монету после того, как она собрана
        """

        pl_pos = self.player.pos_player()

        # Если игрок соприкасается с монетой
        if pl_pos.colliderect(coin_pos):
            sound_mon = pygame.mixer.Sound(f'data/file_music/coin/coin_selection.mp3')
            sound_mon.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)

            # Воспроизведение звука при сборе монеты
            sound_mon.play()

            # Увеличение количества монет
            self.update_coin()

            # Удаление монеты
            kill()

    class Tile(pygame.sprite.Sprite):
        """
        Класс плиток (тайлов) для карты
        """

        def __init__(self, screen, image, x, y) -> None:
            """
            Инициализация тайла для карты

            :param screen: Экран, на котором будет отрисован тайл
            :param image: Изображение тайла
            :param x: Позиция тайла по оси X
            :param y: Позиция тайла по оси Y
            """

            super().__init__()
            self.screen = screen
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def draw(self, pos_player, pos_player_display) -> None:
            """
            Отображение тайла на экране

            :param pos_player: Позиция игрока на карте
            :param pos_player_display: Позиция игрока на экране
            """

            tile_pos = (self.rect.x - (pos_player - pos_player_display), self.rect.y)
            if -32 < tile_pos[0] < 800 and -32 < tile_pos[1] < 600:
                self.screen.blit(self.image, tile_pos)

    class Enemy(pygame.sprite.Sprite):
        """
        Инициализирует объект врага с множеством параметров и настройками

        :param screen: Экран, на котором будет отображаться враг
        :param x: Начальная позиция по оси X
        :param y: Начальная позиция по оси Y
        :param speed: Скорость перемещения врага
        :param list_tile: Список объектов, с которыми враг может столкнуться
        :param grav: Гравитация, влияющая на врага
        :param jump: Сила прыжка врага
        :param rad: Радиус агрессии врага
        :param max_rad: Максимальный радиус, на котором враг может атаковать
        :param animal: Спрайты для анимаций врага
        :param hp: Количество здоровья врага
        :param function_reference: Функция, вызываемая при атаке
        :param delay: Задержка между действиями врага
        :param damage: Урон, который враг наносит
        :param pl_pos: Позиция игрока
        :param func: Функция для дополнительной логики
        :param name: Имя врага, определяющее его особенности
        :param collecting_coins: Функция для сбора монет
        """

        def __init__(self, screen, x, y, speed, list_tile, grav, jump, rad, max_rad, animal, hp,
                     function_reference, delay, damage, pl_pos, func, name, collecting_coins) -> None:
            super().__init__()

            # Инициализация переменных для различных состояний врага
            self.image = None
            self.mask = None
            self.cause_damage = True
            self.expectation = True
            self.napr_right = True
            self.fl_demage = True
            self.fl_coin = True
            self.run = True
            self.persecution = False
            self.collision = False
            self.attack = False
            self.atak = False
            self.cn = False

            # Переменные для анимации и движения
            self.ind_dead = 0
            self.counter = 0
            self.num_1 = 0
            self.num_2 = 0
            self.count = 0
            self.d_x = 0
            self.d_y = 0
            self.sch = 0
            self.ind = 0
            self.cnt = 0
            self.v_y = 0
            self.is_jump = 1

            # Текущая анимация и направление движения
            self.current_animation = 'idle'
            self.napr = 'right'
            self.img = 'right'

            # Присваиваем параметры
            self.function_reference = function_reference
            self.coin = self.Coin(grav, collecting_coins)
            self.list_tile = list_tile
            self.max_rad = max_rad
            self.animal = animal
            self.damage = damage
            self.screen = screen
            self.pl_pos = pl_pos
            self.speed = speed
            self.delay = delay
            self.jump = jump
            self.func = func
            self.grav = grav
            self.name = name
            self.rad = rad
            self.hp = hp
            self.x = x
            self.y = y

            # Обновление изображения и координат
            self.update_image()
            self.rect = self.image.get_rect(topleft=(x, y))
            self.rect.width = 40
            if name == 0:
                self.d_y = 20
                self.rect.height = 70
                self.frame_counter = 3
            elif name == 1:
                self.d_y = 12
                self.rect.height = 70
                self.frame_counter = 5
            elif name == 2:
                self.d_y = 20
                self.rect.height = 70
                self.frame_counter = 4

            # Загрузка звуковых файлов
            self.sound_attack = pygame.mixer.Sound(f'data/file_music/mobs/attack/{name}.mp3')
            self.sound_attack.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)
            self.sound_jump = pygame.mixer.Sound(f'data/file_music/mobs/jump/jump.mp3')
            self.sound_jump.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)

        def play_sound_attack(self) -> None:
            """
            Воспроизводит звук атаки врага, если не включен режим без звука
            """

            if check('audio', 'mute_sound'):
                self.sound_attack.play()

        def play_sound_damage(self) -> None:
            """
            Воспроизводит звук получения урона врагом
            """

            sound_damage = pygame.mixer.Sound(f'data/file_music/mobs/damage/{randint(0, 3)}.mp3')
            sound_damage.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)
            sound_damage.play()

        def draw(self, pos_player, pos_player_display, grav_pl, pl_rect) -> None:
            """
            Обновляет позицию врага, рисует его на экране и обновляет анимацию

            :param pos_player: Позиция игрока
            :param pos_player_display: Позиция игрока на экране
            :param grav_pl: Гравитация игрока
            :param pl_rect: Прямоугольник игрока для столкновений
            """

            self.update_x(pos_player, grav_pl, pl_rect)
            self.update_y()
            self.update_image()

            enemy_pos = (self.rect.x - (pos_player - pos_player_display) + self.d_x,
                         self.rect.y - (self.d_y if self.grav == 1 else 0))

            # Рисует врага, если он в пределах экрана
            if -(self.rect.width + abs(self.d_x)) < enemy_pos[0] < 800:
                self.screen.blit(self.image, enemy_pos)

            # Если враг погиб, рисуем монеты
            if self.cn:
                self.coin.update()
                self.coin.draw(self.screen, pos_player - pos_player_display)

        def kill(self) -> None:
            """
            Останавливает процесс сбора монет и деактивирует монеты
            """

            self.cn = False

        class Coin(pygame.sprite.Sprite):
            """
            Класс для объектов монет, которые могут собирать игроки

            :param grav: Гравитация, влияющая на монету
            :param collecting_coins: Функция для сбора монет
            """

            def __init__(self, grav, collecting_coins) -> None:
                super().__init__()

                # Инициализация монеты
                self.kill = None
                self.y = None
                self.pod = True
                self.speed = 1
                self.count = 0
                self.ind = 0
                self.sch = 0

                # Настройка радиуса и анимации монеты
                self.rad = randint(50, 80)
                self.num = randint(6, 9)

                # Функция для сбора монет
                self.collecting_coins = collecting_coins
                self.v_y = -self.num * grav
                self.animal = coin_animation
                self.image = self.animal[0]
                self.grav = grav

                # Прямоугольник для отслеживания положения монеты
                self.rect = self.image.get_rect()

            def update(self) -> None:
                """
                Обновляет положение монеты, анимацию и проверяет, собрана ли монета
                """

                self.count += 1
                if self.count > 3:
                    self.count = 0
                    self.ind = (self.ind + 1) % len(self.animal)

                    self.image = self.animal[self.ind]

                    self.v_y += self.speed * self.grav

                    if self.rect.y == self.y:
                        self.v_y = -self.num * self.grav

                    self.rect.y += self.v_y

                # Если монета слишком долго не собрана, вызываем функцию сбора
                if self.sch < 120:
                    self.sch += 1
                else:
                    self.collecting_coins(self.rect, self.kill)

            def draw(self, screen, x) -> None:
                """
                Отображает монету на экране

                :param screen: Экран, на котором рисуется монета
                :param x: Смещение по оси X
                """

                screen.blit(self.image, [self.rect.x - x, self.rect.y])

            def x_y(self, x, y, kill) -> None:
                """
                Устанавливает позицию монеты на экране.

                :param x: Позиция по оси X
                :param y: Позиция по оси Y
                :param kill: Функция для уничтожения монеты
                """

                self.rect.x = x
                self.rect.y = y - (self.rect.height if self.grav == 1 else 0)
                self.y = y - (self.rect.height if self.grav == 1 else 0)
                self.kill = kill

        def update_image(self) -> None:
            """
            Обновляет изображение врага в зависимости от его состояния:
            прыжок, атака, смерть
            """

            # Если враг жив
            if self.hp > 0:
                # Если враг не атакует
                if not self.attack:
                    self.count += 1
                    # Если прошло больше 5 кадров
                    if self.count > 5:
                        self.count = 0
                        # Если враг в прыжке
                        if self.is_jump:
                            self.current_animation = 'jump'
                        # Если враг бежит
                        elif self.run:
                            self.current_animation = 'run'
                        # В противном случае враг стоит
                        else:
                            self.current_animation = 'idle'
                        self.ind = (self.ind + 1) % len(self.animal[self.current_animation])
                # Если враг атакует
                else:
                    self.count += 1
                    if self.count > self.frame_counter:
                        self.count = 0
                        self.current_animation = 'attack'
                        self.ind += 1
                        if self.ind >= len(self.animal[self.current_animation]):
                            # Завершаем анимацию атаки
                            self.attack = False
                            self.cause_damage = False
                            self.ind = 0
            # Если враг мертв
            else:
                self.count += 1
                if self.count > 5:
                    self.count = 0
                    self.current_animation = 'dead'
                    # Если враг еще не полностью мертв
                    if self.ind_dead == 0:
                        self.ind += 1
                        if self.ind >= len(self.animal[self.current_animation]):
                            self.ind_dead += 1
                            self.ind = len(self.animal[self.current_animation]) - 1
                    # В противном случае генерируем монету и завершаем анимацию
                    else:
                        if self.fl_coin:
                            self.coin.x_y(
                                self.rect.x + 10, self.rect.y + (self.rect.height if self.grav == 1 else 0), self.kill
                            )
                            self.fl_coin = False
                            self.func()
                        self.ind = len(self.animal[self.current_animation]) - 1

            # Поворот изображения врага в зависимости от направления и гравитации
            if self.img == 'right':
                if self.grav == 1:
                    self.image = pygame.transform.flip(self.animal[self.current_animation][self.ind], False, False)
                else:
                    self.image = pygame.transform.flip(self.animal[self.current_animation][self.ind], False, True)
            else:
                if self.grav == 1:
                    self.image = pygame.transform.flip(self.animal[self.current_animation][self.ind], True, False)
                else:
                    self.image = pygame.transform.flip(self.animal[self.current_animation][self.ind], True, True)

            # Обновление горизонтальной позиции для анимации
            self.d_x = x_offset_mobs[self.name][self.img][self.current_animation]

        def update_x(self, pos_player, grav_pl, pl_rect) -> None:
            """
            Обновляет горизонтальное положение врага и реагирует на столкновения с игроком

            :param pos_player: Позиция игрока
            :param grav_pl: Гравитация игрока
            :param pl_rect: Прямоугольник игрока для столкновений
            """

            # Если моб жив
            if self.hp > 0:
                # Если враг не атакует
                if not self.attack:
                    self.sch += 1
                    if self.sch > self.delay:
                        self.sch = 0
                        self.fl_demage = True

                    if self.rect.colliderect(pl_rect) and self.grav == grav_pl and self.fl_demage:
                        # Если враг столкнулся с игроком
                        if pos_player < self.rect.x and self.collision:
                            self.collision = False
                            self.rect.x -= 5
                        self.attack, self.fl_demage, self.cause_damage = True, False, True
                        self.ind = 0
                        self.play_sound_attack()
                    elif self.fl_demage:
                        self.collision = True
                        pl_pos = self.pl_pos()
                        if pl_pos.colliderect(pygame.Rect(self.x - self.max_rad, self.rect.y - 60, self.max_rad * 2,
                                                          120)) and self.grav == grav_pl:
                            self.run = True
                            if pos_player < self.rect.x:
                                self.napr = 'left'
                            else:
                                self.napr = 'right'
                        else:
                            # Логика для изменения направления врага
                            if self.napr == 'right' and self.rect.x >= self.x + self.rad:
                                if self.run:
                                    self.run = False
                                    self.num_2 = randint(60, 120)
                                else:
                                    self.cnt += 1
                                    if self.cnt > self.num_2:
                                        self.run = True
                                        self.napr = 'left'
                                        self.cnt = 0
                            elif self.napr == 'left' and self.rect.x <= self.x - self.rad:
                                if self.run:
                                    self.run = False
                                    self.num_1 = randint(60, 120)
                                else:
                                    self.cnt += 1
                                    if self.cnt > self.num_1:
                                        self.run = True
                                        self.napr = 'right'
                                        self.cnt = 0
                            else:
                                self.run = True

                        # Если враг бежит, меняем направление
                        if self.run:
                            if self.napr == 'right':
                                self.img = 'right'
                                self.change_x(self.speed)
                            else:
                                self.img = 'left'
                                self.change_x(-self.speed)
                    else:
                        self.run = False

                else:
                    # Если враг атакует
                    if pos_player < self.rect.x:
                        self.img = 'left'
                    else:
                        self.img = 'right'
                    if self.cause_damage:
                        self.function_reference(self, self.rect, self.damage, self.reg, self.img)

        def change_x(self, speed) -> None:
            """
            Изменяет положение врага по оси X и обрабатывает столкновения

            :param speed: Скорость перемещения
            """

            old_x = self.rect.x
            self.rect.x += speed
            if pygame.sprite.spritecollide(self, self.list_tile, False):
                # Если произошло столкновение с объектом
                self.rect.x = old_x
                if not self.is_jump:
                    self.v_y = -self.jump * self.grav
                    self.is_jump = True

        def update_y(self) -> None:
            """
            Обновляет положение врага по оси Y и проверяет столкновения с объектами
            """

            if not self.attack:
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

        def gen_mask(self) -> None:
            """
            Генерирует маску для определения коллизий
            """

            self.mask = pygame.mask.from_surface(self.image)

        def taking_damage(self, dm) -> None:
            """
            Обрабатывает получение урона врагом и вызывает звук повреждения

            :param dm: Урон, который наносится врагу
            """

            if self.hp > 0:
                self.hp -= dm
                self.play_sound_damage()
                if self.hp <= 0:
                    self.ind = 0
                    self.cn = True

        def pos_mobs(self) -> list:
            """
            Возвращает позицию врага

            :return: Прямоугольник, который описывает позицию врага
            """

            return self.rect

        def reg(self) -> None:
            """
            Останавливает процесс нанесения урона
            """

            self.cause_damage = False

        def dm(self) -> int:
            """
            Возвращает урон, который враг наносит

            :return: Урон врага
            """

            return self.damage

    class Player(pygame.sprite.Sprite):
        """
        Класс для представления игрока в игре. Управляет всеми аспектами персонажа,
        включая движение, анимацию, звуки и взаимодействие с окружающей средой.
        """

        def __init__(self) -> None:
            """
            Инициализация игрока. Устанавливаются начальные параметры персонажа.
            """
            super().__init__()

            # Переменные для контроля различных состояний персонажа

            # Переменная для изменения гравитации
            self.change_graviti = True

            # Можно ли нанести урон
            self.cause_damage = True

            # Является ли персонаж в прыжке
            self.is_jumping = True

            # Переменная для смены гравитации
            self.smen_grav = True

            # Переменная для проверки получения урона
            self.fl_demage = True

            # Нажата ли клавиша пробела
            self.pressing_space = False

            # Выполняет ли персонаж атаку
            self.attack = False

            # Переменная для бега персонажа
            self.run = False

            # Количество кадров анимации
            self.count = 6

            # Направление гравитации (1 - нормальная, -1 - инвертированная)
            self.grav = 1

            # Текущий кадр анимации
            self.current_frame = 0

            # Задержка между кадрами анимации
            self.frame_delay = 0

            # Таймер для отслеживания кадров
            self.frame_timer = 0

            # Скорость по оси Y (для прыжков)
            self.velocity_y = 0

            # Индекс анимации смерти
            self.ind_dead = 0

            # Смещение по оси X для фона
            self.x_bac = 0

            # Переменная для отслеживания задержки между действиями
            self.sch = 0

            # Текущая анимация (ожидание)
            self.current_animation = 'idle'

            # Направление движения персонажа
            self.direction = 'right'

            # Инициализация переменных с характеристиками персонажа
            self.x, self.screen, self.hp, self.max_hp, self.speed, self.tiles = None, None, None, None, None, None
            self.gravity, self.numb, self.delay, self.jump_height, self.damage = None, None, None, None, None
            self.animation_frames, self.function_reference, self.image, self.rect = None, None, None, None
            self.d_x, self.name, self.mask, self.d_y, self.sound_attack = None, None, None, None, None
            self.sound_jump, self.sound_death, self.sound_change_gravity = None, None, None

        def definition_character(self, name, screen, cords, tiles, numb, function_reference, type_card) -> None:
            """
            Определяет характеристики персонажа, загружая данные из файла.

            :param name: Имя персонажа
            :param screen: Экран, на котором будет отображаться персонаж
            :param cords: Координаты (x, y) персонажа на экране
            :param tiles: Объекты, с которыми может взаимодействовать персонаж
            :param numb: Максимальная ширина экрана
            :param function_reference: Ссылка на функцию, вызываемую при получении урона
            :param type_card: Тип карты для звука прыжка
            """

            with open(f'data/characteristics_character/{name}.txt', 'r', encoding='utf8') as file:
                date = list(map(int, file.read().split('\n')))

            # Гравитация
            gravity = 0.5

            # Характеристики персонажа
            hp, damage, jump_height, speed, delay = date[0], date[1], date[2], date[3], date[4]

            # Анимация для персонажа
            self.animation_frames = animation_frames_character[name]

            # Ссылка на функцию получения урона
            self.function_reference = function_reference

            # Высота прыжка
            self.jump_height = jump_height

            # Гравитация
            self.gravity = gravity

            # Урон, который наносит персонаж
            self.damage = damage

            # Экран, на котором будет отображаться персонаж
            self.screen = screen

            # Задержка между действиями
            self.delay = delay

            # Скорость персонажа
            self.speed = speed

            # Объекты, с которыми взаимодействует персонаж
            self.tiles = tiles

            # Координата X персонажа
            self.x = cords[0]

            # Максимальное количество здоровья
            self.max_hp = hp

            # Максимальная ширина экрана
            self.numb = numb

            # Имя персонажа
            self.name = name

            # Текущее количество здоровья
            self.hp = hp

            # Смещение по оси X для персонажа
            self.d_x = 0

            # Смещение по оси Y для персонажа
            self.d_y = 0

            # Звук атаки
            self.sound_attack = pygame.mixer.Sound(attack_soun[self.name])

            # Установка громкости
            self.sound_attack.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)

            # Звук прыжка
            self.sound_jump = pygame.mixer.Sound(f'data/file_music/character/jump/{type_card}.mp3')

            # Установка громкости
            self.sound_jump.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)

            # Звук смерти
            self.sound_death = pygame.mixer.Sound('data/file_music/character/death/death.mp3')

            # Установка громкости
            self.sound_death.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)

            # Звук смерти
            self.sound_change_gravity = pygame.mixer.Sound('data/file_music/character/smen_graviti/change_gravity.mp3')

            # Установка громкости
            self.sound_change_gravity.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)

            # Инициализация изображения и rect

            # Изображение персонажа
            self.image = pygame.transform.flip(self.animation_frames['idle'][0], False, False)

            # Прямоугольник для персонажа
            self.rect = self.image.get_rect(topleft=(cords[0], cords[1]))

            # Установка высоты для разных персонажей
            if self.name == 'Лиам':
                self.rect.height = 80
                self.d_y = 25
            elif self.name == 'Келтор':
                self.rect.height = 80
                self.d_y = 28
            elif self.name == 'Золтан':
                self.rect.height = 80
                self.d_y = 2
            elif self.name == 'Финн':
                self.rect.height = 75
                self.d_y = 5

            # Ширина персонажа
            self.rect.width = 50

        def play_sound_attack(self) -> None:
            """
            Проигрывает звук атаки
            """

            # Установка громкости
            self.sound_attack.set_volume(check('audio', 'sound_volume'))

            if check('audio', 'mute_sound'):
                self.sound_attack.play()

        def play_sound_jump(self) -> None:
            """
            Проигрывает звук прыжка
            """

            if check('audio', 'mute_sound'):
                # Установка громкости
                self.sound_jump.set_volume(check('audio', 'sound_volume'))
                self.sound_jump.play()

        def play_sound_death(self) -> None:
            """
            Проигрывает звук смерти
            """

            if check('audio', 'mute_sound'):
                # Установка громкости
                self.sound_death.set_volume(check('audio', 'sound_volume'))

                self.sound_death.play()

        def play_change_gravity(self):
            """
            Проигрывает звук смены гравитации
            """

            if check('audio', 'mute_sound'):
                # Установка громкости
                self.sound_change_gravity.set_volume(check('audio', 'sound_volume'))

                self.sound_change_gravity.play()

        def play_sound_damage(self) -> None:
            """
            Проигрывает звук получения урона
            """

            sound_damage = pygame.mixer.Sound(f'data/file_music/character/damage/{randint(1, 5)}.mp3')
            sound_damage.set_volume(check('audio', 'sound_volume') if check('audio', 'mute_sound') else 0)
            sound_damage.play()

        def draw(self) -> None:
            """
            Отображает персонажа на экране
            """

            self.screen.blit(self.image, (self.x + self.d_x, self.rect.y - (self.d_y if self.grav == 1 else 0)))

        def get_current_image(self) -> None:
            """
            Возвращает текущий кадр анимации с учетом направления

            :return: Текущий кадр анимации персонажа
            """

            # Запоминаем старую анимацию
            old = self.current_animation
            if self.hp > 0:
                if not self.attack:
                    if self.change_graviti:
                        if self.is_jumping:
                            # Анимация прыжка
                            self.current_animation = 'jump'
                        else:
                            if self.run:
                                # Анимация бега
                                self.current_animation = 'run'
                            else:
                                # Анимация ожидания
                                self.current_animation = 'idle'
                    else:
                        # Анимация смены гравитации
                        self.current_animation = 'smen_graviti'
                    if old == self.current_animation:
                        self.frame_delay += 1
                        if self.frame_delay > self.count:
                            self.frame_delay = 0
                            self.current_frame = (self.current_frame + 1) % len(
                                self.animation_frames[self.current_animation])
                    else:
                        self.frame_delay = 0
                        self.current_frame = 0
                else:
                    # Анимация атаки
                    self.current_animation = 'attack'
                    if old != self.current_animation:
                        self.frame_delay = 0
                        self.current_frame = 0
                    self.frame_delay += 1
                    if self.frame_delay > self.count:
                        self.frame_delay = 0
                        self.current_frame = self.current_frame + 1
                        if self.current_frame >= len(self.animation_frames[self.current_animation]):
                            self.attack = False
                            self.current_frame = 0
            else:
                self.frame_delay += 1
                if self.frame_delay > self.count + 1:
                    self.frame_delay = 0
                    # Анимация смерти
                    self.current_animation = 'dead'
                    self.ind_dead += 1
                    if self.ind_dead < len(self.animation_frames['dead']):
                        self.current_frame += 1
                    elif self.ind_dead == len(self.animation_frames['dead']):
                        self.current_frame = len(self.animation_frames['dead']) - 1
                        # Конец игры, если персонаж мертв
                        self.game_over()

            # Отображаем анимацию с учетом направления и гравитации
            if self.direction == 'right':
                if self.grav == 1:
                    self.image = pygame.transform.flip(
                        self.animation_frames[self.current_animation][self.current_frame], False, False)
                else:
                    self.image = pygame.transform.flip(
                        self.animation_frames[self.current_animation][self.current_frame], False, True)
            else:
                if self.grav == 1:
                    self.image = pygame.transform.flip(
                        self.animation_frames[self.current_animation][self.current_frame], True, False)
                else:
                    self.image = pygame.transform.flip(
                        self.animation_frames[self.current_animation][self.current_frame], True, True)

            self.d_x = x_offset_characters[self.name][self.direction][self.current_animation]
            self.mask = pygame.mask.from_surface(self.image)

        def update(self) -> None:
            """
            Обновляет состояние персонажа: движение, анимация, отрисовка.
            """

            # Обработка движения по оси X
            self.moving_x()

            # Обработка движения по оси Y
            self.moving_y()

            # Обновление кадра анимации
            self.get_current_image()

            # Отображение персонажа
            self.draw()

            # Отображение здоровья
            self.draw_hp()

        def draw_stat(self) -> tuple:
            """
            Возвращает параметры здоровья и задержки персонажа

            :return: Кортеж из текущего состояния здоровья и задержки
            """

            return self.sch, self.delay

        def grvit(self) -> None:
            """
            Возвращает текущее значение гравитации персонажа
            :return: Значение гравитации персонажа (float)
            """

            return self.grav

        def gen_mask(self) -> None:
            """
            Генерирует маску для персонажа на основе его текущего изображения
            Маска используется для коллизий с другими объектами
            """

            self.mask = pygame.mask.from_surface(self.image)

        def draw_hp(self) -> None:
            """
            Отображает полоску здоровья персонажа на экране
            Полоска разделена на несколько сегментов в зависимости от максимального здоровья
            Цвет полоски изменяется в зависимости от процента оставшегося здоровья
            """

            # Общее количество сегментов
            segment_count = self.max_hp

            # Ограничиваем здоровье максимальным значением
            self.hp = max(0, min(self.hp, self.max_hp))

            # Количество заполненных сегментов
            segments_filled = int((self.hp / self.max_hp) * segment_count)

            # Размеры полоски
            width, height = 250, 20

            # Начальная позиция
            x, y = 275, 575

            for i in range(segment_count):
                rect = pygame.Rect(x + i * (width // segment_count), y, (width // segment_count), 22)

                if i < segments_filled:
                    # Процент здоровья
                    health_percentage = self.hp / self.max_hp
                    if health_percentage > 0.66:
                        # Зеленый цвет
                        color = (0, 255, 0)
                    elif health_percentage > 0.33:
                        # Желтый цвет
                        color = (255, 255, 0)
                    else:
                        # Красный цвет
                        color = (255, 0, 0)

                    # Отображаем заполненную часть
                    pygame.draw.rect(screen, color, rect)

                    # Отображаем контур
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)
                else:
                    # Отображаем пустую часть
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)

                    # Текстовое отображение текущего здоровья
            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 12)
            text = font.render(f'hp {self.hp}', True, (40, 40, 40))
            text_r = text.get_rect(center=(400, 566))
            self.screen.blit(text, text_r)

        def game_over(self) -> None:
            """
            Окончание игры. Вызывается при смерти персонажа
            Переход к экрану с поражением
            """

            # Переход к сцене проигрыша
            transit('loss')

            # Обработка результатов проигрыша
            res_loss()

            # Изменение экрана
            screen_change('gemplay', 'transition')

        def win(self) -> None:
            """
            Победа. Вызывается при победе персонажа
            Переход к экрану с победой
            """

            # Переход к сцене победы
            transit('win')

            # Обработка результатов победы
            res_win()

            # Изменение экрана
            screen_change('gemplay', 'transition')

        def moving_x(self) -> None:
            """
            Обработка движения персонажа по оси X (влево/вправ)
            Управляется клавишами 'A' и 'D'
            Обрабатывается атака, прыжки и изменение гравитации
            """

            dx = 0
            # Получаем состояние клавиш
            keys = pygame.key.get_pressed()

            # Если персонаж жив
            if self.hp > 0:
                # Если не в атаке
                if not self.attack:
                    if self.sch < self.delay:
                        self.sch += 1
                    else:
                        self.fl_demage = True

                    left_button, middle_button, right_button = pygame.mouse.get_pressed()  # Получаем состояние кнопок мыши

                    # Атака при нажатой левой кнопке мыши
                    if left_button and not self.is_jumping and self.smen_grav and self.fl_demage:
                        self.frame_delay, self.current_frame = 0, 0
                        self.attack, self.fl_demage, self.cause_damage = True, False, True
                        self.sch = 0
                        self.play_sound_attack()

                    # Прыжок при нажатой клавише SPACE
                    if keys[
                        pygame.K_SPACE] and not self.is_jumping and not self.pressing_space and self.velocity_y == 0:
                        self.is_jumping, self.pressing_space = True, True
                        self.velocity_y = -self.jump_height * self.grav
                        self.play_sound_jump()
                    elif not keys[pygame.K_SPACE] and not self.is_jumping:
                        self.pressing_space = False

                    # Движение влево и вправо
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

                    # Изменение гравитации при нажатии W
                    if keys[pygame.K_w] and not self.is_jumping and self.change_graviti:
                        self.play_change_gravity()
                        self.is_jumping = True
                        self.change_graviti = False
                        self.grav = -self.grav
                    elif not keys[pygame.K_w] and not self.change_graviti and not self.is_jumping:
                        self.change_graviti = True

                    # Сохранение старой позиции
                    old_x = self.rect.x

                    self.rect.x = max(min(self.rect.x + dx, self.numb - self.rect.width), 0)

                    # Если столкновение с плитками, отменить движение
                    if pygame.sprite.spritecollide(self, self.tiles, False):
                        self.rect.x = old_x
                    else:
                        if self.rect.x <= 200:
                            self.x = max(min(self.x + dx, 600), 0)
                        elif self.rect.x >= self.numb - 200:
                            self.x = max(min(self.x + dx, 800 - self.rect.width), 200)
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
                else:
                    if self.cause_damage:
                        # Вызов функции, если персонаж причиняет урон
                        self.function_reference()

        def moving_y(self) -> None:
            """
            Обработка движения персонажа по оси Y (вверх/вниз)
            Управляется гравитацией и столкновениями с плитками
            """

            if not self.attack:
                # Увеличиваем скорость по оси Y в зависимости от гравитации
                self.velocity_y += self.gravity * self.grav

                # Изменяем положение по оси Y
                self.rect.y += self.velocity_y

                # Столкновение с плитками
                if collisions := pygame.sprite.spritecollide(self, self.tiles, False):
                    # Если персонаж падал
                    if self.velocity_y > 0:
                        # Корректируем положение
                        self.rect.bottom = collisions[0].rect.top
                        if self.grav == 1:
                            # Заканчиваем прыжок
                            self.is_jumping = False

                    # Если персонаж поднимался
                    elif self.velocity_y < 0:
                        self.rect.top = collisions[0].rect.bottom
                        if self.grav == -1:
                            self.is_jumping = False

                    self.smen_grav = True

                    # Обнуляем скорость
                    self.velocity_y = 0

                # Если персонаж вышел за пределы экрана
                if not (0 < self.rect.y + self.rect.height and self.rect.y < 600):
                    self.hp = 0

                    # Игра окончена
                    self.game_over()

        def cords_map(self) -> tuple:
            """
            Возвращает текущие координаты персонажа по оси X и его позиции на экране

            :return: Кортеж с координатами (x, x_позиция)
            """

            return self.rect.x, self.x

        def taking_damage(self, damag) -> None:
            """
            Персонаж получает урон. Если здоровье меньше или равно 0, вызывается анимация смерти

            :param damag: Сколько урона получает персонаж
            """

            if self.hp > 0:
                # Уменьшаем здоровье
                self.hp -= damag

                # Проигрываем звук повреждения
                self.play_sound_damage()

                # Если здоровье = 0 или меньше
                if self.hp <= 0:
                    # Проигрываем звук смерти
                    self.play_sound_death()
                    self.current_frame = 0

        def cord_bac(self) -> int:
            """
            Возвращает смещение по оси X для фона

            :return: Смещение по оси X
            """

            return self.x_bac

        def pos_player(self) -> list:
            """
            Возвращает текущие координаты и размеры прямоугольника персонажа

            :return: Прямоугольник (rect) персонажа
            """

            return self.rect

        def direct(self) -> str:
            """
            Возвращает текущую сторону персонажа (вправо или влево)

            :return: Направление ('left' или 'right')
            """

            return self.direction

        def dm(self) -> int:
            """
            Возвращает значение урона персонажа

            :return: Урон персонажа
            """

            return self.damage

        def reg(self) -> None:
            """
            Отключает возможность причинять урон персонажем
            """

            self.cause_damage = False
