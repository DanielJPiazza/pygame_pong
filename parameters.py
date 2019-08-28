# Standard imports.
import pygame
from os import environ

# Screen setup.
WINDOW_X, WINDOW_Y = 40, 50
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_X, WINDOW_Y)
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Pong")

# Clock setup.
clock = pygame.time.Clock()
FPS = 120

# Paddle, ball, and net parameters.
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_WIDTH, BALL_VELOCITY = 10, 5
NET = pygame.Rect(WIDTH/2, 0, 1, HEIGHT)

# TitleScene menu button parameters.
TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT = 100, 50

# Global colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Global fonts.
FONT_SM = pygame.font.SysFont(pygame.font.get_default_font(), 24)
FONT_LG = pygame.font.SysFont(pygame.font.get_default_font(), 124)