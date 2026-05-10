import pygame
from .constants import (PlayerType, PLAYER_SPEED, PLAYER_JUMP_POWER, 
                       PLAYER_WIDTH, PLAYER_HEIGHT, GRAVITY, 
                       COLOR_WATER, COLOR_FIRE, SCREEN_WIDTH, SCREEN_HEIGHT)
from .utils import Vector2
from typing import List
import math

class Player:
    def __init__(self, x: float, y: float, player_type: PlayerType, color: tuple):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.player_type = player_type
        self.color = color
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.on_ground = False
        self.gravity = GRAVITY
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.coins_collected = 0
        self.animation_time = 0
        self.direction = 1
        self.jump_spark_time = 0
    
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
        if not self.on_ground:
            self.jump_spark_time += 0.2
        
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
            if coin.check_collision(self.rect, self.player_type):
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
        moving = abs(self.vel.x) > 0.1
        bob_offset = int(3 * math.sin(self.animation_time * 2.8)) if self.on_ground and moving else 0
        jump_stretch = max(-5, min(6, int(-self.vel.y * 0.28))) if not self.on_ground else 0
        run_cycle = self.animation_time * 5.5 if moving else self.animation_time * 1.5

        if self.player_type == PlayerType.WATER:
            self._draw_water_sprite(screen, bob_offset, jump_stretch, run_cycle, moving)
        else:
            self._draw_fire_sprite(screen, bob_offset, jump_stretch, run_cycle, moving)

    def _draw_shadow(self, screen, bob_offset):
        shadow_width = max(18, self.width - abs(int(self.vel.y * 0.35)))
        shadow = pygame.Surface((shadow_width, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 70), shadow.get_rect())
        screen.blit(shadow, (self.pos.x + (self.width - shadow_width) // 2, self.pos.y + self.height + 2 + max(0, bob_offset)))

    def _draw_water_sprite(self, screen, bob_offset, jump_stretch, run_cycle, moving):
        x = int(self.pos.x)
        y = int(self.pos.y + bob_offset)
        body_h = self.height + jump_stretch
        center_x = x + self.width // 2
        splash = abs(math.sin(run_cycle))

        self._draw_shadow(screen, bob_offset)
        for i in range(3 if moving else 1):
            droplet_x = center_x - self.direction * (18 + i * 6)
            droplet_y = y + 30 + int(math.sin(run_cycle + i) * 5)
            pygame.draw.circle(screen, (70, 180, 255), (droplet_x, droplet_y), max(2, 4 - i))

        body_rect = pygame.Rect(x + 2, y + 6 - jump_stretch // 2, self.width - 4, body_h - 4)
        pygame.draw.ellipse(screen, (44, 116, 220), body_rect.inflate(8, 4))
        pygame.draw.ellipse(screen, self.color, body_rect)
        pygame.draw.polygon(screen, self.color, [(center_x, y - 4 - jump_stretch), (x + 5, y + 15), (x + self.width - 5, y + 15)])
        pygame.draw.polygon(screen, (170, 230, 255), [(center_x - 4, y + 3), (center_x - 12, y + 15), (center_x + 2, y + 13)])

        arm_y = y + 24
        arm_swing = int(math.sin(run_cycle) * 7) if moving else 0
        pygame.draw.line(screen, (180, 235, 255), (x + 4, arm_y), (x - 5, arm_y + arm_swing), 4)
        pygame.draw.line(screen, (180, 235, 255), (x + self.width - 4, arm_y), (x + self.width + 5, arm_y - arm_swing), 4)

        foot_y = y + self.height + 1
        step = int(math.sin(run_cycle) * 6) if moving else 0
        pygame.draw.line(screen, (35, 100, 200), (center_x - 6, y + self.height - 3), (center_x - 11 - step, foot_y), 4)
        pygame.draw.line(screen, (35, 100, 200), (center_x + 6, y + self.height - 3), (center_x + 11 + step, foot_y), 4)

        for i in range(2):
            wave_y = y + 30 + i * 7
            pygame.draw.arc(screen, (205, 245, 255), (x + 5, wave_y, self.width - 10, 8), 0, math.pi, 2)

        self._draw_face(screen, x, y + 4, (5, 35, 70))
        if not self.on_ground:
            for i in range(4):
                px = x + 3 + i * 7
                py = y + self.height - 2 + int(math.sin(self.jump_spark_time + i) * 5)
                pygame.draw.circle(screen, (155, 225, 255), (px, py), 2 + int(splash))

    def _draw_fire_sprite(self, screen, bob_offset, jump_stretch, run_cycle, moving):
        x = int(self.pos.x)
        y = int(self.pos.y + bob_offset)
        center_x = x + self.width // 2
        flame_tip = y - 7 - jump_stretch + int(math.sin(self.animation_time * 4) * 3)

        self._draw_shadow(screen, bob_offset)
        for i in range(4 if moving else 2):
            ember_x = center_x - self.direction * (17 + i * 5)
            ember_y = y + 28 - i * 7 + int(math.sin(run_cycle + i) * 4)
            pygame.draw.circle(screen, (255, 178, 64), (ember_x, ember_y), max(2, 4 - i))

        outer = [
            (center_x, flame_tip),
            (x + self.width + 2, y + 13),
            (x + self.width - 1, y + self.height - 2),
            (x + 4, y + self.height),
            (x - 3, y + 14),
        ]
        inner = [
            (center_x + 2, y + 3),
            (x + self.width - 6, y + 17),
            (x + self.width - 9, y + self.height - 5),
            (x + 9, y + self.height - 4),
            (x + 7, y + 18),
        ]
        core = [
            (center_x + int(math.sin(run_cycle) * 2), y + 10),
            (center_x + 8, y + 26),
            (center_x + 2, y + self.height - 7),
            (center_x - 8, y + 27),
        ]
        pygame.draw.polygon(screen, (154, 34, 26), outer)
        pygame.draw.polygon(screen, self.color, inner)
        pygame.draw.polygon(screen, (255, 220, 92), core)

        arm_y = y + 24
        arm_swing = int(math.sin(run_cycle) * 8) if moving else 0
        pygame.draw.line(screen, (255, 172, 65), (x + 5, arm_y), (x - 5, arm_y + arm_swing), 4)
        pygame.draw.line(screen, (255, 172, 65), (x + self.width - 5, arm_y), (x + self.width + 5, arm_y - arm_swing), 4)

        foot_y = y + self.height + 1
        step = int(math.sin(run_cycle) * 6) if moving else 0
        pygame.draw.line(screen, (126, 34, 24), (center_x - 6, y + self.height - 5), (center_x - 12 - step, foot_y), 4)
        pygame.draw.line(screen, (126, 34, 24), (center_x + 6, y + self.height - 5), (center_x + 12 + step, foot_y), 4)

        self._draw_face(screen, x, y + 5, (65, 18, 10))
        if not self.on_ground:
            for i in range(5):
                px = x + 4 + i * 6
                py = y + self.height - 1 + int(math.sin(self.jump_spark_time + i * 0.7) * 7)
                pygame.draw.circle(screen, (255, 205, 88), (px, py), 2)

    def _draw_face(self, screen, x, y, pupil_color):
        eye_y = y + 12
        left_eye_x = x + 9 + (self.direction * 2)
        right_eye_x = x + 21 + (self.direction * 2)
        pygame.draw.circle(screen, (255, 255, 255), (left_eye_x, eye_y), 4)
        pygame.draw.circle(screen, (255, 255, 255), (right_eye_x, eye_y), 4)
        pygame.draw.circle(screen, pupil_color, (left_eye_x + self.direction, eye_y), 2)
        pygame.draw.circle(screen, pupil_color, (right_eye_x + self.direction, eye_y), 2)

        mouth_y = y + 27
        if self.on_ground:
            pygame.draw.arc(screen, pupil_color, (x + 10, mouth_y - 5, 10, 8), 0, math.pi, 2)
        else:
            pygame.draw.circle(screen, pupil_color, (x + 15, mouth_y), 2)

