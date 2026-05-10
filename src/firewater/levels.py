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

        self.hazard_pools.append(HazardPool(250, SCREEN_HEIGHT - 80, 185, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(690, SCREEN_HEIGHT - 80, 210, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(520, 600, 120, 24, "acid", (100, 255, 100)))

        lower_left = self._add_platform(80, 650, 160)
        lower_mid = self._add_platform(455, 620, 145)
        lower_right = self._add_platform(920, 640, 150)
        step_a = self._add_platform(205, 540, 130)
        step_b = self._add_platform(610, 525, 135)
        step_c = self._add_platform(800, 475, 145)
        step_d = self._add_platform(360, 435, 150)
        upper_left_ramp = self._add_platform(255, 365, 120)
        upper_mid = self._add_platform(555, 350, 165)
        upper_left = self._add_platform(170, 300, 145)
        upper_right = self._add_platform(845, 285, 150)

        self._add_coin_on_platform(lower_left, 70, "water")
        self._add_coin_on_platform(step_a, 50, "water")
        self._add_coin_on_platform(step_d, 82, "water")
        self._add_coin_on_platform(upper_left_ramp, 46, "water")
        self._add_coin_on_platform(upper_mid, 38, "water")
        self._add_coin_on_platform(lower_right, 60, "fire")
        self._add_coin_on_platform(step_c, 70, "fire")
        self._add_coin_on_platform(step_b, 92, "fire")
        self._add_coin_on_platform(upper_mid, 118, "fire")

        self.enemies.append(Enemy(382, 405, patrol_left=360, patrol_right=480))
        self.enemies.append(FastEnemy(825, 445, patrol_left=800, patrol_right=915))
        self.crossbows.append(Crossbow(20, 405, 1))

        self._add_door_with_platform(210, 220, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(900, 205, PlayerType.FIRE, self.fire_color)
        self.time_limit = 320

    def _level_2(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(180, SCREEN_HEIGHT - 80, 210, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(520, SCREEN_HEIGHT - 80, 150, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(850, SCREEN_HEIGHT - 80, 170, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(330, 505, 130, 25, "water", self.water_color))

        p1 = self._add_platform(80, 630, 145)
        p2 = self._add_moving_platform(285, 575, 125, move_distance=65, speed=0.65)
        p3 = self._add_platform(480, 505, 145)
        p4 = self._add_platform(720, 575, 135)
        p5 = self._add_moving_platform(905, 520, 130, move_distance=85, speed=0.75)
        p6 = self._add_platform(755, 420, 150)
        p7 = self._add_moving_platform(560, 385, 130, move_distance=75, speed=0.65)
        p8 = self._add_platform(350, 335, 145)
        p9 = self._add_platform(145, 250, 145)
        p9b = self._add_platform(705, 335, 130)
        p10 = self._add_platform(735, 250, 155)

        self._add_coin_on_platform(p1, 60, "water")
        self._add_coin_on_platform(p3, 38, "water")
        self._add_coin_on_platform(p8, 90, "water")
        self._add_coin_on_platform(p9, 55, "water")
        self._add_coin_on_platform(p4, 55, "fire")
        self._add_coin_on_platform(p5, 55, "fire")
        self._add_coin_on_platform(p6, 100, "fire")
        self._add_coin_on_platform(p9b, 52, "fire")
        self._add_coin_on_platform(p10, 70, "fire")

        self.enemies.append(HeavyEnemy(505, 471, patrol_left=485, patrol_right=590))
        self.enemies.append(VerticalEnemy(685, 325, patrol_top=285, patrol_bottom=390))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 40, 345, -1))

        self._add_door_with_platform(185, 170, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(790, 170, PlayerType.FIRE, self.fire_color)
        self.time_limit = 350

    def _level_3(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(260, SCREEN_HEIGHT - 80, 170, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(615, SCREEN_HEIGHT - 80, 160, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(905, SCREEN_HEIGHT - 80, 170, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(515, 565, 170, 25, "acid", (100, 255, 100)))
        self.hazard_pools.append(HazardPool(775, 370, 125, 25, "lava", self.fire_color))

        p1 = self._add_platform(65, 635, 135)
        p2 = self._add_platform(440, 630, 135)
        p3 = self._add_moving_platform(720, 590, 120, move_distance=70, speed=0.8)
        p4 = self._add_platform(960, 535, 130)
        p5 = self._add_moving_platform(180, 520, 120, move_distance=70, speed=0.7)
        p6 = self._add_platform(375, 455, 135)
        p7 = self._add_platform(590, 440, 135)
        p8 = self._add_moving_platform(835, 315, 120, move_distance=70, speed=0.75)
        p9 = self._add_platform(625, 270, 135)
        p10 = self._add_platform(390, 260, 135)
        p11 = self._add_platform(135, 325, 140)

        self._add_coin_on_platform(p1, 55, "water")
        self._add_coin_on_platform(p5, 50, "water")
        self._add_coin_on_platform(p6, 88, "water")
        self._add_coin_on_platform(p10, 58, "water")
        self._add_coin_on_platform(p2, 60, "fire")
        self._add_coin_on_platform(p3, 52, "fire")
        self._add_coin_on_platform(p7, 72, "fire")
        self._add_coin_on_platform(p9, 55, "fire")

        self.enemies.append(JumperEnemy(395, 425, patrol_left=375, patrol_right=480))
        self.enemies.append(ZigZagEnemy(960, 505, patrol_left=960, patrol_right=1060))
        self.enemies.append(VerticalEnemy(560, 340, patrol_top=285, patrol_bottom=410))
        self.crossbows.append(Crossbow(20, 250, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 40, 430, -1))

        self._add_door_with_platform(175, 245, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(665, 190, PlayerType.FIRE, self.fire_color)
        self.time_limit = 380

    def _level_4(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(165, SCREEN_HEIGHT - 80, 185, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(420, SCREEN_HEIGHT - 80, 155, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(765, SCREEN_HEIGHT - 80, 220, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(455, 505, 190, 25, "acid", (100, 255, 100)))
        self.hazard_pools.append(HazardPool(780, 455, 130, 25, "lava", self.fire_color))

        p1 = self._add_platform(70, 650, 130)
        p2 = self._add_moving_platform(260, 590, 120, move_distance=80, speed=0.85)
        p3 = self._add_platform(505, 610, 125)
        p4 = self._add_platform(690, 540, 130)
        p5 = self._add_moving_platform(930, 585, 120, move_distance=75, speed=0.8)
        p6 = self._add_platform(1005, 455, 125)
        p7 = self._add_platform(740, 395, 130)
        p8 = self._add_moving_platform(530, 385, 125, move_distance=80, speed=0.7)
        p9 = self._add_platform(305, 410, 130)
        p10 = self._add_platform(105, 340, 140)
        p11 = self._add_platform(355, 260, 130)
        p12 = self._add_platform(620, 245, 145)
        p13 = self._add_moving_platform(835, 230, 125, move_distance=65, speed=0.7)

        self._add_coin_on_platform(p1, 50, "water")
        self._add_coin_on_platform(p9, 75, "water")
        self._add_coin_on_platform(p10, 58, "water")
        self._add_coin_on_platform(p11, 62, "water")
        self._add_coin_on_platform(p3, 58, "fire")
        self._add_coin_on_platform(p5, 55, "fire")
        self._add_coin_on_platform(p7, 72, "fire")
        self._add_coin_on_platform(p12, 82, "fire")

        self.enemies.append(FastEnemy(725, 510, patrol_left=690, patrol_right=790))
        self.enemies.append(HeavyEnemy(550, 351, patrol_left=530, patrol_right=630))
        self.enemies.append(JumperEnemy(345, 380, patrol_left=305, patrol_right=410))
        self.crossbows.append(Crossbow(20, 285, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 40, 360, -1))

        self._add_door_with_platform(145, 260, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(885, 150, PlayerType.FIRE, self.fire_color)
        self.time_limit = 410

    def _level_5(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(155, SCREEN_HEIGHT - 80, 180, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(420, SCREEN_HEIGHT - 80, 150, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(675, SCREEN_HEIGHT - 80, 155, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(930, SCREEN_HEIGHT - 80, 165, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(490, 515, 155, 25, "acid", (100, 255, 100)))
        self.hazard_pools.append(HazardPool(735, 335, 150, 25, "water", self.water_color))

        p1 = self._add_platform(70, 650, 125)
        p2 = self._add_platform(345, 625, 120)
        p3 = self._add_moving_platform(585, 585, 115, move_distance=85, speed=0.9)
        p4 = self._add_platform(855, 615, 125)
        p5 = self._add_moving_platform(1000, 510, 115, move_distance=70, speed=0.85)
        p6 = self._add_platform(770, 460, 120)
        p7 = self._add_moving_platform(560, 415, 115, move_distance=90, speed=0.85)
        p8 = self._add_platform(335, 455, 120)
        p9 = self._add_moving_platform(145, 380, 115, move_distance=70, speed=0.8)
        p10 = self._add_platform(365, 305, 125)
        p11 = self._add_platform(600, 255, 130)
        p12 = self._add_moving_platform(835, 225, 115, move_distance=75, speed=0.8)
        p13 = self._add_platform(1010, 155, 120)
        p14 = self._add_platform(520, 135, 140)
        p15 = self._add_platform(170, 205, 130)

        self._add_coin_on_platform(p1, 50, "water")
        self._add_coin_on_platform(p8, 48, "water")
        self._add_coin_on_platform(p9, 48, "water")
        self._add_coin_on_platform(p10, 78, "water")
        self._add_coin_on_platform(p15, 56, "water")
        self._add_coin_on_platform(p2, 48, "fire")
        self._add_coin_on_platform(p4, 54, "fire")
        self._add_coin_on_platform(p6, 68, "fire")
        self._add_coin_on_platform(p11, 74, "fire")
        self._add_coin_on_platform(p13, 52, "fire")

        self.enemies.append(JumperEnemy(350, 425, patrol_left=335, patrol_right=425))
        self.enemies.append(ZigZagEnemy(790, 430, patrol_left=770, patrol_right=860))
        self.enemies.append(FastEnemy(1020, 480, patrol_left=1000, patrol_right=1090))
        self.enemies.append(VerticalEnemy(705, 170, patrol_top=130, patrol_bottom=245))
        self.crossbows.append(Crossbow(20, 240, 1))
        self.crossbows.append(Crossbow(SCREEN_WIDTH - 40, 295, -1))
        self.crossbows.append(Crossbow(20, 520, 1))

        self._add_door_with_platform(210, 125, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(555, 55, PlayerType.FIRE, self.fire_color)
        self.time_limit = 450
