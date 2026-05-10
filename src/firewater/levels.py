from .constants import SCREEN_HEIGHT, SCREEN_WIDTH, PlayerType, LEVEL_TIME
from .obstacles import (Obstacle, Coin, Enemy, HazardPool, Door, 
                       ActivationButton, MovingPlatform, Crossbow)

class Level:
    def __init__(self, level_num: int, water_color: tuple, fire_color: tuple):
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
        self.water_color = water_color
        self.fire_color = fire_color
        self._create_level()
    
    def _create_level(self):
        # SpoleÄŤnĂˇ zĂˇkladnĂ­ podlaha pro vĹˇechny ĂşrovnÄ›
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
        # ĂšvodnĂ­ level - zĂˇkladnĂ­ pĹ™eskoky
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # BazĂ©ny
        self.hazard_pools.append(HazardPool(250, SCREEN_HEIGHT - 80, 200, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 450, SCREEN_HEIGHT - 80, 200, 30, "water", self.water_color))
        # Kyselina mimo kritickou cestu
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH // 2 - 100, 600, 200, 30, "acid", (100, 255, 100)))
        
        # Voda cesta - vlevo
        self.obstacles.append(Obstacle(50, 680, 130, 20))
        self.obstacles.append(Obstacle(180, 600, 130, 20))
        self.obstacles.append(Obstacle(310, 520, 130, 20))
        self.obstacles.append(Obstacle(440, 440, 130, 20))
        self.obstacles.append(Obstacle(570, 360, 130, 20))
        # PevnĂˇ platforma pod dveĹ™mi
        self.obstacles.append(Obstacle(650, 300, 130, 20))
        
        self.coins.append(Coin(100, 655, "water"))
        self.coins.append(Coin(230, 575, "water"))
        self.coins.append(Coin(360, 495, "water"))
        self.coins.append(Coin(490, 415, "water"))
        
        self.enemies.append(Enemy(350, 490, patrol_left=310, patrol_right=450))
        self.water_goal = Door(700, 280, PlayerType.WATER, color=self.water_color)

        # OheĹ cesta - vpravo
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 180, 680, 130, 20))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 310, 600, 130, 20))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 440, 520, 130, 20))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 570, 440, 130, 20))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 700, 360, 130, 20))
        # PevnĂˇ platforma pod dveĹ™mi
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 780, 300, 130, 20))
        
        self.coins.append(Coin(SCREEN_WIDTH - 130, 655, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 260, 575, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 390, 495, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 520, 415, "fire"))
        
        self.enemies.append(Enemy(SCREEN_WIDTH - 400, 490, patrol_left=SCREEN_WIDTH-450, patrol_right=SCREEN_WIDTH-300))
        self.fire_goal = Door(SCREEN_WIDTH - 700, 280, PlayerType.FIRE, color=self.fire_color)

        self.time_limit = 300
    
    def _level_2(self):
        # Level s pohyblivĂ˝mi platformami a hazardy
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

        # HazardnĂ­ zĂłny na spodku - motivace skĂˇkat vĂ˝Ĺˇ
        self.hazard_pools.append(HazardPool(200, SCREEN_HEIGHT - 80, 300, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(700, SCREEN_HEIGHT - 80, 300, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH // 2 - 100, 300, 200, 30, "acid", (100, 255, 100)))

        # Voda cesta - vlevo s pohyblivĂ˝mi platformami
        self.obstacles.append(Obstacle(50, 620, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(140, 540, 140, 20, 120, 0.9))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(270, 460, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(380, 380, 140, 20, 120, 0.9))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(510, 300, 140, 20))
        self.obstacles.append(Obstacle(640, 220, 140, 20))
        
        self.coins.append(Coin(110, 560, "water"))
        self.coins.append(Coin(200, 510, "water"))
        self.coins.append(Coin(350, 460, "water"))
        self.coins.append(Coin(450, 410, "water"))
        
        self.enemies.append(Enemy(450, 420, patrol_left=400, patrol_right=550))
        self.water_goal = Door(800, 300, PlayerType.WATER, color=self.water_color)

        # OheĹ cesta - vpravo (symetrickĂˇ)
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 190, 620, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 280, 540, 140, 20, 120, 0.9))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 410, 460, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 520, 380, 140, 20, 120, 0.9))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 650, 300, 140, 20))
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 780, 220, 140, 20))
        
        self.coins.append(Coin(SCREEN_WIDTH - 140, 560, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 240, 510, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 390, 460, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 490, 410, "fire"))
        
        self.enemies.append(Enemy(SCREEN_WIDTH - 490, 420, patrol_left=SCREEN_WIDTH-540, patrol_right=SCREEN_WIDTH-400))
        self.fire_goal = Door(SCREEN_WIDTH - 840, 300, PlayerType.FIRE, color=self.fire_color)

        self.time_limit = 320
    
    def _level_3(self):
        # Level se skĂˇkĂˇnĂ­m, pohyblivĂ˝mi platformami a kuĹˇĂ­
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # BazĂ©ny
        self.hazard_pools.append(HazardPool(250, SCREEN_HEIGHT - 80, 250, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 500, SCREEN_HEIGHT - 80, 250, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH // 2 - 100, 280, 200, 30, "acid", (100, 255, 100)))

        # Voda cesta - vlevo s vĂ­ce platformami
        self.obstacles.append(Obstacle(50, 630, 130, 20))
        
        self.moving_platforms.append(MovingPlatform(130, 540, 130, 20, 130, 1.0))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(270, 450, 130, 20))
        
        self.moving_platforms.append(MovingPlatform(380, 360, 130, 20, 130, 0.95))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(520, 270, 130, 20))
        
        self.moving_platforms.append(MovingPlatform(640, 180, 130, 20, 130, 0.9))
        self.obstacles.append(self.moving_platforms[-1])
        
        # KuĹˇe
        self.crossbows.append(Crossbow(SCREEN_WIDTH // 2 - 80, 200, 1))
        
        self.coins.append(Coin(100, 590, "water"))
        self.coins.append(Coin(170, 500, "water"))
        self.coins.append(Coin(320, 410, "water"))
        self.coins.append(Coin(430, 320, "water"))
        
        self.enemies.append(Enemy(400, 330, patrol_left=330, patrol_right=480))
        self.water_goal = Door(730, 120, PlayerType.WATER, color=self.water_color)

        # OheĹ cesta - vpravo
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 180, 630, 130, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 260, 540, 130, 20, 130, 1.0))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 400, 450, 130, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 510, 360, 130, 20, 130, 0.95))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 650, 270, 130, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 770, 180, 130, 20, 130, 0.9))
        self.obstacles.append(self.moving_platforms[-1])
        
        # KuĹˇe
        self.crossbows.append(Crossbow(SCREEN_WIDTH // 2 + 80, 200, -1))
        
        self.coins.append(Coin(SCREEN_WIDTH - 130, 590, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 210, 500, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 360, 410, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 460, 320, "fire"))
        
        self.enemies.append(Enemy(SCREEN_WIDTH - 450, 330, patrol_left=SCREEN_WIDTH-480, patrol_right=SCREEN_WIDTH-330))
        self.fire_goal = Door(SCREEN_WIDTH - 730, 120, PlayerType.FIRE, color=self.fire_color)

        self.time_limit = 340
    
    def _level_4(self):
        # DelĹˇĂ­ level s vĂ­ce pohyblivĂ˝mi platformami a kuĹˇĂ­
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # BazĂ©ny
        self.hazard_pools.append(HazardPool(150, SCREEN_HEIGHT - 80, 250, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 400, SCREEN_HEIGHT - 80, 250, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH // 2 - 100, 280, 200, 30, "acid", (100, 255, 100)))
        
        # HornĂ­ bezpeÄŤnĂˇ zĂłna pro pĹ™echod
        self.obstacles.append(Obstacle(300, 350, 600, 20))
        self.coins.append(Coin(500, 310, "water"))
        self.coins.append(Coin(700, 310, "fire"))
        self.enemies.append(Enemy(600, 320, patrol_left=300, patrol_right=800))
        
        # KuĹˇe
        self.crossbows.append(Crossbow(SCREEN_WIDTH // 2 - 80, 240, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH // 2 + 80, 240, -1))

        # Voda cesta - vlevo s vĂ­ce platformami
        self.obstacles.append(Obstacle(50, 650, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(110, 560, 140, 20, 150, 1.1))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(240, 470, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(340, 380, 140, 20, 150, 1.0))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(470, 290, 140, 20))
        
        self.coins.append(Coin(100, 610, "water"))
        self.coins.append(Coin(160, 520, "water"))
        self.coins.append(Coin(290, 430, "water"))
        self.coins.append(Coin(390, 340, "water"))
        
        self.water_goal = Door(320, 280, PlayerType.WATER, color=self.water_color)

        # OheĹ cesta - vpravo (symetrickĂˇ)
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 190, 650, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 250, 560, 140, 20, 150, 1.1))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 380, 470, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 480, 380, 140, 20, 150, 1.0))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 610, 290, 140, 20))
        
        self.coins.append(Coin(SCREEN_WIDTH - 140, 610, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 200, 520, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 330, 430, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 430, 340, "fire"))
        
        self.enemies.append(Enemy(SCREEN_WIDTH - 430, 390, patrol_left=SCREEN_WIDTH-480, patrol_right=SCREEN_WIDTH-350))
        
        self.fire_goal = Door(SCREEN_WIDTH - 880, 280, PlayerType.FIRE, color=self.fire_color)
        
        self.time_limit = 360
    
    def _level_5(self):
        # FinĂˇlnĂ­ level - Skok fest s pohyblivĂ˝mi platformami a kuĹˇĂ­
        self.obstacles.append(Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # BazĂ©ny
        self.hazard_pools.append(HazardPool(150, SCREEN_HEIGHT - 80, 250, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 400, SCREEN_HEIGHT - 80, 250, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH // 2 - 100, 200, 200, 30, "acid", (100, 255, 100)))

        # Voda cesta - vlevo s kombinacĂ­ statickĂ˝ch a pohyblivĂ˝ch platforem
        self.obstacles.append(Obstacle(50, 650, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(110, 560, 140, 20, 150, 1.1))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(250, 470, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(350, 380, 140, 20, 150, 1.05))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(490, 290, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(600, 200, 140, 20, 150, 1.0))
        self.obstacles.append(self.moving_platforms[-1])
        
        # KuĹˇe
        self.crossbows.append(Crossbow(SCREEN_WIDTH // 2 - 80, 140, 1))
        
        # FinĂˇlnĂ­ skok
        self.obstacles.append(Obstacle(SCREEN_WIDTH // 2 - 180, 100, 150, 20))
        
        self.coins.append(Coin(100, 610, "water"))
        self.coins.append(Coin(170, 520, "water"))
        self.coins.append(Coin(300, 430, "water"))
        self.coins.append(Coin(400, 340, "water"))
        self.coins.append(Coin(540, 250, "water"))
        self.coins.append(Coin(650, 160, "water"))
        self.coins.append(Coin(SCREEN_WIDTH // 2 - 130, 60, "water"))
        
        self.enemies.append(Enemy(350, 350, patrol_left=280, patrol_right=450))
        self.water_goal = Door(SCREEN_WIDTH // 2 - 140, 50, PlayerType.WATER, color=self.water_color)

        # OheĹ cesta - vpravo (symetrickĂˇ)
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 190, 650, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 250, 560, 140, 20, 150, 1.1))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 390, 470, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 490, 380, 140, 20, 150, 1.05))
        self.obstacles.append(self.moving_platforms[-1])
        
        self.obstacles.append(Obstacle(SCREEN_WIDTH - 630, 290, 140, 20))
        
        self.moving_platforms.append(MovingPlatform(SCREEN_WIDTH - 740, 200, 140, 20, 150, 1.0))
        self.obstacles.append(self.moving_platforms[-1])
        
        # KuĹˇe
        self.crossbows.append(Crossbow(SCREEN_WIDTH // 2 + 80, 140, -1))
        
        # FinĂˇlnĂ­ skok
        self.obstacles.append(Obstacle(SCREEN_WIDTH // 2 + 30, 100, 150, 20))
        
        self.coins.append(Coin(SCREEN_WIDTH - 140, 610, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 210, 520, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 340, 430, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 440, 340, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 580, 250, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH - 690, 160, "fire"))
        self.coins.append(Coin(SCREEN_WIDTH // 2 + 100, 60, "fire"))
        
        self.enemies.append(Enemy(SCREEN_WIDTH - 430, 350, patrol_left=SCREEN_WIDTH-500, patrol_right=SCREEN_WIDTH-300))
        self.fire_goal = Door(SCREEN_WIDTH // 2 + 110, 50, PlayerType.FIRE, color=self.fire_color)
        
        self.time_limit = 400

