import math
import sys
import json
from random import randint

import pygame

running = True
setting = False
fl_menu = False
play_men = False


def main():
    global running, setting, fl_menu, play_men
    pygame.init()
    screen = pygame.display.set_mode((800, 600), flags=pygame.NOFRAME)

    with open('setting.json', 'r', encoding='utf8') as file:
        a = json.load(file)
        fl_music = a['audio']['mute_music']
        fl_sound = a['audio']['mute_sound']
        music = a['audio']['music_volume']
        sound = a['audio']['sound_volume']

    pygame.mixer.music.load("file_music\intro.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(1)

    seting = Settings(screen, music, sound, 'Выключить' if fl_music else 'Включить',
                      'Выключить' if fl_sound else 'Включить')

    fl_zast, zast = True, Zastavka(screen)

    menu = Menu(screen)

    play_menu = Play_menu(screen)

    pygame.display.set_caption('Gravity Flux')
    fps = 60
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    time_zast = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if fl_menu:
                menu.check(event)
            elif setting:
                seting.check(event)
            elif play_men:
                play_menu.check(event)
        if fl_zast:
            if pygame.time.get_ticks() - time_zast >= 9000:
                fl_zast = False
                fl_menu = True
                with open('setting.json', 'r', encoding='utf8') as file:
                    data = json.load(file)
                pygame.mixer.music.load('file_music\music_menu.mp3')
                pygame.mixer.music.set_volume(data['audio']['music_volume'])
                pygame.mixer.music.play(-1)
                if not data['audio']['mute_music']:
                    pygame.mixer.music.pause()

            zast.draw()
        else:
            if fl_menu:
                menu.draw()
            else:
                if setting:
                    seting.draw()
                else:
                    if play_men:
                        play_menu.draw()

        pygame.display.flip()
        clock.tick(fps)


def flag_music():
    with open('setting.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    data['audio']['mute_music'] = not data['audio']['mute_music']

    if not data['audio']['mute_music']:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

    with open('setting.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def flag_sound():
    with open('setting.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    data['audio']['mute_sound'] = not data['audio']['mute_sound']

    with open('setting.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)


def easy_play():
    print('easy')


def normal_play():
    print('normal')


def hard_play():
    print('hard')


def back():
    global play_men, fl_menu
    play_men = False
    fl_menu = True


def close_seting():
    global setting, fl_menu
    setting = False
    fl_menu = True


def setings():
    global setting, fl_menu
    setting = True
    fl_menu = False


def plaing():
    global fl_menu, play_men
    play_men = True
    fl_menu = False


def close():
    global running
    running = False


class Zastavka:
    def __init__(self, screen):
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        self.screen = screen
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
                pygame.draw.polygon(self.screen, self.collor[i],
                                    [[x, y], [x - 60, y + 80], [x - 30, y + 80], [x - 60, y + 140], [x, y + 60],
                                     [x - 30, y + 60]])
            else:
                inner_angle = 2 * math.pi / 10
                outer_radius = 80 / (2 * math.sin(math.pi / 5))
                inner_radius = 80 / (2 * math.tan(math.pi / 5)) * math.tan(math.pi / 10)
                vertices = []
                for j in range(10):
                    angle = j * inner_angle
                    if j % 2 == 0:
                        r = outer_radius
                    else:
                        r = inner_radius
                    vx = x + r * math.cos(angle)
                    vy = y - r * math.sin(angle)
                    vertices.append((vx, vy))
                pygame.draw.polygon(self.screen, self.collor[i], vertices)
        custom_font = pygame.font.Font("Docker.ttf", 80)
        text = custom_font.render('Gravity Flux', True, (0, 0, 0))
        text_rect = text.get_rect(center=(400, 300))
        self.screen.blit(text, text_rect)


class Menu:
    def __init__(self, screen):
        self.coord = [[100, 100], [700, 100], [100, 500], [700, 500]]
        self.collor = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        self.screen = screen
        self.n, self.iter = 0, 0
        self.button1 = Button(300, 155, 200, 50, screen, (255, 255, 255), (0, 255, 255), (105, 105, 105), 'Играть',
                              plaing)
        self.button2 = Button(300, 275, 200, 50, screen, (255, 255, 255), (0, 255, 154), (105, 105, 105), 'Настройки',
                              setings)
        self.button3 = Button(300, 395, 200, 50, screen, (255, 255, 255), (255, 20, 147), (105, 105, 105), 'Выход',
                              close)
        font = pygame.font.Font("Docker.ttf", 15)
        self.text_surface = font.render('Gravity Flux', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(65, 10))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.n = (self.n + 1) % 50
        if self.n == 0:
            self.iter += 1
            self.coord[0][0] = max(48, min(self.coord[0][0] + randint(-80, 80), 300))
            self.coord[0][1] = max(0, min(self.coord[0][1] + randint(-80, 80), 188))
            self.coord[1][0] = max(548, min(self.coord[1][0] + randint(-80, 80), 800))
            self.coord[1][1] = max(0, min(self.coord[1][1] + randint(-80, 80), 188))
            self.coord[2][0] = max(48, min(self.coord[2][0] + randint(-80, 80), 300))
            self.coord[2][1] = max(300, min(self.coord[2][1] + randint(-80, 80), 488))
            self.coord[3][0] = max(548, min(self.coord[3][0] + randint(-80, 80), 800))
            self.coord[3][1] = max(300, min(self.coord[3][1] + randint(-80, 80), 488))
        for i in range(len(self.coord)):
            x, y = self.coord[i][0], self.coord[i][1]
            pygame.draw.polygon(self.screen, self.collor[i],
                                [[x, y], [x - 48, y + 64], [x - 24, y + 64], [x - 48, y + 112], [x, y + 48],
                                 [x - 24, y + 48]])
        self.screen.blit(self.text_surface, self.text_rect)
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()

    def check(self, event):
        self.button1.handle_event(event)
        self.button2.handle_event(event)
        self.button3.handle_event(event)


class Button:
    def __init__(self, x, y, w, h, screen, collor_text, hover_color, collor_button, text, funk):
        self.rect = pygame.Rect((x, y, w, h))
        self.screen = screen
        self.collor_text = collor_text
        self.collor_button = collor_button
        self.hover_color = hover_color
        self.funk = funk
        self.font = pygame.font.Font("Docker.ttf", 30)
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.collor_text)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.hove = False

    def draw(self):
        pygame.draw.rect(self.screen, (self.collor_button if not self.hove else self.hover_color), self.rect)
        self.screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hove = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hove and self.funk:
                self.funk()
                if self.text == 'Выключить':
                    self.text = 'Включить'
                    self.text_surface = self.font.render(self.text, True, self.collor_text)
                    self.text_rect = self.text_surface.get_rect(center=self.rect.center)
                elif self.text == 'Включить':
                    self.text = 'Выключить'
                    self.text_surface = self.font.render(self.text, True, self.collor_text)
                    self.text_rect = self.text_surface.get_rect(center=self.rect.center)


class Slider:
    def __init__(self, screen, x, y, width, height, min_value, max_value, start_value, name):
        self.name = name
        self.screen = screen
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
                with open('setting.json', 'r', encoding='utf8') as file:
                    data = json.load(file)
                data['audio'][self.name] = round(self.value, 2)
                if self.name == 'music_volume':
                    pygame.mixer.music.set_volume(data['audio']['music_volume'])

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


class Settings:
    def __init__(self, screen, music, sound, zn1, zn2):
        self.button1 = Button(80, 100, 220, 50, screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn1, flag_music)
        self.button2 = Button(80, 300, 220, 50, screen, (255, 255, 255), (255, 69, 0), (105, 105, 105), zn2, flag_sound)
        self.button3 = Button(300, 500, 200, 50, screen, (255, 255, 255), (255, 0, 0), (105, 105, 105), 'Назад',
                              close_seting)
        self.screen = screen
        self.slider_music = Slider(screen, 400, 190, 300, 20, 0, 1, music, 'music_volume')
        self.slider_sound = Slider(screen, 400, 390, 300, 20, 0, 1, sound, 'sound_volume')
        self.font = pygame.font.Font(None, 28)
        self.text1 = self.font.render('Громкость музыки: ', True, (255, 255, 255))
        self.text1_rect = self.text1.get_rect(center=(180, 200))
        self.text2 = self.font.render('Громкость звуковых эфектов: ', True, (255, 255, 255))
        self.text2_rect = self.text2.get_rect(center=(200, 400))
        self.text5 = self.font.render('Музыка', True, (255, 255, 255))
        self.text5_rect = self.text1.get_rect(center=(250, 80))
        self.text6 = self.font.render('Звуковые эфекты', True, (255, 255, 255))
        self.text6_rect = self.text2.get_rect(center=(250, 280))
        font = pygame.font.Font("Docker.ttf", 15)
        self.text_surface = font.render('Settings', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(40, 10))

    def draw(self):
        self.screen.fill((0, 0, 0))
        with open('setting.json', 'r', encoding='utf8') as file:
            a = json.load(file)
            fl_music = a['audio']['mute_music']
            fl_sound = a['audio']['mute_sound']
            music = a['audio']['music_volume']
            sound = a['audio']['sound_volume']
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()
        if fl_music:
            self.slider_music.draw()
            self.screen.blit(self.text1, self.text1_rect)
            text3 = self.font.render(str(int(round(float(f'{music:.2f}') * 100, 0))), True, (255, 255, 255))
            text3_rect = text3.get_rect(center=(330, 200))
            self.screen.blit(text3, text3_rect)
        if fl_sound:
            self.slider_sound.draw()
            self.screen.blit(self.text2, self.text2_rect)
            text4 = self.font.render(str(int(round(float(f'{sound:.2f}') * 100, 0))), True, (255, 255, 255))
            text4_rect = text4.get_rect(center=(370, 400))
            self.screen.blit(text4, text4_rect)
        self.screen.blit(self.text5, self.text5_rect)
        self.screen.blit(self.text6, self.text6_rect)
        self.screen.blit(self.text_surface, self.text_rect)

    def check(self, event):
        self.slider_music.handle_event(event)
        self.slider_sound.handle_event(event)
        self.button1.handle_event(event)
        self.button2.handle_event(event)
        self.button3.handle_event(event)


class Play_menu:
    def __init__(self, screen):
        self.screen = screen
        self.button1 = Button(80, 400, 200, 50, screen, (255, 255, 255), (0, 0, 255), (255, 69, 0), 'Easy', easy_play)
        self.button2 = Button(300, 400, 200, 50, screen, (255, 255, 255), (0, 0, 255), (0, 100, 0), 'Normal',
                              normal_play)
        self.button3 = Button(520, 400, 200, 50, screen, (255, 255, 255), (0, 0, 255), (75, 0, 130), 'Hard', hard_play)
        self.button4 = Button(520, 500, 200, 50, screen, (255, 255, 255), (184, 134, 11), (139, 0, 0), 'Назад', back)

        font = pygame.font.Font("Docker.ttf", 15)
        self.text_surface = font.render('Levels', True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(30, 10))

        #self.imeg1 = pygame.image.load('')

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()
        self.button4.draw()
        self.screen.blit(self.text_surface, self.text_rect)

    def check(self, event):
        self.button1.handle_event(event)
        self.button2.handle_event(event)
        self.button3.handle_event(event)
        self.button4.handle_event(event)


if __name__ == '__main__':
    sys.exit(main())
