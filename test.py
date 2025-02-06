import pygame
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Процентное соотношение круга")

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)


def draw_percentage_circle(surface, color, center, radius, percentage):
    start_angle = -math.pi / 2  # Начинаем с 90 градусов (верх)
    end_angle = start_angle + (2 * math.pi * (percentage / 100))

    points = [center]  # Начальная точка в центре круга
    for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1):
        rad = math.radians(angle)
        x = int(center[0] + radius * math.cos(rad))
        y = int(center[1] + radius * math.sin(rad))
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)


# Основные параметры
center_x, center_y = width // 2, height // 2
radius = 100
max_value = 100
current_value = 75

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    center_x, center_y = 200, 200
    radius = 20
    start_angle = -math.pi / 2  # Начинаем с 90 градусов (верх)
    end_angle = start_angle + (2 * math.pi * (((current_value / max_value) * 100) / 100))

    points = [[center_x, center_y]]  # Начальная точка в центре круга
    for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1):
        rad = math.radians(angle)
        x = int(center_x + radius * math.cos(rad))
        y = int(center_y + radius * math.sin(rad))
        points.append((x, y))

    pygame.draw.polygon(screen, (30, 144, 255), points)
    pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), radius + 2, 2)  # Контур круга
    pygame.display.flip()

pygame.quit()
