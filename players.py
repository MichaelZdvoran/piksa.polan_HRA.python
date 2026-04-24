import pygame
from constants import (PlayerType, PLAYER_SPEED, PLAYER_JUMP_POWER, 
                       PLAYER_WIDTH, PLAYER_HEIGHT, GRAVITY, 
                       COLOR_WATER, COLOR_FIRE, SCREEN_WIDTH, SCREEN_HEIGHT)
from utils import Vector2
from typing import List
import math

class Player:
    def __init__(self, x: float, y: float, player_type: PlayerType):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.player_type = player_type
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.on_ground = False
        self.gravity = GRAVITY
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.coins_collected = 0
        self.animation_time = 0
        self.direction = 1
    
    def handle_input(self, keys):
        if self.player_type == PlayerType.WATER:
            if keys[pygame.K_LEFT]:
                self.vel.x = -self.speed
                self.direction = -1
            elif keys[pygame.K_RIGHT]:
                self.vel.x = self.speed
                self.direction = 1
            else:
                self.vel.x = 0
            
            if keys[pygame.K_UP] and self.on_ground:
                self.vel.y = -self.jump_power
                self.on_ground = False
        
        else:
            if keys[pygame.K_a]:
                self.vel.x = -self.speed
                self.direction = -1
            elif keys[pygame.K_d]:
                self.vel.x = self.speed
                self.direction = 1
            else:
                self.vel.x = 0
            
            if keys[pygame.K_w] and self.on_ground:
                self.vel.y = -self.jump_power
                self.on_ground = False
    
    def update(self, obstacles: List, coins: List, enemies: List, 
               hazard_pools: List, crossbows: List, buttons: List):
        self.animation_time += 0.1
        
        self.vel.y += self.gravity
        self.pos = self.pos + self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
        self.on_ground = False
        
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel.y > 0:
                    self.pos.y = obstacle.rect.top - self.height
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.pos.y = obstacle.rect.bottom
                    self.vel.y = 0
                elif self.vel.x > 0:
                    self.pos.x = obstacle.rect.left - self.width
                else:
                    self.pos.x = obstacle.rect.right
                
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
        
        # Coin collection
        for coin in coins:
            if coin.check_collision(self.rect):
                coin.collected = True
                self.coins_collected += 1
        
        # Enemy collision
        for enemy in enemies:
            if enemy.check_collision(self.rect):
                return False
        
        # Hazard pool collision
        for pool in hazard_pools:
            if pool.check_collision(self.rect, self.player_type):
                return False
        
        # Crossbow collision
        for crossbow in crossbows:
            if crossbow.check_collision(self.rect):
                return False
        
        # Button collision
        for button in buttons:
            button.check_collision(self.rect, self.player_type)
        
        # Boundaries
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x + self.width > SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH - self.width
        
        if self.pos.y > SCREEN_HEIGHT:
            return False
        
        return True
    
    def draw(self, screen):
        color = COLOR_WATER if self.player_type == PlayerType.WATER else COLOR_FIRE
        bob_offset = int(2 * math.sin(self.animation_time)) if self.on_ground else 0
        
        # Body with gradient effect
        pygame.draw.rect(screen, color, (self.pos.x, self.pos.y + bob_offset, self.width, self.height), border_radius=5)
        
        # Glow effect
        pygame.draw.rect(screen, (255, 255, 255), (self.pos.x, self.pos.y + bob_offset, self.width, self.height), 2, border_radius=5)
        
        # Eyes
        eye_color = (255, 255, 255)
        left_eye_x = self.pos.x + 8 + (self.direction * 2)
        right_eye_x = self.pos.x + 22 + (self.direction * 2)
        
        pygame.draw.circle(screen, eye_color, (left_eye_x, self.pos.y + 8 + bob_offset), 3)
        pygame.draw.circle(screen, eye_color, (right_eye_x, self.pos.y + 8 + bob_offset), 3)
        pygame.draw.circle(screen, (0, 0, 0), (left_eye_x, self.pos.y + 8 + bob_offset), 1)
        pygame.draw.circle(screen, (0, 0, 0), (right_eye_x, self.pos.y + 8 + bob_offset), 1)
