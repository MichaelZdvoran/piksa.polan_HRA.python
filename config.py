import pygame

# Grafika a velikost
TILE_SIZE = 24
MAZE_ROWS = 21
MAZE_COLS = 21
WIDTH = TILE_SIZE * MAZE_COLS
HEIGHT = TILE_SIZE * MAZE_ROWS
FPS = 60

COLORS = {
    'background': (8, 12, 38),
    'wall': (30, 144, 255),
    'pellet': (250, 250, 210),
    'player': (255, 220, 85),
    'ghosts': [(240, 100, 100), (120, 240, 240), (178, 102, 255), (250, 170, 90)],
    'text': (240, 240, 240),
    'score_bg': (20, 25, 80),
}

PLAYER_SPEED = 150  # px/s
GHOST_SPEED = 110

pygame.init()
FONT = pygame.font.SysFont('Consolas', 22)
FONT_BIG = pygame.font.SysFont('Consolas', 40, bold=True)
