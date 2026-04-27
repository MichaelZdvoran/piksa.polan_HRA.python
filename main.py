import pygame
import sys
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BG, 
                       GameState, PlayerType, LEVEL_TIME)
from players import Player
from levels import Level
from ui import Button, LevelSelectButton, HUD

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fire & Water: Puzzle Adventure")
        self.clock = pygame.time.Clock()
        self.hud = HUD()
        
        self.state = GameState.MENU
        self.current_level = 1
        self.max_level = 5
        self.start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60, "START GAME")
        self.level_select_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60, "LEVEL SELECT")
        
        # Game Over / Death menu buttons
        # place buttons side-by-side so they fit nicely in death menu
        self.retry_button = Button(SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2, 200, 60, "RETRY LEVEL")
        self.menu_button = Button(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2, 200, 60, "MAIN MENU")
        
        # Level select buttons
        self.level_buttons = []
        for i in range(1, self.max_level + 1):
            x = SCREEN_WIDTH // 2 - 200 + (i - 1) * 100
            y = SCREEN_HEIGHT // 2
            self.level_buttons.append(LevelSelectButton(x, y, i, unlocked=True))
        
        self.back_button = Button(50, 50, 100, 50, "BACK")
        
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
                self.start_button.check_hover(event.pos)
                self.level_select_button.check_hover(event.pos)
                self.retry_button.check_hover(event.pos)
                self.menu_button.check_hover(event.pos)
                self.back_button.check_hover(event.pos)
                for btn in self.level_buttons:
                    btn.check_hover(event.pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.MENU:
                    if self.start_button.is_clicked(event.pos):
                        self.start_level(1)
                    elif self.level_select_button.is_clicked(event.pos):
                        self.state = GameState.LEVEL_SELECT
                
                elif self.state == GameState.LEVEL_SELECT:
                    if self.back_button.is_clicked(event.pos):
                        self.state = GameState.MENU
                    for btn in self.level_buttons:
                        if btn.is_clicked(event.pos) and btn.unlocked:
                            self.start_level(btn.level_num)
                
                elif self.state == GameState.GAME_OVER:
                    if self.retry_button.is_clicked(event.pos):
                        self.start_level(self.current_level)
                    elif self.menu_button.is_clicked(event.pos):
                        self.state = GameState.MENU
                
                elif self.state == GameState.LEVEL_COMPLETE:
                    if self.current_level < self.max_level:
                        self.start_level(self.current_level + 1)
                    else:
                        self.state = GameState.MENU
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.LEVEL_SELECT:
                        self.state = GameState.MENU
                    elif self.state == GameState.PLAYING:
                        self.state = GameState.MENU
        
        return True
    
    def update(self):
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            
            self.water_player.handle_input(keys)
            self.fire_player.handle_input(keys)
            
            water_alive = self.water_player.update(self.level.obstacles, self.level.coins, 
                                                   self.level.enemies, self.level.hazard_pools,
                                                   self.level.crossbows, self.level.buttons)
            fire_alive = self.fire_player.update(self.level.obstacles, self.level.coins, 
                                                self.level.enemies, self.level.hazard_pools,
                                                self.level.crossbows, self.level.buttons)
            
            for enemy in self.level.enemies:
                enemy.update()
            
            for coin in self.level.coins:
                coin.update()
            
            for pool in self.level.hazard_pools:
                pool.update()
            
            for platform in self.level.moving_platforms:
                platform.update()
            
            for button in self.level.buttons:
                button.update()
            
            for crossbow in self.level.crossbows:
                crossbow.update()
            
            self.level.water_goal.update()
            self.level.fire_goal.update()
            
            if not water_alive or not fire_alive:
                self.state = GameState.GAME_OVER
            
            # Check goal collisions - only if unlocked
            if not self.level.water_goal.locked and not self.level.fire_goal.locked:
                water_reached = self.water_player.rect.colliderect(self.level.water_goal.rect)
                fire_reached = self.fire_player.rect.colliderect(self.level.fire_goal.rect)
                if water_reached and fire_reached:
                    self.state = GameState.LEVEL_COMPLETE
            
            # Update timer
            elapsed = (pygame.time.get_ticks() - self.level_start_time) / 1000
            self.level_time_remaining = max(0, self.level.time_limit - elapsed)
            
            if self.level_time_remaining <= 0:
                self.state = GameState.GAME_OVER
        
        if self.state in [GameState.MENU, GameState.LEVEL_SELECT]:
            self.start_button.update()
            self.level_select_button.update()
            self.retry_button.update()
            self.menu_button.update()
            for btn in self.level_buttons:
                btn.update()
    
    def draw(self):
        self.screen.fill(COLOR_BG)
        self._draw_background()
        
        if self.state == GameState.MENU:
            self._draw_menu()
        elif self.state == GameState.LEVEL_SELECT:
            self._draw_level_select()
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.LEVEL_COMPLETE:
            self._draw_level_complete()
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()
        
        pygame.display.flip()
    
    def _draw_background(self):
        """Draw an animated background with gradient effect"""
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(20 + ratio * 10)
            g = int(20 + ratio * 5)
            b = int(30 + ratio * 15)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def _draw_menu(self):
        self.hud.draw_menu(self.screen)
        self.start_button.draw(self.screen)
        self.level_select_button.draw(self.screen)
        
        # Draw water player na levé straně
        water_player_demo = Player(80, 450, PlayerType.WATER)
        water_player_demo.draw(self.screen)
        
        # Draw fire player na pravé straně
        fire_player_demo = Player(SCREEN_WIDTH - 110, 450, PlayerType.FIRE)
        fire_player_demo.draw(self.screen)
        
        # Instructions above players
        font_small = pygame.font.Font(None, 24)
        water_controls = font_small.render("Arrow Keys", True, (100, 180, 255))
        fire_controls = font_small.render("WASD", True, (255, 150, 80))
        
        self.screen.blit(water_controls, (20, 410))
        self.screen.blit(fire_controls, (SCREEN_WIDTH - 120, 410))
    
    def _draw_level_select(self):
        self.hud.draw_level_select(self.screen)
        self.back_button.draw(self.screen)
        for btn in self.level_buttons:
            btn.draw(self.screen)
    
    def _draw_game(self):
        # Draw level
        for obstacle in self.level.obstacles:
            obstacle.draw(self.screen)
        
        # Draw moving platforms
        for platform in self.level.moving_platforms:
            platform.draw(self.screen)
        
        # Draw hazard pools
        for pool in self.level.hazard_pools:
            pool.draw(self.screen)
        
        # Draw coins
        for coin in self.level.coins:
            coin.draw(self.screen)
        
        # Draw crossbows
        for crossbow in self.level.crossbows:
            crossbow.draw(self.screen)
        
        # Draw buttons
        for button in self.level.buttons:
            button.draw(self.screen)
        
        # Draw enemies
        for enemy in self.level.enemies:
            enemy.draw(self.screen)
        
        # Draw goals
        self.level.water_goal.draw(self.screen)
        self.level.fire_goal.draw(self.screen)
        
        # Draw players
        self.water_player.draw(self.screen)
        self.fire_player.draw(self.screen)
        
        # Draw UI
        self.hud.draw_game_hud(self.screen, self.current_level, self.level_time_remaining, 
                               self.water_player.coins_collected, self.fire_player.coins_collected)
    
    def _draw_level_complete(self):
        self._draw_game()
        self.hud.draw_level_complete(self.screen, self.current_level, self.max_level)
    
    def _draw_game_over(self):
        self._draw_game()
        self.hud.draw_game_over(self.screen)
        self.retry_button.draw(self.screen)
        self.menu_button.draw(self.screen)
    
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
