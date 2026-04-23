import pygame
import sys
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple
import random

pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
LEVEL_TIME = 300  # 5 minutes in seconds

# Colors
COLOR_BG = (20, 20, 30)
COLOR_WATER = (100, 150, 255)
COLOR_FIRE = (255, 100, 50)
COLOR_GROUND = (80, 120, 60)
COLOR_WALL = (100, 100, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON = (100, 150, 255)
COLOR_BUTTON_HOVER = (150, 200, 255)

class PlayerType(Enum):
    WATER = 1
    FIRE = 2

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, screen):
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 3, border_radius=10)
        
        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Player:
    def __init__(self, x: float, y: float, player_type: PlayerType):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.width = 30
        self.height = 40
        self.player_type = player_type
        self.speed = 5
        self.jump_power = 15
        self.on_ground = False
        self.gravity = 0.6
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def handle_input(self, keys):
        if self.player_type == PlayerType.WATER:
            if keys[pygame.K_LEFT]:
                self.vel.x = -self.speed
            elif keys[pygame.K_RIGHT]:
                self.vel.x = self.speed
            else:
                self.vel.x = 0
            
            if keys[pygame.K_UP] and self.on_ground:
                self.vel.y = -self.jump_power
                self.on_ground = False
        
        else:  # FIRE
            if keys[pygame.K_a]:
                self.vel.x = -self.speed
            elif keys[pygame.K_d]:
                self.vel.x = self.speed
            else:
                self.vel.x = 0
            
            if keys[pygame.K_w] and self.on_ground:
                self.vel.y = -self.jump_power
                self.on_ground = False
    
    def update(self, obstacles: List['Obstacle'], other_player: 'Player'):
        # Apply gravity
        self.vel.y += self.gravity
        
        # Update position
        self.pos = self.pos + self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
        # Collision detection
        self.on_ground = False
        
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel.y > 0:  # Falling
                    self.pos.y = obstacle.rect.top - self.height
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:  # Jumping
                    self.pos.y = obstacle.rect.bottom
                    self.vel.y = 0
                elif self.vel.x > 0:  # Moving right
                    self.pos.x = obstacle.rect.left - self.width
                else:  # Moving left
                    self.pos.x = obstacle.rect.right
                
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
        
        # Boundary collision
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x + self.width > SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH - self.width
        
        # Out of bounds
        if self.pos.y > SCREEN_HEIGHT:
            return False
        
        return True
    
    def draw(self, screen):
        color = COLOR_WATER if self.player_type == PlayerType.WATER else COLOR_FIRE
        pygame.draw.rect(screen, color, (self.pos.x, self.pos.y, self.width, self.height), border_radius=5)
        pygame.draw.circle(screen, (255, 255, 255), (self.pos.x + self.width // 2, self.pos.y + 8), 4)

class Obstacle:
    def __init__(self, x: float, y: float, width: float, height: float, obstacle_type: str = "solid"):
        self.rect = pygame.Rect(x, y, width, height)
        self.obstacle_type = obstacle_type
        self.x = x
        self.y = y
    
    def draw(self, screen):
        if self.obstacle_type == "solid":
            pygame.draw.rect(screen, COLOR_WALL, self.rect)
        elif self.obstacle_type == "water_platform":
            pygame.draw.rect(screen, COLOR_WATER, self.rect)
        elif self.obstacle_type == "fire_platform":
            pygame.draw.rect(screen, COLOR_FIRE, self.rect)

class Goal:
    def __init__(self, x: float, y: float, player_type: PlayerType):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.player_type = player_type
        self.radius = 20
        self.x = x
        self.y = y
    
    def draw(self, screen):
        color = COLOR_WATER if self.player_type == PlayerType.WATER else COLOR_FIRE
        pygame.draw.circle(screen, color, self.rect.center, self.radius, 3)
        pygame.draw.circle(screen, color, self.rect.center, self.radius - 8, 2)

class Level:
    def __init__(self, level_num: int):
        self.level_num = level_num
        self.obstacles = []
        self.water_goal = None
        self.fire_goal = None
        self.time_limit = LEVEL_TIME
        self._create_level()
    
    def _create_level(self):
        if self.level_num == 1:
            self._level_1()
        elif self.level_num == 2:
            self._level_2()
        elif self.level_num == 3:
            self._level_3()
        elif self.level_num == 4:
            self._level_4()
        else:
            self._level_5()
    
    def _level_1(self):
        # Simple introduction level
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.obstacles.append(Obstacle(200, 600, 150, 30))
        self.obstacles.append(Obstacle(600, 500, 150, 30))
        self.obstacles.append(Obstacle(1000, 400, 150, 30))
        
        self.water_goal = Goal(100, 650, PlayerType.WATER)
        self.fire_goal = Goal(1100, 300, PlayerType.FIRE)
        self.time_limit = 300
    
    def _level_2(self):
        # Multiple platforms and coordination
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.obstacles.append(Obstacle(100, 600, 200, 30))
        self.obstacles.append(Obstacle(450, 550, 300, 30))
        self.obstacles.append(Obstacle(900, 600, 200, 30))
        self.obstacles.append(Obstacle(300, 350, 600, 30))
        self.obstacles.append(Obstacle(150, 200, 200, 30))
        self.obstacles.append(Obstacle(850, 200, 200, 30))
        
        self.water_goal = Goal(200, 100, PlayerType.WATER)
        self.fire_goal = Goal(950, 100, PlayerType.FIRE)
        self.time_limit = 300
    
    def _level_3(self):
        # Challenging puzzle with narrow passages
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.obstacles.append(Obstacle(0, 0, 50, SCREEN_HEIGHT))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT))
        
        self.obstacles.append(Obstacle(100, 650, 150, 30))
        self.obstacles.append(Obstacle(400, 600, 100, 30))
        self.obstacles.append(Obstacle(700, 650, 150, 30))
        self.obstacles.append(Obstacle(300, 450, 600, 30))
        self.obstacles.append(Obstacle(150, 300, 250, 30))
        self.obstacles.append(Obstacle(800, 300, 250, 30))
        self.obstacles.append(Obstacle(450, 150, 300, 30))
        
        self.water_goal = Goal(550, 50, PlayerType.WATER)
        self.fire_goal = Goal(550, 50, PlayerType.FIRE)
        self.time_limit = 300
    
    def _level_4(self):
        # Puzzle requiring both players to cooperate
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.obstacles.append(Obstacle(200, 650, 800, 30))
        self.obstacles.append(Obstacle(100, 500, 300, 30))
        self.obstacles.append(Obstacle(800, 500, 300, 30))
        self.obstacles.append(Obstacle(450, 350, 300, 30))
        
        self.water_goal = Goal(550, 250, PlayerType.WATER)
        self.fire_goal = Goal(550, 250, PlayerType.FIRE)
        self.time_limit = 300
    
    def _level_5(self):
        # Final challenge
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.obstacles.append(Obstacle(150, 700, 100, 30))
        self.obstacles.append(Obstacle(400, 650, 100, 30))
        self.obstacles.append(Obstacle(650, 700, 100, 30))
        self.obstacles.append(Obstacle(900, 650, 100, 30))
        self.obstacles.append(Obstacle(300, 550, 600, 30))
        self.obstacles.append(Obstacle(150, 400, 200, 30))
        self.obstacles.append(Obstacle(850, 400, 200, 30))
        self.obstacles.append(Obstacle(450, 250, 300, 30))
        
        self.water_goal = Goal(550, 150, PlayerType.WATER)
        self.fire_goal = Goal(550, 150, PlayerType.FIRE)
        self.time_limit = 300

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fire & Water: Puzzle Adventure")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)
        
        self.state = GameState.MENU
        self.current_level = 1
        self.max_level = 5
        self.start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60, "START GAME")
        
        self.water_player = None
        self.fire_player = None
        self.level = None
        self.level_time_remaining = 0
        self.level_start_time = 0
    
    def start_level(self, level_num: int):
        self.current_level = level_num
        self.level = Level(level_num)
        self.water_player = Player(100, SCREEN_HEIGHT - 150, PlayerType.WATER)
        self.fire_player = Player(SCREEN_WIDTH - 130, SCREEN_HEIGHT - 150, PlayerType.FIRE)
        self.state = GameState.PLAYING
        self.level_start_time = pygame.time.get_ticks()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEMOTION:
                if self.state == GameState.MENU:
                    self.start_button.check_hover(event.pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.MENU:
                    if self.start_button.is_clicked(event.pos):
                        self.start_level(1)
                
                elif self.state == GameState.LEVEL_COMPLETE:
                    if self.current_level < self.max_level:
                        self.start_level(self.current_level + 1)
                    else:
                        self.state = GameState.MENU
                
                elif self.state == GameState.GAME_OVER:
                    self.state = GameState.MENU
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
        
        return True
    
    def update(self):
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            
            self.water_player.handle_input(keys)
            self.fire_player.handle_input(keys)
            
            water_alive = self.water_player.update(self.level.obstacles, self.fire_player)
            fire_alive = self.fire_player.update(self.level.obstacles, self.water_player)
            
            if not water_alive or not fire_alive:
                self.state = GameState.GAME_OVER
            
            # Check goal collisions
            if self.water_player.rect.colliderect(self.level.water_goal.rect):
                if self.fire_player.rect.colliderect(self.level.fire_goal.rect):
                    self.state = GameState.LEVEL_COMPLETE
            
            # Update timer
            elapsed = (pygame.time.get_ticks() - self.level_start_time) / 1000
            self.level_time_remaining = max(0, self.level.time_limit - elapsed)
            
            if self.level_time_remaining <= 0:
                self.state = GameState.GAME_OVER
    
    def draw(self):
        self.screen.fill(COLOR_BG)
        
        if self.state == GameState.MENU:
            self._draw_menu()
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.LEVEL_COMPLETE:
            self._draw_level_complete()
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()
        
        pygame.display.flip()
    
    def _draw_menu(self):
        title = self.font_large.render("FIRE & WATER", True, COLOR_TEXT)
        subtitle = self.font_medium.render("Puzzle Adventure", True, COLOR_TEXT)
        instructions = self.font_tiny.render("Water: Arrow Keys | Fire: WASD", True, COLOR_TEXT)
        
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 300))
        
        self.start_button.draw(self.screen)
        
        water_text = self.font_small.render("Guide Water to the goal!", True, COLOR_WATER)
        fire_text = self.font_small.render("Guide Fire to the goal!", True, COLOR_FIRE)
        self.screen.blit(water_text, (50, SCREEN_HEIGHT - 150))
        self.screen.blit(fire_text, (50, SCREEN_HEIGHT - 100))
    
    def _draw_game(self):
        # Draw level
        for obstacle in self.level.obstacles:
            obstacle.draw(self.screen)
        
        # Draw goals
        self.level.water_goal.draw(self.screen)
        self.level.fire_goal.draw(self.screen)
        
        # Draw players
        self.water_player.draw(self.screen)
        self.fire_player.draw(self.screen)
        
        # Draw UI
        level_text = self.font_small.render(f"Level {self.current_level}", True, COLOR_TEXT)
        self.screen.blit(level_text, (20, 20))
        
        minutes = int(self.level_time_remaining) // 60
        seconds = int(self.level_time_remaining) % 60
        time_text = self.font_medium.render(f"{minutes}:{seconds:02d}", True, COLOR_TEXT)
        time_rect = time_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(time_text, time_rect)
        
        # Warning if time low
        if self.level_time_remaining < 30:
            warning = self.font_small.render("Time Running Out!", True, (255, 100, 100))
            self.screen.blit(warning, (SCREEN_WIDTH // 2 - warning.get_width() // 2, 20))
    
    def _draw_level_complete(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        complete_text = self.font_large.render("LEVEL COMPLETE!", True, (100, 255, 100))
        self.screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        if self.current_level < self.max_level:
            next_text = self.font_small.render("Click to continue...", True, COLOR_TEXT)
        else:
            next_text = self.font_small.render("You completed all levels! Click to return to menu.", True, COLOR_TEXT)
        self.screen.blit(next_text, (SCREEN_WIDTH // 2 - next_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        gameover_text = self.font_large.render("GAME OVER", True, (255, 100, 100))
        self.screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        retry_text = self.font_small.render("Click to return to menu", True, COLOR_TEXT)
        self.screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
