import pygame
import math
import random
from constants import (COLOR_WALL, COLOR_WATER, COLOR_FIRE, 
                       COLOR_LAVA, COLOR_WATER_POOL, COLOR_DOOR, PlayerType,
                       COLOR_DOOR_OPEN, COLOR_BUTTON_INACTIVE, COLOR_BUTTON_ACTIVE,
                       COLOR_PLATFORM_MOVING, SCREEN_WIDTH)

class Obstacle:
    def __init__(self, x: float, y: float, width: float, height: float, obstacle_type: str = "solid"):
        self.rect = pygame.Rect(x, y, width, height)
        self.obstacle_type = obstacle_type
        self.x = x
        self.y = y
    
    def draw(self, screen):
        if self.obstacle_type == "solid":
            pygame.draw.rect(screen, COLOR_WALL, self.rect)
            pygame.draw.rect(screen, (80, 80, 80), self.rect, 2)
            # Add pattern
            for i in range(0, int(self.rect.width), 20):
                pygame.draw.line(screen, (60, 60, 70), (self.rect.x + i, self.rect.y), (self.rect.x + i + 10, self.rect.y + self.rect.height), 1)
        elif self.obstacle_type == "water_platform":
            pygame.draw.rect(screen, COLOR_WATER, self.rect)
            pygame.draw.rect(screen, (50, 100, 200), self.rect, 2)
        elif self.obstacle_type == "fire_platform":
            pygame.draw.rect(screen, COLOR_FIRE, self.rect)
            pygame.draw.rect(screen, (200, 50, 20), self.rect, 2)

class MovingPlatform(Obstacle):
    """Platform that moves back and forth"""
    def __init__(self, x: float, y: float, width: float, height: float, 
                 move_distance: float = 100, speed: float = 2):
        super().__init__(x, y, width, height, "solid")
        self.start_x = x
        self.move_distance = move_distance
        self.speed = speed
        self.direction = 1
        self.animation_time = 0
    
    def update(self):
        self.animation_time += self.speed
        # Use sine wave for smooth movement
        offset = math.sin(self.animation_time * 0.05) * self.move_distance
        self.rect.x = self.start_x + offset
    
    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_PLATFORM_MOVING, self.rect)
        pygame.draw.rect(screen, (100, 100, 255), self.rect, 2)
        # Add animation indicator
        pygame.draw.circle(screen, (200, 200, 255), (self.rect.x + self.rect.width // 2, self.rect.y - 5), 3)

class Coin:
    def __init__(self, x: float, y: float, coin_type: str = "water"):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.x = x
        self.y = y
        self.coin_type = coin_type  # "water" or "fire"
        self.collected = False
        self.pulse_time = 0
    
    def update(self):
        self.pulse_time += 0.1
    
    def draw(self, screen):
        if not self.collected:
            if self.coin_type == "water":
                color = (100, 180, 255)
                inner_color = (50, 120, 200)
            else:
                color = (255, 150, 80)
                inner_color = (200, 80, 50)
            
            radius = 9 + int(3 * abs(math.sin(self.pulse_time)))
            pygame.draw.circle(screen, color, self.rect.center, radius)
            pygame.draw.circle(screen, inner_color, self.rect.center, radius - 2, 2)
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, 2)
    
    def check_collision(self, player_rect, player_type: PlayerType):
        """Only collect if coin matches player type and hasn't been collected"""
        if self.collected:
            return False
        if self.rect.colliderect(player_rect):
            # Only collect if coin type matches player type
            if (self.coin_type == "water" and player_type == PlayerType.WATER) or \
               (self.coin_type == "fire" and player_type == PlayerType.FIRE):
                self.collected = True
                return True
        return False

class Enemy:
    def __init__(self, x: float, y: float, width: float = 30, height: float = 30, 
                 patrol_left: float = None, patrol_right: float = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.pos_x = x
        self.pos_y = y
        self.width = width
        self.height = height
        self.speed = 2
        self.direction = random.choice([-1, 1])
        self.patrol_left = patrol_left if patrol_left else x - 100
        self.patrol_right = patrol_right if patrol_right else x + 100
        self.animation_time = 0
        self.change_direction_timer = random.randint(60, 180)  # frames before random direction change
    
    def update(self):
        self.pos_x += self.speed * self.direction
        self.animation_time += 0.05
        self.change_direction_timer -= 1
        
        # Random direction changes
        if self.change_direction_timer <= 0:
            self.direction = random.choice([-1, 1])
            self.change_direction_timer = random.randint(60, 180)
        
        # Boundary patrol
        if self.pos_x <= self.patrol_left or self.pos_x >= self.patrol_right:
            self.direction *= -1
        
        self.rect.x = self.pos_x
    
    def draw(self, screen):
        # Body with gradient effect
        pygame.draw.rect(screen, (200, 50, 50), self.rect, border_radius=5)
        pygame.draw.rect(screen, (255, 100, 100), self.rect, 2, border_radius=5)
        
        # Animated eyes looking in direction
        eye_offset = int(2 * math.sin(self.animation_time)) * self.direction
        left_eye_x = self.rect.x + 8 + eye_offset
        right_eye_x = self.rect.x + 20 + eye_offset
        
        pygame.draw.circle(screen, (255, 255, 255), (left_eye_x, self.rect.y + 10), 3)
        pygame.draw.circle(screen, (255, 255, 255), (right_eye_x, self.rect.y + 10), 3)
        pygame.draw.circle(screen, (0, 0, 0), (left_eye_x, self.rect.y + 10), 1)
        pygame.draw.circle(screen, (0, 0, 0), (right_eye_x, self.rect.y + 10), 1)
    
    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

class Crossbow:
    """Shoots projectiles in one direction"""
    def __init__(self, x: float, y: float, direction: int = 1):
        self.x = x
        self.y = y
        self.direction = direction
        self.rect = pygame.Rect(x, y, 20, 20)
        self.shoot_timer = 0
        self.projectiles = []
    
    def update(self):
        self.shoot_timer += 1
        if self.shoot_timer > 60:
            self.projectiles.append(Projectile(self.x, self.y, self.direction))
            self.shoot_timer = 0
        
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.x < -50 or projectile.x > SCREEN_WIDTH + 50:
                self.projectiles.remove(projectile)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (100, 50, 50), self.rect, border_radius=3)
        pygame.draw.circle(screen, (150, 100, 100), (self.x + 10, self.y + 10), 5)
        
        for projectile in self.projectiles:
            projectile.draw(screen)
    
    def check_collision(self, player_rect):
        for projectile in self.projectiles:
            if projectile.rect.colliderect(player_rect):
                self.projectiles.remove(projectile)
                return True
        return False

class Projectile:
    def __init__(self, x: float, y: float, direction: int = 1):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 5
        self.rect = pygame.Rect(x, y, 8, 8)
    
    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), 4)

class HazardPool:
    """Water or Lava pools that only certain players can pass through"""
    def __init__(self, x: float, y: float, width: float, height: float, hazard_type: str = "lava"):
        self.rect = pygame.Rect(x, y, width, height)
        self.hazard_type = hazard_type
        self.animation_time = 0
    
    def update(self):
        self.animation_time += 0.05
    
    def draw(self, screen):
        if self.hazard_type == "lava":
            # Base lava color with gradient
            base_color = COLOR_LAVA
            pygame.draw.rect(screen, base_color, self.rect)
            
            # Animated lava bubbles and waves
            num_waves = int(self.rect.width / 25)
            for i in range(num_waves):
                wave_offset = int(4 * math.sin(self.animation_time + i * 0.3)) + 3
                x_pos = self.rect.x + i * 25
                pygame.draw.line(screen, (255, 180, 50), 
                               (x_pos, self.rect.y + self.rect.height // 2 + wave_offset),
                               (x_pos + 25, self.rect.y + self.rect.height // 2 + wave_offset), 3)
            
            # Darker overlay for depth
            pygame.draw.rect(screen, (200, 80, 0), self.rect, 3)
        else:  # water
            color = COLOR_WATER_POOL
            pygame.draw.rect(screen, color, self.rect)
            
            # Ripple animation - multiple layers
            num_ripples = int(self.rect.width / 30)
            for i in range(num_ripples):
                ripple_offset = int(3 * math.sin(self.animation_time + i * 0.4)) + 2
                x_pos = self.rect.x + i * 30
                pygame.draw.line(screen, (120, 200, 255),
                               (x_pos, self.rect.y + ripple_offset),
                               (x_pos + 30, self.rect.y + ripple_offset), 2)
                pygame.draw.line(screen, (80, 160, 220),
                               (x_pos, self.rect.y + self.rect.height - ripple_offset),
                               (x_pos + 30, self.rect.y + self.rect.height - ripple_offset), 2)
            
            # Border
            pygame.draw.rect(screen, (50, 100, 180), self.rect, 3)
    
    def is_dangerous(self, player_type: PlayerType):
        if self.hazard_type == "lava":
            return player_type == PlayerType.WATER
        else:
            return player_type == PlayerType.FIRE
    
    def check_collision(self, player_rect, player_type: PlayerType):
        if self.rect.colliderect(player_rect):
            return self.is_dangerous(player_type)
        return False

class Door:
    """Goal door with activation button requirement"""
    def __init__(self, x: float, y: float, player_type: PlayerType, locked: bool = False):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.player_type = player_type
        self.locked = locked
        self.pulse_time = 0
    
    def update(self):
        self.pulse_time += 0.05
    
    def unlock(self):
        self.locked = False
    
    def draw(self, screen):
        color = COLOR_WATER if self.player_type == PlayerType.WATER else COLOR_FIRE
        door_color = COLOR_DOOR if self.locked else COLOR_DOOR_OPEN
        
        # Door frame with shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=5)
        
        pygame.draw.rect(screen, door_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (100, 60, 20) if self.locked else (50, 150, 50), self.rect, 3, border_radius=5)
        
        # Door handle
        handle_color = (200, 150, 50)
        pygame.draw.circle(screen, handle_color, (self.rect.x + self.rect.width - 5, self.rect.y + self.rect.height // 2), 3)
        
        # Glowing effect
        pulse = int(3 * abs(math.sin(self.pulse_time)))
        pygame.draw.rect(screen, color, (self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10), pulse)
        
        # Lock indicator
        if self.locked:
            pygame.draw.circle(screen, (255, 50, 50), (self.rect.x + self.rect.width // 2, self.rect.y - 10), 4, 2)

class ActivationButton:
    """Button that unlocks doors"""
    def __init__(self, x: float, y: float, button_type: str = "water"):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.button_type = button_type
        self.activated = False
        self.pulse_time = 0
        self.doors_to_unlock = []
    
    def update(self):
        self.pulse_time += 0.05
    
    def draw(self, screen):
        color = COLOR_BUTTON_INACTIVE if not self.activated else COLOR_BUTTON_ACTIVE
        pulse = int(2 * abs(math.sin(self.pulse_time))) if self.activated else 0
        
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2 + pulse, border_radius=5)
    
    def check_collision(self, player_rect, player_type: PlayerType):
        if self.rect.colliderect(player_rect):
            if (self.button_type == "water" and player_type == PlayerType.WATER) or \
               (self.button_type == "fire" and player_type == PlayerType.FIRE):
                self.activated = True
                # Unlock all doors
                for door in self.doors_to_unlock:
                    door.unlock()
                return True
        return False
