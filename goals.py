import pygame
from constants import COLOR_WATER, COLOR_FIRE, PlayerType

class Goal:
    def __init__(self, x: float, y: float, player_type: PlayerType):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.player_type = player_type
        self.radius = 20
        self.x = x
        self.y = y
        self.pulse_time = 0
    
    def update(self):
        self.pulse_time += 0.05
    
    def draw(self, screen):
        color = COLOR_WATER if self.player_type == PlayerType.WATER else COLOR_FIRE
        import math
        pulse = int(3 * abs(math.sin(self.pulse_time)))
        
        pygame.draw.circle(screen, color, self.rect.center, self.radius + pulse, 3)
        pygame.draw.circle(screen, color, self.rect.center, self.radius - 8, 2)

# This file is replaced by the Door class in obstacles.py
