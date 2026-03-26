import random
import pygame
from config import *

MAZE = [
    "#####################",
    "#........#........#.#",
    "#.###.###.#.###.###.#",
    "#*###.###.#.###.###*#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#####.### # ###.#####",
    "    #.#       #.#    ",
    "#####.# ##### #.#####",
    "     .  #   #  .     ",
    "#####.# ##### #.#####",
    "    #.#       #.#    ",
    "#####.# ##### #.#####",
    "#.........#.........#",
    "#.###.###.#.###.###.#",
    "#*..#.....P.....#..*#",
    "###.#.#.##.##.#.#.###",
    "#.....#...#...#.....#",
    "#.########.#.########",
    "#...................#",
    "#####################",
]


class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

    def move(self, dt, walls):
        speed = GHOST_SPEED * dt
        dx, dy = self.dir
        newx = self.x + dx * speed
        newy = self.y + dy * speed

        if not self.collides(newx, newy, walls):
            self.x, self.y = newx, newy
        else:
            self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

    def collides(self, x, y, walls):
        r = TILE_SIZE // 2 - 1
        for wx, wy in walls:
            if abs(x - (wx + TILE_SIZE/2)) < TILE_SIZE - 2 and abs(y - (wy + TILE_SIZE/2)) < TILE_SIZE - 2:
                return True
        return False


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Mini Pacman')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.walls = []
        self.pellets = []
        self.powerups = []
        self.player_x = 0
        self.player_y = 0
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.score = 0
        self.game_over = False
        self.win = False

        for row, line in enumerate(MAZE):
            for col, c in enumerate(line):
                x = col * TILE_SIZE + TILE_SIZE//2
                y = row * TILE_SIZE + TILE_SIZE//2
                if c == '#':
                    self.walls.append((col * TILE_SIZE, row * TILE_SIZE))
                elif c == '.':
                    self.pellets.append((x, y))
                elif c == '*':
                    self.powerups.append((x, y))
                elif c == 'P':
                    self.player_x = x
                    self.player_y = y

        self.ghosts = [
            Ghost(10 * TILE_SIZE + TILE_SIZE/2, 9 * TILE_SIZE + TILE_SIZE/2, COLORS['ghosts'][0]),
            Ghost(9 * TILE_SIZE + TILE_SIZE/2, 9 * TILE_SIZE + TILE_SIZE/2, COLORS['ghosts'][1]),
            Ghost(11 * TILE_SIZE + TILE_SIZE/2, 9 * TILE_SIZE + TILE_SIZE/2, COLORS['ghosts'][2]),
        ]

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.game_over and not self.win:
                self.update(dt)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    raise SystemExit
                if event.key == pygame.K_r and (self.game_over or self.win):
                    self.reset()
                    self.game_over = False
                    self.win = False
                if event.key == pygame.K_UP:
                    self.next_dir = (0, -1)
                elif event.key == pygame.K_DOWN:
                    self.next_dir = (0, 1)
                elif event.key == pygame.K_LEFT:
                    self.next_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.next_dir = (1, 0)

    def update(self, dt):
        speed = PLAYER_SPEED * dt
        self.move_player(speed)

        for ghost in self.ghosts:
            ghost.move(dt, self.walls)

        # Kolize s duchy
        for ghost in self.ghosts:
            if (self.player_x - ghost.x)**2 + (self.player_y - ghost.y)**2 < (TILE_SIZE*0.8)**2:
                self.game_over = True

        # sbírání
        self.pellets = [p for p in self.pellets if not self.check_collect(p, 6)]
        collected = len([p for p in self.pellets if False])  # not used, just placeholder

        # powerups
        self.powerups = [p for p in self.powerups if not self.check_collect(p, 10)]

        # vyhra
        if len(self.pellets) == 0 and len(self.powerups) == 0:
            self.win = True

    def check_collect(self, item, dist):
        x, y = item
        if (self.player_x - x)**2 + (self.player_y - y)**2 < dist*dist:
            self.score += 10 if dist == 6 else 50
            return True
        return False

    def move_player(self, speed):
        # Prefer new direction if možné
        nx = self.player_x + self.next_dir[0] * speed
        ny = self.player_y + self.next_dir[1] * speed
        if not self.collides(nx, ny):
            self.dir = self.next_dir

        px = self.player_x + self.dir[0] * speed
        py = self.player_y + self.dir[1] * speed
        if not self.collides(px, py):
            self.player_x = px
            self.player_y = py

        # teleport v bocích
        if self.player_x < -TILE_SIZE:
            self.player_x = WIDTH + TILE_SIZE
        elif self.player_x > WIDTH + TILE_SIZE:
            self.player_x = -TILE_SIZE

    def collides(self, x, y):
        r = TILE_SIZE * 0.35
        for wx, wy in self.walls:
            if abs(x - (wx + TILE_SIZE/2)) < TILE_SIZE*0.5 and abs(y - (wy + TILE_SIZE/2)) < TILE_SIZE*0.5:
                return True
        return False

    def draw(self):
        self.screen.fill(COLORS['background'])

        # map
        for wx, wy in self.walls:
            pygame.draw.rect(self.screen, COLORS['wall'], (wx, wy, TILE_SIZE, TILE_SIZE), border_radius=6)

        for x, y in self.pellets:
            pygame.draw.circle(self.screen, COLORS['pellet'], (int(x), int(y)), 3)

        for x, y in self.powerups:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 6)

        # player
        pygame.draw.circle(self.screen, COLORS['player'], (int(self.player_x), int(self.player_y)), TILE_SIZE//2 - 2)
        mouth = pygame.Rect(int(self.player_x), int(self.player_y - 5), 10, 10)
        pygame.draw.polygon(self.screen, COLORS['background'], [
            (self.player_x, self.player_y),
            (self.player_x + 12 * self.dir[0], self.player_y + 12 * self.dir[1] if self.dir != (0,0) else self.player_y),
            (self.player_x + 3, self.player_y + 3)
        ])

        # ghosts
        for ghost in self.ghosts:
            pygame.draw.circle(self.screen, ghost.color, (int(ghost.x), int(ghost.y)), TILE_SIZE//2 - 1)
            pygame.draw.circle(self.screen, (255,255,255), (int(ghost.x-6), int(ghost.y-5)), 4)
            pygame.draw.circle(self.screen, (255,255,255), (int(ghost.x+6), int(ghost.y-5)), 4)
            pygame.draw.circle(self.screen, (0,0,0), (int(ghost.x-6), int(ghost.y-5)), 2)
            pygame.draw.circle(self.screen, (0,0,0), (int(ghost.x+6), int(ghost.y-5)), 2)

        # HUD
        pygame.draw.rect(self.screen, COLORS['score_bg'], (0, 0, WIDTH, 30))
        score_text = FONT.render(f'Skóre: {self.score}', True, COLORS['text'])
        self.screen.blit(score_text, (12, 4))

        if self.game_over:
            over = FONT_BIG.render('GAME OVER', True, (255, 90, 90))
            self.screen.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 30))
            hint = FONT.render('Stiskni R pro restart, ESC pro konec', True, COLORS['text'])
            self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 20))

        if self.win:
            win_txt = FONT_BIG.render('WIN!', True, (120, 255, 140))
            self.screen.blit(win_txt, (WIDTH//2 - win_txt.get_width()//2, HEIGHT//2 - 30))
            hint = FONT.render('Stiskni R pro restart, ESC pro konec', True, COLORS['text'])
            self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 20))

        pygame.display.flip()
