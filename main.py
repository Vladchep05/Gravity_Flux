import json

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


def main(screen):
    pygame.init()

    fps = 60
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)


def check_setting():
    with open('setting.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    return (data['audio']['mute_music'], data['audio']['mute_sound'], data['audio']['music_volume'],
            data['audio']['sound_volume'])


if __name__ == '__main__':
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), flags=pygame.NOFRAME)
    main(screen)
