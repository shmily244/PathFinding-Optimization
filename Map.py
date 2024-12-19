import pygame
import sys

screen_size = 800
cell_size = screen_size // 25

# Màu sắc
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

screen = pygame.display.set_mode((screen_size, screen_size))
N = 25

dx = [1, -1, 0, 0]
dy = [0, 0, -1, 1]

# Vẽ lưới
def draw_grid():
    for x in range(0, screen_size, cell_size):
        for y in range(0, screen_size, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, black, rect, 1)  # Vẽ ô vuông


def fill_cell(x, y, color):
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, color, rect)  # Tô màu ô
    pygame.display.flip()  # Cập nhật màn hình
