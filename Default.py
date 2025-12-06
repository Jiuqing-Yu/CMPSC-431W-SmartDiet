import pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 150, 255)
GRAY = (180, 180, 180)
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TITLE = "Pygame Template"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
