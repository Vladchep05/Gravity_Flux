import json
import math
import time
import threading
import datetime
from random import randint, random, uniform, sample

from scr.constants import (rating_cost, belonging_to_level, portal_cords, spawn_coordinates, type_card_background,
                           catering_coefficients_levels, catering_coefficients_cards, opening_levels, range_rating,
                           map_index, level_map, rating_character, list_name_card, spavn_mobs, list_tiles,
                           animation_frames_character, animations_mob, coin_animation, maximum_improvement,
                           character_level, level_improvement, x_offset)

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


def loading(fl=False):
    loading_screen.updaute(fl)


def time_check(name_card, time):
    with open('data/better_time.txt', 'r', encoding='utf8') as file:
        data = file.read().split('\n')

    ind = map_index[name_card]
    if (old_time := data[ind + 1]) != '-':
        if int(old_time) > time:
            data[ind + 1] = str(time)
            with open('data/better_time.txt', 'w', encoding='utf8') as file:
                file.writelines([i + '\n' for i in data[:-1]] + [data[-1]])
    else:
        data[ind + 1] = str(time)
        with open('data/better_time.txt', 'w', encoding='utf8') as file:
            file.writelines([i + '\n' for i in data[:-1]] + [data[-1]])


def card_selection_easy() -> None:
    """
    pass
    """

    setting_value('level', 'easy')
    character_types.creating_buttons('Блейв', 'Элиза', 'Кассиан')
    card_selection.creating_buttons(*level_map['easy'])
    transit('cards')
    screen_change('levels', 'transition')


def card_selection_normal() -> None:
    """
    pass
    """

    setting_value('level', 'normal')
    character_types.creating_buttons('Рен', 'Келтор', 'Золтан')
    card_selection.creating_buttons(*level_map['normal'])
    transit('cards')
    screen_change('levels', 'transition')


def card_selection_hard() -> None:
    """
    pass
    """

    setting_value('level', 'hard')
    character_types.creating_buttons('Финн', 'Лиам', 'Эйден')
    card_selection.creating_buttons(*level_map['hard'])
    transit('cards')
    screen_change('levels', 'transition')


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

    data['screen']['improvement_character'] = False
    data['screen']['past_position'] = 'fl_zastavka'
    data['screen']['reset_confirmation'] = False
    data['screen']['character_types'] = False
    data['screen']['loading_screen'] = False
    data['screen']['info_player'] = False
    data['screen']['transition'] = False
    data['screen']['fl_zastavka'] = True
    data['screen']['card_type'] = False
    data['screen']['settings'] = False
    data['screen']['gemplay'] = False
    data['screen']['fl_menu'] = False
    data['screen']['results'] = False
    data['screen']['running'] = True
    data['screen']['levels'] = False
    data['screen']['cards'] = False
    data['screen']['loss'] = False
    data['screen']['win'] = False

    data['gameplay']['type_card'] = "tundra"
    data['gameplay']['name_card'] = ""
    data['gameplay']['character'] = ""
    data['gameplay']['level'] = ""

    with open('data/data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def recording_data(rating, coins, name_card, res):
    with open('data/data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    data['gameplay']['rating'] += rating
    if res == 'win':
        data['gameplay']['coins'] += coins

    for name, rat in rating_cost.items():
        if data['gameplay']['rating'] >= rat:
            data['open_cards'][belonging_to_level[name]][name] = True
        else:
            data['open_cards'][belonging_to_level[name]][name] = False

    if res == 'win' and name_card in ['Рассветный путь', 'Скалистый склон'] and \
            not data['open_levels'][(level := opening_levels[belonging_to_level[name_card]])]:
        data['open_levels'][level] = True

    with open('data/better_time.txt', 'r', encoding='utf8') as file:
        dat = file.read().split('\n')
        max_rat, dat1 = int(dat[0]), dat[1:]

    if data['gameplay']['rating'] > max_rat:
        with open('data/better_time.txt', 'w', encoding='utf8') as file:
            file.writelines([i + '\n' for i in [str(data['gameplay']['rating'])] + dat1[:-1]] + [dat[-1]])

    for name, rat in rating_character.items():
        if data['gameplay']['rating'] >= rat:
            data['open_characters'][name] = True
        else:
            data['open_characters'][name] = False

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


def player_inform(name):
    pl_info.update(name)


def update_improvement(name):
    improvement_character.update_button(name)


def collecting_coins(coin_pos, kill):
    pl_pos = game.player.rect
    if pl_pos.colliderect(coin_pos):
        game.update_coin()
        kill()


def res_loss():
    mobs, time, coin, level, card = game.inf()
    res.update(mobs, time, coin, 'loss', level, card)


def res_win():
    mobs, time, coin, level, card = game.inf()
    res.update(mobs, time, coin, 'win', level, card)


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


def menu_update_but():
    main_menu.update_buttom()


def setting_update_but():
    setting.update_button()


def levels_update_but():
    levels_selection.creating_buttons()


def card_sel_update_but():
    card_selection.creating_buttons(*level_map[check('gameplay', 'level')])


def card_type_update_but():
    card_type.update_button()


def character_update_but():
    character_types.rollback()


def pl_info_update_but():
    pl_info.update_button()


def game_update_but():
    game.update_button()


def results_update_but():
    results.update_button()


def factory_reset():
    transit('loading_screen')
    screen_change('reset_confirmation', 'transition')
    loading()

    with open('data/data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    data['screen']['running'] = True
    data['screen']['past_position'] = 'fl_menu'
    data['screen']['fl_zastavka'] = False
    data['screen']['transition'] = False
    data['screen']['fl_menu'] = False
    data['screen']['settings'] = False
    data['screen']['levels'] = False
    data['screen']['cards'] = False
    data['screen']['card_type'] = False
    data['screen']['character_types'] = False
    data['screen']['info_player'] = False
    data['screen']['loading_screen'] = True
    data['screen']['gemplay'] = False
    data['screen']['win'] = False
    data['screen']['loss'] = False

    data['gameplay']['level'] = ""
    data['gameplay']['name_card'] = ""
    data['gameplay']['type_card'] = ""
    data['gameplay']['character'] = ""
    data['gameplay']['rating'] = 0
    data['gameplay']['coins'] = 0

    data['audio']['music_volume'] = 0.6
    data['audio']['sound_volume'] = 0.6
    data['audio']['mute_music'] = True
    data['audio']['mute_sound'] = True

    data['open_characters']['Блейв'] = True
    data['open_characters']['Золтан'] = False
    data['open_characters']['Кассиан'] = False
    data['open_characters']['Келтор'] = False
    data['open_characters']['Лиам'] = False
    data['open_characters']['Рен'] = False
    data['open_characters']['Финн'] = False
    data['open_characters']['Элиза'] = False
    data['open_characters']['Эйден'] = False

    data['open_levels']['easy'] = True
    data['open_levels']['normal'] = False
    data['open_levels']['hard'] = False

    data['open_cards']['easy']['Тихая долина'] = True
    data['open_cards']['easy']['Прогулка по роще'] = False
    data['open_cards']['easy']['Рассветный путь'] = False

    data['open_cards']['normal']['Встреча ветров'] = False
    data['open_cards']['normal']['Зеленый лабиринт'] = False
    data['open_cards']['normal']['Скалистый склон'] = False

    data['open_cards']['hard']['Заточенные пики'] = False
    data['open_cards']['hard']['Тень дракона'] = False
    data['open_cards']['hard']['Дыхание вечного'] = False

    with open('data/data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)

    with open('data/better_time.txt', 'r', encoding='utf8') as file:
        data = file.read().split('\n')
        max_rat = [data[0] + '\n']

    with open('data/better_time.txt', 'w', encoding='utf8') as file:
        file.writelines(max_rat + ['-\n' * 8] + ['-'])


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

    def __init__(self, screen, sound) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Координаты положения молний
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'), (800, 600))

        # Список цветов молний
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        self.buttons = []

        self.update_buttom()

        # Создание счётчика
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
        for button in self.buttons:
            button.draw()

    def update_buttom(self) -> None:
        # Обновление кнопок
        self.buttons = []

        self.buttons.append(
            ImageButton(
                [260, 125, 280, 60], screen, "images/buttons/main_menu/play_0.png",
                "images/buttons/main_menu/play_1.png", self.start_game, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [260, 200, 280, 60], screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [260, 275, 280, 60], screen, "images/buttons/main_menu/result_0.png",
                "images/buttons/main_menu/result_1.png", self.open_results, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [260, 350, 280, 60], screen, "images/buttons/main_menu/reset_0.png",
                "images/buttons/main_menu/reset_1.png", self.open_reset_confirmation, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [260, 425, 280, 60], screen, "images/buttons/main_menu/exit_0.png",
                "images/buttons/main_menu/exit_1.png",
                self.close, scale=1.0, hover_scale=1.1
            )
        )

    def open_results(self):
        transit('results')
        screen_change('fl_menu', 'transition')
        results_update_but()

    def open_reset_confirmation(self):
        transit('reset_confirmation')
        screen_change('fl_menu', 'transition')
        self.update_buttom()

    def start_game(self) -> None:
        """
        Метод начала игры
        """

        determination_levels()
        transit('levels')
        screen_change('fl_menu', 'transition')
        self.update_buttom()

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('fl_menu', 'transition')
        self.update_buttom()

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

        for button in self.buttons:
            button.handle_event(event)


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

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'),
                                                 (800, 600))

        self.button1, self.button2, self.button3, self.button4, self.button5 = None, None, None, None, None
        self.update_button()

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

        if check('screen', 'past_position') == 'gemplay':
            self.screen.blit(self.text7, self.text7_rect)
            self.screen.blit(self.text8, self.text8_rect)
            self.screen.blit(self.text9, self.text9_rect)
            self.screen.blit(self.text10, self.text10_rect)
            self.screen.blit(self.text11, self.text11_rect)
            self.screen.blit(self.text12, self.text12_rect)

    def return_menu(self):
        start_screen()
        music_menu()
        screen_change('fl_zastavka', 'fl_menu')
        transit('fl_menu')
        screen_change('fl_menu', 'transition')
        self.update_button()

    def play_game(self):
        loading(True)
        transit('loading_screen')
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
        past_position = check('screen', 'past_position')
        # if past_position == 'fl_menu':
        #    menu_update_but()
        # elif past_position == 'levels':
        #    levels_update_but()
        # elif past_position == 'cards':
        #    card_sel_update_but()
        # elif past_position == 'card_type':
        #    card_type_update_but()
        # elif past_position == 'character_types':
        #    character_update_but()
        # elif past_position == 'info_player':
        #    pl_info_update_but()
        # elif past_position == 'gemplay':
        #    game_update_but()
        transit(past_position)
        screen_change('settings', 'transition')
        self.update_button()

    def update_button(self):
        # Создание/бновление кнопок

        zn1 = 'Выключить' if check('audio', 'mute_music') else 'Включить'
        zn2 = 'Выключить' if check('audio', 'mute_sound') else 'Включить'
        self.button1 = Button(
            [80, 120, 220, 50], screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn1, self.onn_off_music, 30,
            "data/BlackOpsOne-Regular_RUS_by_alince.otf", False
        )
        self.button2 = Button(
            [80, 320, 220, 50], screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn2, self.onn_off_sound, 30,
            "data/BlackOpsOne-Regular_RUS_by_alince.otf", False
        )
        self.button3 = ImageButton(
            [280, 510, 240, 60], screen, f"images/buttons/other/back_{randint(0, 3)}.png",
            "images/buttons/other/back_0.png", self.close_seting, scale=1.0, hover_scale=1.1
        )
        self.button4 = ImageButton(
            [30, 510, 240, 60], screen, "images/buttons/other/restart_0.png", "images/buttons/other/restart_1.png",
            self.play_game, scale=1.0, hover_scale=1.1
        )
        self.button5 = ImageButton(
            [530, 510, 240, 60], screen, "images/buttons/other/menu_0.png", "images/buttons/other/menu_1.png",
            self.return_menu, scale=1.0, hover_scale=1.1
        )


class Levels_Selection:
    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
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
        setting_update_but()
        screen_change('levels', 'transition')

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

        self.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw()
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.text, self.text_r)
        for i in self.image:
            self.screen.blit(i[0], i[1])

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        # Проверка событий кнопок
        for button in range(len(self.buttons)):
            if button > 2:
                self.buttons[button].handle_event(event)
            else:
                if check('open_levels', ['easy', 'normal', 'hard'][button]):
                    self.buttons[button].handle_event(event)


class Card_Selection:
    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
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

        transit('card_type')
        card_type_update_but()
        screen_change('cards', 'transition')

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('cards', 'transition')
        self.update_botton()

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора карты
        """

        setting_value('name_card', '')
        transit('levels')
        screen_change('cards', 'transition')
        self.update_botton()

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        self.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw()
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.text, self.text_r)
        for i in self.image:
            self.screen.blit(i[0], i[1])

        self.screen.blit(self.rating, self.rating_r)

        self.screen.blit(self.rt_one, self.rt_r_one)
        self.screen.blit(self.rt_two, self.rt_r_two)
        self.screen.blit(self.rt_free, self.rt_r_free)

    def check_event(self, event) -> None:
        """
        Метод проверки событий
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

        self.card_1 = name1
        self.card_2 = name2
        self.card_3 = name3

        self.level = check('gameplay', 'level')

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
    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Сохранение как экземпляр класса объект окна
        self.screen = screen

        # Создание фона
        self.background = pygame.transform.scale(pygame.image.load('images/background/background.png'), (800, 600))

        self.buttons = []

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

    def update_button(self):
        # Создание кнопок
        self.buttons = []

        self.buttons.append(
            ImageButton(
                [90, 430, 170, 50], screen, "images/buttons/tiles/choco_0.png", "images/buttons/tiles/choco_1.png",
                self.choice_choco, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [305, 430, 170, 50], screen, "images/buttons/tiles/grass_0.png", "images/buttons/tiles/grass_1.png",
                self.choice_grass, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [520, 430, 170, 50], screen, "images/buttons/tiles/snow_0.png", "images/buttons/tiles/snow_1.png",
                self.choice_snow, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(ImageButton(
            [90, 290, 170, 50], screen, "images/buttons/tiles/cake_0.png", "images/buttons/tiles/cake_1.png",
            self.choice_cake, scale=1.0, hover_scale=1.1
        )
        )
        self.buttons.append(
            ImageButton(
                [305, 290, 170, 50], screen, "images/buttons/tiles/dirt_0.png", "images/buttons/tiles/dirt_1.png",
                self.choice_dirt, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [520, 290, 170, 50], screen, "images/buttons/tiles/sand_0.png", "images/buttons/tiles/sand_1.png",
                self.choice_sand, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [90, 150, 170, 50], screen, "images/buttons/tiles/tundra_0.png", "images/buttons/tiles/tundra_1.png",
                self.choice_tundra, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [305, 150, 170, 50], screen, "images/buttons/tiles/castle_0.png", "images/buttons/tiles/castle_1.png",
                self.choice_castle, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [520, 150, 170, 50], screen, "images/buttons/tiles/purple_0.png", "images/buttons/tiles/purple_1.png",
                self.choice_purple, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [500, 500, 210, 50], screen, f"images/buttons/other/back_{randint(0, 3)}.png",
                "images/buttons/other/back_0.png", self.closing_window, scale=1.0, hover_scale=1.1
            )
        )
        self.buttons.append(
            ImageButton(
                [65, 500, 210, 50], screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )

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
        character_update_but()
        screen_change('card_type', 'transition')
        self.update_button()

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('card_type', 'transition')
        self.update_button()

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора типа карты
        """

        setting_value('type_card', '')
        transit('cards')
        screen_change('card_type', 'transition')
        self.update_button()

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        self.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw()
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.text, self.text_r)

        for i in self.images:
            self.screen.blit(i[0], i[1])

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        # Проверка событий кнопок
        for button in self.buttons:
            button.handle_event(event)


class Character_Types:
    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
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

    def chek_open_pl_but(self, name, fl=False):
        if check('open_characters', name):
            if fl:
                return f'images/buttons/characters/{name}_2.png', f'images/buttons/characters/{name}_1.png', 1.0, 1.1
            else:
                return f'images/buttons/characters/{name}_0.png', f'images/buttons/characters/{name}_1.png', 1.0, 1.1
        else:
            return f'images/buttons/characters/close.png', f'images/buttons/characters/close.png', 1.0, 1.0

    def chek_open_pl_img(self, name):
        if check('open_characters', name):
            return f'open/{name}'
        else:
            return f'close/{randint(0, 2)}'

    def player_one(self) -> None:
        # Добавление имени выбраннного персонажа
        setting_value('character', self.name1)
        self.start = True

        self.buttons = []

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
        self.update_button()

    def player_two(self) -> None:
        # Добавление имени выбраннного персонажа
        setting_value('character', self.name2)
        self.start = True

        self.buttons = []

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
        self.update_button()

    def player_three(self) -> None:
        # Добавление имени выбраннного персонажа
        setting_value('character', self.name3)
        self.start = True

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

        img_one, img_two, k1, k2 = self.chek_open_pl_but(self.name3, True)
        self.buttons.append(
            ImageButton(
                [540, 420, 240, 50], screen, img_one, img_two, self.player_three, scale=k1, hover_scale=k2
            )
        )

        self.fl = True
        self.update_button()

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('character_types', 'transition')
        self.update_button()

    def play_game(self):
        """
        Запуск загрузки
        """

        transit('loading_screen')
        screen_change('character_types', 'transition')
        loading(True)

        thread = threading.Thread(target=play_game)
        thread.daemon = True
        thread.start()

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора персонажа
        """

        self.start = False
        setting_value('character', '')
        transit('card_type')
        screen_change('character_types', 'transition')
        self.rollback()

    def open_win_info_pl_one(self):
        player_inform(self.name1)
        transit('info_player')
        screen_change('character_types', 'transition')

    def open_win_info_pl_two(self):
        player_inform(self.name2)
        transit('info_player')
        screen_change('character_types', 'transition')

    def open_win_info_pl_three(self):
        player_inform(self.name3)
        transit('info_player')
        screen_change('character_types', 'transition')

    def draw(self) -> None:
        """
        Метод отрисовки окна
        """

        self.count += 1
        if self.count > 30:
            self.count, self.fl = 0, True

        self.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw()
        if self.start and self.fl:
            self.button.draw()
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.text, self.text_r)
        for i in range(len(self.pl_image)):
            size = self.pl_image[i].get_size()
            self.screen.blit(self.pl_image[i], (40 + 250 * i + ((240 - size[0]) // 2), 170))

        self.screen.blit(self.rating, self.rating_r)

        self.screen.blit(self.rt_one, self.rt_r_one)
        self.screen.blit(self.rt_two, self.rt_r_two)
        self.screen.blit(self.rt_free, self.rt_r_free)

    def check_event(self, event) -> None:
        """
        Метод проверки событий
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
        """

        # Сохранение названия игроков
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3

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
            pygame.image.load(f'images/players/{self.chek_open_pl_img(name1)}.png').convert_alpha()
        )
        self.pl_image.append(
            pygame.image.load(f'images/players/{self.chek_open_pl_img(name2)}.png').convert_alpha()
        )
        self.pl_image.append(
            pygame.image.load(f'images/players/{self.chek_open_pl_img(name3)}.png').convert_alpha()
        )

        self.start = False
        self.fl = False
        self.count = 0

    def rollback(self):
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

        self.update_button()

    def update_button(self):
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
                [200, 385, 80, 22], screen, (255, 255, 255), col1, col2, 'info', self.open_win_info_pl_one, 15,
                "data/BlackOpsOne-Regular_RUS_by_alince.otf"
            )
        )

        if check('open_characters', self.name2):
            col1, col2 = (210, 150, 0), (150, 0, 0)
        else:
            col1, col2 = (120, 120, 120), (120, 120, 120)
        self.buttons.append(
            Button(
                [450, 385, 80, 22], screen, (255, 255, 255), col1, col2, 'info', self.open_win_info_pl_two, 15,
                "data/BlackOpsOne-Regular_RUS_by_alince.otf"
            )
        )

        if check('open_characters', self.name3):
            col1, col2 = (200, 150, 0), (150, 0, 0)
        else:
            col1, col2 = (120, 120, 120), (120, 120, 120)
        self.buttons.append(
            Button(
                [700, 385, 80, 22], screen, (255, 255, 255), col1, col2, 'info', self.open_win_info_pl_three, 15,
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
    def __init__(self, screen):
        self.screen = screen

        self.progress = None
        self.rotation, self.message, self.font, self.clock, self.step, self.fl = None, None, None, None, None, None

        # Создание фона
        self.background = pygame.transform.scale(
            pygame.image.load('images/background/background_loading.jpg'), (800, 600)
        )

        self.pl_music = True

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
        if self.pl_music:
            pygame.mixer.music.load('data/file_music/loading.mp3')
            pygame.mixer.music.set_volume(check('audio', 'music_volume'))
            pygame.mixer.music.play(-1)
            self.pl_music = False

        self.progress = self.step / 20
        self.message = f"Loading... ({int(self.progress * 100)}%)"

        self.rotation += randint(10, 60)
        if self.rotation >= 360:
            self.rotation = 0

        time.sleep(0.03)
        self.step += randint(1, 2)
        # if self.step == 14:
        #     play_game()
        if self.step > 20 and self.fl:
            transit('gemplay')
            screen_change('loading_screen', 'transition')
            pygame.mixer.music.pause()
        elif self.step > 20 and not self.fl:
            music_menu()
            transit(check('screen', 'past_position'))
            screen_change('loading_screen', 'transition')

        self.draw()

    def updaute(self, fl):
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
    Класс, реализующий кнопку с изображением.
    """

    def __init__(self, coord, screen, image_path, hover_image_path, funk, scale=1.0, hover_scale=1.2):
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения.
        """
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), coord[2:])
        self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
        self.funk = funk  # Функция для вызова при нажатии
        self.scale = scale
        self.hover_scale = hover_scale
        self.current_image = self.image
        self.rect = self.current_image.get_rect(topleft=coord[:2])  # Изначальный rect на основе исходного изображения
        self.original_width = self.rect.width
        self.original_height = self.rect.height
        self.is_hovered = False
        self.update_image()  # Первоначальное масштабирование

    def update_image(self):
        """Обновляет изображение и rect в соответствии с текущим масштабом."""
        scale = self.hover_scale if self.is_hovered else self.scale
        width = int(self.original_width * scale)
        height = int(self.original_height * scale)
        image = self.hover_image if self.is_hovered else self.image
        self.current_image = pygame.transform.scale(image, (width, height))
        # Обновляем rect, сохраняя центр кнопки на месте
        center = self.rect.center
        self.rect = self.current_image.get_rect(center=center)

    def draw(self):
        """
        Метод отрисовки кнопки.
        """
        self.screen.blit(self.current_image, self.rect)

    def handle_event(self, event):
        """
        Метод, который обрабатывает события, связанные с кнопкой.
        """
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if not self.is_hovered:
                    self.is_hovered = True
                    self.update_image()  # Обновляем изображение при наведении
            else:
                if self.is_hovered:
                    self.is_hovered = False
                    self.update_image()  # Возвращаем исходное изображение

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.funk:
                self.funk()  # Вызов функции
                play_sound()


class Button:
    """
    Класс реализующий кнопку
    """

    def __init__(self, coord, screen, collor_text, hover_color, collor_button, text, funk, zn, font="data/Docker.ttf",
                 fl=True, scale=1.0, hover_scale=1.1) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """
        # Задаёт координаты
        self.original_rect = pygame.Rect(coord)  # Сохраняем оригинальные координаты
        self.rect = self.original_rect.copy()  # rect для текущего состояния (с учетом масштаба)
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
        self.font_size = zn  # Сохраняем размер шрифта
        self.font = pygame.font.Font(font, zn)  # Создаем шрифт

        # Реализация текста для кнопки
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.collor_text)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        # Флаг, показывающий находится ли курсор на кнопке
        self.hove = False
        self.scale = scale  # Изначальный масштаб
        self.hover_scale = hover_scale  # Масштаб при наведении

        self.update_scale()  # Применяем начальный масштаб

    def update_font(self):
        """Обновляет шрифт и текстовую поверхность"""
        self.font = pygame.font.Font(self.font_name,
                                     int(self.font_size * (self.hover_scale if self.hove else self.scale)))
        self.text_surface = self.font.render(self.text, True, self.collor_text)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def update_scale(self):
        """Обновляет размер кнопки"""
        scale = self.hover_scale if self.hove else self.scale
        width = int(self.original_rect.width * scale)
        height = int(self.original_rect.height * scale)
        center = self.rect.center  # Сохраняем центр
        self.rect = pygame.Rect(0, 0, width, height)  # Создаем новый rect
        self.rect.center = center  # Восстанавливаем центр
        self.update_font()  # Обновляем шрифт при изменении размера

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
        """
        # Проверяет тип события (наведения на кнопку курсора)
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if not self.hove:
                    self.hove = True
                    self.update_scale()  # Обновляем размер
            else:
                if self.hove:
                    self.hove = False
                    self.update_scale()  # Возвращаем размер

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


class Improvement_character:
    def __init__(self, screen):
        self.character, self.price = None, None
        self.damage, self.hp, self.delay = None, None, None
        self.screen = screen
        self.buttons = []

    def draw(self) -> None:
        """
        Метод отрисовки слайдеров
        """

        self.screen.fill((0, 0, 0))
        for button in self.buttons:
            button.draw()

    def cost_calculation(self):
        return

    def update_button(self, name_character):
        self.buttons = []
        self.character = name_character

        with open(f'data/characteristics_character/{name_character}.txt', 'r', encoding='utf8') as file:
            data = file.read().split('\n')

        self.damage, self.hp, self.delay = data[1], data[0], data[4]

        self.price = level_improvement[character_level[name_character]]

        self.buttons.append(
            ImageButton(
                [50, 400, 200, 50], screen, f"images/buttons/price/price_{self.price}_0.png",
                f"images/buttons/price/price_{self.price}_1.png", self.improvement_damage, scale=1.0,
                hover_scale=1.1
            )
        )

        self.buttons.append(
            ImageButton(
                [300, 400, 200, 50], screen, f"images/buttons/price/price_{self.price}_0.png",
                f"images/buttons/price/price_{self.price}_1.png", self.improvement_hp, scale=1.0, hover_scale=1.1
            )
        )

        self.buttons.append(
            ImageButton(
                [550, 400, 200, 50], screen, f"images/buttons/price/price_{self.price}_1.png",
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
                [55, 500, 210, 50], screen, "images/buttons/other/settings_0.png",
                "images/buttons/other/settings_1.png", self.open_setting, scale=1.0, hover_scale=1.1
            )
        )

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора типа карты
        """

        setting_value('improvement_character', '')
        transit('info_player')
        screen_change('improvement_character', 'transition')

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        screen_change('improvement_character', 'transition')
        self.update_button(self.character)

    def improvement_damage(self):
        max_damage = maximum_improvement[self.character]['damage']

        if check('gameplay', 'coins') > self.price:
            if self.damage < max_damage:
                self.damage += 1

        data = self.read_data()
        data[1] = self.damage
        self.write_data([i + '\n' for i in data[:-1]] + [data[-1]])

    def improvement_hp(self):
        max_hp = maximum_improvement[self.character]['hp']

        if check('gameplay', 'coins') > self.price:
            if self.hp < max_hp:
                self.hp += 1

        data = self.read_data()
        data[0] = self.hp
        self.write_data([i + '\n' for i in data[:-1]] + [data[-1]])

    def improvement_delay(self):
        max_delay = maximum_improvement[self.character]['delay']

        if check('gameplay', 'coins') > self.price:
            if self.delay < max_delay:
                self.delay += 1

        data = self.read_data()
        data[4] = self.delay
        self.write_data([i + '\n' for i in data[:-1]] + [data[-1]])

    def read_data(self):
        with open(f'data/characteristics_character/{self.character}.txt', 'r', encoding='utf8') as file:
            data = file.read().split('\n')

        return data

    def write_data(self, data):
        with open(f'data/characteristics_character/{self.character}.txt', 'w', encoding='utf8') as file:
            file.writelines(data)

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        for button in self.buttons:
            button.handle_event(event)


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


class Reset_confirmation:
    def __init__(self, screen):
        self.screen = screen

        self.button1, self.button2 = None, None

        # Создание текста
        font1 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 30)

        self.text1 = font1.render(f'Вы действительно хотите сбросить', True, (0, 255, 255))
        self.text_r1 = self.text1.get_rect(center=(400, 150))

        self.text2 = font1.render(f'настройки игры?', True, (255, 255, 0))
        self.text_r2 = self.text2.get_rect(center=(400, 185))

        font2 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 20)

        self.text3 = font2.render(f'(все ваши достижения и результаты удаляться)', True, (140, 40, 230))
        self.text_r3 = self.text3.get_rect(center=(400, 235))

        self.update_button()

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.button1.draw()
        self.button2.draw()

        self.screen.blit(self.text1, self.text_r1)
        self.screen.blit(self.text2, self.text_r2)
        self.screen.blit(self.text3, self.text_r3)

    def update_button(self):
        self.button1 = ImageButton(
            [500, 400, 200, 80], screen, 'images/buttons/other/yes_0.png', 'images/buttons/other/yes_1.png',
            self.update, scale=1.0, hover_scale=1.1
        )
        self.button2 = ImageButton(
            [100, 400, 200, 80], screen, 'images/buttons/other/no_0.png', 'images/buttons/other/no_1.png',
            self.close_window, scale=1.0, hover_scale=1.1
        )

    def update(self):
        factory_reset()

    def close_window(self):
        transit('fl_menu')
        screen_change('reset_confirmation', 'transition')
        self.update_button()

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        self.button1.handle_event(event)
        self.button2.handle_event(event)


class Results:
    def __init__(self, screen):
        self.screen = screen

        self.button = None
        self.list_time, self.list_name_card = [], []
        self.text1, self.text2, self.text3, self.text4 = None, None, None, None
        self.text_r1, self.text_r2, self.text_r3, self.text_r4 = None, None, None, None
        self.text5, self.text6 = None, None
        self.text_r5, self.text_r6 = None, None

        self.update_button()

    def update_button(self):
        self.button = ImageButton(
            [550, 500, 210, 50], screen, f"images/buttons/other/back_{randint(0, 3)}.png",
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

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.button.draw()

        for card in self.list_name_card:
            screen.blit(card[0], card[1])

        for time in self.list_time:
            screen.blit(time[0], time[1])

        for y in range(78, 484, 45):
            pygame.draw.line(self.screen, (255, 255, 255), [20, y], [780, y], 2)
        pygame.draw.line(self.screen, (255, 255, 255), [400, 40], [400, 483], 2)

        self.screen.blit(self.text1, self.text_r1)
        self.screen.blit(self.text2, self.text_r2)
        self.screen.blit(self.text3, self.text_r3)
        self.screen.blit(self.text4, self.text_r4)
        self.screen.blit(self.text5, self.text_r5)
        self.screen.blit(self.text6, self.text_r6)

    def closing_window(self):
        transit('fl_menu')
        screen_change('results', 'transition')
        self.update_button()

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        self.button.handle_event(event)


class Playear_info:
    def __init__(self, screen):
        self.screen = screen

        self.buttons = []
        self.update_button()

        self.image, self.name = None, None

        self.text1, self.text_r1, self.text2, self.text_r2, self.text3 = None, None, None, None, None
        self.text_r3, self.text4, self.text_r4, self.text5, self.text_r5 = None, None, None, None, None
        self.text6, self.text_r6 = None, None

    def draw(self):
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

        for button in self.buttons:
            button.draw()

    def update_button(self):
        self.buttons.append(
            Button(
                [560, 500, 180, 50], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Назад',
                self.closing_window, 25
            )
        )
        self.buttons.append(
            Button(
                [330, 500, 180, 50], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Прокачать',
                self.open_improvement, 25
            )
        )
        self.buttons.append(
            Button(
                [100, 500, 180, 50], screen, (255, 255, 255), (218, 165, 32), (220, 20, 60), 'Настройки',
                self.open_setting, 25
            )
        )

    def open_improvement(self):
        """
        Метод открытия окна улучшения персонажа
        """

        update_improvement(self.name)
        transit('improvement_character')
        setting_update_but()
        screen_change('info_player', 'transition')

    def open_setting(self) -> None:
        """
        Метод открытия настроек
        """

        transit('settings')
        setting_update_but()
        screen_change('info_player', 'transition')

    def closing_window(self) -> None:
        """
        Метод закрытия окна выбора типа карты
        """

        transit('character_types')
        character_update_but()
        screen_change('info_player', 'transition')

    def update(self, name):
        self.name = name
        self.image = pygame.image.load(f'images/players/open/{name}.png')

        # Создание текста
        font1 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 27)

        self.text1 = font1.render(f'Имя персонажа: {self.name}', True, (255, 255, 255))
        self.text_r1 = self.text1.get_rect(center=(300, 120))

        font2 = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 24)

        date = check('characteristics', self.name)

        self.text2 = font2.render(f'Здоровье: {date[0]}', True, pygame.Color('green'))
        self.text_r2 = self.text2.get_rect(center=(300, 200))

        self.text3 = font2.render(f'Атака: {date[1]}', True, pygame.Color('red'))
        self.text_r3 = self.text3.get_rect(center=(300, 240))

        self.text4 = font2.render(f'Пыжок: {date[2]}', True, pygame.Color('yellow'))
        self.text_r4 = self.text4.get_rect(center=(300, 280))

        self.text5 = font2.render(f'Скорость: {date[3]}', True, (0, 255, 255))
        self.text_r5 = self.text5.get_rect(center=(300, 320))

        self.text6 = font2.render(f'Задержка: {"{:.2f}".format(date[4] / 60)} сек', True, (255, 0, 255))
        self.text_r6 = self.text6.get_rect(center=(300, 360))

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        for button in self.buttons:
            button.handle_event(event)


class Gamplay:
    def __init__(self, screen):
        self.screen = screen
        self.level, self.name_card, self.background_map, self.cards, self.tile_images = None, None, None, None, None
        self.character, self.tiles, self.port, self.player, self.numb = None, None, None, None, None
        self.time, self.dis_time, self.dis_time_rect, self.start_time, self.date_start = None, None, None, None, None
        self.spis_enemy = []
        self.count, self.ind, self.mobs, self.coin = 0, 0, 0, 0
        self.anim_port = [
            pygame.transform.scale(pygame.image.load(f'images/portal/{i}.png'), (32, 80)) for i in range(4)
        ]
        self.image_coin = pygame.transform.scale(pygame.image.load('images/coin/0.png'), (32, 32))
        self.button_setting = None
        self.update_button()

    def loading(self):
        self.time = 0
        self.start_time = f'{datetime.datetime.now().time():%H:%M}'
        self.date_start = '.'.join(f'{datetime.datetime.now().date()}'.split('-')[::-1])
        self.level = check('gameplay', 'level')
        self.coin, self.mobs = 0, 0
        self.name_card = check('gameplay', 'name_card')
        type_card = check('gameplay', 'type_card')
        self.background_map = pygame.transform.scale(
            pygame.image.load(type_card_background[type_card]).convert_alpha(), (800, 600))
        self.tiles = pygame.sprite.Group()
        self.generate_map(type_card)
        self.creating_enemy()
        self.port = portal_cords[self.name_card]
        self.player = self.Player()
        self.player.definition_character(
            check('gameplay', 'character'), self.screen, spawn_coordinates[self.name_card], self.tiles, self.numb,
            self.collision_with_mobs
        )

    def update_button(self):
        # Сщздание/обновление кнопок
        self.button_setting = Button([6, 6, 32, 32], screen, (255, 255, 255), (100, 100, 100), (0, 0, 0), 'X',
                                     self.open_setting, 32, "data/BlackOpsOne-Regular_RUS_by_alince.otf")

    def draw(self):
        self.time += 1
        self.teleport()
        self.draw_map()
        self.draw_enemy()
        self.draw_stats()
        self.draw_portal()
        self.draw_coin()
        self.player.update()

    def draw_portal(self):
        self.count += 1
        if self.count > 10:
            self.count = 0
            self.ind = (self.ind + 1) % len(self.anim_port)

        num_one, num_two = self.player.cords_map()
        pos_port = (self.port[0] - (num_one - num_two), self.port[1])
        if -32 < pos_port[0] < 800 and -32 < pos_port[1] < 600:
            self.screen.blit(self.anim_port[self.ind], pos_port)

    def draw_stats(self):
        current_value, max_value = self.player.draw_stat()
        center_x, center_y = 765, 563
        radius = 18
        start_angle = -math.pi / 2  # Начинаем с 90 градусов (верх)
        end_angle = start_angle + (2 * math.pi * ((current_value / max_value) * 100 / 100))

        points = [[center_x, center_y]]  # Начальная точка в центре круга
        for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1):
            rad = math.radians(angle)
            x = int(center_x + radius * math.cos(rad))
            y = int(center_y + radius * math.sin(rad))
            points.append((x, y))
        if len(points) > 2:
            pygame.draw.polygon(self.screen, (30, 144, 255, 180), points)
        pygame.draw.circle(screen, (10, 10, 10), (center_x, center_y), radius + 2, 2)

        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 12)
        text = font.render(f'recharge', True, (0, 0, 0))
        text_r = text.get_rect(center=(765, 589))
        self.screen.blit(text, text_r)

    def draw_coin(self):
        self.screen.blit(self.image_coin, [760, 8])
        font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 22)
        text = font.render(f'{self.coin}', True, (255, 255, 255))
        text_r = text.get_rect(center=(747, 26))
        self.screen.blit(text, text_r)

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
        self.spis_enemy = pygame.sprite.Group()

        number_mobs, data, damage, hp = spavn_mobs[self.name_card]
        data_mobs = sample(data, number_mobs)
        for i in data_mobs:
            range_x, y, rad, rad_max, grav = i
            x = randint(range_x[0], range_x[1])
            self.spis_enemy.add(
                self.Enemy(
                    screen, x, y, randint(2, 3), self.tiles, grav, 10, rad, rad_max, animations_mob[randint(0, 1)],
                    randint(hp[0], hp[1]), self.collision_with_player, randint(60, 80), randint(damage[0], damage[1]),
                    self.pos_pl, self.kill_mob
                )
            )

    def pos_pl(self):
        return self.player.pos_player()

    def kill_mob(self):
        self.mobs += 1

    def collision_with_player(self, pos_mob, dmg, reg, napr):
        pos_pl = self.player.pos_player()

        if pos_pl.colliderect(pos_mob):
            if pos_pl[0] > pos_mob[0] and napr == 'right' or pos_pl[0] < pos_mob[0] and napr == 'left':
                self.player.taking_damage(dmg)
                reg()

    def collision_with_mobs(self):
        pos_pl = self.player.pos_player()
        if mob := pygame.sprite.spritecollide(self.player, self.spis_enemy, False):
            pos_mob = mob[0].pos_mobs()

            if pos_pl[0] > pos_mob[0] and self.player.direct() == 'left' or \
                    pos_pl[0] < pos_mob[0] and self.player.direct() == 'right':
                mob[0].taking_damage(self.player.dm())
                self.player.reg()

    def draw_enemy(self):
        num_one, num_two = self.player.cords_map()
        pl_rect = self.player.pos_player()
        graviti_player = self.player.grvit()
        for enemy in self.spis_enemy:
            enemy.draw(num_one, num_two, graviti_player, pl_rect)

    def inf(self):
        return self.mobs, self.time, self.coin, self.level, self.name_card

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
        setting_update_but()
        screen_change('gemplay', 'transition')

    def teleport(self):
        port_rect = self.anim_port[0].get_rect()
        port_rect.x = self.port[0]
        port_rect.y = self.port[1]
        pl_rect = self.player.pos_player()
        if pl_rect.colliderect(port_rect):
            self.player.win()

    def load_images(self, t_s, number_cart):
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

        for key, image in images.items():
            images[key] = pygame.transform.scale(image, (t_s, t_s))

        return images

    def generate_map(self, type_card):
        tile_images = self.load_images(32, type_card)
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

    def update_coin(self):
        self.coin += 1

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
        def __init__(self, screen, x, y, speed, list_tile, grav, jump, rad, max_rad, animal, hp,
                     function_reference, delay, damage, pl_pos, func):
            super().__init__()

            self.image = None

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

            self.ind_dead = 0
            self.counter = 0
            self.num_1 = 0
            self.num_2 = 0
            self.count = 0
            self.sch = 0
            self.ind = 0
            self.cnt = 0
            self.v_y = 0

            self.is_jump = 1

            self.current_animation = 'idle'
            self.napr = 'right'
            self.img = 'right'

            self.function_reference = function_reference
            self.coin = self.Coin(grav)
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
            self.rad = rad
            self.hp = hp
            self.x = x
            self.y = y

            self.update_image()
            self.rect = self.image.get_rect(topleft=(x, y))

        def draw(self, pos_player, pos_player_display, grav_pl, pl_rect):
            self.update_x(pos_player, grav_pl, pl_rect)
            self.update_y()
            self.update_image()
            enemy_pos = (self.rect.x - (pos_player - pos_player_display), self.rect.y)
            if -self.rect.width < enemy_pos[0] < 800:
                self.screen.blit(self.image, enemy_pos)

            if self.cn:
                self.coin.update()
                self.coin.draw(self.screen, pos_player - pos_player_display)

        def kill(self):
            self.cn = False

        class Coin(pygame.sprite.Sprite):
            def __init__(self, grav):
                super().__init__()

                self.kill = None
                self.y = None

                self.pod = True

                self.speed = 1
                self.count = 0
                self.ind = 0
                self.sch = 0

                self.rad = randint(50, 80)
                self.num = randint(6, 9)

                self.v_y = -self.num * grav
                self.animal = coin_animation
                self.image = self.animal[0]
                self.grav = grav

                self.rect = self.image.get_rect()

            def update(self):
                self.count += 1
                if self.count > 3:
                    self.count = 0
                    self.ind = (self.ind + 1) % len(self.animal)

                    self.image = self.animal[self.ind]

                    self.v_y += self.speed * self.grav

                    if self.rect.y == self.y:
                        self.v_y = -self.num * self.grav

                    self.rect.y += self.v_y

                if self.sch < 120:
                    self.sch += 1
                else:
                    collecting_coins(self.rect, self.kill)

            def draw(self, screen, x):
                screen.blit(self.image, [self.rect.x - x, self.rect.y])

            def x_y(self, x, y, kill):
                self.rect.x = x
                self.rect.y = y - (self.rect.height if self.grav == 1 else 0)
                self.y = y - (self.rect.height if self.grav == 1 else 0)
                self.kill = kill

        def update_image(self):
            if self.hp > 0:
                if not self.attack:
                    self.count += 1
                    if self.count > 5:
                        self.count = 0
                        if self.is_jump:
                            self.current_animation = 'jump'
                        elif self.run:
                            self.current_animation = 'run'
                        else:
                            self.current_animation = 'idle'
                        self.ind = (self.ind + 1) % len(self.animal[self.current_animation])
                else:
                    self.count += 1
                    if self.count > 8:
                        self.count = 0
                        self.current_animation = 'attack'
                        self.ind += 1
                        if self.ind >= len(self.animal[self.current_animation]):
                            self.attack = False
                            self.cause_damage = False
                            self.ind = 0
            else:
                self.count += 1
                if self.count > 5:
                    self.count = 0
                    self.current_animation = 'dead'
                    if self.ind_dead == 0:
                        self.ind += 1
                        if self.ind >= len(self.animal[self.current_animation]):
                            self.ind_dead += 1
                            self.ind = len(self.animal[self.current_animation]) - 1
                    else:
                        if self.fl_coin:
                            self.coin.x_y(
                                self.rect.x + 10, self.rect.y + (self.rect.height if self.grav == 1 else 0), self.kill
                            )
                            self.fl_coin = False
                            self.func()
                        self.ind = len(self.animal[self.current_animation]) - 1

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

        def update_x(self, pos_player, grav_pl, pl_rect):
            if self.hp > 0:
                if not self.attack:
                    self.sch += 1
                    if self.sch > self.delay:
                        self.sch = 0
                        self.fl_demage = True

                    if self.rect.colliderect(pl_rect) and self.grav == grav_pl and self.fl_demage:
                        if pos_player < self.rect.x and self.collision:
                            self.collision = False
                            self.rect.x -= 5
                        self.attack, self.fl_demage, self.cause_damage = True, False, True
                        self.ind = 0
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
                    if pos_player < self.rect.x:
                        self.img = 'left'
                    else:
                        self.img = 'right'
                    if self.cause_damage:
                        self.function_reference(self.rect, self.damage, self.reg, self.img)

        def change_x(self, speed):
            old_x = self.rect.x
            self.rect.x += speed
            if pygame.sprite.spritecollide(self, self.list_tile, False):
                self.rect.x = old_x
                if not self.is_jump:
                    self.v_y = -self.jump * self.grav
                    self.is_jump = True

        def update_y(self):
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

        def taking_damage(self, dm):
            self.hp -= dm
            if self.hp <= 0:
                self.ind = 0
                self.cn = True

        def pos_mobs(self):
            return self.rect

        def reg(self):
            self.cause_damage = False

        def dm(self):
            return self.damage

    class Player(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()

            self.change_graviti = True
            self.cause_damage = True
            self.is_jumping = True
            self.smen_grav = True
            self.fl_demage = True

            self.pressing_space = False
            self.attack = False
            self.run = False

            self.count = 6

            self.grav = 1

            self.current_frame = 0
            self.frame_delay = 0  # Задержка между кадрами анимации
            self.frame_timer = 0  # Таймер для анимации
            self.velocity_y = 0
            self.ind_dead = 0
            self.x_bac = 0
            self.sch = 0

            self.current_animation = 'idle'
            self.direction = 'right'

            self.x, self.screen, self.hp, self.max_hp, self.speed, self.tiles = None, None, None, None, None, None
            self.gravity, self.numb, self.delay, self.jump_height, self.damage = None, None, None, None, None
            self.animation_frames, self.function_reference, self.image, self.rect = None, None, None, None
            self.d_x, self.name = None, None

        def definition_character(self, name, screen, cords, tiles, numb, function_reference):

            with open(f'data/characteristics_character/{name}.txt', 'r', encoding='utf8') as file:
                date = list(map(int, file.read().split('\n')))

            gravity = 0.5
            hp, damage, jump_height, speed, delay = date[0], date[1], date[2], date[3], date[4]

            self.animation_frames = animation_frames_character[name]
            self.function_reference = function_reference
            self.jump_height = jump_height
            self.gravity = gravity
            self.damage = damage
            self.screen = screen
            self.delay = delay
            self.speed = speed
            self.tiles = tiles
            self.x = cords[0]
            self.max_hp = hp
            self.numb = numb
            self.name = name
            self.d_x = 0
            self.hp = hp

            # Инициализация изображения и rect
            self.image = pygame.transform.flip(self.animation_frames['idle'][0], False, False)
            self.rect = self.image.get_rect(topleft=(cords[0], cords[1]))
            self.rect.width = 50

        def draw(self):
            self.screen.blit(self.image, (self.x + self.d_x, self.rect.y))
            pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.rect.y, 50, self.rect.height), 2)

        def get_current_image(self):
            """
            Возвращает текущий кадр анимации с учетом направления
            """

            old = self.current_animation
            if self.hp > 0:
                if not self.attack:
                    if self.change_graviti:
                        if self.is_jumping:
                            self.current_animation = 'jump'
                        else:
                            if self.run:
                                self.current_animation = 'run'
                            else:
                                self.current_animation = 'idle'
                    else:
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
                    self.current_animation = 'attack'
                    self.frame_delay += 1
                    if self.frame_delay > self.count:
                        self.frame_delay = 0
                        self.current_frame = self.current_frame + 1
                        if self.current_frame >= len(self.animation_frames[self.current_animation]):
                            self.attack = False
                            self.current_frame = 0
            else:
                self.frame_delay += 1
                if self.frame_delay > self.count + 2:
                    self.frame_delay = 0
                    self.current_animation = 'dead'
                    if self.ind_dead < len(self.animation_frames['dead']):
                        self.ind_dead += 1

                    if self.ind_dead == len(self.animation_frames['dead']):
                        self.current_frame = len(self.animation_frames[self.current_animation]) - 1
                        self.game_over()
                    else:
                        self.current_frame = (self.current_frame + 1) % len(
                            self.animation_frames[self.current_animation])

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

            self.d_x = x_offset[self.name][self.direction][self.current_animation]
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            self.moving_x()
            self.moving_y()
            self.get_current_image()
            self.draw()
            self.draw_hp()

        def draw_stat(self):
            return self.sch, self.delay

        def grvit(self):
            return self.grav

        def draw_hp(self):
            segment_count = self.max_hp
            self.hp = max(0, min(self.hp, self.max_hp))
            segments_filled = int((self.hp / self.max_hp) * segment_count)

            width, height = 250, 20
            x, y = 275, 575

            for i in range(segment_count):
                rect = pygame.Rect(x + i * (width // segment_count), y, (width // segment_count), 22)

                if i < segments_filled:
                    health_percentage = self.hp / self.max_hp
                    if health_percentage > 0.66:
                        color = (0, 255, 0)
                    elif health_percentage > 0.33:
                        color = (255, 255, 0)
                    else:
                        color = (255, 0, 0)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)
                else:
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)

            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 12)
            text = font.render(f'hp {self.hp}', True, (40, 40, 40))
            text_r = text.get_rect(center=(400, 566))
            self.screen.blit(text, text_r)

        def game_over(self):
            transit('loss')
            res_loss()
            screen_change('gemplay', 'transition')

        def win(self):
            transit('win')
            res_win()
            screen_change('gemplay', 'transition')

        def moving_x(self):
            dx = 0
            keys = pygame.key.get_pressed()

            if self.hp > 0:
                if not self.attack:
                    if self.sch < self.delay:
                        self.sch += 1
                    else:
                        self.fl_demage = True

                    if keys[pygame.K_h]:
                        self.hp -= 1

                    left_button, middle_button, right_button = pygame.mouse.get_pressed()

                    if left_button and not self.is_jumping and self.smen_grav and self.fl_demage:
                        self.frame_delay, self.current_frame = 0, 0
                        self.attack, self.fl_demage, self.cause_damage = True, False, True
                        self.sch = 0

                    if keys[
                        pygame.K_SPACE] and not self.is_jumping and not self.pressing_space and self.velocity_y == 0:
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
                    self.rect.x = max(min(self.rect.x + dx, self.numb - self.rect.width), 0)
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
                        self.function_reference()

        def moving_y(self):
            if not self.attack:
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

                if not (0 < self.rect.y + self.rect.height and self.rect.y < 600):
                    self.hp = 0
                    self.game_over()

        def cords_map(self):
            return self.rect.x, self.x

        def taking_damage(self, damag):
            self.hp -= damag
            if self.hp >= 0:
                self.current_frame = 0

        def cord_bac(self):
            return self.x_bac

        def pos_player(self):
            return self.rect

        def direct(self):
            return self.direction

        def dm(self):
            return self.damage

        def reg(self):
            self.cause_damage = False


class Result:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("images/background/background.png").convert()

        self.button1 = Button(
            [60, 520, 200, 50], screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Restart', self.restart, 30
        )
        self.button2 = Button(
            [540, 520, 200, 50], screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Menu', self.return_menu, 30
        )

        self.time, self.mobs, self.coins, self.res, self.rat, self.name_level = None, None, None, None, None, None
        self.name_card, self.font = None, None
        self.confetti = []

    def return_menu(self):
        start_screen()
        music_menu()
        screen_change('fl_zastavka', 'fl_menu')
        transit('fl_menu')
        screen_change('fl_menu', 'transition')

    def restart(self):
        loading()
        transit('loading_screen')
        screen_change('character_types', 'transition')

        thread = threading.Thread(target=play_game)
        thread.daemon = True
        thread.start()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 36)

        if self.res == 'win':
            self.screen.blit(self.background, (0, 0))

            text_surface = self.font.render('ПОБЕДА!', True, (255, 255, 0))
            text_rect = text_surface.get_rect(center=(400, 100))
            self.screen.blit(text_surface, text_rect)

            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 24)
            congrats_text = font.render('Превосходно! Вы одержали победу!', True, (0, 255, 255))
            congrats_rect = congrats_text.get_rect(center=(400, 160))
            self.screen.blit(congrats_text, congrats_rect)

            if not self.confetti:
                self.init_confetti()

            self.update_confetti()
            self.draw_confetti()

        else:
            self.screen.blit(self.background, (0, 0))
            text_surface = self.font.render('ПОРАЖЕНИЕ', True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(400, 100))
            self.screen.blit(text_surface, text_rect)

            font = pygame.font.Font("data/BlackOpsOne-Regular_RUS_by_alince.otf", 20)
            text_sur = font.render('Повезёт в следующий раз...', True, (0, 255, 255))
            text_rct = text_sur.get_rect(center=(400, 165))
            self.screen.blit(text_sur, text_rct)
        if self.time < 3600:
            time = f'{self.time // 60}сек'
        elif self.time < 216000:
            time = f'{self.time // 3600}мин {self.time % 3600 // 60}сек'
        else:
            time = f'{self.time // 216000}ч {self.time % 216000 // 3600}мин {self.time % 216000 % 3600 // 60}сек'
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

        self.button1.draw()
        self.button2.draw()

    def check_event(self, event) -> None:
        """
        Метод проверки событий
        """

        self.button1.handle_event(event)
        self.button2.handle_event(event)

    def rating_calculation(self):
        """
        Расчёт рейтинг на основе игровой статистики
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

        recording_data(rating, self.coins, self.name_card, self.res)
        time_check(self.name_card, self.time)

        return rating

    def update(self, mobs, time, coins, res, name_level, name_card):
        self.time = time
        self.mobs = mobs
        self.coins = coins
        self.res = res
        self.name_level = name_level
        self.name_card = name_card
        self.rat = self.rating_calculation()

    def init_confetti(self):
        """
        Инициализация частицы конфетти
        """

        for _ in range(200):
            x = randint(0, self.screen.get_width())
            y = randint(0, self.screen.get_height())
            size = randint(5, 15)
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            speed_x = uniform(-2, 2)  # Add horizontal movement
            speed_y = uniform(1, 5)
            self.confetti.append({'x': x, 'y': y, 'size': size, 'color': color, 'speed_x': speed_x, 'speed_y': speed_y})

    def update_confetti(self):
        """
        Обновление положение частиц конфетти
        """

        for particle in self.confetti:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']

            if particle['x'] < 0:
                particle['x'] = self.screen.get_width()
            elif particle['x'] > self.screen.get_width():
                particle['x'] = 0

            if particle['y'] > self.screen.get_height():
                particle['y'] = 0

    def draw_confetti(self):
        """
        Рисовка частиц конфетти на экране
        """

        for particle in self.confetti:
            pygame.draw.circle(
                self.screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size']
            )


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
            elif check('screen', 'reset_confirmation'):
                reset_confirmation.check_event(event)
            elif check('screen', 'results'):
                results.check_event(event)
            elif check('screen', 'levels'):
                levels_selection.check_event(event)
            elif check('screen', 'cards'):
                card_selection.check_event(event)
            elif check('screen', 'card_type'):
                card_type.check_event(event)
            elif check('screen', 'character_types'):
                character_types.check_event(event)
            elif check('screen', 'improvement_character'):
                improvement_character.check_event(event)
            elif check('screen', 'info_player'):
                pl_info.check_event(event)
            elif check('screen', 'gemplay'):
                game.check_event(event)
            elif check('screen', 'loss') or check('screen', 'win'):
                res.check_event(event)

        if check('screen', 'fl_zastavka'):
            if pygame.time.get_ticks() - start_time >= 8600:
                screen_change('fl_zastavka', 'fl_menu')
                music_menu()
            zastavka.draw()
        elif check('screen', 'fl_menu'):
            main_menu.draw()
        elif check('screen', 'settings'):
            setting.draw()
        elif check('screen', 'reset_confirmation'):
            reset_confirmation.draw()
        elif check('screen', 'results'):
            results.draw()
        elif check('screen', 'levels'):
            levels_selection.draw()
        elif check('screen', 'cards'):
            card_selection.draw()
        elif check('screen', 'card_type'):
            card_type.draw()
        elif check('screen', 'character_types'):
            character_types.draw()
        elif check('screen', 'improvement_character'):
            improvement_character.draw()
        elif check('screen', 'loading_screen'):
            loading_screen.update()
        elif check('screen', 'info_player'):
            pl_info.draw()
        elif check('screen', 'transition'):
            transition.draw()
        elif check('screen', 'gemplay'):
            game.draw()
        elif check('screen', 'loss') or check('screen', 'win'):
            res.draw()

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

    res = Result(screen)

    main()

    start_screen()
