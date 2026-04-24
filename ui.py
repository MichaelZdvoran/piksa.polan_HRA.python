import pygame
import math
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BUTTON, COLOR_BUTTON_HOVER, 
                       COLOR_TEXT, COLOR_WATER, COLOR_FIRE, COLOR_SUCCESS, COLOR_ERROR)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        self.font = pygame.font.Font(None, 36)
        self.pulse_time = 0
    
    def update(self):
        self.pulse_time += 0.05
    
    def draw(self, screen):
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        pulse = int(2 * abs(math.sin(self.pulse_time))) if self.hovered else 0
        
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=10)
        
        # Draw button with gradient effect
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 3 + pulse, border_radius=10)
        
        # Add highlight on top for depth
        highlight_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height // 3)
        highlight_color = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=5)
        
        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class LevelSelectButton(Button):
    def __init__(self, x: int, y: int, level_num: int, unlocked: bool = True):
        super().__init__(x, y, 80, 80, str(level_num))
        self.level_num = level_num
        self.unlocked = unlocked
    
    def draw(self, screen):
        if not self.unlocked:
            color = (80, 80, 80)
            pygame.draw.rect(screen, color, self.rect, border_radius=10)
            pygame.draw.rect(screen, (120, 120, 120), self.rect, 3, border_radius=10)
            lock_font = pygame.font.Font(None, 48)
            lock_text = lock_font.render("🔒", True, (200, 200, 200))
            lock_rect = lock_text.get_rect(center=self.rect.center)
            screen.blit(lock_text, lock_rect)
        else:
            super().draw(screen)

class HUD:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)
    
    def draw_game_hud(self, screen, level_num, time_remaining, water_coins, fire_coins):
        # Draw HUD background panel
        hud_bg = pygame.Surface((SCREEN_WIDTH, 120))
        hud_bg.set_alpha(40)
        hud_bg.fill((20, 20, 30))
        screen.blit(hud_bg, (0, 0))
        
        # Level info
        level_text = self.font_small.render(f"Level {level_num}", True, COLOR_TEXT)
        screen.blit(level_text, (20, 20))
        
        # Timer
        minutes = int(time_remaining) // 60
        seconds = int(time_remaining) % 60
        time_text = self.font_medium.render(f"{minutes}:{seconds:02d}", True, COLOR_TEXT)
        time_rect = time_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(time_text, time_rect)
        
        if time_remaining < 30:
            warning = self.font_small.render("Time Running Out!", True, COLOR_ERROR)
            screen.blit(warning, (SCREEN_WIDTH // 2 - warning.get_width() // 2, 20))
        
        # Coin counters
        water_text = self.font_tiny.render(f"💧 Water Coins: {water_coins}", True, COLOR_WATER)
        fire_text = self.font_tiny.render(f"🔥 Fire Coins: {fire_coins}", True, COLOR_FIRE)
        screen.blit(water_text, (20, 70))
        screen.blit(fire_text, (20, 100))
    
    def draw_menu(self, screen):
        # Draw gradient title background
        title_bg = pygame.Surface((SCREEN_WIDTH, 150))
        title_bg.set_alpha(30)
        title_bg.fill((100, 150, 255))
        screen.blit(title_bg, (0, 40))
        
        title = self.font_large.render("FIRE & WATER", True, COLOR_TEXT)
        subtitle = self.font_medium.render("Puzzle Adventure", True, COLOR_TEXT)
        instructions = self.font_tiny.render("Water: Arrow Keys | Fire: WASD", True, COLOR_TEXT)
        
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 180))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 280))
        
        water_text = self.font_small.render("🌊 Guide Water to the goal!", True, COLOR_WATER)
        fire_text = self.font_small.render("🔥 Guide Fire to the goal!", True, COLOR_FIRE)
        screen.blit(water_text, (50, SCREEN_HEIGHT - 150))
        screen.blit(fire_text, (50, SCREEN_HEIGHT - 100))
    
    def draw_level_select(self, screen):
        # Draw title background
        title_bg = pygame.Surface((SCREEN_WIDTH, 120))
        title_bg.set_alpha(30)
        title_bg.fill((150, 100, 50))
        screen.blit(title_bg, (0, 20))
        
        title = self.font_large.render("SELECT LEVEL", True, COLOR_TEXT)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        instruction = self.font_small.render("Click a level to start", True, COLOR_TEXT)
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 130))
    
    def draw_level_complete(self, screen, current_level, max_level):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw decorative box
        box_width = 500
        box_height = 250
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2
        pygame.draw.rect(screen, (100, 150, 255), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(screen, COLOR_SUCCESS, (box_x, box_y, box_width, box_height), 3, border_radius=10)
        
        complete_text = self.font_large.render("LEVEL COMPLETE!", True, COLOR_SUCCESS)
        screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        
        if current_level < max_level:
            next_text = self.font_small.render("Click to continue...", True, COLOR_TEXT)
        else:
            next_text = self.font_small.render("🎉 You completed all levels! 🎉", True, COLOR_SUCCESS)
        screen.blit(next_text, (SCREEN_WIDTH // 2 - next_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    def draw_game_over(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw decorative box
        box_width = 500
        box_height = 250
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2
        pygame.draw.rect(screen, (150, 50, 50), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(screen, COLOR_ERROR, (box_x, box_y, box_width, box_height), 3, border_radius=10)
        
        gameover_text = self.font_large.render("GAME OVER", True, COLOR_ERROR)
        screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        
        retry_text = self.font_small.render("Click to return to menu", True, COLOR_TEXT)
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
