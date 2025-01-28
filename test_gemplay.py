import pygame


def load_images(t_s, number_cart):
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


platfomis = pygame.sprite.Group()


def generate_map(name_card):
    list_map = {
        'winter_breeze': [
            "                       FMLBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBKE              GBBBBBBH               GBBBBBBBBH                                           M               M             FMMMMMMMMMMMMMLBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH    GBBBBBBBH    GBBBBBBBKMMMMLBBBBBBBBBBBBBBH                                ",
            "                         FLBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBKE    M          GBBBBBBH               FMMMMMMMME                                                                                       GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBKMMMMLBBBBJAAAMMMMLBBBBH    GBBBBBBBH    GBBBBKMMMMMMMMMMMMMMMMMMMMMMME                  ",
            "                          FLBBBBBBBBBBBBBBBBBBBBBBBBBBBBKE                FMMMMMME                                                               M                M             FMMMMMMMMMMMMMMMMMMMLBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH    FMMMLBBBH    FMMMLJAAAAIBBBBBBBJAAAAIBBBBH                                          ",
            "                           FLBBBBBBBBBBBBBBBBBBBBBBBBBBKE         M                                                                                                                                 GBBBBBBBBBBBBBBBBBBBBBBKMMMMMMMMMMMMME    FMMMMMMME    GBBBBBBBBBBBBBBBBBBBBBBBJAAAD                                      ",
            "                            FLBBBBBBBBBBBBBBBBBBBBKMMMME  M                                                                                                                                M  CAAAAAIBBBBBBBBBBBBBBBBBBBBBKE                               FMMMMMMLBBBBBBBBBBBBBBBBBBBBH                                      ",
            "                             FMMMMMMMMMMMMMMLBBBBKE                                                                                                                                           FMMMMMMMLBBBBBBBBBBBBBBBBBBBH                                       FMLMMMMMMLBBBBBBBBBBBH                                      ",
            "                                            FMMMME        M                                                                                                                                           FMMMMMMLBBBBBBBBBBBBJAAAAAAAD           CD                           FLBBBBBBBBBBJAAAAD                                 ",
            "                                                                                                                                                                                                             FMLBBBKMMMMLBBBBBBBBBJD          FE                            FMMMLBBBBBBBKMMME                                 ",
            "                                                                                                                                                                                                               FMMME    FMMMMMMMMMME                                            FMMMMMMME                                     ",
            "                                                                                        CAAAAAD            CD                                            A                                       CAAAAAD                                                                                                                      ",
            "                                                                                     CAAIBBBBBH            GJD                                         A                                      CAAIBBBBBJD                                                                                                                     ",
            "                                                                                    CIBBBBBBBBH            GBJAAAAAAAD                     A                                              CAAAIBBBBBBBBBJD                                                                                                                    ",
            "                                                                            CAAAAAAAIBBBBBBBBBH            GBBBBBBBBBJAD            CAAAD                               CAAD             CIBBBBBBBBBBBBBBJAAAD                                                                                                                ",
            "AAAAAAAAAAAAAAAAAAAAD                                                     CAIBBBBBBBBBBBBBBKMME            GBBBBBBBBBBBJAD     CAAAAIBBBH                               GBBJD          CAIBBBBBKMMLBBBBBBBBBBJAAAAAAAAAAD                                                                                                     ",
            "BBBBBBBBBBBBBBBBBBBBJD                                                  CAIBBBBBBBBBBBBBBBBH               GBBBBBBBBBBBBBJAAAAAIBBBBBBBBH                        A      GBBBJD      CAAIBBBBBKME  FMMLBBBBBBBBBBBBBBBBBBJAAD                                                                                                  ",
            "BBBBBBBBBBBBBBBBBBBBBJAAD                                            CAAIBBKMMMLBBBBBBBBBBBH       A       GBBBBBBBBBBBBBBBBBBBBBBBBBBBBH                     A         GBBBBJAAAAAAIBBBBBBBBH       GBBBBBBBBBBBBBBBBBBBBBJAD                                                                                                ",
            "BBBBBBBBBBBBBBBBBBBBBBBBJAAAD                                       CIBBBBBH   FMMLBBBBBBBBJAAD            GBBBBBBBBBKMMMMLBBBBBBBBBBBBBH                   A           GBBBBBBBBBBBBBBBBBBBBJAD   CAIBBBBBBBBBBBBBBBBBBBBBBBJAAAAAAAAD                                                                CAAAAAD   CAAAAAAAAAAAA",
            "BBBBBBBBBBBBBBBBBBBBBBBBBBBBJD                                     CIBBBKMME      FMMMLBBBBBBBH            GBBBBBBBBBH    FMMLBBBBBBBBBBH       A                       GBBBBBBBBBBBBBBBBBBBBBBJAAAIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH                                                                GBBBBBJAAAIBBBBBBBBBBBB",
            "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBJD                                CAAAIBBBBH             GBBBBBBBH            GBBBBBBBBBH       GBBBBBBBBBBH                               GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBH                                                                GBBBBBBBBBBBBBBBBBBBBBB"
        ],
        'winter_kingdom': [
            "                                                                               GBBBBBBBH                                    ",
            "                                                                               GBBBBBBBH        CAAAAAAAAAAAAAD             ",
            "                                     CAAAAAAAAAD                               GBBBBBBBH        FMMMMMMMMMMMMME             ",
            "                                     GKMMMMMMMMECAAAAAAAAAAD                   FMMMMMMME                                    ",
            "                        CAAAAAAAAAAADFE         FMMMMMMMMMME                                                                ",
            "                        GBBBKMMMLBBBH                                                                                       ",
            "                        FMMME   FMMME                                                   CAD                                 ",
            "                                                                                        FME                                 ",
            "                                                                                                                            ",
            "                                                               CAAAAAAAAAAAAAD                                              ",
            "                                                               FMMMMMMMMMMMMME                                              ",
            "                                                                                               CAAAAAAAAAAAAAD              ",
            "                                                                                            A  FMMMMMMMMMMMMME              ",
            "AAAAAAAAAAAAD                                                                                                               ",
            "BBBBBBBBBBBBH                                          CAAAAAAAAAAAAAD                                                      ",
            "MMMMMMMMMMMMECD                                        FMMMMMMMMMMMMME                                                      ",
            "             GJAAAAAAAAAD                                                    CAAAAAAAAAAAAAD                                ",
            "             FMMMMMMMMMME                                                    FMMMMMMMMMMMMME               CAAAAAAAAAAAAAAAA",
            "                                                                                                           FMMMMMMMMMMMMMMMM"
        ]
    }

    return list_map[name_card]


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        return self.rect


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, image_folder, animation_frames, speed, jump_height, gravity, tile_size, tiles,
                 numb):
        super().__init__()

        self.image_folder = image_folder  # Папка с изображениями анимации
        self.animation_frames = animation_frames  # Словарь с кадрами анимации
        self.current_frame = 0
        self.screen = screen
        self.current_animation = 'mest_right'
        self.frame_delay = 5  # Задержка между кадрами анимации
        self.frame_timer = 0  # Таймер для анимации
        self.gravity = gravity
        self.jump_height = jump_height
        self.speed = speed
        self.tile_size = tile_size
        self.tiles = tiles
        self.numb = numb
        self.x = x
        self.velocity_y = 0
        self.change_graviti = True
        self.smen_grav = True
        self.is_jumping = False
        self.pressing_space = False
        self.grav = 1
        self.direction = 'right'

        # Инициализация изображения и rect
        self.image = self.get_current_image()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        self.screen.fill((0, 0, 0))
        n = self.rect.copy()
        n[0] = self.x
        self.screen.blit(self.image, n)
        for tile in self.tiles:
            cord = tile.update().copy()
            pos = (cord[0] - (self.rect.x - self.x), cord[1])
            if -32 < pos[0] < 800 and -32 < pos[1] < 600:
                self.screen.blit(tile.image, pos)

    def get_current_image(self):
        """Возвращает текущий кадр анимации с учетом направления."""
        frame = self.animation_frames[self.current_animation][self.current_frame]
        return frame

    def update(self):
        self.moving_x()
        self.moving_y()
        self.draw()

    def moving_x(self):
        dx = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.is_jumping and not self.pressing_space and self.velocity_y == 0:
            self.is_jumping, self.pressing_space = True, True
            print(self.velocity_y)
            self.velocity_y = -self.jump_height * self.grav
        elif not keys[pygame.K_SPACE] and not self.is_jumping:
            self.pressing_space = False

        if keys[pygame.K_a]:
            dx -= self.speed
            self.direction = 'left'
        if keys[pygame.K_d]:
            dx += self.speed
            self.direction = 'right'

        if keys[pygame.K_w] and not self.is_jumping and self.change_graviti:
            self.is_jumping = True
            self.change_graviti = False
            self.grav = -self.grav
        elif not keys[pygame.K_w] and not self.change_graviti and not self.is_jumping:
            self.change_graviti = True

        old_x = self.rect.x
        self.rect.x = max(min(self.rect.x + dx, self.numb), 0)
        print(self.numb, self.rect.x)
        if pygame.sprite.spritecollide(self, self.tiles, False):
            self.rect.x = old_x
        else:
            if self.rect.x <= 200:
                self.x = max(min(self.x + dx, 600), 0)
            elif self.rect.x >= self.numb - 200:
                self.x = max(min(self.x + dx, 800), 0)
            else:
                self.x = max(min(self.x + dx, 600), 200)

    def moving_y(self):
        self.velocity_y += self.gravity * self.grav
        self.rect.y += self.velocity_y

        if collisions := pygame.sprite.spritecollide(self, self.tiles, False):
            if self.velocity_y > 0:
                self.rect.bottom = collisions[0].rect.top
            elif self.velocity_y < 0:
                self.rect.top = collisions[0].rect.bottom

            self.smen_grav = True
            self.velocity_y = 0
            self.is_jumping = False


class Eloise(Player):
    def __init__(self, screen, x, y, tile_size):
        image_folder = "image_Eloise"
        animation_frames = {
            'img_right': [pygame.transform.scale(pygame.image.load(f'image_Eloise/Run_{i}.png'), (40, 80)) for i in
                          range(9)],
            'img_left': [
                pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'image_Eloise/Run_{i}.png'), (40, 80)),
                                      True, False) for i in range(9)],
            'mest_right': [pygame.transform.scale(pygame.image.load(f'image_Eloise/mest_{i}.png'), (40, 80)) for i in
                           range(9)],
            'mest_left': [
                pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'image_Eloise/mest_{i}.png'), (40, 80)),
                                      True, False) for i in range(9)],
            'jump_right': [pygame.transform.scale(pygame.image.load(f'image_Eloise/Jump_{i}.png'), (40, 85)) for i in
                           range(9)],
            'jump_left': [
                pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'image_Eloise/Jump_{i}.png'), (40, 85)),
                                      True, False) for i in range(9)]
        }
        tiles = pygame.sprite.Group()
        tile_images = load_images(32, '9')
        map_data = generate_map('winter_kingdom')
        for y, row in enumerate(map_data):
            for x, symbol in enumerate(row):
                if symbol in tile_images:
                    image = tile_images[symbol]
                    tile = Tile(image, x * 32, y * 32)
                    tiles.add(tile)
        speed = 4
        jump_height = 10
        gravity = 0.5
        super().__init__(screen, x, y, image_folder, animation_frames, speed, jump_height, gravity, tile_size, tiles,
                         (len(map_data[0]) * 32))


class Gemplay:
    def __init__(self, screen):
        self.screen = screen

    def loading(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))

    class Map:
        def __init__(self):
            pass

    class Tile(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            return self.rect

    class Player(pygame.sprite.Sprite):
        def __init__(self, screen, x, y, image_folder, animation_frames, speed, jump_height, gravity, tile_size, tiles,
                     numb):
            super().__init__()

            self.image_folder = image_folder  # Папка с изображениями анимации
            self.animation_frames = animation_frames  # Словарь с кадрами анимации
            self.current_frame = 0
            self.screen = screen
            self.current_animation = 'mest_right'
            self.frame_delay = 5  # Задержка между кадрами анимации
            self.frame_timer = 0  # Таймер для анимации
            self.gravity = gravity
            self.jump_height = jump_height
            self.speed = speed
            self.tile_size = tile_size
            self.tiles = tiles
            self.numb = numb
            self.x = x
            self.velocity_y = 0
            self.change_graviti = True
            self.smen_grav = True
            self.is_jumping = False
            self.pressing_space = False
            self.grav = 1
            self.direction = 'right'

            # Инициализация изображения и rect
            self.image = self.get_current_image()
            self.rect = self.image.get_rect(topleft=(x, y))

        def draw(self):
            n = self.rect.copy()
            n[0] = self.x
            self.screen.blit(self.image, n)
            for tile in self.tiles:
                cord = tile.update().copy()
                pos = (cord[0] - (self.rect.x - self.x), cord[1])
                if -32 < pos[0] < 800 and -32 < pos[1] < 600:
                    self.screen.blit(tile.image, pos)

        def get_current_image(self):
            """Возвращает текущий кадр анимации с учетом направления."""
            frame = self.animation_frames[self.current_animation][self.current_frame]
            return frame

        def update(self):
            self.moving_x()
            self.moving_y()
            self.draw()

        def moving_x(self):
            dx = 0
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and not self.is_jumping and not self.pressing_space and self.velocity_y == 0:
                self.is_jumping, self.pressing_space = True, True
                print(self.velocity_y)
                self.velocity_y = -self.jump_height * self.grav
            elif not keys[pygame.K_SPACE] and not self.is_jumping:
                self.pressing_space = False

            if keys[pygame.K_a]:
                dx -= self.speed
                self.direction = 'left'
            if keys[pygame.K_d]:
                dx += self.speed
                self.direction = 'right'

            if keys[pygame.K_w] and not self.is_jumping and self.change_graviti:
                self.is_jumping = True
                self.change_graviti = False
                self.grav = -self.grav
            elif not keys[pygame.K_w] and not self.change_graviti and not self.is_jumping:
                self.change_graviti = True

            old_x = self.rect.x
            self.rect.x = max(min(self.rect.x + dx, self.numb), 0)
            print(self.numb, self.rect.x)
            if pygame.sprite.spritecollide(self, self.tiles, False):
                self.rect.x = old_x
            else:
                if self.rect.x <= 200:
                    self.x = max(min(self.x + dx, 600), 0)
                elif self.rect.x >= self.numb - 200:
                    self.x = max(min(self.x + dx, 800), 0)
                else:
                    self.x = max(min(self.x + dx, 600), 200)

        def moving_y(self):
            self.velocity_y += self.gravity * self.grav
            self.rect.y += self.velocity_y

            if collisions := pygame.sprite.spritecollide(self, self.tiles, False):
                if self.velocity_y > 0:
                    self.rect.bottom = collisions[0].rect.top
                elif self.velocity_y < 0:
                    self.rect.top = collisions[0].rect.bottom

                self.smen_grav = True
                self.velocity_y = 0
                self.is_jumping = False


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Передвижение карты")

    player = Eloise(screen, 400, 200, 32)

    game = Gemplay(screen)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    tiles = pygame.sprite.Group()
    main()
