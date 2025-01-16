import json
import math
from random import randint

import pygame

list_map = {'winter_breeze': [
    '                          GCCCCCCCF          GCCCCCF                     GCCCCF                          ',
    '                          GCCCCCCCF          GCCCCCH                     GCCCCF                          ',
    '                          ICCCCCCCF          GCCCCF                      GCCCCF                          ',
    '                           GCCCCCCF          GCCCCF                      IJJJJH                          ',
    '                           GKCCCCCF          IJJJJH                                                      ',
    '                           IJJJJJJH                                                                      ',
    '                                                                                                         ',
    '                                                                                                         ',
    '                                                      DAAAAE                                             ',
    '                                                     DCCCCCCE                                            ',
    '                                          DABBE     DCCCCCCCCE                                           ',
    '                                         DCCCCF  DBBCCCCCCCCCCAAE                                        ',
    '             DABBAE                    DACCCCCF  GCCCCCCCCCCCCCCCE                                       ',
    '            DCCCCCCE                  DCCCCCCCF  GCCCCCCCCCCCCCCCCE                                      ',
    '           DCCCCCCCCE                DCCCCCCCCF  GCCCCCCCCCCCCCCCCCE         DAABE        DABBBE     DAAA',
    '          DCCCCCCCCCCBAAAAAAE    DAAACCCCCCCCCF  GCCCCCCCCCCCCCCCCCCEABBBAE  GCCCCE      DCCCCCCE   DCCCC',
    'BBBBBBBBBBCCCCCCCCCCCCCCCCCCF    GCCCCCCCCCCCCF  GCCCCCCCCCCCCCCCCCCCCCCCCF  GCCCCCE    DCCCCCCCCAAACCCCC',
    'CCCCCCCCCCCCCCCCCCCCCCCCCCCCF    GCCCCCCCCCCCCF  GCCCCCCCCCCCCCCCCCCCCCCCCF  GCCCCCCBBAACCCCCCCCCCCCCCCCC',
    'CCCCCCCCCCCCCCCCCCCCCCCCCCCCF    GCCCCCCCCCCCCF  GCCCCCCCCCCCCCCCCCCCCCCCCF  GCCCCCCCCCCCCCCCCCCCCCCCCCCC'
],
    'winter_kingdom': [
        '                                                                       GBBBBBBH                       FMLBBBBBBH                GBBBBBBBBBBBBH                                FMLBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH    GBBBBBBBH    GBBBBBBBBBBBBBBBBBBBBBBBBBBBH       ',
        '                                                                       GBBBBBBH                         FLBBBBBJAD           CAAIBBBBBBBBBBBBH                                  GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH    GBBBBBBBH    GBBBBBBBBBBBBBBBBBBBBBBBBBBBH       ',
        '                                                                       FMMMMMME                          GBBBBBBBJAAAAAAAAAAAIBBKMMMMMMMMMMMME                                  FMMMMMMMMMMMMMMMMMMMLBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH    GBBBBBBBH    GBBBBBBBBBBBBBBBBBBBBBBBBBBBH       ',
        '                                                                                                         FMMMMMMMLBBBBBBBBBBKMMME                                                                   GBBBBBBBBBBBBBBBBBBBBBBBKMMMMMMMMMMMMME    FMMMMMMMM    GBBBBBBBBBBBBBBBBBBBBBBBBBBBH       ',
        '                                                                                                                 FMLBBBBBKMME                                                               M      CAIBBBBBBBBBBBBBBBBBBBBBBJD                              FMMMMMMLBBBBBBBBBBBBBBBBBBBBH       ',
        '                                                                                                                   FMMMMME                                                                     M  CIBBBBBBBBBBBBBBBBBBBBBBBBBJAD                                   FMLBBBBBBBBBBBBBBBBBBH       ',
        '                                                                                                                                                                                                  FMMMMMMMMLBBBBBBBBBBBBBBBBBBBJD           CD                       FLBBBBBBBBBBBBBBKME        ',
        '                                                                                                                                                                                                           FMLBBBKMMMMLBBBBBBBBBJD          FE                        FMMMLBBBBBBBBKMME         ',
        '                                                                                                                                                                                                             FMMME    FMMMMMMMMMME                                        FMMMMMMME             ',
        '                                                                  CAAAAAD    CD                                                                                    CAAAAAD                                                                                                                      ',
        '                                                               CAAIBBBBBH    GJD                                                                                CAAIBBBBBJD                                                                                                                     ',
        '                                                              CIBBBBBBBBH    GBJAAAAAAAD                                                                    CAAABBBBBBBBBBJD                                                                                                                    ',
        '                                                      CAAAAAAAIBBBBBBBBBH    GBBBBBBBBBJAD            CAAAD                               CAAD             CIBBBBBBBBBBBBBBJAAAD                                                                                                                ',
        '                                                    CAIBBBBBBBBBBBBBBBBBH    GBBBBBBBBBBBJAD     CAAAAIBBBH                               GBBJD          CAIBBBBBKMMLBBBBBBBBBBJAAAAAAAAAAD                                                                                                     ',
        '                                                  CAIBBBBBBBBBBBBBBBBBBBH    GBBBBBBBBBBBBBJAAAAAIBBBBBBBBH                               GBBBJD      CAAIBBBBBKME  FMMLBBBBBBBBBBBBBBBBBBJAAD                                                                                                  ',
        '                     CAAAAAAAAAD               CAAIBBKMMMLBBBBBBBBBBBBBBH    GBBBBBBBBBBBBBBBBBBBBBBBBBBBBH                               GBBBBJAAAAAAIBBBBBBBBH       GBBBBBBBBBBBBBBBBBBBBBJAD                                                                                                ',
        'AAAAAAAAAAD         CIBBBBBBBBBJAD            CIBBBBBH   FMMLBBBBBBBBBBBH    GBBBBBBBBBKMMMMLBBBBBBBBBBBBBH                               GBBBBBBBBBBBBBBBBBBBBJAD   CAIBBBBBBBBBBBBBBBBBBBBBBBJAAAAAAAAD                                                                                       ',
        'BBBBBBBBBBJAD    CAAIBBBBBBBBBBBBJAAAAAAAAD  CIBBBKMME      FMMMLBBBBBBBH    GBBBBBBBBBH    FMMLBBBBBBBBBBH                               GBBBBBBBBBBBBBBBBBBBBBBJAAAIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH                                                                CAAAAAAAAAAAAAAAAAAAAAA',
        'BBBBBBBBBBBBJAAAAIBBBBBBBBBBBBBBBBBBBBBBBBH  GBBBBH             GBBBBBBBH    GBBBBBBBBBH       GBBBBBBBBBBH                               GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH                                                                GBBBBBBBBBBBBBBBBBBBBBB'
    ]
}


def main(screen, zastavka, main_menu):
    pygame.mixer.music.load("file_music\intro.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(1)

    fps = 60
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while check_screen('running'):
        for event in pygame.event.get():
            if check_screen('fl_menu'):
                main_menu.check_event(event)

        if check_screen('fl_zastavka'):
            if pygame.time.get_ticks() - start_time >= 9200:
                screen_change('fl_zastavka', 'fl_menu')
                music_menu()

            zastavka.draw()

        elif check_screen('fl_menu'):
            main_menu.draw()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)


def check_setting(name_setting):
    with open('setting.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    return data['audio'][name_setting]


def check_screen(screen):
    with open('data.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    return data['screen'][screen]


def screen_change(screen_one, screen_two):
    with open('data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    data['screen'][screen_one] = False
    data['screen'][screen_two] = True

    data['screen']['past_position'] = screen_one

    with open('data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def start_screen():
    with open('data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    data['screen']['running'] = True
    data['screen']['past_position'] = 'fl_zastavka'
    data['screen']['fl_zastavka'] = True
    data['screen']['fl_menu'] = False
    data['screen']['settings'] = False
    data['screen']['play'] = False

    with open('data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def music_menu():
    pygame.mixer.music.load('file_music\music_menu.mp3')
    pygame.mixer.music.set_volume(check_setting('music_volume'))
    pygame.mixer.music.play(-1)
    if not check_setting('mute_music'):
        pygame.mixer.music.pause()
    if not check_setting('mute_sound'):
        sound.set_volume(0)


def on_off_playback_music():
    if not check_setting('mute_music'):
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


def on_off_playback_sound():
    if not check_setting('mute_sound'):
        sound.set_volume(0)
    else:
        sound.set_volume(check_setting('sound_volume'))


def play_sound():
    sound.play()


class Zastavka:
    def __init__(self, screen):
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        self.screen = screen

        self.star = []
        inner_angle, outer_radius = 2 * math.pi / 10, 80 / (2 * math.sin(math.pi / 5))
        inner_radius = 80 / (2 * math.tan(math.pi / 5)) * math.tan(math.pi / 10)
        for j in range(10):
            angle = j * inner_angle
            a = outer_radius if j % 2 == 0 else inner_radius
            self.star.append([a * math.cos(angle), a * math.sin(angle)])

        custom_font = pygame.font.Font('Docker.ttf', 80)
        self.text = custom_font.render('Gravity Flux', True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(400, 300))

        self.n = 0

    def draw(self):
        self.n = (self.n + 1) % 5
        if self.n == 0:
            for i in range(len(self.coord)):
                self.coord[i][0] = max(0, min(self.coord[i][0] + randint(-200, 200), 800))
                self.coord[i][1] = max(0, min(self.coord[i][1] + randint(-200, 200), 600))
        for i in range(len(self.coord)):
            x, y = self.coord[i][0], self.coord[i][1]
            p = randint(1, 4)
            if p % 2 == 0:
                pygame.draw.polygon(self.screen, self.collor[i], [[x, y], [x - 60, y + 80], [x - 30, y + 80],
                                                                  [x - 60, y + 140], [x, y + 60], [x - 30, y + 60]])
            else:
                pygame.draw.polygon(self.screen, self.collor[i], [[i[0] + x, i[1] + y] for i in self.star])

        self.screen.blit(self.text, self.text_rect)


class Menu:
    def __init__(self, screen, sound):
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        self.screen = screen
        self.n = 0
        self.button1 = Button([300, 155, 200, 50], screen, (255, 255, 255), (0, 255, 255), (105, 105, 105), 'Играть',
                              self.start_game, 30, sound)
        self.button2 = Button([300, 275, 200, 50], screen, (255, 255, 255), (0, 255, 154), (105, 105, 105), 'Настройки',
                              self.open_setting, 30, sound)
        self.button3 = Button([300, 395, 200, 50], screen, (255, 255, 255), (255, 20, 147), (105, 105, 105), 'Выход',
                              self.close, 30, sound)
        font = pygame.font.Font("Docker.ttf", 15)
        self.name_screen = font.render('Gravity Flux', True, (255, 255, 255))
        self.screen_rect = self.name_screen.get_rect(center=(65, 10))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.n = (self.n + 1) % 50
        self.change_coordinates()

        for i in range(len(self.coord)):
            x, y = self.coord[i][0], self.coord[i][1]
            pygame.draw.polygon(self.screen, self.collor[i],
                                [[x, y], [x - 48, y + 64], [x - 24, y + 64], [x - 48, y + 112], [x, y + 48],
                                 [x - 24, y + 48]])
        self.screen.blit(self.name_screen, self.screen_rect)
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()

    def start_game(self):
        screen_change('fl_menu', 'play')

    def open_setting(self):
        screen_change('fl_menu', 'settings')

    def close(self):
        screen_change('running', 'fl_menu')

    def change_coordinates(self):
        if self.n == 0:
            self.coord[0][0] = max(48, min(self.coord[0][0] + randint(-80, 80), 300))
            self.coord[0][1] = max(0, min(self.coord[0][1] + randint(-80, 80), 188))
            self.coord[1][0] = max(548, min(self.coord[1][0] + randint(-80, 80), 800))
            self.coord[1][1] = max(0, min(self.coord[1][1] + randint(-80, 80), 188))
            self.coord[2][0] = max(48, min(self.coord[2][0] + randint(-80, 80), 300))
            self.coord[2][1] = max(300, min(self.coord[2][1] + randint(-80, 80), 488))
            self.coord[3][0] = max(548, min(self.coord[3][0] + randint(-80, 80), 800))
            self.coord[3][1] = max(300, min(self.coord[3][1] + randint(-80, 80), 488))

    def check_event(self, event):
        self.button1.handle_event(event)
        self.button2.handle_event(event)
        self.button3.handle_event(event)


class Settings:
    """
    Класс, реализующий окно Настроек
    """

    def __init__(self, screen) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        music_volume = check_setting('music_volume')
        sound_volume = check_setting('sound_volume')
        zn1 = 'Выключить' if check_setting('mute_music') else 'Включить'
        zn2 = 'Выключить' if check_setting('mute_sound') else 'Включить'

        # Создание кнопок
        self.button1 = Button([80, 100, 220, 50], screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn1,
                              self.onn_off_music, 30, False)
        self.button2 = Button([80, 300, 220, 50], screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn2,
                              self.onn_off_sound, 30, False)
        self.button3 = Button([300, 500, 200, 50], screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Назад',
                              self.close_seting, 30)

        self.screen = screen

        # Создание слайдеров
        self.slider_music = Slider(screen, 400, 190, 300, 20, 0, 1, music_volume, 'music_volume')
        self.slider_sound = Slider(screen, 400, 390, 300, 20, 0, 1, sound_volume, 'sound_volume')

        # Создание вспомогательного текста
        self.font = pygame.font.Font(None, 28)
        self.text1 = self.font.render('Громкость музыки: ', True, (255, 255, 255))
        self.text1_rect = self.text1.get_rect(center=(180, 200))
        self.text2 = self.font.render('Громкость звуковых эфектов: ', True, (255, 255, 255))
        self.text2_rect = self.text2.get_rect(center=(200, 400))
        self.text5 = self.font.render('Музыка', True, (255, 255, 255))
        self.text5_rect = self.text1.get_rect(center=(250, 80))
        self.text6 = self.font.render('Звуковые эфекты', True, (255, 255, 255))
        self.text6_rect = self.text2.get_rect(center=(250, 280))

        # Создание текста - название окна
        font = pygame.font.Font("Docker.ttf", 15)
        self.text_surface = font.render('Settings', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(40, 10))

    def draw(self) -> None:
        """
        Метод отрисовки окна настроек
        """

        # Закрашивание фона в чёрный
        self.screen.fill((0, 0, 0))

        # Отрисовка всех кнопок
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()

        # Отрисовка слайдера громкости музыки, если музыка включена
        if check_setting('mute_music'):
            self.slider_music.draw()
            self.screen.blit(self.text1, self.text1_rect)
            text3 = self.font.render(str(int(round(float(f'{check_setting("music_volume"):.2f}') * 100, 0))), True,
                                     (255, 255, 255))
            text3_rect = text3.get_rect(center=(330, 200))
            self.screen.blit(text3, text3_rect)

        # Отрисовка слайдера громкости звуковых эффектов, если музыка включена
        if check_setting('mute_sound'):
            self.slider_sound.draw()
            self.screen.blit(self.text2, self.text2_rect)
            text4 = self.font.render(str(int(round(float(f'{check_setting("sound_volume"):.2f}') * 100, 0))), True,
                                     (255, 255, 255))
            text4_rect = text4.get_rect(center=(370, 400))
            self.screen.blit(text4, text4_rect)

        # Отображение всех текстов
        self.screen.blit(self.text5, self.text5_rect)
        self.screen.blit(self.text6, self.text6_rect)
        self.screen.blit(self.text_surface, self.text_rect)

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
        Метод, который присваивает противоположное значение для "name" из файла 'setting.json'
        """

        # Чтение данных из файла 'setting.json'
        with open('setting.json', 'r', encoding='utf8') as file:
            data = json.load(file)

        # Изменение полученных данных
        data['audio'][name] = not data['audio'][name]

        # Запись в файл 'setting.json' изменённых данных
        with open('setting.json', 'w', encoding='utf8') as file:
            json.dump(data, file, indent=2)

    def check(self, event) -> None:
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

    def close_seting(self) -> None:
        """
        Метод, который закрывает окно нстроек
        """

        # Определение в каком окне был пользователь, перед тем как зайти в настройки
        if check_setting('past_position') == 'fl_menu':
            screen_change('fl_menu', 'settings')
        elif check_setting('past_position') == 'play':
            screen_change('play', 'settings')


class Button:
    """
    Класс реализующий кнопку
    """

    def __init__(self, coord, screen, collor_text, hover_color, collor_button, text, funk, zn, fl=True) -> None:
        """
        Метод, который создаёт экземпляры класса и присваивает им полученные значения
        """

        # Задаёт координаты
        self.rect = pygame.Rect(coord)

        # Флаг отслеживания наведения мыши
        self.fl = fl

        # Экран отрисовки
        self.screen = screen

        # Присваивание цветов объектам
        self.collor_text = collor_text
        self.collor_button = collor_button
        self.hover_color = hover_color

        # Сохранение ссылки на функцию, которая будет вызываться по нажатию на кнопку
        self.funk = funk

        # Задание шрифта
        self.font = pygame.font.Font("Docker.ttf", zn)

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

        if self.text == 'Выключить':
            self.text = 'Включить'
            self.text_surface = self.font.render(self.text, True, self.collor_text)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        elif self.text == 'Включить':
            self.text = 'Выключить'
            self.text_surface = self.font.render(self.text, True, self.collor_text)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)


class Slider:
    def __init__(self, screen, x, y, width, height, min_value, max_value, start_value, name, sound):
        self.name = name
        self.screen = screen
        self.sound = sound
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        self.slider_rect = pygame.Rect(x, y, width, height)
        self.cursor_width = 10
        self.cursor_rect = pygame.Rect(self.x + (self.width * self.value) - self.cursor_width // 2, self.y,
                                       self.cursor_width, self.height)
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.cursor_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x = event.pos[0]
                self.value = self.calculate_value(mouse_x)
                self.value = max(self.min_value, min(self.value, self.max_value))
                self.cursor_rect.x = self.x + (self.width * self.value) - self.cursor_width // 2
                self.volume_change()

    def volume_change(self):
        with open('setting.json', 'r', encoding='utf8') as file:
            data = json.load(file)
        data['audio'][self.name] = round(self.value, 2)
        if self.name == 'music_volume':
            pygame.mixer.music.set_volume(data['audio']['music_volume'])
        elif self.name == 'sound_volume':
            self.sound.set_volume(data['audio']['sound_volume'])

        with open('setting.json', 'w', encoding='utf8') as file:
            json.dump(data, file, indent=2)

    def calculate_value(self, mouse_x):
        position = (mouse_x - self.x) / self.width
        return position

    def draw(self):
        pygame.draw.rect(self.screen, (150, 150, 150), self.slider_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.cursor_rect)

    def get_value(self):
        return self.value


if __name__ == '__main__':
    width, height = 800, 600
    start_screen()

    pygame.init()
    sound = pygame.mixer.Sound("file_music/button_sound.wav")
    sound.set_volume(check_setting('sound_volume') if check_setting('mute_sound') else 0)

    screen = pygame.display.set_mode((width, height), flags=pygame.NOFRAME)

    zastavka = Zastavka(screen)

    main_menu = Menu(screen, sound)

    main(screen, zastavka, main_menu)
