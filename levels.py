from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PlayerType, LEVEL_TIME
from obstacles import (Obstacle, Coin, Enemy, HazardPool, Door, 
                       ActivationButton, MovingPlatform, Crossbow)

class Level:
    def __init__(self, level_num: int):
        self.level_num = level_num
        self.obstacles = []
        self.coins = []
        self.enemies = []
        self.hazard_pools = []
        self.moving_platforms = []
        self.buttons = []
        self.crossbows = []
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
        # Easy - Introduction with moving platforms
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Staircase platforms
        self.obstacles.append(Obstacle(100, 700, 100, 30))
        self.obstacles.append(Obstacle(250, 650, 100, 30))
        self.obstacles.append(Obstacle(400, 600, 100, 30))
        
        # Moving platform
        self.moving_platforms.append(MovingPlatform(550, 550, 100, 30, 80, 2))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(700, 500, 100, 30))
        self.obstacles.append(Obstacle(850, 450, 100, 30))
        self.obstacles.append(Obstacle(1000, 400, 100, 30))
        
        # Coins on platforms
        self.coins.append(Coin(150, 660))
        self.coins.append(Coin(300, 610))
        self.coins.append(Coin(450, 560))
        self.coins.append(Coin(600, 510))
        self.coins.append(Coin(750, 460))
        self.coins.append(Coin(900, 410))
        self.coins.append(Coin(1050, 360))
        
        # Goals at end
        self.water_goal = Door(100, 620, PlayerType.WATER)
        self.fire_goal = Door(SCREEN_WIDTH - 140, 360, PlayerType.FIRE)
        self.time_limit = 300
    
    def _level_2(self):
        # Medium - Buttons and locked doors
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Left section
        self.obstacles.append(Obstacle(50, 700, 120, 30))
        self.obstacles.append(Obstacle(50, 550, 120, 30))
        self.moving_platforms.append(MovingPlatform(50, 400, 120, 30, 60, 1.5))
        self.obstacles.append(self.moving_platforms[-1])
        
        # Middle section
        self.obstacles.append(Obstacle(350, 650, 100, 30))
        self.obstacles.append(Obstacle(350, 500, 100, 30))
        self.obstacles.append(Obstacle(350, 350, 100, 30))
        
        # Right section
        self.obstacles.append(Obstacle(1000, 700, 120, 30))
        self.obstacles.append(Obstacle(1000, 550, 120, 30))
        self.moving_platforms.append(MovingPlatform(1000, 400, 120, 30, 60, 1.5))
        self.obstacles.append(self.moving_platforms[-1])
        
        # Hazards
        self.hazard_pools.append(HazardPool(200, 680, 100, 30, "lava"))
        self.hazard_pools.append(HazardPool(700, 680, 100, 30, "water"))
        
        # Buttons to unlock doors
        self.buttons.append(ActivationButton(120, 470, "water"))
        self.buttons.append(ActivationButton(1070, 470, "fire"))
        
        # Coins
        self.coins.append(Coin(120, 660))
        self.coins.append(Coin(120, 510))
        self.coins.append(Coin(420, 610))
        self.coins.append(Coin(420, 460))
        self.coins.append(Coin(1070, 660))
        self.coins.append(Coin(1070, 510))
        
        # Enemies
        self.enemies.append(Enemy(420, 350, patrol_left=300, patrol_right=500))
        
        # Goals locked until buttons pressed
        self.water_goal = Door(50, 320, PlayerType.WATER, locked=True)
        self.fire_goal = Door(SCREEN_WIDTH - 140, 320, PlayerType.FIRE, locked=True)
        
        # Unlock doors when buttons activated
        for button in self.buttons:
            button.doors_to_unlock = [self.water_goal, self.fire_goal]
        
        self.time_limit = 300
    
    def _level_3(self):
        # Hard - Crossbows and narrow passages
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.obstacles.append(Obstacle(0, 0, 50, SCREEN_HEIGHT))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT))
        
        # Platform maze
        self.obstacles.append(Obstacle(100, 700, 80, 25))
        self.obstacles.append(Obstacle(220, 670, 80, 25))
        self.obstacles.append(Obstacle(340, 700, 80, 25))
        self.obstacles.append(Obstacle(460, 670, 80, 25))
        self.obstacles.append(Obstacle(580, 700, 80, 25))
        self.obstacles.append(Obstacle(700, 670, 80, 25))
        self.obstacles.append(Obstacle(820, 700, 80, 25))
        self.obstacles.append(Obstacle(940, 670, 80, 25))
        
        # Moving platforms
        self.moving_platforms.append(MovingPlatform(200, 550, 80, 25, 100, 2))
        self.obstacles.append(self.moving_platforms[-1])
        self.moving_platforms.append(MovingPlatform(700, 550, 80, 25, 100, 2))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(450, 400, 300, 30))
        self.obstacles.append(Obstacle(150, 300, 150, 30))
        self.obstacles.append(Obstacle(900, 300, 150, 30))
        self.obstacles.append(Obstacle(450, 150, 300, 30))
        
        # Crossbows shooting from sides
        self.crossbows.append(Crossbow(80, 550, 1))  # shoots right
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 100, 550, -1))  # shoots left
        
        # Hazards
        self.hazard_pools.append(HazardPool(350, 680, 60, 30, "water"))
        self.hazard_pools.append(HazardPool(700, 680, 60, 30, "lava"))
        
        # Coins
        for x in [130, 260, 390, 520, 640, 770, 900]:
            self.coins.append(Coin(x, 650))
        for x in [150, 450, 900]:
            self.coins.append(Coin(x, 250))
        
        # Enemies
        self.enemies.append(Enemy(525, 360, patrol_left=400, patrol_right=650))
        self.enemies.append(Enemy(300, 250, patrol_left=150, patrol_right=400))
        self.enemies.append(Enemy(900, 250, patrol_left=750, patrol_right=1050))
        
        self.water_goal = Door(100, 580, PlayerType.WATER)
        self.fire_goal = Door(SCREEN_WIDTH - 140, 580, PlayerType.FIRE)
        self.time_limit = 300
    
    def _level_4(self):
        # Very Hard - Cooperation required
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Platforms that require cooperation
        self.obstacles.append(Obstacle(100, 700, 100, 30))
        self.obstacles.append(Obstacle(300, 650, 100, 30))
        self.obstacles.append(Obstacle(500, 700, 100, 30))
        self.obstacles.append(Obstacle(700, 650, 100, 30))
        self.obstacles.append(Obstacle(900, 700, 100, 30))
        
        self.moving_platforms.append(MovingPlatform(200, 550, 120, 30, 100, 2))
        self.obstacles.append(self.moving_platforms[-1])
        self.moving_platforms.append(MovingPlatform(800, 550, 120, 30, 100, 2))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(450, 400, 300, 30))
        self.obstacles.append(Obstacle(200, 250, 150, 30))
        self.obstacles.append(Obstacle(850, 250, 150, 30))
        self.obstacles.append(Obstacle(450, 100, 300, 30))
        
        # Multiple hazards
        self.hazard_pools.append(HazardPool(220, 680, 50, 30, "lava"))
        self.hazard_pools.append(HazardPool(600, 680, 50, 30, "water"))
        self.hazard_pools.append(HazardPool(820, 680, 50, 30, "lava"))
        
        # Buttons controlling doors
        self.buttons.append(ActivationButton(150, 360, "water"))
        self.buttons.append(ActivationButton(1050, 360, "fire"))
        
        # Crossbows
        self.crossbows.append(Crossbow(150, 450, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 150, 450, -1))
        
        # Coins
        for x in [130, 370, 540, 770, 940, 275, 825, 525]:
            self.coins.append(Coin(x, 200))
        
        # Enemies
        self.enemies.append(Enemy(260, 510, patrol_left=150, patrol_right=350))
        self.enemies.append(Enemy(860, 510, patrol_left=750, patrol_right=950))
        self.enemies.append(Enemy(525, 300, patrol_left=400, patrol_right=650))
        
        self.water_goal = Door(100, 180, PlayerType.WATER, locked=True)
        self.fire_goal = Door(SCREEN_WIDTH - 140, 180, PlayerType.FIRE, locked=True)
        
        for button in self.buttons:
            button.doors_to_unlock = [self.water_goal, self.fire_goal]
        
        self.time_limit = 300
    
    def _level_5(self):
        # Extreme - Ultimate challenge
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.obstacles.append(Obstacle(0, 0, 50, SCREEN_HEIGHT))  # Left wall
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT))  # Right wall
        
        # Complex maze with moving platforms
        for i in range(10):
            x = 100 + i * 100
            y = 700 - (i % 2) * 40
            if i % 3 == 0:
                self.moving_platforms.append(MovingPlatform(x, y, 80, 25, 60, 1.5))
                self.obstacles.append(self.moving_platforms[-1])
            else:
                self.obstacles.append(Obstacle(x, y, 80, 25))
        
        # Middle platforms
        self.obstacles.append(Obstacle(150, 550, 100, 30))
        self.moving_platforms.append(MovingPlatform(400, 500, 100, 30, 120, 2))
        self.obstacles.append(self.moving_platforms[-1])
        self.obstacles.append(Obstacle(700, 550, 100, 30))
        self.moving_platforms.append(MovingPlatform(1000, 500, 100, 30, 120, 2))
        self.obstacles.append(self.moving_platforms[-1])
        
        # Upper section
        self.obstacles.append(Obstacle(250, 350, 120, 30))
        self.obstacles.append(Obstacle(600, 300, 120, 30))
        self.obstacles.append(Obstacle(950, 350, 120, 30))
        self.obstacles.append(Obstacle(450, 150, 300, 30))
        
        # Many hazards
        for x in [130, 350, 570, 790]:
            self.hazard_pools.append(HazardPool(x, 725, 50, 25, "lava" if x % 300 < 150 else "water"))
        
        # Multiple crossbows
        self.crossbows.append(Crossbow(60, 550, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 80, 550, -1))
        self.crossbows.append(Crossbow(200, 300, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 200, 300, -1))
        
        # Many coins
        for x in range(120, 1100, 200):
            self.coins.append(Coin(x, 650))
        for x in range(200, 1000, 250):
            self.coins.append(Coin(x, 400))
        for x in range(250, 1000, 300):
            self.coins.append(Coin(x, 200))
        
        # Many enemies
        self.enemies.append(Enemy(280, 450, patrol_left=150, patrol_right=400))
        self.enemies.append(Enemy(620, 400, patrol_left=450, patrol_right=750))
        self.enemies.append(Enemy(980, 450, patrol_left=850, patrol_right=1100))
        self.enemies.append(Enemy(625, 200, patrol_left=450, patrol_right=800))
        
        # Buttons
        self.buttons.append(ActivationButton(200, 310, "water"))
        self.buttons.append(ActivationButton(1000, 310, "fire"))
        
        self.water_goal = Door(100, 100, PlayerType.WATER, locked=True)
        self.fire_goal = Door(SCREEN_WIDTH - 140, 100, PlayerType.FIRE, locked=True)
        
        for button in self.buttons:
            button.doors_to_unlock = [self.water_goal, self.fire_goal]
        
        self.time_limit = 300
