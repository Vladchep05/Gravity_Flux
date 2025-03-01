import pygame

belonging_to_level = {
    'Тихая долина': 'easy',
    'Прогулка по роще': 'easy',
    'Рассветный путь': 'easy',
    'Встреча ветров': 'normal',
    'Зеленый лабиринт': 'normal',
    'Скалистый склон': 'normal',
    'Заточенные пики': 'hard',
    'Тень дракона': 'hard',
    'Дыхание вечного': 'hard'
}

level_improvement = {
    'easy': 1,
    'normal': 2,
    'hard': 3
}

character_genitive = {
    'Блейв': 'Блейва',
    'Элиза': 'Элизы',
    'Кассиан': 'Кассиана',
    'Рен': 'Рена',
    'Келтор': 'Келтора',
    'Золтан': 'Золтана',
    'Финн': 'Финна',
    'Лиам': 'Лиама',
    'Эйден': 'Эйдена'
}

character_level = {
    'Блейв': 'easy',
    'Элиза': 'easy',
    'Кассиан': 'easy',
    'Рен': 'normal',
    'Келтор': 'normal',
    'Золтан': 'normal',
    'Финн': 'hard',
    'Лиам': 'hard',
    'Эйден': 'hard'
}

list_tiles = [
    'tundra',
    'cake',
    'choco',
    'castle',
    'dirt',
    'grass',
    'purple',
    'sand',
    'snow'
]

attack_soun = {
    'Блейв': 'data/file_music/character/attack/2.mp3',
    'Элиза': 'data/file_music/character/attack/6.mp3',
    'Кассиан': 'data/file_music/character/attack/5.mp3',
    'Рен': 'data/file_music/character/attack/1.mp3',
    'Келтор': 'data/file_music/character/attack/6.mp3',
    'Золтан': 'data/file_music/character/attack/4.mp3',
    'Финн': 'data/file_music/character/attack/9.mp3',
    'Лиам': 'data/file_music/character/attack/7.mp3',
    'Эйден': 'data/file_music/character/attack/8.mp3'
}

x_offset_mobs = {
    0: {
        'left': {
            'attack': -44,
            'jump': -44,
            'run': -44,
            'idle': -44,
            'dead': -44,
            'smen_graviti': -44
        },
        'right': {
            'attack': -44,
            'jump': -44,
            'run': -44,
            'idle': -44,
            'dead': -44,
            'smen_graviti': -44
        }
    },
    1: {
        'left': {
            'attack': -48,
            'jump': -48,
            'run': -48,
            'idle': -48,
            'dead': -48,
            'smen_graviti': -48
        },
        'right': {
            'attack': -20,
            'jump': -20,
            'run': -20,
            'idle': -20,
            'dead': -20,
            'smen_graviti': -20
        }
    },
    2: {
        'left': {
            'attack': -44,
            'jump': -44,
            'run': -44,
            'idle': -48,
            'dead': -44,
            'smen_graviti': -44
        },
        'right': {
            'attack': -44,
            'jump': -44,
            'run': -44,
            'idle': -40,
            'dead': -44,
            'smen_graviti': -44
        }
    }
}

x_offset_characters = {
    'Блейв': {
        'left': {
            'attack': -24,
            'jump': -20,
            'run': 3,
            'idle': 0,
            'dead': -19,
            'smen_graviti': -30
        },
        'right': {
            'attack': -24,
            'jump': -10,
            'run': -15,
            'idle': 0,
            'dead': -19,
            'smen_graviti': 0
        }
    },
    'Элиза': {
        'left': {
            'attack': -16,
            'jump': 0,
            'run': 0,
            'idle': 0,
            'dead': -20,
            'smen_graviti': 0
        },
        'right': {
            'attack': 0,
            'jump': 0,
            'run': 0,
            'idle': 0,
            'dead': 0,
            'smen_graviti': 0
        }
    },
    'Кассиан': {
        'left': {
            'attack': -15,
            'jump': -10,
            'run': -10,
            'idle': -10,
            'dead': -24,
            'smen_graviti': -10
        },
        'right': {
            'attack': 0,
            'jump': 0,
            'run': 0,
            'idle': 0,
            'dead': 0,
            'smen_graviti': 0
        }
    },
    'Рен': {
        'left': {
            'attack': -44,
            'jump': -15,
            'run': -15,
            'idle': -9,
            'dead': -15,
            'smen_graviti': -15
        },
        'right': {
            'attack': -10,
            'jump': -15,
            'run': -15,
            'idle': -9,
            'dead': -15,
            'smen_graviti': -15
        }
    },
    'Келтор': {
        'left': {
            'attack': -30,
            'jump': -20,
            'run': -35,
            'idle': -9,
            'dead': -25,
            'smen_graviti': -20
        },
        'right': {
            'attack': -25,
            'jump': -30,
            'run': -15,
            'idle': -9,
            'dead': -25,
            'smen_graviti': -30
        }
    },
    'Золтан': {
        'left': {
            'attack': -34,
            'jump': -34,
            'run': -34,
            'idle': -34,
            'dead': -34,
            'smen_graviti': -34
        },
        'right': {
            'attack': -6,
            'jump': -6,
            'run': -6,
            'idle': -6,
            'dead': -6,
            'smen_graviti': -6
        }
    },
    'Финн': {
        'left': {
            'attack': -45,
            'jump': -45,
            'run': -45,
            'idle': -45,
            'dead': 0,
            'smen_graviti': -45
        },
        'right': {
            'attack': -5,
            'jump': -5,
            'run': -5,
            'idle': -5,
            'dead': 0,
            'smen_graviti': -5
        }
    },
    'Лиам': {
        'left': {
            'attack': -29,
            'jump': -9,
            'run': -9,
            'idle': -9,
            'dead': -9,
            'smen_graviti': -9
        },
        'right': {
            'attack': -9,
            'jump': -9,
            'run': -9,
            'idle': -9,
            'dead': -9,
            'smen_graviti': -9
        }
    },
    'Эйден': {
        'left': {
            'attack': -25,
            'jump': -25,
            'run': -25,
            'idle': -25,
            'dead': -25,
            'smen_graviti': -25
        },
        'right': {
            'attack': -5,
            'jump': -5,
            'run': -5,
            'idle': -5,
            'dead': -5,
            'smen_graviti': -5
        }
    },
}

list_name_card = [
    'Тихая долина',
    'Прогулка по роще',
    'Рассветный путь',
    'Встреча ветров',
    'Зеленый лабиринт',
    'Скалистый склон',
    'Заточенные пики',
    'Тень дракона',
    'Дыхание вечного'
]

maximum_improvement = {
    'Блейв': {
        'damage': 3,
        'hp': 25,
        'delay': 64
    },
    'Элиза': {
        'damage': 4,
        'hp': 28,
        'delay': 62
    },
    'Кассиан': {
        'damage': 5,
        'hp': 30,
        'delay': 60
    },
    'Рен': {
        'damage': 6,
        'hp': 34,
        'delay': 58
    },
    'Келтор': {
        'damage': 7,
        'hp': 36,
        'delay': 56
    },
    'Золтан': {
        'damage': 8,
        'hp': 39,
        'delay': 54
    },
    'Финн': {
        'damage': 14,
        'hp': 42,
        'delay': 52
    },
    'Лиам': {
        'damage': 17,
        'hp': 52,
        'delay': 50
    },
    'Эйден': {
        'damage': 20,
        'hp': 68,
        'delay': 48
    }
}

spavn_mobs = {
    # [[3168, 3456], 352, 64, 128, 1]]  -  от x1 до x2, y, rad_min, rad_max, grav
    #                       [
    #                          2, 4 - damage
    #                      ],
    #                      [
    #                          3, 6 - hp
    #                      ]
    'Тихая долина': [4,
                     [
                         [
                             [896, 897], 384, 64, 128, 1
                         ],
                         [
                             [1056, 1116], 224, 64, 128, -1
                         ],
                         [
                             [1696, 1792], 192, 64, 128, -1
                         ],
                         [
                             [2080, 2081], 175, 32, 96, 1
                         ],
                         [
                             [2720, 2752], 160, 64, 128, -1
                         ],
                         [
                             [3360, 3361], 352, 64, 128, 1
                         ]
                     ],
                     [
                         1, 1
                     ],
                     [
                         2, 6
                     ]
                     ],
    'Прогулка по роще': [4,
                         [
                             [
                                 [896, 1024], 256, 70, 127, -1
                             ],
                             [
                                 [1440, 1728], 224, 64, 128, -1
                             ],
                             [
                                 [1888, 2080], 355, 65, 126, 1
                             ],
                             [
                                 [2150, 2325], 192, 64, 128, 1
                             ],
                             [
                                 [2600, 2778], 384, 60, 124, 1
                             ],
                             [
                                 [2656, 2657], 160, 64, 128, -1
                             ],
                             [
                                 [3200, 3328], 160, 72, 158, 1
                             ]
                         ],
                         [
                             1, 2
                         ],
                         [
                             4, 9
                         ]
                         ],
    'Рассветный путь': [4,
                        [
                            [
                                [896, 897], 128, 160, 320, -1
                            ],
                            [
                                [1400, 1625], 192, 66, 134, 1
                            ],
                            [
                                [2690, 2912], 355, 65, 126, 1
                            ],
                            [
                                [3125, 3142], 96, 144, 302, -1
                            ],
                            [
                                [3712, 3904], 384, 60, 124, 1
                            ]
                        ],
                        [
                            1, 3
                        ],
                        [
                            8, 11
                        ]
                        ],
    'Встреча ветров': [7,
                       [
                           [
                               [1120, 1504], 160, 144, 300, -1
                           ],
                           [
                               [2240, 2368], 288, 64, 128, 1
                           ],
                           [
                               [2720, 2880], 160, 72, 126, 1
                           ],
                           [
                               [3520, 3525], 160, 40, 92, 1
                           ],
                           [
                               [6240, 6400], 325, 73, 134, 1
                           ],
                           [
                               [6976, 7200], 325, 82, 162, 1
                           ],
                           [
                               [7744, 8000], 352, 76, 156, -1
                           ],
                           [
                               [8800, 9120], 416, 72, 164, -1
                           ],
                           [
                               [6400, 7000], 96, 68, 154, 1
                           ],
                           [
                               [7808, 7968], 96, 76, 184, 1
                           ],
                           [
                               [9344, 9472], 160, 74, 142, 1
                           ],
                           [
                               [9824, 9825], 160, 44, 96, 1
                           ]
                       ],
                       [
                           2, 3
                       ],
                       [
                           10, 13
                       ]
                       ],
    'Зеленый лабиринт': [8,
                         [
                             [
                                 [800, 896], 384, 66, 128, 1
                             ],
                             [
                                 [1824, 1825], 256, 64, 134, 1
                             ],
                             [
                                 [2368, 2370], 128, 44, 96, -1
                             ],
                             [
                                 [2720, 3168], 192, 76, 164, 1
                             ],
                             [
                                 [3776, 3780], 224, 128, 346, -1
                             ],
                             [
                                 [4672, 4736], 324, 68, 142, 1
                             ],
                             [
                                 [5544, 5582], 192, 76, 156, 1
                             ],
                             [
                                 [6400, 6408], 256, 66, 142, -1
                             ],
                             [
                                 [7008, 7010], 322, 71, 154, -1
                             ],
                             [
                                 [7390, 7392], 160, 42, 96, -1
                             ],
                             [
                                 [7776, 7777], 160, 74, 120, -1
                             ],
                             [
                                 [8544, 8640], 324, 68, 142, -1
                             ],
                             [
                                 [8640, 8641], 448, 72, 132, 1
                             ]
                         ],
                         [
                             2, 4
                         ],
                         [
                             10, 15
                         ]
                         ],
    'Скалистый склон': [9,
                        [
                            [
                                [1200, 1400], 256, 77, 232, -1
                            ],
                            [
                                [2560, 2562], 288, 64, 134, 1
                            ],
                            [
                                [2463, 2465], 128, 52, 96, -1
                            ],
                            [
                                [3232, 3233], 96, 64, 128, -1
                            ],
                            [
                                [3680, 3900], 256, 108, 212, 1
                            ],
                            [
                                [5632, 5664], 384, 82, 160, 1
                            ],
                            [
                                [6240, 6272], 232, 68, 146, 1
                            ],
                            [
                                [6816, 7104], 312, 76, 128, -1
                            ],
                            [
                                [7008, 7010], 322, 71, 154, -1
                            ],
                            [
                                [6688, 6746], 320, 66, 156, 1
                            ],
                            [
                                [7712, 7777], 134, 74, 120, -1
                            ],
                            [
                                [8672, 8896], 316, 73, 136, -1
                            ],
                            [
                                [9568, 9632], 422, 52, 96, 1
                            ]
                        ],
                        [
                            3, 5
                        ],
                        [
                            13, 18
                        ]
                        ],
    'Заточенные пики': [10,
                        [
                            [
                                [703, 704], 320, 52, 96, 1
                            ],
                            [
                                [992, 1008], 64, 82, 148, -1
                            ],
                            [
                                [1504, 1512], 96, 52, 128, -1
                            ],
                            [
                                [2176, 2182], 288, 68, 132, 1
                            ],
                            [
                                [3296, 3320], 192, 62, 128, 1
                            ],
                            [
                                [3904, 3934], 192, 70, 136, 1
                            ],
                            [
                                [4512, 4540], 100, 86, 212, 1
                            ],
                            [
                                [5472, 5536], 324, 76, 156, 1
                            ],
                            [
                                [5056, 5096], 100, 64, 128, -1
                            ],
                            [
                                [7616, 7621], 72, 71, 136, -1
                            ],
                            [
                                [8192, 8448], 270, 58, 118, -1
                            ],
                            [
                                [8864, 9056], 160, 73, 136, -1
                            ],
                            [
                                [9792, 9824], 158, 75, 136, -1
                            ],
                            [
                                [10560, 10561], 460, 42, 96, -1
                            ]
                        ],
                        [
                            4, 6
                        ],
                        [
                            16, 20
                        ]
                        ],
    'Тень дракона': [12,
                     [
                         [
                             [896, 912], 224, 73, 136, 1
                         ],
                         [
                             [1440, 1472], 160, 63, 128, -1
                         ],
                         [
                             [1984, 1985], 320, 68, 136, 1
                         ],
                         [
                             [2176, 2182], 288, 68, 132, 1
                         ],
                         [
                             [2336, 2348], 256, 72, 138, 1
                         ],
                         [
                             [3454, 3456], 288, 70, 136, 1
                         ],
                         [
                             [4000, 4008], 235, 64, 134, -1
                         ],
                         [
                             [4606, 4610], 324, 76, 156, 1
                         ],
                         [
                             [5178, 5190], 135, 74, 142, 1
                         ],
                         [
                             [5804, 5872], 40, 68, 128, 1
                         ],
                         [
                             [6560, 6570], 40, 94, 216, -1
                         ],
                         [
                             [7020, 7080], 70, 66, 130, 1
                         ],
                         [
                             [8732, 8748], 158, 75, 136, 1
                         ],
                         [
                             [7776, 7777], 70, 72, 145, -1
                         ],
                         [
                             [10650, 10700], 192, 75, 136, -1
                         ],
                         [
                             [11520, 11552], 448, 65, 128, 1
                         ],
                         [
                             [11838, 11842], 192, 45, 96, -1
                         ],
                         [
                             [5728, 5760], 355, 72, 145, 1
                         ],
                         [
                             [6456, 6500], 390, 77, 252, 1
                         ],
                         [
                             [7160, 7178], 392, 68, 135, -1
                         ],
                         [
                             [8204, 8262], 390, 82, 231, -1
                         ]
                     ],
                     [
                         4, 7
                     ],
                     [
                         18, 22
                     ]
                     ],
    'Дыхание вечного': [13,
                        [
                            [
                                [768, 769], 352, 52, 96, 1
                            ],
                            [
                                [2208, 2209], 50, 74, 132, -1
                            ],
                            [
                                [3103, 3105], 384, 52, 128, 1
                            ],
                            [
                                [3840, 3904], 192, 68, 132, 1
                            ],
                            [
                                [4928, 4942], 192, 73, 144, -1
                            ],
                            [
                                [5888, 5894], 295, 92, 193, -1
                            ],
                            [
                                [6784, 6880], 295, 86, 212, -1
                            ],
                            [
                                [7008, 7040], 295, 76, 156, 1
                            ],
                            [
                                [8352, 8392], 100, 64, 128, -1
                            ],
                            [
                                [7776, 7823], 100, 71, 136, 1
                            ],
                            [
                                [8128, 8213], 384, 71, 152, -1
                            ],
                            [
                                [8672, 8724], 480, 73, 136, -1
                            ],
                            [
                                [9664, 9721], 224, 75, 142, -1
                            ],
                            [
                                [10240, 10324], 320, 76, 152, -1
                            ],
                            [
                                [13280, 13342], 256, 64, 128, 1
                            ]
                        ],
                        [
                            5, 7
                        ],
                        [
                            19, 25
                        ]
                        ]
}

rating_cost = {
    'Тихая долина': 0,
    'Прогулка по роще': 1000,
    'Рассветный путь': 3000,
    'Встреча ветров': 5000,
    'Зеленый лабиринт': 7000,
    'Скалистый склон': 10000,
    'Заточенные пики': 12000,
    'Тень дракона': 15000,
    'Дыхание вечного': 18000
}

rating_character = {
    'Блейв': 0,
    'Элиза': 1200,
    'Кассиан': 3500,
    'Рен': 5400,
    'Келтор': 8000,
    'Золтан': 10900,
    'Финн': 13200,
    'Лиам': 15100,
    'Эйден': 17800
}

portal_cords = {
    "Тихая долина": [
        3744,
        368
    ],
    "Прогулка по роще": [
        3936,
        464
    ],
    "Рассветный путь": [
        4256,
        368
    ],
    "Встреча ветров": [
        10336,
        432
    ],
    "Зеленый лабиринт": [
        9184,
        464
    ],
    "Скалистый склон": [
        10144,
        432
    ],
    "Заточенные пики": [
        10976,
        496
    ],
    "Тень дракона": [
        12384,
        432
    ],
    "Дыхание вечного": [
        14112,
        464
    ]
}

spawn_coordinates = {
    "Тихая долина": [
        256,
        320
    ],
    "Прогулка по роще": [
        256,
        224
    ],
    "Рассветный путь": [
        256,
        256
    ],
    "Встреча ветров": [
        256,
        320
    ],
    "Зеленый лабиринт": [
        256,
        320
    ],
    "Скалистый склон": [
        256,
        224
    ],
    "Заточенные пики": [
        256,
        224
    ],
    "Тень дракона": [
        256,
        256
    ],
    "Дыхание вечного": [
        256,
        256
    ]
}

type_card_background = {
    "choco": "images/background/choco.png",
    "grass": "images/background/grass.png",
    "snow": "images/background/snow.png",
    "cake": "images/background/cake.png",
    "dirt": "images/background/dirt.png",
    "sand": "images/background/sand.png",
    "tundra": "images/background/tundra.png",
    "castle": "images/background/castle.png",
    "purple": "images/background/purple.png"
}

catering_coefficients_levels = {
    'easy': 1.0,
    'normal': 1.4,
    'hard': 1.8
}

catering_coefficients_cards = {
    'Тихая долина': 1.0,
    'Прогулка по роще': 1.2,
    'Рассветный путь': 1.4,
    'Встреча ветров': 1.0,
    'Зеленый лабиринт': 1.2,
    'Скалистый склон': 1.4,
    'Заточенные пики': 1.0,
    'Тень дракона': 1.2,
    'Дыхание вечного': 1.4
}

opening_levels = {
    'easy': 'normal',
    'normal': 'hard'
}

range_rating = {
    'Тихая долина': {
        'loss': [
            100,
            150
        ],
        'win': [
            300,
            390
        ]
    },
    'Прогулка по роще': {
        'loss': [
            120,
            170
        ],
        'win': [
            300,
            400
        ]
    },
    'Рассветный путь': {
        'loss': [
            140,
            190
        ],
        'win': [
            300,
            410
        ]
    },
    'Встреча ветров': {
        'loss': [
            150,
            200
        ],
        'win': [
            300,
            450
        ]
    },
    'Зеленый лабиринт': {
        'loss': [
            170,
            220
        ],
        'win': [
            300,
            400
        ]
    },
    'Скалистый склон': {
        'loss': [
            190,
            240
        ],
        'win': [
            300,
            410
        ]
    },
    'Заточенные пики': {
        'loss': [
            200,
            250
        ],
        'win': [
            300,
            420
        ]
    },
    'Тень дракона': {
        'loss': [
            210,
            260
        ],
        'win': [
            300,
            400
        ]
    },
    'Дыхание вечного': {
        'loss': [
            220,
            270
        ],
        'win': [
            300,
            410
        ]
    }
}

map_index = {
    'Тихая долина': 0,
    'Прогулка по роще': 1,
    'Рассветный путь': 2,
    'Встреча ветров': 3,
    'Зеленый лабиринт': 4,
    'Скалистый склон': 5,
    'Заточенные пики': 6,
    'Тень дракона': 7,
    'Дыхание вечного': 8
}

level_map = {
    'easy': [
        'Тихая долина',
        'Прогулка по роще',
        'Рассветный путь'
    ],
    'normal': [
        'Встреча ветров',
        'Зеленый лабиринт',
        'Скалистый склон'
    ],
    'hard': [
        'Заточенные пики',
        'Тень дракона',
        'Дыхание вечного'
    ]
}

animation_frames_character = {
    'Блейв': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Блейв/attack/{i}.png'), (98, 90))
            for i in range(5)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Блейв/dead/{i}.png'), (90, 90))
            for i in range(5)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Блейв/idle/{i}.png'), (52, 90))
            for i in range(5)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Блейв/jump/{i}.png'), (82, 90))
            for i in range(9)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Блейв/run/{i}.png'), (62, 90))
            for i in range(8)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Блейв/jump/3.png'), (82, 90))
        ]
    },
    'Золтан': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Золтан/attack/{i}.png'), (90, 82))
            for i in range(10)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Золтан/dead/{i}.png'), (90, 82))
            for i in range(10)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Золтан/idle/{i}.png'), (90, 82))
            for i in range(10)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Золтан/jump/{i}.png'), (90, 82))
            for i in range(10)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Золтан/run/{i}.png'), (90, 82))
            for i in range(10)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Золтан/jump/3.png'), (90, 82))
        ]
    },
    'Кассиан': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Кассиан/attack/{i}.png'), (65, 83))
            for i in range(10)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Кассиан/dead/{i}.png'), (74, 83))
            for i in range(10)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Кассиан/idle/{i}.png'), (60, 83))
            for i in range(10)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Кассиан/jump/{i}.png'), (60, 83))
            for i in range(10)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Кассиан/run/{i}.png'), (60, 83))
            for i in range(10)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Кассиан/jump/3.png'), (60, 83))
        ]
    },
    'Келтор': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Келтор/attack/{i}.png'), (110, 108))
            for i in range(5)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Келтор/dead/{i}.png'), (100, 108))
            for i in range(5)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Келтор/idle/{i}.png'), (68, 108))
            for i in range(9)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Келтор/jump/{i}.png'), (100, 108))
            for i in range(9)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Келтор/run/{i}.png'), (100, 108))
            for i in range(8)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Келтор/jump/3.png'), (100, 108))
        ]
    },
    'Лиам': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Лиам/attack/{i}.png'), (90, 105))
            for i in range(5)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Лиам/dead/{i}.png'), (68, 105))
            for i in range(6)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Лиам/idle/{i}.png'), (68, 105))
            for i in range(6)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Лиам/jump/{i}.png'), (68, 105))
            for i in range(9)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Лиам/run/{i}.png'), (68, 105))
            for i in range(8)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Лиам/jump/4.png'), (68, 105))
        ]
    },
    'Рен': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Рен/attack/{i}.png'), (104, 85))
            for i in range(6)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Рен/dead/{i}.png'), (80, 85))
            for i in range(3)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Рен/idle/{i}.png'), (68, 85))
            for i in range(6)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Рен/jump/{i}.png'), (80, 85))
            for i in range(12)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Рен/run/{i}.png'), (80, 85))
            for i in range(8)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Рен/jump/7.png'), (80, 85))
        ]
    },
    'Финн': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Финн/attack/{i}.png'), (100, 80))
            for i in range(10)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Финн/dead/{i}.png'), (100, 80))
            for i in range(10)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Финн/idle/{i}.png'), (100, 80))
            for i in range(10)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Финн/jump/{i}.png'), (100, 80))
            for i in range(10)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Финн/run/{i}.png'), (100, 80))
            for i in range(10)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Финн/jump/2.png'), (100, 80))
        ]
    },
    'Эйден': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Эйден/attack/{i}.png'), (80, 80))
            for i in range(10)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Эйден/dead/{i}.png'), (80, 80))
            for i in range(10)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Эйден/idle/{i}.png'), (80, 80))
            for i in range(10)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Эйден/jump/{i}.png'), (80, 80))
            for i in range(10)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Эйден/run/{i}.png'), (80, 80))
            for i in range(10)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Эйден/jump/3.png'), (80, 80))
        ]
    },
    'Элиза': {
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Элиза/attack/{i}.png'), (66, 82))
            for i in range(10)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Элиза/dead/{i}.png'), (70, 82))
            for i in range(10)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Элиза/idle/{i}.png'), (50, 82))
            for i in range(10)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Элиза/jump/{i}.png'), (50, 82))
            for i in range(10)
        ],
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Элиза/run/{i}.png'), (50, 82))
            for i in range(10)
        ],
        'smen_graviti': [
            pygame.transform.scale(pygame.image.load(f'images/characters/Элиза/jump/3.png'), (50, 82))
        ]
    }
}

animations_mob = {
    0: {
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_0/run/{i}.png'), (128, 90))
            for i in range(8)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_0/idle/{i}.png'), (128, 90))
            for i in range(7)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_0/jump/0.png'), (128, 90))
        ],
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_0/attack/{i}.png'), (128, 90))
            for i in range(15)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_0/dead/{i}.png'), (128, 90))
            for i in range(4)
        ]
    },
    1: {
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_1/run/{i}.png'), (108, 82))
            for i in range(6)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_1/idle/{i}.png'), (108, 82))
            for i in range(7)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_1/jump/0.png'), (108, 82))
        ],
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_1/attack/{i}.png'), (108, 82))
            for i in range(8)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_1/dead/{i}.png'), (108, 82))
            for i in range(5)
        ]
    },
    2: {
        'run': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_2/run/{i}.png'), (128, 90))
            for i in range(8)
        ],
        'idle': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_2/idle/{i}.png'), (128, 90))
            for i in range(7)
        ],
        'jump': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_2/jump/0.png'), (128, 90))
        ],
        'attack': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_2/attack/{i}.png'), (128, 90))
            for i in range(12)
        ],
        'dead': [
            pygame.transform.scale(pygame.image.load(f'images/mobs/skelet_2/dead/{i}.png'), (128, 90))
            for i in range(5)
        ]
    }
}

coin_animation = [
    pygame.transform.scale(pygame.image.load(f'images/coin/{i}.png'), (35, 35)) for i in range(18)
]
