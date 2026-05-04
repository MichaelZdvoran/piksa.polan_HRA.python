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
        self.moving_platforms.append(MovingPlatform(550, 550, 100, 30, 60, 0.8))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(700, 500, 100, 30))
        self.obstacles.append(Obstacle(850, 450, 100, 30))
        
        # Solid platform for door
        self.obstacles.append(Obstacle(1000, 400, 100, 30))
        
        # Water player coins (blue) - above platforms, need to collect for door to open
        self.coins.append(Coin(130, 660, "water"))
        self.coins.append(Coin(280, 610, "water"))
        self.coins.append(Coin(430, 560, "water"))
        
        # Fire player coins (red) - above platforms, need to collect for door to open
        self.coins.append(Coin(730, 460, "fire"))
        self.coins.append(Coin(880, 410, "fire"))
        
        # Solid platforms for doors - very important that they are solid
        self.obstacles.append(Obstacle(80, 610, 60, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 160, 360, 60, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 220, 410, 60, 30)) # Pomocný schod pro oheň
        
        # Goals on solid platforms - doors only open when coins collected
        self.water_goal = Door(80, 550, PlayerType.WATER, locked=True)
        self.fire_goal = Door(SCREEN_WIDTH - 160, 300, PlayerType.FIRE, locked=True)
        self.time_limit = 300
    
    def _level_2(self):
        # Medium - Hazards and moving platforms
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

        # Left section - water path
        self.obstacles.append(Obstacle(50, 700, 120, 30))
        self.obstacles.append(Obstacle(50, 550, 120, 30))
        self.moving_platforms.append(MovingPlatform(50, 400, 120, 30, 60, 0.8))
        self.obstacles.append(self.moving_platforms[-1])

        # Middle section
        self.obstacles.append(Obstacle(350, 650, 100, 30))
        self.obstacles.append(Obstacle(350, 500, 100, 30))
        self.obstacles.append(Obstacle(350, 350, 100, 30))

        # Right section - fire path
        self.obstacles.append(Obstacle(1000, 700, 120, 30))
        self.obstacles.append(Obstacle(1000, 550, 120, 30))
        self.moving_platforms.append(MovingPlatform(1000, 400, 120, 30, 60, 0.8))
        self.obstacles.append(self.moving_platforms[-1])

        # Hazards with solid platforms underneath
        self.obstacles.append(Obstacle(200, 710, 100, 20))
        self.hazard_pools.append(HazardPool(200, 680, 100, 30, "lava"))

        self.obstacles.append(Obstacle(700, 710, 100, 20))
        self.hazard_pools.append(HazardPool(700, 680, 100, 30, "water"))

        # Water player coins (blue)
        self.coins.append(Coin(120, 660, "water"))
        self.coins.append(Coin(120, 510, "water"))
        self.coins.append(Coin(420, 610, "water"))

        # Fire player coins (red)
        self.coins.append(Coin(1070, 660, "fire"))
        self.coins.append(Coin(1070, 510, "fire"))
        self.coins.append(Coin(980, 610, "fire"))

        # Enemies
        self.enemies.append(Enemy(420, 350, patrol_left=300, patrol_right=500))

        # Solid platforms for doors
        self.obstacles.append(Obstacle(50, 320, 80, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 140, 320, 80, 30))

        # Goals locked until coins are collected
        self.water_goal = Door(50, 260, PlayerType.WATER, locked=True)
        self.fire_goal = Door(SCREEN_WIDTH - 140, 260, PlayerType.FIRE, locked=True)

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
        self.moving_platforms.append(MovingPlatform(200, 550, 80, 25, 60, 0.8))
        self.obstacles.append(self.moving_platforms[-1])
        self.moving_platforms.append(MovingPlatform(700, 550, 80, 25, 60, 0.8))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(450, 400, 300, 30))
        self.obstacles.append(Obstacle(150, 300, 150, 30))
        self.obstacles.append(Obstacle(900, 300, 150, 30))
        self.obstacles.append(Obstacle(450, 150, 300, 30))
        
        # Crossbows shooting from sides
        self.crossbows.append(Crossbow(80, 550, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 100, 550, -1))
        
        # Hazards with platforms underneath
        self.obstacles.append(Obstacle(350, 690, 60, 20))
        self.hazard_pools.append(HazardPool(350, 660, 60, 30, "water"))
        
        self.obstacles.append(Obstacle(700, 690, 60, 20))
        self.hazard_pools.append(HazardPool(700, 660, 60, 30, "lava"))
        
        # Coins - water player
        self.coins.append(Coin(130, 650, "water"))
        self.coins.append(Coin(260, 640, "water"))
        self.coins.append(Coin(390, 650, "water"))
        self.coins.append(Coin(240, 510, "water"))
        self.coins.append(Coin(150, 250, "water"))
        
        # Coins - fire player
        self.coins.append(Coin(640, 650, "fire"))
        self.coins.append(Coin(770, 640, "fire"))
        self.coins.append(Coin(900, 650, "fire"))
        self.coins.append(Coin(760, 510, "fire"))
        self.coins.append(Coin(1000, 250, "fire"))
        
        # Enemies
        self.enemies.append(Enemy(525, 360, patrol_left=400, patrol_right=650))
        self.enemies.append(Enemy(300, 250, patrol_left=150, patrol_right=400))
        self.enemies.append(Enemy(900, 250, patrol_left=750, patrol_right=1050))
        
        # Schody ke dveřím
        self.obstacles.append(Obstacle(120, 200, 100, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 220, 200, 100, 30))
        
        # Solid platforms for doors
        self.obstacles.append(Obstacle(100, 100, 40, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 140, 100, 40, 30))
        
        self.water_goal = Door(100, 40, PlayerType.WATER)
        self.fire_goal = Door(SCREEN_WIDTH - 140, 40, PlayerType.FIRE)
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
        
        self.moving_platforms.append(MovingPlatform(200, 550, 120, 30, 60, 0.8))
        self.obstacles.append(self.moving_platforms[-1])
        self.moving_platforms.append(MovingPlatform(800, 550, 120, 30, 60, 0.8))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(450, 400, 300, 30))
        self.obstacles.append(Obstacle(200, 250, 150, 30))
        self.obstacles.append(Obstacle(850, 250, 150, 30))
        self.obstacles.append(Obstacle(450, 100, 300, 30))
        
        # Multiple hazards with platforms underneath
        self.obstacles.append(Obstacle(220, 690, 50, 20))
        self.hazard_pools.append(HazardPool(220, 660, 50, 30, "lava"))
        
        self.obstacles.append(Obstacle(600, 690, 50, 20))
        self.hazard_pools.append(HazardPool(600, 660, 50, 30, "water"))
        
        self.obstacles.append(Obstacle(820, 690, 50, 20))
        self.hazard_pools.append(HazardPool(820, 660, 50, 30, "lava"))
        
        # Crossbows
        self.crossbows.append(Crossbow(150, 450, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 150, 450, -1))
        
        # Coins - water player
        self.coins.append(Coin(130, 660, "water"))
        self.coins.append(Coin(370, 610, "water"))
        self.coins.append(Coin(540, 660, "water"))
        self.coins.append(Coin(275, 200, "water"))
        
        # Coins - fire player
        self.coins.append(Coin(770, 610, "fire"))
        self.coins.append(Coin(940, 660, "fire"))
        self.coins.append(Coin(825, 200, "fire"))
        
        # Enemies
        self.enemies.append(Enemy(260, 510, patrol_left=150, patrol_right=350))
        self.enemies.append(Enemy(860, 510, patrol_left=750, patrol_right=950))
        self.enemies.append(Enemy(525, 300, patrol_left=400, patrol_right=650))
        
        # Schody ke dveřím
        self.obstacles.append(Obstacle(150, 180, 100, 30))
        self.obstacles.append(Obstacle(100, 110, 100, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 250, 180, 100, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 200, 110, 100, 30))
        
        # Solid platforms for doors
        self.obstacles.append(Obstacle(100, 40, 40, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 140, 40, 40, 30))
        
        self.water_goal = Door(100, -20, PlayerType.WATER)
        self.fire_goal = Door(SCREEN_WIDTH - 140, -20, PlayerType.FIRE)
        
        self.time_limit = 300
    
    def _level_5(self):
        # Extreme - Ultimate challenge
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        self.obstacles.append(Obstacle(0, 0, 50, SCREEN_HEIGHT))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT))
        
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
        
        # Many hazards with platforms underneath
        for x in [130, 350, 570, 790]:
            hazard_type = "lava" if x % 300 < 150 else "water"
            self.obstacles.append(Obstacle(x, 715, 50, 20))
            self.hazard_pools.append(HazardPool(x, 685, 50, 30, hazard_type))
        
        # Multiple crossbows
        self.crossbows.append(Crossbow(60, 550, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 80, 550, -1))
        self.crossbows.append(Crossbow(200, 300, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 200, 300, -1))
        
        # Coins - water player
        water_coin_positions = [(120, 650), (260, 640), (390, 650), (240, 450), (150, 200)]
        for x, y in water_coin_positions:
            self.coins.append(Coin(x, y, "water"))
        
        # Coins - fire player
        fire_coin_positions = [(900, 650), (1000, 650), (760, 450), (1000, 200)]
        for x, y in fire_coin_positions:
            self.coins.append(Coin(x, y, "fire"))
        
        # Many enemies
        self.enemies.append(Enemy(280, 450, patrol_left=150, patrol_right=400))
        self.enemies.append(Enemy(620, 400, patrol_left=450, patrol_right=750))
        self.enemies.append(Enemy(980, 450, patrol_left=850, patrol_right=1100))
        self.enemies.append(Enemy(625, 200, patrol_left=450, patrol_right=800))
        
        # Schody ke dveřím
        self.obstacles.append(Obstacle(180, 260, 100, 30))
        self.obstacles.append(Obstacle(120, 180, 100, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 280, 260, 100, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 220, 180, 100, 30))
        
        # Solid platforms for doors
        self.obstacles.append(Obstacle(100, 100, 40, 30))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 140, 100, 40, 30))
        
        self.water_goal = Door(100, 40, PlayerType.WATER)
        self.fire_goal = Door(SCREEN_WIDTH - 140, 40, PlayerType.FIRE)
        
        self.time_limit = 300
