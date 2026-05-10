import pygame
import math
from .constants import (SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BUTTON, COLOR_BUTTON_HOVER, 
                       COLOR_TEXT, COLOR_WATER, COLOR_FIRE, COLOR_SUCCESS, COLOR_ERROR)


def draw_fire_water_background(screen, time_value: float):
    """Draw a split elemental menu backdrop."""
    horizon = SCREEN_HEIGHT // 2 + 60
    for y in range(0, SCREEN_HEIGHT, 2):
        ratio = y / SCREEN_HEIGHT
        left = (
            int(14 + ratio * 14),
            int(38 + ratio * 18),
            int(78 + ratio * 55),
        )
        right = (
            int(88 + ratio * 42),
            int(28 + ratio * 16),
            int(18 + ratio * 10),
        )
        for x in range(0, SCREEN_WIDTH, 8):
            side = x / SCREEN_WIDTH
            wave = math.sin((y * 0.018) + time_value + side * 4) * 0.08
            mix = max(0, min(1, side + wave))
            color = tuple(int(left[i] * (1 - mix) + right[i] * mix) for i in range(3))
            pygame.draw.rect(screen, color, (x, y, 8, 2))

    for i in range(9):
        x = 70 + i * 115
        y = horizon + math.sin(time_value * 1.4 + i) * 10
        width = 95 + math.sin(i) * 22
        pygame.draw.arc(screen, (80, 185, 255), (x, y, width, 28), math.pi, math.tau, 2)

    for i in range(14):
        x = SCREEN_WIDTH - 70 - i * 74
        base_y = 690 - (i % 5) * 37
        flicker = math.sin(time_value * 4 + i * 1.7)
        height = 32 + flicker * 9
        points = [(x, base_y), (x + 14, base_y - height), (x + 28, base_y)]
        pygame.draw.polygon(screen, (255, 128 + int(flicker * 30), 44), points)
        pygame.draw.polygon(screen, (255, 210, 84), [(x + 8, base_y), (x + 15, base_y - height * 0.62), (x + 22, base_y)])


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
        base = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        fire_mix = max(0, min(1, (self.rect.centerx - SCREEN_WIDTH * 0.45) / (SCREEN_WIDTH * 0.35)))
        water_tint = (70, 150, 235)
        fire_tint = (225, 78, 42)
        color = tuple(int(base[i] * 0.35 + (water_tint[i] * (1 - fire_mix) + fire_tint[i] * fire_mix) * 0.65) for i in range(3))
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
            lock_text = lock_font.render("đź”’", True, (200, 200, 200))
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
    
    def draw_game_hud(self, screen, level_num, time_remaining, water_coins, fire_coins, timer_enabled=True):
        # Draw HUD background panel
        hud_bg = pygame.Surface((SCREEN_WIDTH, 120))
        hud_bg.set_alpha(40)
        hud_bg.fill((20, 20, 30))
        screen.blit(hud_bg, (0, 0))
        
        # Level info
        level_text = self.font_small.render(f"Level {level_num}", True, COLOR_TEXT)
        screen.blit(level_text, (20, 20))
        
        # Timer
        if timer_enabled:
            minutes = int(time_remaining) // 60
            seconds = int(time_remaining) % 60
            timer_label = f"{minutes}:{seconds:02d}"
        else:
            timer_label = "NO LIMIT"
        time_text = self.font_medium.render(timer_label, True, COLOR_TEXT)
        time_rect = time_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(time_text, time_rect)
        
        if timer_enabled and time_remaining < 30:
            warning = self.font_small.render("Time Running Out!", True, COLOR_ERROR)
            screen.blit(warning, (SCREEN_WIDTH // 2 - warning.get_width() // 2, 20))
        
        # Coin counters
        water_text = self.font_tiny.render(f"đź’§ Water Coins: {water_coins}", True, COLOR_WATER)
        fire_text = self.font_tiny.render(f"đź”Ą Fire Coins: {fire_coins}", True, COLOR_FIRE)
        screen.blit(water_text, (20, 70))
        screen.blit(fire_text, (20, 100))
    
    def draw_menu(self, screen):
        time_value = pygame.time.get_ticks() / 1000
        draw_fire_water_background(screen, time_value)

        title_shadow = self.font_large.render("FIRE & WATER", True, (18, 15, 22))
        title = self.font_large.render("FIRE & WATER", True, COLOR_TEXT)
        subtitle = self.font_medium.render("Temple Puzzle", True, (255, 215, 120))
        instructions = self.font_tiny.render("Water: Arrow Keys   Fire: WASD", True, (220, 232, 245))

        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        screen.blit(title_shadow, (title_x + 4, 86))
        screen.blit(title, (title_x, 82))
        pygame.draw.line(screen, COLOR_WATER, (title_x, 160), (SCREEN_WIDTH // 2 - 10, 160), 4)
        pygame.draw.line(screen, COLOR_FIRE, (SCREEN_WIDTH // 2 + 10, 160), (title_x + title.get_width(), 160), 4)

        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 182))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 262))

        water_text = self.font_small.render("Water opens the blue door", True, COLOR_WATER)
        fire_text = self.font_small.render("Fire burns toward the red door", True, COLOR_FIRE)
        screen.blit(water_text, (70, SCREEN_HEIGHT - 130))
        screen.blit(fire_text, (SCREEN_WIDTH - fire_text.get_width() - 70, SCREEN_HEIGHT - 130))
    
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
            next_text = self.font_small.render("đźŽ‰ You completed all levels! đźŽ‰", True, COLOR_SUCCESS)
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

    def draw_pause(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = self.font_large.render("PAUSED", True, COLOR_TEXT)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 180))

        hint = self.font_tiny.render("Press P or ESC to resume", True, COLOR_TEXT)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 - 120))

    def draw_settings(self, screen, timer_enabled, opened_from_pause):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((20, 20, 30))
        screen.blit(overlay, (0, 0))

        title = self.font_large.render("SETTINGS", True, COLOR_TEXT)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        source = "Opened from pause" if opened_from_pause else "Main menu settings"
        source_text = self.font_tiny.render(source, True, COLOR_TEXT)
        screen.blit(source_text, (SCREEN_WIDTH // 2 - source_text.get_width() // 2, 190))

        timer_text = "Timer is enabled" if timer_enabled else "Timer is disabled"
        description = self.font_small.render(timer_text, True, COLOR_SUCCESS if timer_enabled else COLOR_ERROR)
        screen.blit(description, (SCREEN_WIDTH // 2 - description.get_width() // 2, SCREEN_HEIGHT // 2 - 95))

