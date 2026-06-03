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
    def __init__(
        self,
        level_num: int,
        water_color: tuple,
        fire_color: tuple,
        screen_width: int = SCREEN_WIDTH,
        screen_height: int = SCREEN_HEIGHT,
    ):
        self.level_num = level_num
        self.screen_width = screen_width
        self.screen_height = screen_height
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
        self.water_spawn = (80, self.screen_height - 90)
        self.fire_spawn = (self.screen_width - 110, self.screen_height - 90)
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

    def _level_y(self, y: float):
        if self.level_num >= 4:
            return y + (self.screen_height - SCREEN_HEIGHT)
        return y

    def _add_platform(self, x: float, y: float, width: float, height: float = 20):
        platform = Obstacle(x, self._level_y(y), width, height)
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
        color: tuple = None,
    ):
        platform = MovingPlatform(x, self._level_y(y), width, height, move_distance, speed, color)
        self.moving_platforms.append(platform)
        self.obstacles.append(platform)
        return platform

    def _add_coin_on_platform(self, platform: Obstacle, x_offset: float, coin_type: str):
        coin_x = platform.rect.x + x_offset
        coin_y = platform.rect.y - 28
        self.coins.append(Coin(coin_x, coin_y, coin_type))

    def _add_door_with_platform(self, x: float, y: float, player_type: PlayerType, color: tuple):
        platform_x = max(0, min(self.screen_width - 150, x - 55))
        self._add_platform(platform_x, y + 60, 150, 20)
        door = Door(x, self._level_y(y), player_type, color=color)
        if player_type == PlayerType.WATER:
            self.water_goal = door
        else:
            self.fire_goal = door

    def _add_default_spawns(self):
        self.water_spawn = (80, self.screen_height - 90)
        self.fire_spawn = (self.screen_width - 110, self.screen_height - 90)

    def _add_ground(self):
        self._add_platform(0, SCREEN_HEIGHT - 50, self.screen_width, 50)

    def _add_edge_crossbows(self, y: float):
        self.crossbows.append(Crossbow(20, self._level_y(y), 1))
        self.crossbows.append(Crossbow(self.screen_width - 40, self._level_y(y), -1))

    def _level_1(self):
        self._add_default_spawns()
        self._add_ground()

        pink = (175, 70, 175)

        self.hazard_pools.append(HazardPool(160, self.screen_height - 80, 120, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(875, self.screen_height - 80, 135, 30, "water", self.water_color))

        lower_left = self._add_moving_platform(220, 680, 130, move_distance=55, speed=0.55, color=pink)
        lower_right = self._add_moving_platform(845, 660, 130, move_distance=55, speed=0.55, color=pink)

        left_step = self._add_platform(330, 600, 110)
        left_mid = self._add_platform(425, 530, 120)
        center_low = self._add_platform(520, 455, 110)
        center_high = self._add_platform(545, 385, 110)
        right_mid = self._add_platform(625, 520, 110)
        right_step = self._add_platform(745, 600, 115)

        upper_left = self._add_moving_platform(285, 300, 125, move_distance=60, speed=0.5, color=pink)
        upper_right = self._add_moving_platform(645, 300, 125, move_distance=60, speed=0.5, color=pink)

        self._add_coin_on_platform(left_step, 45, "water")
        self._add_coin_on_platform(left_mid, 55, "water")
        self._add_coin_on_platform(center_high, 22, "water")
        self._add_coin_on_platform(center_high, 75, "fire")
        self._add_coin_on_platform(right_mid, 45, "fire")
        self._add_coin_on_platform(right_step, 55, "fire")

        self._add_door_with_platform(110, 185, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(870, 175, PlayerType.FIRE, self.fire_color)
        self.time_limit = 320

    def _level_2(self):
        self.water_spawn = (520, self.screen_height - 90)
        self.fire_spawn = (640, self.screen_height - 90)
        self._add_ground()

        pink = (175, 70, 175)

        self.hazard_pools.append(HazardPool(300, self.screen_height - 80, 120, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(750, self.screen_height - 80, 140, 30, "water", self.water_color))

        lower_left = self._add_moving_platform(225, 675, 130, move_distance=55, speed=0.55, color=pink)
        lower_right = self._add_moving_platform(845, 675, 130, move_distance=55, speed=0.55, color=pink)

        left_low = self._add_platform(90, 600, 110)
        left_mid = self._add_platform(245, 515, 115)
        left_high = self._add_platform(385, 445, 90)
        center = self._add_platform(530, 365, 110)
        right_high = self._add_platform(680, 445, 95)
        right_mid = self._add_platform(845, 515, 95)
        right_low = self._add_platform(1010, 600, 110)

        upper_left = self._add_moving_platform(50, 330, 125, move_distance=45, speed=0.45, color=pink)
        upper_right = self._add_moving_platform(980, 330, 125, move_distance=45, speed=0.45, color=pink)
        top_left = self._add_platform(210, 235, 165)
        top_right = self._add_platform(845, 235, 165)

        self._add_coin_on_platform(left_low, 55, "water")
        self._add_coin_on_platform(left_mid, 45, "water")
        self._add_coin_on_platform(left_high, 34, "water")
        self._add_coin_on_platform(top_left, 78, "water")
        self._add_coin_on_platform(center, 25, "water")
        self._add_coin_on_platform(center, 75, "fire")
        self._add_coin_on_platform(right_high, 42, "fire")
        self._add_coin_on_platform(right_mid, 43, "fire")
        self._add_coin_on_platform(right_low, 50, "fire")
        self._add_coin_on_platform(top_right, 82, "fire")

        self._add_door_with_platform(465, 150, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(615, 140, PlayerType.FIRE, self.fire_color)
        self.time_limit = 350

    def _level_3(self):
        self.water_spawn = (535, self.screen_height - 90)
        self.fire_spawn = (665, self.screen_height - 90)
        self._add_ground()

        pink = (175, 70, 175)

        lower_left = self._add_platform(175, 675, 105)
        lower_mid_left = self._add_platform(350, 625, 105)
        lower_right = self._add_platform(820, 625, 120)
        right_low = self._add_platform(925, 545, 105)
        right_mid = self._add_platform(805, 460, 125)
        left_low = self._add_platform(175, 535, 105)
        left_mid = self._add_platform(270, 445, 85)
        middle = self._add_platform(390, 360, 165)
        right_high = self._add_platform(795, 275, 160)

        left_lower_move = self._add_moving_platform(55, 455, 130, move_distance=45, speed=0.5, color=pink)
        left_upper_move = self._add_moving_platform(235, 285, 130, move_distance=55, speed=0.5, color=pink)
        right_mid_move = self._add_moving_platform(960, 355, 125, move_distance=50, speed=0.55, color=pink)
        right_lower_move = self._add_moving_platform(1060, 630, 125, move_distance=45, speed=0.5, color=pink)

        self._add_coin_on_platform(lower_left, 45, "water")
        self._add_coin_on_platform(lower_mid_left, 50, "water")
        self._add_coin_on_platform(left_low, 45, "water")
        self._add_coin_on_platform(left_mid, 35, "water")
        self._add_coin_on_platform(middle, 75, "water")
        self._add_coin_on_platform(lower_right, 55, "fire")
        self._add_coin_on_platform(right_low, 45, "fire")
        self._add_coin_on_platform(right_mid, 62, "fire")
        self._add_coin_on_platform(right_high, 70, "fire")

        self.enemies.append(VerticalEnemy(465, 230, patrol_top=205, patrol_bottom=250))
        self.enemies.append(JumperEnemy(1075, 300, patrol_left=1060, patrol_right=1115))
        self.crossbows.append(Crossbow(0, 250, 1))
        self.crossbows.append(Crossbow(self.screen_width - 20, 420, -1))

        self._add_door_with_platform(105, 190, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(650, 185, PlayerType.FIRE, self.fire_color)
        self.time_limit = 380

    def _level_4(self):
        self.water_spawn = (80, self.screen_height - 105)
        self.fire_spawn = (self.screen_width - 115, self.screen_height - 105)
        self._add_ground()

        moving_blue = (170, 170, 235)

        self.hazard_pools.append(HazardPool(165, self.screen_height - 80, 185, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(610, self._level_y(395), 165, 25, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(1090, self.screen_height - 80, 220, 30, "water", self.water_color))

        bottom_left = self._add_platform(70, 625, 135)
        bottom_mid_left = self._add_moving_platform(235, 575, 140, move_distance=55, speed=0.55, color=moving_blue)
        center_left = self._add_platform(355, 490, 150)
        middle_lava_left = self._add_platform(505, 445, 145)
        middle_lava_right = self._add_platform(735, 425, 120)
        right_lower = self._add_platform(900, 510, 125)
        right_mid_move = self._add_moving_platform(1175, 585, 150, move_distance=55, speed=0.55, color=moving_blue)
        far_left_move = self._add_moving_platform(245, 300, 125, move_distance=60, speed=0.5, color=moving_blue)
        upper_left = self._add_platform(360, 205, 120)
        upper_mid = self._add_platform(555, 260, 120)
        center_high = self._add_platform(705, 330, 160)
        upper_right_move = self._add_moving_platform(960, 415, 165, move_distance=60, speed=0.55, color=moving_blue)
        right_high = self._add_platform(1160, 235, 170)
        fire_goal_step = self._add_platform(1300, 260, 150)

        self._add_coin_on_platform(bottom_left, 58, "water")
        self._add_coin_on_platform(center_left, 78, "water")
        self._add_coin_on_platform(upper_left, 56, "water")
        self._add_coin_on_platform(upper_mid, 62, "water")
        self._add_coin_on_platform(far_left_move, 62, "water")
        self._add_coin_on_platform(middle_lava_right, 72, "fire")
        self._add_coin_on_platform(right_lower, 55, "fire")
        self._add_coin_on_platform(right_mid_move, 68, "fire")
        self._add_coin_on_platform(right_high, 82, "fire")
        self._add_coin_on_platform(fire_goal_step, 72, "fire")

        self.enemies.append(JumperEnemy(450, self._level_y(480), patrol_left=415, patrol_right=495))
        self.enemies.append(FastEnemy(725, self._level_y(350), patrol_left=705, patrol_right=835))
        self.enemies.append(HeavyEnemy(1125, self._level_y(405), patrol_left=1085, patrol_right=1215))
        self.enemies.append(FastEnemy(1390, self._level_y(735), patrol_left=1345, patrol_right=1455))
        self.crossbows.append(Crossbow(20, self._level_y(260), 1))
        self.crossbows.append(Crossbow(390, self._level_y(95), 1))
        self.crossbows.append(Crossbow(675, self._level_y(245), 1))
        self.crossbows.append(Crossbow(self.screen_width - 40, self._level_y(360), -1))

        self._add_door_with_platform(420, -20, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(1365, 70, PlayerType.FIRE, self.fire_color)
        self.time_limit = 410

    def _level_5(self):
        self._add_default_spawns()
        self._add_ground()

        self.hazard_pools.append(HazardPool(155, self.screen_height - 80, 180, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(420, self.screen_height - 80, 150, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(675, self.screen_height - 80, 155, 30, "water", self.water_color))
        self.hazard_pools.append(HazardPool(930, self.screen_height - 80, 165, 30, "lava", self.fire_color))
        self.hazard_pools.append(HazardPool(490, self._level_y(515), 155, 25, "acid", (100, 255, 100)))
        self.hazard_pools.append(HazardPool(735, self._level_y(335), 150, 25, "water", self.water_color))

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

        self.enemies.append(JumperEnemy(350, self._level_y(425), patrol_left=335, patrol_right=425))
        self.enemies.append(ZigZagEnemy(790, self._level_y(430), patrol_left=770, patrol_right=860))
        self.enemies.append(FastEnemy(1020, self._level_y(480), patrol_left=1000, patrol_right=1090))
        self.enemies.append(VerticalEnemy(705, self._level_y(170), patrol_top=self._level_y(130), patrol_bottom=self._level_y(245)))
        self.crossbows.append(Crossbow(20, self._level_y(240), 1))
        self.crossbows.append(Crossbow(self.screen_width - 40, self._level_y(295), -1))
        self.crossbows.append(Crossbow(20, self._level_y(520), 1))

        self._add_door_with_platform(210, 125, PlayerType.WATER, self.water_color)
        self._add_door_with_platform(555, 55, PlayerType.FIRE, self.fire_color)
        self.time_limit = 450
