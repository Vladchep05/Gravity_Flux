import datetime
import json
import math
import time
from random import randint, uniform, sample

import pygame

from scr.functions import (
    start_screen, check, screen_change, music_menu
)

from scr.classes import initialization


def main():
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
                result.check_event(event)

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
            result.draw()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    start_screen()

    initialization()

    from scr.classes import (
        screen, zastavka, transition, main_menu, setting, reset_confirmation, results, levels_selection, card_selection,
        card_type, character_types, improvement_character, pl_info, loading_screen, game, result
    )

    main()

    start_screen()
