import pygame


def load_images():
    images = {
        'A': pygame.image.load("images/1.png").convert_alpha(),
        'B': pygame.image.load("images/2.png").convert_alpha(),
        'C': pygame.image.load("images/3.png").convert_alpha(),
        'D': pygame.image.load("images/4.png").convert_alpha(),
        'E': pygame.image.load("images/5.png").convert_alpha(),
        'F': pygame.image.load("images/6.png").convert_alpha(),
        'G': pygame.image.load("images/7.png").convert_alpha(),
        'H': pygame.image.load("images/8.png").convert_alpha(),
        'I': pygame.image.load("images/9.png").convert_alpha(),
        'J': pygame.image.load("images/10.png").convert_alpha(),
        'K': pygame.image.load("images/11.png").convert_alpha()
    }

    for key, image in images.items():
        images[key] = pygame.transform.scale(image, (32, 32))

    return images


platfomis = pygame.sprite.Group()


def generate_map():
    map_data = [
        '                                 GCCCCCCCF          GCCCCCF                     GCCCCF                          ',
        '                                 GCCCCCCCF          GCCCCCH                     GCCCCF                          ',
        '                                 ICCCCCCCF          GCCCCF                      GCCCCF                          ',
        '                                  GCCCCCCF          GCCCCF                      IJJJJH                          ',
        '                                  GKCCCCCF          IJJJJH                                                      ',
        '                                  IJJJJJJH                                                                      ',
        '                                                                                                                ',
        '                                                                                                                ',
        '                                                             DAAAAE                                             ',
        '                                                            DCCCCCCE                                            ',
        '                                                 DABBE     DCCCCCCCCE                                           ',
        '                                                DCCCCF  DBBCCCCCCCCCCAAE                                        ',
        '                    DABBAE                    DACCCCCF  GCCCCCCCCCCCCCCCE                                       ',
        '                   DCCCCCCE                  DCCCCCCCF  GCCCCCCCCCCCCCCCCE                                      ',
        '                  DCCCCCCCCE                DCCCCCCCCF  GCCCCCCCCCCCCCCCCCE         DAABE        DABBBE     DAAA',
        '                 DCCCCCCCCCCBAAAAAAE    DAAACCCCCCCCCF  GCCCCCCCCCCCCCCCCCCEABBBAE  GCCCCE      DCCCCCCE   DCCCC',
        'BBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCF    GCCCCCCCCCCCCF  GCCCCCCCCCCCCCCCCCCCCCCCCF  GCCCCCE    DCCCCCCCCAAACCCCC',
        'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCF    GCCCCCCCCCCCCF  GCCCCCCCCCCCCCCCCCCCCCCCCF  GCCCCCCBBAACCCCCCCCCCCCCCCCC',
        'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCF    GCCCCCCCCCCCCF  GCCCCCCCCCCCCCCCCCCCCCCCCF  GCCCCCCCCCCCCCCCCCCCCCCCCCCC']

    return map_data


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.map_data = generate_map()
        self.images = load_images()
        self.x = 0
        self.bac_x = 0
        self.bac = pygame.image.load('image/background.jpeg')

        self.tile_list = []

        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                x, y = col * 32, row * 32
                if (zn := self.map_data[row][col]) != ' ':
                    img = self.images[str(zn)]
                    img_rect = img.get_rect()
                    img_rect.x = x
                    img_rect.y = y
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

    def draw(self):
        self.screen.blit(self.bac, (self.bac_x, 0))
        self.screen.blit(self.bac, (self.bac_x + 800, 0))
        for i in range(len(self.tile_list)):
            cord = self.tile_list[i][1].copy()
            cord.x = self.x + cord.x
            self.screen.blit(self.tile_list[i][0], cord)

    def update(self, x):
        if self.bac_x > 0:
            self.bac_x = -800
        elif self.bac_x < -800:
            self.bac_x = 0

        if x < 300:
            self.x += 4
        if x > 500:
            self.x -= 4

        self.x = min(max(self.x, -len(self.map_data[0]) * 32 + 800), 0)


class Player:
    def __init__(self, screen, x, y, map):
        self.screen = screen
        self.map = map
        img = pygame.image.load('image/Idle__007.png')
        self.image = pygame.transform.scale(img, (40, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.jumped:
            self.vel_y = -18
            self.jumped = False
        if keys[pygame.K_a]:
            dx -= 5
        if keys[pygame.K_d]:
            dx += 5

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in self.map.tile_list:
            cords = tile[1].copy()
            cords.x = self.map.x + cords.x

            if cords.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if cords.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = cords.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.jumped = True
                    dy = cords.top - self.rect.bottom
                    self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

        self.map.update(self.rect.x)

        if not (300 < self.rect.x < 500):
            if self.rect.x < 300 and self.map.x != 0:
                self.rect.x = 300
                self.map.bac_x += 3
            elif self.rect.x > 500 and self.map.x != -len(self.map.map_data[0]) * 32 + 800:
                self.rect.x = 500
                self.map.bac_x -= 3

            if self.rect.x > 750:
                self.rect.x = 750
            elif self.rect.x < 0:
                self.rect.x = 0

        self.draw()


class Platform(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__(platfomis)
        self.image = pygame.Surface((coords[2], coords[3]))
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(coords[0], coords[1], coords[2], coords[3])


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Передвижение карты")

    map = Map(screen)
    player = Player(screen, 400, 200, map)

    platform_coords = [
        (100, 200, 150, 20),  # x, y, width, height
        (300, 350, 200, 30),
        (550, 150, 100, 40),
        (150, 450, 300, 20),
        (650, 500, 80, 50),
    ]

    # for coords in platform_coords:
    #    Platform(coords)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        map.draw()
        player.update()
        # platfomis.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
