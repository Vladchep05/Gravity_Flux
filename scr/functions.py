from scr.constants import rating_cost, rating_character

from random import randint
import pygame
import json

from scr.constants import (
    rating_cost, rating_character, level_map, belonging_to_level, map_index, opening_levels
)


def check(name1, name2) -> int | str:
    """
    Функция, возвращающая значения по ключам name1 и name2 из файла data.json
    """

    # Открытие data/data.json в режиме чтения
    with open('data/data.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Возвращение значения, используя переданные ключи (name1, name2)
    return data[name1][name2]


def check_levels(name1, name2) -> list:
    """
    Функция, возвращающая значения по ключам name1 и name2 из файла cards.json
    """

    # Открытие data/cards.json в режиме чтения
    with open('data/cards.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Возвращение значения, используя переданные ключи (name1, name2)
    return data[name1][name2]


def transit(pos) -> None:
    """
    Функция бновления окна затемнения
    """

    from scr.classes import transition

    # Вызов метод new_pos(pos) у объекта transition, изменение затемнение окна
    transition.new_pos(pos)


def check_open_cards(name1, name2) -> bool:
    """
    Функция проверки, открыты ли определенные карты в игре используя данные из файла data.json
    """

    # Открытие data/data.json в режиме чтения
    with open('data/data.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Возвращение значения, используя переданные ключи
    return data['open_cards'][name1][name2]


def setting_value(key, name) -> None:
    """
    Функция, которая изменяет значение настройки игры и сохраняет изменения в data.json
    """

    # Открытие data/data.json в режиме чтения
    with open('data/data.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Изменение данных из файла по ключам (gameplay[key])
    data['gameplay'][key] = name

    # Открытие data/data.json в режиме записи
    with open('data/data.json', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый json файл
        json.dump(data, file, indent=2)


def determination_levels() -> None:
    """
    Функция Обновления кнопок выбора уровней
    """

    from scr.classes import levels_selection

    # Вызов метода creating_buttons() объекта levels_selection
    levels_selection.creating_buttons()


def update_text_info(name):
    """
    Функция Обновления характеристик персонажа
    """

    from scr.classes import pl_info

    # Вызов метода update() объекта pl_info
    pl_info.update(name)


def play_musik() -> None:
    """
    Функция запуска фоновой музыку в игре с учетом настроек
    """

    # Загрузка случайного аудиофайла (0-6.mp3) из background_music/
    pygame.mixer.music.load(f'data/file_music/background_music/{randint(0, 6)}.mp3')

    # Устанавление громкости при помощи функции check()
    pygame.mixer.music.set_volume(check('audio', 'music_volume'))

    # Запуск музыки в бесконечном цикле (-1)
    pygame.mixer.music.play(-1)

    # Проверка, включена ли музка в настройках
    if not check('audio', 'mute_music'):
        # Музыка ставится на паузу
        pygame.mixer.music.pause()


def loading(fl=False) -> None:
    """
    Функция обновления окна загрузки
    """

    from scr.classes import loading_screen

    # Вызывает метод initial_update(fl) у объекта loading_screen
    loading_screen.initial_update(fl)


def time_check(name_card, time) -> None:
    """
    Фнкция обновления времени прохождения карты 'name_card'
    """

    # Открытие data/better_time.txt в режиме чтения
    with open('data/better_time.txt', 'r', encoding='utf8') as file:
        # Загрузка данных из файла txt
        data = file.read().split('\n')

    # Определение индекса карты name_card с помощью константы map_index
    ind = map_index[name_card]

    if (old_time := data[ind + 1]) != '-':
        # Сравнение старого времени прохождения и нового (time)
        if int(old_time) > time:
            # Задаётся новое значение минимального времени, если оно меньше предыдущего
            data[ind + 1] = str(time)

            # Открытие data/better_time.txt в режиме записи
            with open('data/better_time.txt', 'w', encoding='utf8') as file:
                # Записываем и сохраняем новый txt файл
                file.writelines([i + '\n' for i in data[:-1]] + [data[-1]])
    else:
        # Задаётся новое значение минимального времени, если раньше не проходил эту кару
        data[ind + 1] = str(time)

        # Открытие data/better_time.txt в режиме записи
        with open('data/better_time.txt', 'w', encoding='utf8') as file:
            # Записываем и сохраняем новый txt файл
            file.writelines([i + '\n' for i in data[:-1]] + [data[-1]])


def card_selection_easy() -> None:
    """
    Функция установления сложности "Легкий" и создания кнопок выбора персонажей и уровней
    """

    from scr.classes import character_types, card_selection, levels_selection

    # Вызов setting_value(), становление уровня сложности
    setting_value('level', 'easy')

    # Создание кнопок для персонажей (Блейв, Элиза, Кассиан)
    character_types.creating_buttons('Блейв', 'Элиза', 'Кассиан')

    # Создание кнопок для выбора карт (level_map['easy'])
    card_selection.creating_buttons(*level_map['easy'])

    # Смена окна с levels на transition
    transit('cards')
    screen_change('levels', 'transition')

    # Обновление копок уровней
    levels_selection.creating_buttons()


def card_selection_normal() -> None:
    """
    Функция установления сложности "Нормальный" и создания кнопок выбора персонажей и уровней
    """

    from scr.classes import character_types, card_selection, levels_selection

    # Вызов setting_value(), становление уровня сложности
    setting_value('level', 'normal')

    # Создание кнопок для персонажей (Рен, Келтор, Золтан)
    character_types.creating_buttons('Рен', 'Келтор', 'Золтан')

    # Создание кнопок для выбора карт (level_map['normal'])
    card_selection.creating_buttons(*level_map['normal'])

    # Смена окна с levels на transition
    transit('cards')
    screen_change('levels', 'transition')

    # Обновление копок уровней
    levels_selection.creating_buttons()


def card_selection_hard() -> None:
    """
    Функция установления сложности "Сложный" и создания кнопок выбора персонажей и уровней
    """

    from scr.classes import character_types, card_selection, levels_selection

    # Вызов setting_value(), становление уровня сложности
    setting_value('level', 'hard')

    # Создание кнопок для персонажей (Финн, Лиам, Эйден)
    character_types.creating_buttons('Финн', 'Лиам', 'Эйден')

    # Создание кнопок для выбора карт (level_map['hard'])
    card_selection.creating_buttons(*level_map['hard'])

    # Смена окна с levels на transition
    transit('cards')
    screen_change('levels', 'transition')

    # Обновление копок уровней
    levels_selection.creating_buttons()


def play_game() -> None:
    """
    Функция загрузки игры через объект game
    """

    from scr.classes import game

    # Вызов game.loading()
    game.loading()


def screen_change(screen_one, screen_two) -> None:
    """
    Функция переключения активного окна (screen_one -> screen_two), обновляя data.json
    """

    # Открытие data/data.json в режиме чтения
    with open('data/data.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Установление screen_one в False (выключение старого окна)
    data['screen'][screen_one] = False

    # Установление screen_two в True (включение нового окна)
    data['screen'][screen_two] = True

    # Если screen_one не 'transition', созранение его как past_position
    if screen_one != 'transition':
        data['screen']['past_position'] = screen_one

    # Открытие data/data.json в режиме записи
    with open('data/data.json', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый json файл
        json.dump(data, file, indent=2)


def start_screen() -> None:
    """
    Сбрасывание состояния игры и переключение окна на fl_zastavka (заставку), очищение дынных о текущей игре
    """

    # Открытие data/data.json в режиме чтения
    with open('data/data.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Установление всех окон (screen) в False, кроме fl_zastavka, которое становится True
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

    # Очищение параметров gameplay (тип карты, имя карты, персонаж, уровень)
    data['gameplay']['type_card'] = ""
    data['gameplay']['name_card'] = ""
    data['gameplay']['character'] = ""
    data['gameplay']['level'] = ""

    # Открытие data/data.json в режиме записи
    with open('data/data.json', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый json файл
        json.dump(data, file, indent=2)


def recording_data(rating, coins, name_card, res) -> None:
    """
    Обновление рейтинга и монет игрока, открытие новых карт и уровней
    """

    # Открытие data/data.json в режиме чтения
    with open('data/data.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Добавление rating к текущему рейтингу
    data['gameplay']['rating'] += rating

    # Если игрок победил, добавляются монеты
    if res == 'win':
        data['gameplay']['coins'] += coins

    # Проверка, можно ли открыть новые карты (rating_cost)
    for name, rat in rating_cost.items():
        if data['gameplay']['rating'] >= rat:
            data['open_cards'][belonging_to_level[name]][name] = True
        else:
            data['open_cards'][belonging_to_level[name]][name] = False

    # Если победа на определенных картах (Рассветный путь, Скалистый склон),
    # открывается следующий уровень (opening_levels)
    if res == 'win' and name_card in ['Рассветный путь', 'Скалистый склон'] and \
            not data['open_levels'][(level := opening_levels[belonging_to_level[name_card]])]:
        data['open_levels'][level] = True

    # Открытие data/better_time.txt в режиме чтения
    with open('data/better_time.txt', 'r', encoding='utf8') as file:
        # Загрузка данных из файла txt
        dat = file.read().split('\n')

        # Получение максимального рейтинга и остальных данных
        max_rat, dat1 = int(dat[0]), dat[1:]

    # Обновление максимального рейтинга, если новый выше
    if data['gameplay']['rating'] > max_rat:
        # Открытие data/better_time.txt в режиме записи
        with open('data/better_time.txt', 'w', encoding='utf8') as file:
            # Записываем и сохраняем новый txt файл
            file.writelines([i + '\n' for i in [str(data['gameplay']['rating'])] + dat1[:-1]] + [dat[-1]])

    # Проверка, возможно ли открыть новых персонажей (rating_character)
    for name, rat in rating_character.items():
        if data['gameplay']['rating'] >= rat:
            data['open_characters'][name] = True
        else:
            data['open_characters'][name] = False

    # Открытие data/data.json в режиме записи
    with open('data/data.json', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый json файл
        json.dump(data, file, indent=2)


def music_menu() -> None:
    """
    Функция, загружает и управляет музыкой главного меню.
    """

    # Загрузка случайного файла (music_menu_0.mp3 или music_menu_1.mp3)
    pygame.mixer.music.load(f'data/file_music/music_menu_{randint(0, 1)}.mp3')

    # Установление громкости музыки, используя check('audio', 'music_volume')
    pygame.mixer.music.set_volume(check('audio', 'music_volume'))

    # Включение музыки в бесконечном цикле (play(-1))
    pygame.mixer.music.play(-1)

    # Если музыка выключена (mute_music), ставится паузу
    if not check('audio', 'mute_music'):
        pygame.mixer.music.pause()


def player_inform(name) -> None:
    """
    Функция обновления информации о персонаже
    """

    from scr.classes import pl_info

    # Вызов update(name) у объекта pl_info, передавая имя персонажа
    pl_info.update(name)


def update_improvement(name) -> None:
    """
    Функция обновления состояния кнопок улучшения персонажа
    """

    from scr.classes import improvement_character

    # Вызов update_button(name) у объекта improvement_character
    improvement_character.update_button(name)


def res_loss() -> None:
    """
    Функция обновления окна результатов после поражения
    """

    from scr.classes import game, result

    # Получение данные (mobs, time, coin, level, card) через game.inf()
    mobs, time, coin, level, card = game.inf()

    # Передача данных в result.update(), указывая loss (поражение)
    result.update(mobs, time, coin, 'loss', level, card)


def res_win() -> None:
    """
    Функция обновления окна результатов после победы
    """

    from scr.classes import game, result

    # Получение данные (mobs, time, coin, level, card) через game.inf()
    mobs, time, coin, level, card = game.inf()

    # Передача данных в result.update(), указывая win  (победа)
    result.update(mobs, time, coin, 'win', level, card)


def volume_change(value, name) -> None:
    """
    Функция, которая изменяет громкость музыки или звуков в игре
    """

    # Открытие data/data.json в режиме чтения
    with open('data/data.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Обновление значения громкости (audio[name]), округляя до двух знаков
    data['audio'][name] = round(value, 2)

    # Если name == 'music_volume', изменяет громкость музыки pygame.mixer.music.set_volume()
    if name == 'music_volume':
        pygame.mixer.music.set_volume(data['audio']['music_volume'])

    # Открытие data/data.json в режиме записи
    with open('data/data.json', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый json файл
        json.dump(data, file, indent=2)


def on_off_playback_music() -> None:
    """
    Функция, которая включает или выключает фоновую музыку
    """

    # Проверка настроек mute_music с помощью check('audio', 'mute_music')
    if not check('audio', 'mute_music'):
        # Если mute_music == False, ставиться паузу (pause())
        pygame.mixer.music.pause()
    else:
        # Если mute_music == True, возобновляется воспроизведение (unpause())
        pygame.mixer.music.unpause()


def on_off_playback_sound() -> None:
    """
    Функция, которая включает или выключает звуковые эффекты в игре
    """

    # Проверка настроек mute_sound с помощью check('audio', 'mute_sound')
    if not check('audio', 'mute_sound'):
        # Если mute_sound == False, устанавливается громкость звука в 0
        sound.set_volume(0)
    else:
        # Если mute_sound == True, устанавливается громкость на сохраненное значение (check('audio', 'sound_volume'))
        sound.set_volume(check('audio', 'sound_volume'))


def character_update_but() -> None:
    """
    Функция обновления кнопок кона выбора персонажа
    """

    from scr.classes import character_types

    # Вызов rollback() у объекта character_types
    character_types.rollback()


def factory_reset() -> None:
    """
    Функция полного сброса прогресса игрока до стандартных значений
    """

    global setting, screen

    # Переключение окна на loading_screen и запуск анимации перехода
    transit('loading_screen')
    screen_change('reset_confirmation', 'transition')
    loading()

    # Открытие data/data.json в режиме чтения
    with open('data/data.json', 'r', encoding='utf8') as file:
        # Загрузка данных из файла json
        data = json.load(file)

    # Установка начальных параметров окон (screen)
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

    # Обнуление игровых данных (gameplay)
    data['gameplay']['level'] = ""
    data['gameplay']['name_card'] = ""
    data['gameplay']['type_card'] = ""
    data['gameplay']['character'] = ""
    data['gameplay']['rating'] = 0
    data['gameplay']['coins'] = 0

    # Установка параметров звука (audio)
    data['audio']['music_volume'] = 0.6
    data['audio']['sound_volume'] = 0.6
    data['audio']['mute_music'] = True
    data['audio']['mute_sound'] = True

    # Открытие только стартового персонажа ("Блейв"), все остальные закрыты
    data['open_characters']['Блейв'] = True
    data['open_characters']['Золтан'] = False
    data['open_characters']['Кассиан'] = False
    data['open_characters']['Келтор'] = False
    data['open_characters']['Лиам'] = False
    data['open_characters']['Рен'] = False
    data['open_characters']['Финн'] = False
    data['open_characters']['Элиза'] = False
    data['open_characters']['Эйден'] = False

    # Открытие уровень easy, блокировка normal и hard
    data['open_levels']['easy'] = True
    data['open_levels']['normal'] = False
    data['open_levels']['hard'] = False

    # Открытие только стартовой карты, блокируя остальные
    data['open_cards']['easy']['Тихая долина'] = True
    data['open_cards']['easy']['Прогулка по роще'] = False
    data['open_cards']['easy']['Рассветный путь'] = False

    data['open_cards']['normal']['Встреча ветров'] = False
    data['open_cards']['normal']['Зеленый лабиринт'] = False
    data['open_cards']['normal']['Скалистый склон'] = False

    data['open_cards']['hard']['Заточенные пики'] = False
    data['open_cards']['hard']['Тень дракона'] = False
    data['open_cards']['hard']['Дыхание вечного'] = False

    # Открытие data/data.json в режиме записи
    with open('data/data.json', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый json файл
        json.dump(data, file, indent=2)

    from scr.classes import setting

    # Перемоздание объекта Settings(screen), что бы небыло бага с слайдерами
    setting = setting.update_sliders()

    # Открытие data/better_time.txt в режиме чтения
    with open('data/better_time.txt', 'r', encoding='utf8') as file:
        # Загрузка данных из файла txt
        data = file.read().split('\n')

        # Сохранение максимального рейтинга
        max_rat = [data[0] + '\n']

    # Открытие data/better_time.txt в режиме записи
    with open('data/better_time.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл
        file.writelines(max_rat + ['-\n' * 8] + ['-'])

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Блейв.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Блейва
        file.writelines('\n'.join(['10', '1', '8', '3', '80']))

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Элиза.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Элизы
        file.writelines('\n'.join(['12', '2', '8', '3', '78']))

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Кассиан.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Кассиана
        file.writelines('\n'.join(['14', '3', '9', '3', '76']))

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Рен.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Рена
        file.writelines('\n'.join(['16', '4', '9', '3', '74']))

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Келтор.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Келтора
        file.writelines('\n'.join(['18', '5', '9', '3', '72']))

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Золтан.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Золтана
        file.writelines('\n'.join(['22', '6', '9', '3', '70']))

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Финн.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Финна
        file.writelines('\n'.join(['26', '7', '10', '3', '68']))

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Лиам.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Лиама
        file.writelines('\n'.join(['30', '8', '10', '3', '66']))

    # Открытие data/better_time.txt в режиме записи
    with open('data/characteristics_character/Эйден.txt.txt', 'w', encoding='utf8') as file:
        # Записываем и сохраняем новый txt файл с начальной характеристикой Эйдена
        file.writelines('\n'.join(['35', '9', '10', '3', '64']))
