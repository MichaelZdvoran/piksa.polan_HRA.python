from .constants import SCREEN_HEIGHT, SCREEN_WIDTH, PlayerType, LEVEL_TIME
from .obstacles import (
    Coin,
    Crossbow,
    Door,
    Enemy,
    FastEnemy,
    HazardPool,
    HeavyEnemy,
    JumperEnemy,
    MovingPlatform,
    Obstacle,
    VerticalEnemy,
    ZigZagEnemy,
)


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
        self.water_spawn = (80, SCREEN_HEIGHT - 90)
        self.fire_spawn = (SCREEN_WIDTH - 110, SCREEN_HEIGHT - 90)
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

    def _add_platform(self, x: float, y: float, width: float, height: float = 20):
        platform = Obstacle(x, y, width, height)
        self.obstacles.append(platform)
        return platform

    def _add_moving_platform(
        self,
        x: float,
        y: float,
        width: float,
        height: float = 20,
        move_distance: float = 90,
        speed: float = 0.8,
    ):
        platform = MovingPlatform(x, y, width, height, move_distance, speed)
        self.moving_platforms.append(platform)
        self.obstacles.append(platform)
        return platform

    def _add_coin_on_platform(self, platform: Obstacle, x_offset: float, coin_type: str):
        coin_x = platform.rect.x + x_offset
        coin_y = platform.rect.y - 28
        self.coins.append(Coin(coin_x, coin_y, coin_type))

    def _add_door_with_platform(self, x: float, y: float, player_type: PlayerType, color: tuple):
        platform_x = max(0, min(SCREEN_WIDTH - 150, x - 55))
        self._add_platform(platform_x, y + 60, 150, 20)
        door = Door(x, y, player_type, color=color)
        if player_type == PlayerType.WATER:
            self.water_goal = door
        else:
            self.fire_goal = door

    def _add_default_spawns(self):
        self.water_spawn = (80, SCREEN_HEIGHT - 90)
        self.fire_spawn = (SCREEN_WIDTH - 110, SCREEN_HEIGHT - 90)

    def _add_ground(self):
        self._add_platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)

    def _add_edge_crossbows(self, y: float):
        self.crossbows.append(Crossbow(20, y, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 40, y, -1))

    def _level_1(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(280, SCREEN_HEIGHT - 80, 190, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 470, SCREEN_HEIGHT - 80, 190, 30, "water", self.water_color))

        water_platforms = [
            self._add_platform(70, 650, 150),
            self._add_platform(230, 565, 150),
            self._add_platform(390, 480, 150),
            self._add_platform(550, 395, 150),
        ]
        fire_platforms = [
            self._add_platform(SCREEN_WIDTH - 220, 650, 150),
            self._add_platform(SCREEN_WIDTH - 380, 565, 150),
            self._add_platform(SCREEN_WIDTH - 540, 480, 150),
            self._add_platform(SCREEN_WIDTH - 700, 395, 150),
        ]

        for platform in water_platforms:
            self._add_coin_on_platform(platform, 65, "water")
        for platform in fire_platforms:
            self._add_coin_on_platform(platform, 65, "fire")

        self.enemies.append(Enemy(410, 450, patrol_left=390, patrol_right=510))
        self.enemies.append(FastEnemy(SCREEN_WIDTH - 520, 450, patrol_left=SCREEN_WIDTH - 540, patrol_right=SCREEN_WIDTH - 420))
        self._add_edge_crossbows(330)

        self._add_door_with_platform(710, 315, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(SCREEN_WIDTH - 750, 315, PlayerType.FIRE, self.fire_color)
        self.time_limit = 300

    def _level_2(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(210, SCREEN_HEIGHT - 80, 260, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 470, SCREEN_HEIGHT - 80, 260, 30, "water", self.water_color))

        water_static = [
            self._add_platform(70, 625, 150),
            self._add_platform(290, 465, 150),
            self._add_platform(520, 305, 150),
        ]
        fire_static = [
            self._add_platform(SCREEN_WIDTH - 220, 625, 150),
            self._add_platform(SCREEN_WIDTH - 440, 465, 150),
            self._add_platform(SCREEN_WIDTH - 670, 305, 150),
        ]

        self._add_moving_platform(170, 545, 135, move_distance=80, speed=0.7)
        self._add_moving_platform(400, 385, 135, move_distance=80, speed=0.7)
        self._add_moving_platform(SCREEN_WIDTH - 305, 545, 135, move_distance=80, speed=0.7)
        self._add_moving_platform(SCREEN_WIDTH - 535, 385, 135, move_distance=80, speed=0.7)

        for platform in water_static:
            self._add_coin_on_platform(platform, 65, "water")
        self._add_coin_on_platform(water_static[1], 105, "water")
        for platform in fire_static:
            self._add_coin_on_platform(platform, 65, "fire")
        self._add_coin_on_platform(fire_static[1], 25, "fire")

        self.enemies.append(HeavyEnemy(325, 431, patrol_left=295, patrol_right=405))
        self.enemies.append(VerticalEnemy(SCREEN_WIDTH - 405, 405, patrol_top=375, patrol_bottom=450))
        self._add_edge_crossbows(330)

        self._add_door_with_platform(710, 245, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(SCREEN_WIDTH - 750, 245, PlayerType.FIRE, self.fire_color)
        self.time_limit = 330

    def _level_3(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(240, SCREEN_HEIGHT - 80, 230, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 470, SCREEN_HEIGHT - 80, 230, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH // 2 - 90, 585, 180, 25, "acid", (100, 255, 100)))

        water_platforms = [
            self._add_platform(65, 640, 140),
            self._add_platform(235, 550, 140),
            self._add_platform(405, 460, 140),
            self._add_platform(575, 370, 140),
            self._add_platform(720, 280, 140),
        ]
        fire_platforms = [
            self._add_platform(SCREEN_WIDTH - 205, 640, 140),
            self._add_platform(SCREEN_WIDTH - 375, 550, 140),
            self._add_platform(SCREEN_WIDTH - 545, 460, 140),
            self._add_platform(SCREEN_WIDTH - 715, 370, 140),
            self._add_platform(SCREEN_WIDTH - 860, 280, 140),
        ]

        for platform in water_platforms[:4]:
            self._add_coin_on_platform(platform, 60, "water")
        for platform in fire_platforms[:4]:
            self._add_coin_on_platform(platform, 60, "fire")

        self.enemies.append(JumperEnemy(420, 430, patrol_left=405, patrol_right=510))
        self.enemies.append(ZigZagEnemy(SCREEN_WIDTH - 525, 430, patrol_left=SCREEN_WIDTH - 545, patrol_right=SCREEN_WIDTH - 440))
        self._add_edge_crossbows(255)

        self._add_door_with_platform(765, 200, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(SCREEN_WIDTH - 805, 200, PlayerType.FIRE, self.fire_color)
        self.time_limit = 350

    def _level_4(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(170, SCREEN_HEIGHT - 80, 250, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 420, SCREEN_HEIGHT - 80, 250, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH // 2 - 110, 520, 220, 25, "acid", (100, 255, 100)))

        center_bridge = self._add_platform(350, 345, 500)
        water_platforms = [
            self._add_platform(70, 655, 145),
            self._add_moving_platform(155, 570, 140, move_distance=70, speed=0.75),
            self._add_platform(275, 485, 145),
            self._add_moving_platform(395, 400, 140, move_distance=70, speed=0.75),
            self._add_platform(515, 315, 145),
        ]
        fire_platforms = [
            self._add_platform(SCREEN_WIDTH - 215, 655, 145),
            self._add_moving_platform(SCREEN_WIDTH - 295, 570, 140, move_distance=70, speed=0.75),
            self._add_platform(SCREEN_WIDTH - 420, 485, 145),
            self._add_moving_platform(SCREEN_WIDTH - 535, 400, 140, move_distance=70, speed=0.75),
            self._add_platform(SCREEN_WIDTH - 660, 315, 145),
        ]

        for platform in [water_platforms[0], water_platforms[2], water_platforms[4], center_bridge]:
            self._add_coin_on_platform(platform, 60, "water")
        for platform in [fire_platforms[0], fire_platforms[2], fire_platforms[4], center_bridge]:
            self._add_coin_on_platform(platform, 75, "fire")

        self.enemies.append(FastEnemy(455, 315, patrol_left=355, patrol_right=580))
        self.enemies.append(HeavyEnemy(690, 311, patrol_left=610, patrol_right=820))
        self._add_edge_crossbows(250)

        self._add_door_with_platform(305, 235, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(SCREEN_WIDTH - 345, 235, PlayerType.FIRE, self.fire_color)
        self.time_limit = 370

    def _level_5(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(170, SCREEN_HEIGHT - 80, 250, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH - 420, SCREEN_HEIGHT - 80, 250, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(SCREEN_WIDTH // 2 - 95, 445, 190, 25, "acid", (100, 255, 100)))

        water_platforms = [
            self._add_platform(65, 655, 145),
            self._add_moving_platform(145, 570, 140, move_distance=75, speed=0.8),
            self._add_platform(285, 485, 145),
            self._add_moving_platform(365, 400, 140, move_distance=75, speed=0.8),
            self._add_platform(505, 315, 145),
            self._add_moving_platform(585, 230, 140, move_distance=70, speed=0.7),
        ]
        fire_platforms = [
            self._add_platform(SCREEN_WIDTH - 210, 655, 145),
            self._add_moving_platform(SCREEN_WIDTH - 285, 570, 140, move_distance=75, speed=0.8),
            self._add_platform(SCREEN_WIDTH - 430, 485, 145),
            self._add_moving_platform(SCREEN_WIDTH - 505, 400, 140, move_distance=75, speed=0.8),
            self._add_platform(SCREEN_WIDTH - 650, 315, 145),
            self._add_moving_platform(SCREEN_WIDTH - 725, 230, 140, move_distance=70, speed=0.7),
        ]
        final_water = self._add_platform(SCREEN_WIDTH // 2 - 205, 145, 160)
        final_fire = self._add_platform(SCREEN_WIDTH // 2 + 45, 145, 160)

        for platform in [water_platforms[0], water_platforms[2], water_platforms[4]]:
            self._add_coin_on_platform(platform, 62, "water")
        self._add_coin_on_platform(water_platforms[4], 105, "water")

        for platform in [fire_platforms[0], fire_platforms[2], fire_platforms[4]]:
            self._add_coin_on_platform(platform, 62, "fire")
        self._add_coin_on_platform(fire_platforms[4], 25, "fire")

        self.enemies.append(JumperEnemy(305, 455, patrol_left=285, patrol_right=400))
        self.enemies.append(ZigZagEnemy(SCREEN_WIDTH - 410, 455, patrol_left=SCREEN_WIDTH - 430, patrol_right=SCREEN_WIDTH - 315))
        self._add_edge_crossbows(185)

        self._add_door_with_platform(SCREEN_WIDTH // 2 - 145, 65, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(SCREEN_WIDTH // 2 + 105, 65, PlayerType.FIRE, self.fire_color)
        self.time_limit = 410
